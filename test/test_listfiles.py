# author: Muhammad Burhan Bin Din
# description: test function to list files in drive

from gwsfunc import GoogleWorkspaceFunc

creds = GoogleWorkspaceFunc.getAuthCredential()

items = GoogleWorkspaceFunc.listFiles(creds)

if not items:
    print('No files found.')

else:
    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))
        print(item)