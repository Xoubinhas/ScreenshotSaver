import os
import xml.etree.ElementTree as ET
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

config_file = ET.parse('resources/config.xml').getroot()


def get_credentials():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    credentials = None
    # Use token.json to access Google Drive
    if os.path.exists('resources/token.json'):
        credentials = Credentials.from_authorized_user_file('resources/token.json', SCOPES)
    # If there is no credentials, either refresh or create a new token file with new credentials
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('resources/client_secret.json', SCOPES)
            credentials = flow.run_local_server(port=50000)
        # Save the credentials for the next access
        with open('resources/token.json', 'w') as token:
            token.write(credentials.to_json())
    return credentials
