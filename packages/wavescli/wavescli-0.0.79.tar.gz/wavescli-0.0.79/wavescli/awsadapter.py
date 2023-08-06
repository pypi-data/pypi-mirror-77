import os
import boto3
import urllib.parse
from wavescli.config import get_config

config = get_config()


def send_file(filepath, target_bucket, key):
    """ Upload a file data to s3://target_bucket/file_path/file_name"""
    s3 = _create_boto_client("s3")
    s3.upload_file(filepath, target_bucket, key)
    return "s3://{}/{}".format(target_bucket, key)


def get_file(remote_uri, local_target_dir, basename=None):
    if not os.path.isdir(local_target_dir):
        os.makedirs(local_target_dir)

    s3 = _create_boto_client("s3")

    bucket_name, path = _extract_bucket_and_key(remote_uri)
    if not basename:
        basename = os.path.basename(path)
    target_path = os.path.join(local_target_dir, basename)
    s3.download_file(urllib.parse.unquote(bucket_name), urllib.parse.unquote(path), urllib.parse.unquote(target_path))
    return target_path


def public_url(remote_uri):
    if not remote_uri:
        return None

    bucket, key = _extract_bucket_and_key(remote_uri)
    s3 = _create_boto_client("s3")
    _24hours = 86400
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket,
            "Key": key
        },
        ExpiresIn=_24hours,
    )


def update_file_metadata(remote_uri, metadata):
    """ Adiciona metadata em um arquivo existente no S3 """
    bucket_name, key = _extract_bucket_and_key(remote_uri)
    s3 = _create_boto_client("s3")
    metadata['preview'] = metadata['preview'].strip('"')
    metadata['thumb'] = metadata['thumb'].strip('"')
    response = s3.copy(
        CopySource={
            "Bucket": bucket_name,
            "Key": key,
        },
        Key=key,
        Bucket=bucket_name,
        ExtraArgs={
            "Metadata": metadata,
            "MetadataDirective": "REPLACE",
        }
    )
    return response


def _create_boto_client(name):
    if config.AWS_ENDPOINT_URL:
        return boto3.client(name, endpoint_url=config.AWS_ENDPOINT_URL)
    return boto3.client(name)


def _extract_bucket_and_key(url):
    schema_prefix = "s3://"

    if not url.startswith(schema_prefix):
        raise RuntimeError("Invalid S3 URL: {}".format(repr(url)))
    bucket, key = url[len(schema_prefix):].split("/", 1)
    return bucket, key
