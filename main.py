import re, os, io
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud.storage import Client
from flask import Flask
from time import sleep
from pathlib import Path

load_dotenv()

STORAGE_NAME: str = os.getenv('STORAGE_NAME')
BUCKET_NAME: str = os.getenv('BUCKET_NAME')
JSON_PRIVATE_KEY_ID: str = os.getenv('JSON_PRIVATE_KEY_ID')
JSON_PRIVATE_KEY: str = os.getenv('JSON_PRIVATE_KEY')
JSON_CLIENT_EMAIL: str = os.getenv('JSON_CLIENT_EMAIL')
JSON_CLIENT_ID: str = os.getenv('JSON_CLIENT_ID')
JSON_CLIENT_X509_CERT_URL: str = os.getenv('JSON_CLIENT_X509_CERT_URL')
JSON_PROJECT_ID: str = os.getenv('JSON_PROJECT_ID')
JSON_AUTH_URI:str = os.getenv('JSON_AUTH_URI')
GOOGLE_DRIVER_FOLDER_ID: str = os.getenv('GOOGLE_DRIVER_FOLDER_ID')


    
def _get_credentials_gcp():
    creds: dict = {
        "type": "service_account",
        "project_id": JSON_PROJECT_ID,
        "private_key_id": JSON_PRIVATE_KEY_ID,
        "private_key": re.sub(r'\\n', '\n', JSON_PRIVATE_KEY),
        "client_email": JSON_CLIENT_EMAIL,
        "client_id": JSON_CLIENT_ID,
        "auth_uri": JSON_AUTH_URI,
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": JSON_CLIENT_X509_CERT_URL,
        "universe_domain": "googleapis.com"
    }
    credentials = service_account.Credentials.from_service_account_info(creds)
    return credentials

app = Flask(__name__)

@app.route('/down')
def download_storage(bucket_name, file_name):
    client = Client(project=JSON_PROJECT_ID, credentials=_get_credentials_gcp())
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(file_name)

@app.route('/up')
def upload_file_to_drive():
    client = Client(project=JSON_PROJECT_ID, credentials=_get_credentials_gcp())
    file_path = Path(Path('test_file.txt')).resolve()
    with open(file_path, 'rb') as file:
        file_content = file.read()
    file_content = io.BytesIO(file_content)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob('test_file.txt')
    blob.upload_from_file(file_content, num_retries=3, timeout=300)
    return 'Upload realizado com sucesso!'

@app.route('/')
def home():
    for _ in range(1,6):
        sleep(1)
    return "Script finalizado no Cloud Run!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)