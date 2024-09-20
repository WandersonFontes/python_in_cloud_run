from flask import Request, jsonify
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud.storage import Client
from pathlib import Path
import os, re, io

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

CREDENTIALS_GCP = _get_credentials_gcp()

def _download_storage(bucket_name: str, file_name: str) -> None:
    client = Client(project=JSON_PROJECT_ID, credentials=CREDENTIALS_GCP)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(file_name)

def _upload_file_to_drive(bucket_name: str, file_name: str) -> None:
    client = Client(project=JSON_PROJECT_ID, credentials=CREDENTIALS_GCP)

    file_path = Path(Path('test_file.txt')).resolve()
    with open(file_path, 'rb') as file:
        file_content = file.read()
    file_content = io.BytesIO(file_content)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob('test_file.txt')
    blob.upload_from_file(file_content, num_retries=3, timeout=300)
    # return 'Upload realizado com sucesso!'

def handle_event(request: Request):
    try:
        event = request.get_json()
        if not event:
            return jsonify({"error": "Invalid event format"}), 400

        print("Received event:", event)
        _download_storage(event['bucket'], event['name'])
        _upload_file_to_drive(event['bucket'], event['name'])

        return jsonify({"message": "Event received successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500