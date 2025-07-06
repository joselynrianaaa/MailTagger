from __future__ import print_function
import os.path
import base64
import re
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# If modifying these scopes, delete the token.json file.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']



def load_label_rules():
    with open("label_rules.json", "r") as f:
        return json.load(f)
    

LABEL_RULES = load_label_rules()
   

def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_matching_label(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    headers = msg['payload']['headers']

    subject = ''
    sender = ''
    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']
        if header['name'] == 'From':
            sender = header['value']

    body = ''
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8', errors='ignore')
                    break

    combined = f"{subject} {body}".lower()
    sender_lower = sender.lower()

    for label, rules in LABEL_RULES.items():
        keywords = rules.get("keywords", [])
        senders = rules.get("senders", [])
        if any(s in sender_lower for s in senders) or any(k in combined for k in keywords):
            return label

    return None




def get_or_create_label(service, label_name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for label in labels:
        if label['name'].lower() == label_name.lower():
            return label['id']
    # Create label if it doesn't exist
    label_obj = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }
    label = service.users().labels().create(userId='me', body=label_obj).execute()
    return label['id']

def tag_emails():
    service = get_service()
    results = service.users().messages().list(userId='me', q="is:inbox", maxResults=500).execute()
    messages = results.get('messages', [])

    for message in messages:
        label_name = get_matching_label(service, message)
        if label_name:
            label_id = get_or_create_label(service, label_name)

            modify_body = {'addLabelIds': [label_id]}

            if label_name.lower() in ["nptel", "unstop", "others"]:
                modify_body['removeLabelIds'] = ['INBOX']

            service.users().messages().modify(
                userId='me',
                id=message['id'],
                body=modify_body
            ).execute()

            print(f"Tagged: {label_name} | Message ID: {message['id']}")
            if label_name.lower() in ["nptel", "unstop", "others"]:
                print(f" -> Archived (removed from Inbox)")



if __name__ == '__main__':
    tag_emails()
