import boto3

from django.conf import settings


AWS_S3_ACCESS_ID = getattr(settings, 'AWS_S3_ACCESS_ID', None)
AWS_S3_ACCESS_KEY = getattr(settings, 'AWS_S3_ACCESS_KEY', None)
AWS_S3_BUCKET_NAME = getattr(settings, 'AWS_S3_BUCKET_NAME', None)
AWS_ROOT_KEY = getattr(settings, 'AWS_ROOT_FOLDER', '')


def has_credentials(func):
    def wrapper(*args, **kwargs):
        if AWS_S3_ACCESS_ID and AWS_S3_ACCESS_KEY and AWS_S3_BUCKET_NAME:
            return func(*args, **kwargs)            
        else:
            print('NO CREDENTIALS PROVIDED, you must to add credentials in .env file')
        return False
    return wrapper


def get_boto_client():
    client = boto3.client('s3', 
                    aws_access_key_id=AWS_S3_ACCESS_ID,
                    aws_secret_access_key=AWS_S3_ACCESS_KEY)
    return client


def get_boto_resourse():
    resource = boto3.resource(
                's3',
                aws_access_key_id=AWS_S3_ACCESS_ID,
                aws_secret_access_key=AWS_S3_ACCESS_KEY
            )
    return resource


@has_credentials
def create_folder(directory_name: str) -> str:
    """Create folder in AWS bucket S3

    Args:
        directory_name (str): name of folder

    Returns:
        str: name of folder if the bucket folder was created
    """

    try:
        s3 = get_boto_client()
        key = directory_name.lower().replace(' ', '_') + '/'
        s3.put_object(
            Bucket=AWS_S3_BUCKET_NAME, 
            Key=AWS_ROOT_KEY + key
        )
        return key
    except Exception as error:
        print(error)
    return None


@has_credentials
def upload_image(mediafile_key: str, file: str) -> any:
    try:
        s3 = get_boto_resourse()
        bucket = s3.Bucket(AWS_S3_BUCKET_NAME)

        return bucket.put_object(
            ACL='public-read',
            Key=AWS_ROOT_KEY + mediafile_key,
            ContentType=file.content_type,
            Body=file
        )
    
    except Exception as error:
        print(error)
    return False
        


@has_credentials
def rename_file(old_mediafile_key: str, new_mediafile_key: str) -> bool:
    try:
        s3 = get_boto_resourse()

        old_key = AWS_ROOT_KEY + old_mediafile_key
        new_key = AWS_ROOT_KEY + new_mediafile_key

        s3.Object(AWS_S3_BUCKET_NAME, new_key).copy_from(CopySource=AWS_S3_BUCKET_NAME + '/' + old_key)
        s3.Object(AWS_S3_BUCKET_NAME, old_key).delete()

        s3.Object(AWS_S3_BUCKET_NAME, new_key).Acl().put(ACL='public-read')

        return True
    
    except Exception as error:
        print(error)
    return False


@has_credentials
def delete_file(mediafile_key: str) -> bool:
    try:
        s3 = get_boto_resourse()
        file_key = AWS_ROOT_KEY + mediafile_key
        s3.Object(AWS_S3_BUCKET_NAME, file_key).delete()
        return True
    except Exception as error:
        print(error)
    return False


@has_credentials
def get_file_content(mediafile_key: str) -> any:
    try:
        s3 = get_boto_client()
        file_key = AWS_ROOT_KEY + mediafile_key
        data = s3.get_object(Bucket=AWS_S3_BUCKET_NAME, Key=file_key)
        return data['Body'].read()
    except Exception as error:
        print(error)
    return None


@has_credentials
def download_file(mediafile_key: str, local_path: str) -> any:
    try:
        s3 = get_boto_client()
        file_key = AWS_ROOT_KEY + mediafile_key
        with open(local_path, 'wb') as file:
            s3.download_fileobj(AWS_S3_BUCKET_NAME, file_key, file)
    except Exception as error:
        print(error)
    return None