import base64
import email
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class GmailService:
    def __init__(self, credentials: Credentials):
        self.service = build('gmail', 'v1', credentials=credentials)
    
    def read_inbox(self, max_results: int = 10, query: str = None) -> List[Dict]:
        """Read emails from inbox"""
        try:
            if query:
                results = self.service.users().messages().list(
                    userId='me', 
                    labelIds=['INBOX'], 
                    q=query,
                    maxResults=max_results
                ).execute()
            else:
                results = self.service.users().messages().list(
                    userId='me', 
                    labelIds=['INBOX'], 
                    maxResults=max_results
                ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id']
                ).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
                
                # Get email body
                body = self._get_email_body(msg['payload'])
                
                emails.append({
                    'id': message['id'],
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body': body,
                    'snippet': msg.get('snippet', ''),
                    'labels': msg.get('labelIds', [])
                })
            
            return emails
            
        except Exception as e:
            return {'error': str(e)}
    
    def create_email(self, to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> Dict:
        """Create and send an email"""
        try:
            message = MIMEMultipart()
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc
            
            # Add body to email
            text_part = MIMEText(body, 'plain')
            message.attach(text_part)
            
            # Encode the message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send the email
            sent_message = self.service.users().messages().send(
                userId='me', 
                body={'raw': raw_message}
            ).execute()
            
            return {
                'success': True,
                'message_id': sent_message['id'],
                'thread_id': sent_message['threadId']
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def check_sent_emails(self, max_results: int = 10) -> List[Dict]:
        """Check sent emails"""
        try:
            results = self.service.users().messages().list(
                userId='me', 
                labelIds=['SENT'], 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            sent_emails = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id']
                ).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                to = next((h['value'] for h in headers if h['name'] == 'To'), 'Unknown Recipient')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
                
                sent_emails.append({
                    'id': message['id'],
                    'subject': subject,
                    'to': to,
                    'date': date,
                    'snippet': msg.get('snippet', '')
                })
            
            return sent_emails
            
        except Exception as e:
            return {'error': str(e)}
    
    def check_drafts(self, max_results: int = 10) -> List[Dict]:
        """Check draft emails"""
        try:
            results = self.service.users().messages().list(
                userId='me', 
                labelIds=['DRAFT'], 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            drafts = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id']
                ).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                to = next((h['value'] for h in headers if h['name'] == 'To'), 'Unknown Recipient')
                
                drafts.append({
                    'id': message['id'],
                    'subject': subject,
                    'to': to,
                    'snippet': msg.get('snippet', '')
                })
            
            return drafts
            
        except Exception as e:
            return {'error': str(e)}
    
    def check_promotions(self, max_results: int = 10) -> List[Dict]:
        """Check promotional emails"""
        try:
            results = self.service.users().messages().list(
                userId='me', 
                labelIds=['CATEGORY_PROMOTIONS'], 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            promotions = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id']
                ).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                
                promotions.append({
                    'id': message['id'],
                    'subject': subject,
                    'sender': sender,
                    'snippet': msg.get('snippet', '')
                })
            
            return promotions
            
        except Exception as e:
            return {'error': str(e)}
    
    def check_important_emails(self, max_results: int = 10) -> List[Dict]:
        """Check important emails"""
        try:
            results = self.service.users().messages().list(
                userId='me', 
                labelIds=['IMPORTANT'], 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            important_emails = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id']
                ).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
                
                important_emails.append({
                    'id': message['id'],
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'snippet': msg.get('snippet', '')
                })
            
            return important_emails
            
        except Exception as e:
            return {'error': str(e)}
    
    def search_emails(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search emails using Gmail query syntax"""
        try:
            results = self.service.users().messages().list(
                userId='me', 
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            search_results = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id']
                ).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
                
                search_results.append({
                    'id': message['id'],
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'snippet': msg.get('snippet', ''),
                    'labels': msg.get('labelIds', [])
                })
            
            return search_results
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_email_body(self, payload: Dict) -> str:
        """Extract email body from payload"""
        if 'body' in payload and payload['body'].get('data'):
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        elif 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        return "No readable body content"
