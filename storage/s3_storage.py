import boto3
from boto3.s3.transfer import S3UploadFailedError
from utils.logger import logger

class S3Storage:
    def __init__(self, bucket_name: str, region: str, access_key_id: str, secret_access_key: str):
        self.bucket_name = bucket_name
        self.region = region
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

    def upload_to_s3(self, local_file: str) -> bool:
        try:
            s3_client = boto3.client(
                service_name='s3',
                region_name=self.region,
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key
            )
            file_name = local_file.split('/')[-1]
            s3_client.upload_file(local_file, self.bucket_name, file_name)
            logger.info(f"Upload of data dump to s3 successful for file {file_name} ✅")
            return True
        except S3UploadFailedError as err:
            logger.error(f"Couldn't upload file {file_name} to {self.bucket_name} due to {err}")
            raise
        except Exception as e:
            logger.error(f"Failed to upload data dump to {self.bucket_name} due to {e}")
            raise
