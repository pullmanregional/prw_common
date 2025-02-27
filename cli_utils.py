"""
Functions shared by all ingest scripts for command line handling
"""
import argparse

# Default values
DEFAULT_PRW_CONN = "sqlite:///prw.sqlite3"
DEFAULT_PRW_ID_CONN = "sqlite:///prw_id.sqlite3"

def cli_parser(
    description: str = None,
    require_prw: bool = False,
    require_prwid: bool = False, 
    require_in: bool = False,
    require_out: bool = False
) -> argparse.ArgumentParser:
    """
    Create a parser with common command line parameters used across ingest scripts.
    """
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument(
        "-prw", "--prw",
        help='PRW database connection string. For Azure SQL use format: "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=tcp:{server},1433;Database={db};Uid={user};Pwd={pwd};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"',
        required=require_prw,
        default=DEFAULT_PRW_CONN
    )
    
    parser.add_argument(
        "-prwid", "--prwid",
        help="PRW ID database connection string. Specify 'None' to explicitly skip.",
        required=require_prwid,
        default=DEFAULT_PRW_ID_CONN
    )
    
    parser.add_argument(
        "-i", "--in",
        help="Path to input data",
        required=require_in,
        dest="input"  # Use input instead of in since 'in' is a Python keyword
    )
    
    parser.add_argument(
        "-o", "--out", 
        help="Path to output",
        required=require_out
    )

    return parser