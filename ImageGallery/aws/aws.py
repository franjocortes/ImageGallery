import boto3

from django.conf import settings


def create_folder(bucket, directory_name):

    AWS_S3_ACCESS_ID = getattr(settings, 'AWS_S3_ACCESS_ID', None)
    AWS_S3_ACCESS_KEY = getattr(settings, 'AWS_S3_ACCESS_KEY', None)

    if AWS_S3_ACCESS_ID and AWS_S3_ACCESS_KEY:
        try:
            s3 = boto3.client('s3', 
                            aws_access_key_id=AWS_S3_ACCESS_ID,
                            aws_secret_access_key=AWS_S3_ACCESS_KEY)
            key = directory_name + '/'
            s3.put_object(Bucket=bucket, Key=key)
            return key
        except Exception as error:
            print(error)
    else:
        print('NO CREDENTIALS PROVIDED, you must to add credentials in .env file')