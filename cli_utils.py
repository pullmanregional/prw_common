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
    require_out: bool = False,
) -> argparse.ArgumentParser:
    """
    Create a parser with common command line parameters used across ingest scripts.
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "--prw",
        help='PRW database connection string. For Azure SQL use format: "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=tcp:{server},1433;Database={db};Uid={user};Pwd={pwd};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"',
        required=require_prw,
        default=DEFAULT_PRW_CONN,
    )

    parser.add_argument(
        "--prwid",
        help="PRW ID database connection string. Specify 'None' to explicitly skip.",
        required=require_prwid,
        default=DEFAULT_PRW_ID_CONN,
    )

    parser.add_argument(
        "-i",
        "--in",
        help="Path to input data",
        required=require_in,
        dest="input",  # Use input instead of in since 'in' is a Python keyword
    )

    parser.add_argument("-o", "--out", help="Path to output", required=require_out)

    return parser


def add_s3_args(parser: argparse.ArgumentParser, require_s3: bool = False):
    """
    Add S3 config CLI options:
        --s3url https://<baseurl>/<bucket>
        --s3auth <account_id>:<account_key>
    """
    parser.add_argument(
        "--s3url",
        help="S3 URL to upload output to including endpoint URL and bucket, i.e. https://<baseurl>/<bucket>. Required with --s3auth to upload to S3.",
        required=require_s3,
    )
    parser.add_argument(
        "--s3auth",
        help="S3 auth information in the format <account_id>:<account_key>. Required with --s3url to upload to S3.",
        required=require_s3,
    )
    return parser
