import json
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
# Google Drive Folder ID (Get this from your Google Drive folder URL)
FOLDER_ID = os.getenv("FOLDER_ID")

# Path to your service account credentials JSON file
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE_NAME")

# Authenticate using the service account
def authenticate_gdrive():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive"])
    return build("drive", "v3", credentials=creds)

# Upload JSON file to Google Drive
def upload_json_to_gdrive(file_name):
    drive_service = authenticate_gdrive()

    # Create a media file upload object
    media = MediaFileUpload(file_name, mimetype="application/json")

    # Define file metadata
    file_metadata = {
        "name": file_name,
        "parents": [FOLDER_ID]  # Store in a specific folder
    }

    # Upload file
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    
    print(f"✅ File uploaded successfully! File ID: {file.get('id')}")