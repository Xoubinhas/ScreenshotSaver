from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import xml.etree.ElementTree as ET
from Access import get_credentials

config_file = ET.parse('resources/config.xml').getroot()


def find_or_create_folder(service):
    # Search for the folder that isn't in the trash with the name specified in the config file
    query = "mimeType='application/vnd.google-apps.folder' and name='" + config_file[2][0].text + "' and trashed=false"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    folders = response.get('files', [])

    # Get the first folder from the list
    if folders:
        return folders[0]['id']

    # Create folder
    file_metadata = {
        'name': config_file[2][0].text,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')


def upload_file(response, file_name):
    service = build('drive', 'v3', credentials=get_credentials())

    # Find or create the folder and get its ID
    folder_id = find_or_create_folder(service)

    # Set file metadata including the folder ID in the 'parents' field
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]  # Specify the folder ID as the parent
    }

    # Upload the file directly from the response obtained from the make_screenshot method
    media = MediaIoBaseUpload(io.BytesIO(response.content), mimetype='image/jpeg', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print("File uploaded successfully")
