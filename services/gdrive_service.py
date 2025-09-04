import io
import os
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from google.oauth2.credentials import Credentials

class GoogleDriveService:
    def __init__(self, credentials: Credentials):
        self.service = build('drive', 'v3', credentials=credentials)
    
    def list_files(self, page_size: int = 10, query: str = None) -> List[Dict]:
        """List files in Google Drive"""
        try:
            if query:
                results = self.service.files().list(
                    pageSize=page_size,
                    q=query,
                    fields="nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime, parents, webViewLink)"
                ).execute()
            else:
                results = self.service.files().list(
                    pageSize=page_size,
                    fields="nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime, parents, webViewLink)"
                ).execute()
            
            files = results.get('files', [])
            return files
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_file_info(self, file_id: str) -> Dict:
        """Get detailed information about a specific file"""
        try:
            file_info = self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, size, createdTime, modifiedTime, parents, webViewLink, description, owners, permissions"
            ).execute()
            
            return file_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def create_folder(self, name: str, parent_id: str = None) -> Dict:
        """Create a new folder in Google Drive"""
        try:
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id, name, mimeType, webViewLink'
            ).execute()
            
            return {
                'success': True,
                'folder_id': folder.get('id'),
                'name': folder.get('name'),
                'web_link': folder.get('webViewLink')
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def upload_file(self, file_path: str, name: str = None, parent_id: str = None, mime_type: str = None) -> Dict:
        """Upload a file to Google Drive"""
        try:
            if not os.path.exists(file_path):
                return {'error': 'File not found'}
            
            if not name:
                name = os.path.basename(file_path)
            
            if not mime_type:
                # Try to guess MIME type from file extension
                import mimetypes
                mime_type, _ = mimetypes.guess_type(file_path)
                if not mime_type:
                    mime_type = 'application/octet-stream'
            
            file_metadata = {'name': name}
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            media = MediaIoBaseUpload(
                io.FileIO(file_path, 'rb'),
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, mimeType, size, webViewLink'
            ).execute()
            
            return {
                'success': True,
                'file_id': file.get('id'),
                'name': file.get('name'),
                'size': file.get('size'),
                'web_link': file.get('webViewLink')
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def download_file(self, file_id: str, destination_path: str) -> Dict:
        """Download a file from Google Drive"""
        try:
            file_info = self.service.files().get(fileId=file_id).execute()
            
            request = self.service.files().get_media(fileId=file_id)
            
            with open(destination_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
            
            return {
                'success': True,
                'file_path': destination_path,
                'file_name': file_info.get('name'),
                'size': file_info.get('size')
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def share_file(self, file_id: str, email: str, role: str = 'reader', type: str = 'user') -> Dict:
        """Share a file with specific permissions"""
        try:
            permission = {
                'type': type,
                'role': role,
                'emailAddress': email
            }
            
            result = self.service.permissions().create(
                fileId=file_id,
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
    
    def search_files(self, query: str, page_size: int = 10) -> List[Dict]:
        """Search for files using Google Drive query syntax"""
        try:
            results = self.service.files().list(
                q=query,
                pageSize=page_size,
                fields="nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            return files
            
        except Exception as e:
            return {'error': str(e)}
    
    def delete_file(self, file_id: str) -> Dict:
        """Delete a file from Google Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            
            return {
                'success': True,
                'message': f'File {file_id} deleted successfully'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def move_file(self, file_id: str, new_parent_id: str) -> Dict:
        """Move a file to a different folder"""
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='parents'
            ).execute()
            
            previous_parents = ",".join(file.get('parents', []))
            
            file = self.service.files().update(
                fileId=file_id,
                addParents=new_parent_id,
                removeParents=previous_parents,
                fields='id, name, parents'
            ).execute()
            
            return {
                'success': True,
                'file_id': file.get('id'),
                'name': file.get('name'),
                'new_parent': new_parent_id
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_shared_files(self, page_size: int = 10) -> List[Dict]:
        """Get files shared with the current user"""
        try:
            results = self.service.files().list(
                pageSize=page_size,
                q="sharedWithMe=true",
                fields="nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            return files
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_starred_files(self, page_size: int = 10) -> List[Dict]:
        """Get starred files"""
        try:
            results = self.service.files().list(
                pageSize=page_size,
                q="starred=true",
                fields="nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            return files
            
        except Exception as e:
            return {'error': str(e)}
