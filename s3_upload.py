from boto3 import session
from botocore.client import Config
import os

ACCESS_ID = ''
SECRET_KEY = ''

# Initiate session
session = session.Session()
client = session.client('s3',
                        region_name='fra1',
                        endpoint_url='https://fra1.digitaloceanspaces.com',
                        aws_access_key_id=ACCESS_ID,
                        aws_secret_access_key=SECRET_KEY)
recordings_folder = 'audio'
do_space = 'pypatcher-recordings'

for filename in os.listdir(recordings_folder):

    file_key_name = recordings_folder + '/' + filename
    local_path = os.getcwd()
    local_name = local_path + '/' + recordings_folder + '/' + filename
    try:
        client.upload_file(local_name, do_space, file_key_name)
    except:
        print(local_name, 'failed to upload, not deleting')
    else:
        print(local_name, 'succesfully uploaded, deleting local copy')
        os.remove(local_name)
        print(local_name, 'deleted')
