import re, urllib, logging
import pandas as pd
import sqlalchemy
import time
from datetime import datetime
from dataclasses import dataclass
from typing import List
from sqlmodel import SQLModel, Session, create_engine, delete
from sqlalchemy import inspect


@dataclass
class TableData:
    """
    Associate a table with its data to update in a DB
    """

    table: SQLModel
    df: pd.DataFrame


def mask_conn_pw(conn_str: str) -> str:
    """
    Mask uid and pwd in ODBC connection string for logging
    """
    # Use regex to mask uid= and pwd= values
    masked_str = re.sub(r"(uid=|pwd=)[^;]*", r"\1****", conn_str, flags=re.IGNORECASE)
    return masked_str


def get_db_connection(
    conn_str: str, echo: bool = False, max_retries: int = 3, retry_delay: int = 5
) -> sqlalchemy.Engine:
    """
    Given an ODBC connection string, return a connection to the DB via SQLModel

    Args:
        odbc_str: ODBC connection string
        echo: Whether to echo SQL statements
        max_retries: Maximum number of connection retry attempts
        retry_delay: Delay in seconds between retry attempts
    """
    # Split connection string into odbc prefix and parameters (ie everything after odbc_connect=)
    match = re.search(r"^(.*odbc_connect=)(.*)$", conn_str)
    prefix = match.group(1) if match else ""
    params = match.group(2) if match else ""
    if prefix and params:
        # URL escape ODBC connection string if found
        conn_str = prefix + urllib.parse.quote_plus(params)

    # Use SQLModel to establish connection to DB with retries
    retries = 0
    while retries < max_retries:
        try:
            if conn_str.startswith("mssql"):
                # Optimize with fast_executemany, which is supported by MSSQL / Azure SQL
                engine = create_engine(conn_str, echo=echo, fast_executemany=True)
            else:
                engine = create_engine(conn_str, echo=echo)
            return engine
        except Exception as e:
            retries += 1
            if retries == max_retries:
                logging.error(
                    f"ERROR: failed to connect to DB after {max_retries} attempts"
                )
                logging.error(e)
                return None
            logging.warning(
                f"Connection attempt {retries} failed, retrying in {retry_delay} seconds..."
            )
            time.sleep(retry_delay)


def clear_tables(session: Session, tables: List[SQLModel]):
    """
    Delete all rows from specified tables
    """
    for table in tables:
        logging.info(f"Clearing table: {table.__tablename__}")
        session.exec(delete(table))


def clear_tables_and_insert_data(
    session: Session, tables_data: List[TableData], chunk_size: int = 100000
):
    """
    Write data from dataframes to DB tables, clearing and overwriting existing tables
    """
    for table_data in tables_data:
        logging.info(
            f"Writing data to table: {table_data.table.__tablename__}, rows: {len(table_data.df)}"
        )

        # Clear data in DB if table exists
        try:
            inspector = inspect(session.bind)
            if inspector.has_table(table_data.table.__tablename__):
                session.exec(delete(table_data.table))
        except Exception as e:
            logging.warning(
                f"WARN: failed to clear table: {table_data.table.__tablename__}", e
            )

        # Select columns from dataframe that match table columns
        table_columns = table_data.table.__table__.columns.keys()

        # Remove columns that aren't in the dataframe
        table_columns = [col for col in table_columns if col in table_data.df.columns]

        # Remove the PK column from the dataframe, which will be computed by the DB
        if table_data.table.__table__.primary_key.columns.keys()[0] in table_columns:
            table_columns.remove(
                table_data.table.__table__.primary_key.columns.keys()[0]
            )

        # Convert dataframe datatypes to match DB types
        _convert_df_dtypes_to_db(table_data, table_columns)

        # Write data from dataframe
        start_time = time.time()
        logging.info(f"Writing table: {table_data.table.__tablename__}")
        df = table_data.df[table_columns]
        df.to_sql(
            name=table_data.table.__tablename__,
            con=session.connection(),
            if_exists="append",
            index=False,
            chunksize=chunk_size,
        )
        elapsed_time = time.time() - start_time
        logging.info(
            f"Wrote {len(df)} rows to {table_data.table.__tablename__} in {elapsed_time:.2f}s"
        )


def _convert_df_dtypes_to_db(table_data: TableData, table_columns: List[str]):
    """
    Convert dataframe columns to match database column types by
    mapping SQLAlchemy types to pandas-compatible dtypes
    """
    df = table_data.df
    for col in table_columns:
        if col in df.columns:
            sa_column = table_data.table.__table__.columns[col]
            current_dtype = str(df[col].dtype)

            if isinstance(sa_column.type, sqlalchemy.String):
                target_dtype = "object"
            elif isinstance(sa_column.type, sqlalchemy.Integer):
                # Use pandas nullable integer type if there are NaNs
                target_dtype = "Int64" if df[col].isna().any() else "int64"
            elif isinstance(sa_column.type, sqlalchemy.Float):
                target_dtype = "float64"
            elif isinstance(sa_column.type, sqlalchemy.DateTime) or isinstance(
                sa_column.type, sqlalchemy.Date
            ):
                target_dtype = "datetime64[ns]"
            elif isinstance(sa_column.type, sqlalchemy.Boolean):
                target_dtype = "bool"
            else:
                target_dtype = "object"

            # Only convert if needed
            if current_dtype != target_dtype:
                logging.info(
                    f"Converting column {col} from {current_dtype} to {target_dtype}"
                )
                # Can use .copy() to avoid SettingWithCopyWarning
                df[col] = df[col].astype(target_dtype, copy=False)


def write_meta(session: Session, meta_table: SQLModel):
    """
    Populate the meta table with last modified time. prw-warehouse ingest has a 
    different version specific for the PRW schema which includes tables prw_meta and 
    prw_sources_meta
    """
    logging.info("Writing metadata")

    # Clear and reset last ingest time
    inspector = inspect(session.bind)
    if inspector.has_table(meta_table.__tablename__):
        session.exec(delete(meta_table))
    session.add(meta_table(modified=datetime.now()))
