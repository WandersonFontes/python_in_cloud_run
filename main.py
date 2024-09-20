import re, os
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud.storage import Client
import functions_framework

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


    
def get_credentials_gcp():
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

def download_storage(bucket_name, file_name):
    client = Client(project=JSON_PROJECT_ID, credentials=get_credentials_gcp())
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(file_name)

@functions_framework.cloud_event
def main(event) -> None:
    dados: dict = event.data
    print(dados['bucket'])

if __name__ == "__main__":
    main({"bucket":"", "name": ""})