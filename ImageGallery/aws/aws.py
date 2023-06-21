import boto3

from django.conf import settings


AWS_S3_ACCESS_ID = getattr(settings, 'AWS_S3_ACCESS_ID', None)
AWS_S3_ACCESS_KEY = getattr(settings, 'AWS_S3_ACCESS_KEY', None)
AWS_S3_BUCKET_NAME = getattr(settings, 'AWS_S3_BUCKET_NAME', None)
AWS_ROOT_KEY = getattr(settings, 'AWS_ROOT_FOLDER', '')


def create_folder(directory_name: str) -> str:
    """Create folder in AWS bucket S3

    Args:
        directory_name (str): name of folder

    Returns:
        str: name of folder if the bucket folder was created
    """

    if AWS_S3_ACCESS_ID and AWS_S3_ACCESS_KEY and AWS_S3_BUCKET_NAME:
        try:
            s3 = boto3.client('s3', 
                            aws_access_key_id=AWS_S3_ACCESS_ID,
                            aws_secret_access_key=AWS_S3_ACCESS_KEY)
            key = directory_name.lower().replace(' ', '_') + '/'
            s3.put_object(
                Bucket=AWS_S3_BUCKET_NAME, 
                Key=AWS_ROOT_KEY + key
            )
            return key
        except Exception as error:
            print(error)
    else:
        print('NO CREDENTIALS PROVIDED, you must to add credentials in .env file')


def upload_image(mediafile_key, file):
    
    if AWS_S3_ACCESS_ID and AWS_S3_ACCESS_KEY and AWS_S3_BUCKET_NAME:
    
        try:
            s3 = boto3.resource(
                's3',
                aws_access_key_id=AWS_S3_ACCESS_ID,
                aws_secret_access_key=AWS_S3_ACCESS_KEY
            )

            bucket = s3.Bucket(AWS_S3_BUCKET_NAME)

            return bucket.put_object(
                ACL='public-read',
                Key=AWS_ROOT_KEY + mediafile_key,
                ContentType=file.content_type,
                Body=file
            )
        
        except Exception as error:
            print(error)
        
    else:
        print('NO CREDENTIALS PROVIDED, you must to add credentials in .env file')


def rename_file(old_mediafile_key, new_mediafile_key):
    
    if AWS_S3_ACCESS_ID and AWS_S3_ACCESS_KEY and AWS_S3_BUCKET_NAME:
    
        try:
            s3 = boto3.resource(
                's3',
                aws_access_key_id=AWS_S3_ACCESS_ID,
                aws_secret_access_key=AWS_S3_ACCESS_KEY
            )

            old_key = AWS_ROOT_KEY + old_mediafile_key
            new_key = AWS_ROOT_KEY + new_mediafile_key

            s3.Object(AWS_S3_BUCKET_NAME, new_key).copy_from(CopySource=AWS_S3_BUCKET_NAME + '/' + old_key)
            s3.Object(AWS_S3_BUCKET_NAME, old_key).delete()

            s3.Object(AWS_S3_BUCKET_NAME, new_key).Acl().put(ACL='public-read')

            return True
        
        except Exception as error:
            print(error)
        
    else:
        print('NO CREDENTIALS PROVIDED, you must to add credentials in .env file')
