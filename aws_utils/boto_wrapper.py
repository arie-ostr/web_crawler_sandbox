import boto3
import os

def upload_file_to_s3(file_path, bucket_name, s3_file_name):
    """
    Uploads a file to an S3 bucket.

    :param file_path: Path to the file to upload
    :param bucket_name: Name of the S3 bucket
    :param s3_file_name: Name of the file in the S3 bucket
    """
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, s3_file_name)
    print(f"File uploaded to S3 bucket {bucket_name} as {s3_file_name}")
