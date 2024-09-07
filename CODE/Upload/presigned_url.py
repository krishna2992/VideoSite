import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_presigned_url(bucket_name, object_key, expiration=3600):
    """Generate a presigned URL for uploading a file to an S3 bucket.

    :param bucket_name: Name of the S3 bucket
    :param object_key: Object key in the S3 bucket
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as a string
    """
    s3_client = boto3.client('s3')
    
    try:
        # Generate the presigned URL for a PUT request
        presigned_url = s3_client.generate_presigned_url('put_object',
                                                        Params={'Bucket': bucket_name,
                                                                'Key': object_key},
                                                        ExpiresIn=expiration)
        return presigned_url
    except (NoCredentialsError, PartialCredentialsError) as e:
        logger.error(f'Credentials error: {e}')
        return None
    except Exception as e:
        logger.error(f'Error generating presigned URL: {e}')
        return None

