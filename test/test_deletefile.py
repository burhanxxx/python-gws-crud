# author: Muhammad Burhan Bin Din
# description: test function to delete a sample file

from gwsfunc import GoogleWorkspaceFunc

creds = GoogleWorkspaceFunc.getAuthCredential()

filename = 'sample.txt'

items = GoogleWorkspaceFunc.deleteFile(creds, filename)