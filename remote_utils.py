"""
Utilities to handle upload/download from remote storage, including Cloudflare R2
"""

import os
import logging
import boto3
from urllib.parse import urlparse


def get_s3_client(url_and_bucket: str, auth_id_and_key: str) -> boto3.client:
    """
    Create an S3 client using the provided config information.
    URL in the format https://<baseurl>/<bucket>
    Auth information in the format <account_id>:<account_key>
    Returns an S3 client with an additional bucket attribute from the URL.
    """
    urlparts = urlparse(url_and_bucket)
    baseurl = f"{urlparts.scheme}://{urlparts.netloc}"
    bucket = urlparts.path.lstrip("/")
    acct_id, acct_key = auth_id_and_key.split(":")
    s3_client = boto3.client(
        "s3",
        endpoint_url=baseurl,
        region_name="auto",
        aws_access_key_id=acct_id,
        aws_secret_access_key=acct_key,
    )
    s3_client.bucket = bucket
    return s3_client


def upload_file_to_s3(
    s3_url_and_bucket: str,
    s3_auth_id_and_key: str,
    file_path: str,
    s3_object_name: str | None = None,
):
    """Upload a file, file_path, to S3"""
    # Create S3 client using provided endpoint URL and bucket with auth info
    s3_client = get_s3_client(s3_url_and_bucket, s3_auth_id_and_key)

    # Default object name to same as file name
    if s3_object_name is None:
        s3_object_name = os.path.basename(file_path)

    logging.info(f"Uploading: {file_path} -> {s3_client.bucket}/{s3_object_name}")
    s3_client.upload_file(file_path, s3_client.bucket, s3_object_name)
