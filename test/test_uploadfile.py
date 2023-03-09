# author: Muhammad Burhan Bin Din
# description: test function to upload a sample file

from gwsfunc import GoogleWorkspaceFunc

creds = GoogleWorkspaceFunc.getAuthCredential()

filepath = 'upload\\sample.txt'

items = GoogleWorkspaceFunc.uploadFile(creds, filepath)

