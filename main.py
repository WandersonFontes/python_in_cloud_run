import re, os, io
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud.storage import Client
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import functions_framework
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

def upload_file_to_drive(file_path, drive_folder_id=None):
    """Faz upload de um arquivo para o Google Drive."""
    creds = get_credentials_gcp()

    try:
        # Cria o serviço do Google Drive
        service = build('drive', 'v3', credentials=creds)

        user_info = service.about().get(fields="user").execute()
        print(user_info)
        
        # Define o arquivo a ser enviado
        file_metadata = {'name': os.path.basename(file_path)}
        if drive_folder_id:
            file_metadata['parents'] = [drive_folder_id]
        
        media = MediaFileUpload(file_path, resumable=True)
        
        # Faz o upload do arquivo
        file = service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        
        print(f"Arquivo enviado com sucesso ao Google Drive com ID: {file.get('id')}")
    
    except Exception as e:
        print(f"Erro ao fazer upload para o Google Drive: {e}")

# @functions_framework.cloud_event
# def main(event) -> None:
#     dados: dict = event.data
#     print(dados['bucket'])
#     download_storage(dados['bucket'], dados['name'])
#     upload_file_to_drive(dados['name'], GOOGLE_DRIVER_FOLDER_ID)

# if __name__ == "__main__":
#     main({"bucket":"", "name": ""})

app = Flask(__name__)

@app.route('/up')
def upload_file_to_drive():

    client = Client(project=JSON_PROJECT_ID, credentials=get_credentials_gcp())

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
    app.run(host='0.0.0.0', port=8081)