# author: Muhammad Burhan Bin Din
# description: Google Workspace python function to list, upload, download, delete, and etc
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START drive_quickstart]
from __future__ import print_function

import io
import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
# refer to https://developers.google.com/identity/protocols/oauth2/scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleWorkspaceFunc:

    @staticmethod
    def refreshAuthToken():
        filename = 'token.json'
        tokenjson = None
        for root, dir, files in os.walk(os.path.curdir):
            if filename in files:
                tokenjson = os.path.join(root, filename)
                break
        
        print(F'Removing {filename}')
        
        if tokenjson is not None:
            os.remove(tokenjson)
            print(F'Removed {tokenjson}')
        else:
            print(F'Not found {filename}')

        return GoogleWorkspaceFunc.getAuthCredential()

    @staticmethod
    def getAuthCredential():

        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        tokenjson = os.path.dirname(__file__) + '\\token.json'
        if os.path.exists(tokenjson):
            creds = Credentials.from_authorized_user_file(tokenjson, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        credentialsjson = os.path.dirname(__file__) + '\\credentials.json'
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentialsjson, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(tokenjson, 'w') as token:
                token.write(creds.to_json())

        return creds

    @staticmethod
    def listFiles(creds):

        items = None

        try:
            service = build('drive', 'v3', credentials=creds)

            # Call the Drive v3 API
            results = service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            
            return items
            
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}') 
            items = None 

    @staticmethod
    def uploadFile(creds, filepath):

        filepath = F'{os.path.dirname(__file__)}\\{filepath}'
        # restrict upload file within the python execution folder
        if not os.path.exists(filepath):
            print(f'No such file: {filepath}')
            return
        
        try:
            # create drive api client
            service = build('drive', 'v3', credentials=creds)
            # example file meta upload into specific parents. remove parents properties if not needed
            file_metadata = {'name': os.path.basename(filepath), 'parents': ['1IQbidLPlPAP73JjkfO69S-Vqj1etXHPA']}
            media = MediaFileUpload(filepath, mimetype='application/octet-stream')
            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, media_body=media,
                                        fields='id').execute()
            print(F'File ID: {file.get("id")}')
            print(F'Uploaded: {filepath}')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.get('id')      

    @staticmethod
    def downloadFile(creds, filename):

        items = GoogleWorkspaceFunc.listFiles(creds)
        fileid = None

        if items is None or not items:
            print('No files found.')
            return
        else:
            for item in items:
                if item['name'] == filename:
                    print(u'{0} ({1})'.format(item['name'], item['id']))
                    fileid = item['id']
                    break
        
        if fileid is None:
            print(F'No file {filename} found.')
            return
        
        try:
            # create drive api client
            service = build('drive', 'v3', credentials=creds)

            file_id = fileid

            # pylint: disable=maybe-no-member
            request = service.files().get_media(fileId=file_id)
            file = io.FileIO(filename, 'w')
            # file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return None  

    @staticmethod
    def deleteFile(creds, filename):

        items = GoogleWorkspaceFunc.listFiles(creds)
        fileid = None

        if items is None or not items:
            print('No files found.')
            return
        else:
            for item in items:
                if item['name'] == filename:
                    print(u'{0} ({1})'.format(item['name'], item['id']))
                    fileid = item['id']
                    break
        
        if fileid is None:
            print(F'No file {filename} found.')
            return
        
        try:
            # create drive api client
            service = build('drive', 'v3', credentials=creds)

            file_id = fileid

            # pylint: disable=maybe-no-member
            print(F'Delete {filename}.')
            service.files().delete(fileId=file_id).execute()


        except HttpError as error:
            print(F'An error occurred: {error}')

        return None    

