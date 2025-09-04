import io
import os
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from google.oauth2.credentials import Credentials

class GoogleDocsService:
    def __init__(self, credentials: Credentials):
        self.docs_service = build('docs', 'v1', credentials=credentials)
        self.drive_service = build('drive', 'v3', credentials=credentials)
    
    def create_document(self, title: str, content: str = None) -> Dict:
        """Create a new Google Doc"""
        try:
            # Create empty document
            document = {
                'title': title
            }
            
            doc = self.docs_service.documents().create(body=document).execute()
            document_id = doc.get('documentId')
            
            # Add content if provided
            if content:
                requests = [
                    {
                        'insertText': {
                            'location': {
                                'index': 1
                            },
                            'text': content
                        }
                    }
                ]
                
                self.docs_service.documents().batchUpdate(
                    documentId=document_id,
                    body={'requests': requests}
                ).execute()
            
            return {
                'success': True,
                'document_id': document_id,
                'title': title,
                'url': f"https://docs.google.com/document/d/{document_id}/edit"
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_document(self, document_id: str) -> Dict:
        """Get document content and metadata"""
        try:
            document = self.docs_service.documents().get(
                documentId=document_id
            ).execute()
            
            # Extract text content
            content = self._extract_text_content(document)
            
            return {
                'document_id': document_id,
                'title': document.get('title', ''),
                'content': content,
                'url': f"https://docs.google.com/document/d/{document_id}/edit",
                'last_modified': document.get('revisionId', ''),
                'body': document.get('body', {})
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def update_document(self, document_id: str, content: str, append: bool = False) -> Dict:
        """Update document content"""
        try:
            if append:
                # Get current document to find end index
                document = self.docs_service.documents().get(
                    documentId=document_id
                ).execute()
                
                # Find the end of the document
                end_index = 1
                if 'body' in document and 'content' in document['body']:
                    for element in document['body']['content']:
                        if 'endIndex' in element:
                            end_index = element['endIndex']
                
                requests = [
                    {
                        'insertText': {
                            'location': {
                                'index': end_index - 1
                            },
                            'text': '\n' + content
                        }
                    }
                ]
            else:
                # Clear existing content and insert new content
                requests = [
                    {
                        'deleteContentRange': {
                            'range': {
                                'startIndex': 1,
                                'endIndex': -1
                            }
                        }
                    },
                    {
                        'insertText': {
                            'location': {
                                'index': 1
                            },
                            'text': content
                        }
                    }
                ]
            
            self.docs_service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': requests}
            ).execute()
            
            return {
                'success': True,
                'document_id': document_id,
                'message': 'Document updated successfully'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def list_documents(self, page_size: int = 10) -> List[Dict]:
        """List all Google Docs"""
        try:
            results = self.drive_service.files().list(
                pageSize=page_size,
                q="mimeType='application/vnd.google-apps.document'",
                fields="nextPageToken, files(id, name, createdTime, modifiedTime, webViewLink)"
            ).execute()
            
            documents = results.get('files', [])
            return documents
            
        except Exception as e:
            return {'error': str(e)}
    
    def search_documents(self, query: str, page_size: int = 10) -> List[Dict]:
        """Search for documents by content or title"""
        try:
            # Search in Drive for documents
            results = self.drive_service.files().list(
                pageSize=page_size,
                q=f"mimeType='application/vnd.google-apps.document' and (name contains '{query}' or fullText contains '{query}')",
                fields="nextPageToken, files(id, name, createdTime, modifiedTime, webViewLink)"
            ).execute()
            
            documents = results.get('files', [])
            return documents
            
        except Exception as e:
            return {'error': str(e)}
    
    def delete_document(self, document_id: str) -> Dict:
        """Delete a Google Doc"""
        try:
            self.drive_service.files().delete(fileId=document_id).execute()
            
            return {
                'success': True,
                'message': f'Document {document_id} deleted successfully'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def share_document(self, document_id: str, email: str, role: str = 'reader') -> Dict:
        """Share a document with specific permissions"""
        try:
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }
            
            result = self.drive_service.permissions().create(
                fileId=document_id,
                body=permission,
                fields='id, emailAddress, role'
            ).execute()
            
            return {
                'success': True,
                'permission_id': result.get('id'),
                'email': result.get('emailAddress'),
                'role': result.get('role')
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def export_document(self, document_id: str, export_format: str = 'pdf', output_path: str = None) -> Dict:
        """Export document in different formats"""
        try:
            if not output_path:
                output_path = f"exported_doc.{export_format}"
            
            # Supported export formats
            mime_types = {
                'pdf': 'application/pdf',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'txt': 'text/plain',
                'html': 'text/html'
            }
            
            if export_format not in mime_types:
                return {'error': f'Unsupported export format: {export_format}'}
            
            mime_type = mime_types[export_format]
            
            request = self.drive_service.files().export_media(
                fileId=document_id,
                mimeType=mime_type
            )
            
            with open(output_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
            
            return {
                'success': True,
                'output_path': output_path,
                'format': export_format,
                'message': f'Document exported as {export_format}'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def add_comment(self, document_id: str, content: str, location: int = 1) -> Dict:
        """Add a comment to a document"""
        try:
            requests = [
                {
                    'createComment': {
                        'comment': {
                            'content': content
                        },
                        'location': {
                            'index': location
                        }
                    }
                }
            ]
            
            result = self.docs_service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': requests}
            ).execute()
            
            return {
                'success': True,
                'comment_id': result.get('replies', [{}])[0].get('createComment', {}).get('comment', {}).get('commentId'),
                'message': 'Comment added successfully'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_document_permissions(self, document_id: str) -> List[Dict]:
        """Get list of users who have access to the document"""
        try:
            permissions = self.drive_service.permissions().list(
                fileId=document_id,
                fields="permissions(id, emailAddress, role, type, displayName)"
            ).execute()
            
            return permissions.get('permissions', [])
            
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_text_content(self, document: Dict) -> str:
        """Extract text content from document body"""
        content = ""
        
        if 'body' in document and 'content' in document['body']:
            for element in document['body']['content']:
                if 'paragraph' in element:
                    for para_element in element['paragraph']['elements']:
                        if 'textRun' in para_element:
                            content += para_element['textRun']['content']
                    content += '\n'
        
        return content.strip()
