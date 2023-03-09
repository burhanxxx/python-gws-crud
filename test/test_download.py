# author: Muhammad Burhan Bin Din
# description: test function to download a sample file

from gwsfunc import GoogleWorkspaceFunc

creds = GoogleWorkspaceFunc.getAuthCredential()

filename = 'sample.txt'

items = GoogleWorkspaceFunc.downloadFile(creds, filename)