import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_key_gcloud.json'

storage_client = storage.Client()

# dir(storage_client)

"""
Create a New Bucket
"""

bucket_name = 'data_bucket_imikami_1'
bucket = storage_client.bucket(bucket_name)
# bucket.location = 'AUSTRALIA-SOUTHEAST2'
# bucket = storage_client.create_bucket(bucket)

# PRINT BUCKET DETAILS
vars(bucket)

# ACCESSING BUCKET
my_bucket = storage_client.get_bucket('data_bucket_imikami_1')


# UPLOAD FILES
def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False


file_path = r'X:\Limitless\A - Skeletal Tracking'
upload_to_bucket('WDocuments1', os.path.join(file_path, 'Limitless - Skeletal Tracking.docx'), 'data_bucket_imikami_1')
upload_to_bucket('/WD/WDocuments2', os.path.join(file_path, 'Limitless - Skeletal Tracking.docx'),'data_bucket_imikami_1')

# DOWNLOAD FILES

def download_file_from_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path,'wb') as f:
            storage_client.download_blob_to_file(blob, f)

        return True
    except Exception as e:
        print(e)
        return False

bucket_name = 'data_bucket_imikami_1'
download_file_from_bucket('WDocuments1', os.path.join(os.getcwd(),'file1.docx'), bucket_name)