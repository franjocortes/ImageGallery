import boto3

from django.conf import settings


def create_folder(directory_name: str) -> str:
    """Create folder in AWS bucket S3

    Args:
        directory_name (str): name of folder

    Returns:
        str: name of folder if the bucket folder was created
    """

    AWS_S3_ACCESS_ID = getattr(settings, 'AWS_S3_ACCESS_ID', None)
    AWS_S3_ACCESS_KEY = getattr(settings, 'AWS_S3_ACCESS_KEY', None)
    AWS_S3_BUCKET_NAME = getattr(settings, 'AWS_S3_BUCKET_NAME', None)

    if AWS_S3_ACCESS_ID and AWS_S3_ACCESS_KEY and AWS_S3_BUCKET_NAME:
        try:
            s3 = boto3.client('s3', 
                            aws_access_key_id=AWS_S3_ACCESS_ID,
                            aws_secret_access_key=AWS_S3_ACCESS_KEY)
            key = directory_name.lower().replace(' ', '') + '/'
            s3.put_object(Bucket=AWS_S3_BUCKET_NAME, Key=key)
            return key
        except Exception as error:
            print(error)
    else:
        print('NO CREDENTIALS PROVIDED, you must to add credentials in .env file')