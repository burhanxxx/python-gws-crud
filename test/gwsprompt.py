# author: Muhammad Burhan Bin Din
# description: Run the Google Workspace Functions through CLI
# python version: 3.10.10

import re
import os

from gwsfunc import GoogleWorkspaceFunc

def clearCmd():
    os.system('cls')

def voidCmd():
    print('Unidentified Command! Try again!')

def listCmd():

    creds = GoogleWorkspaceFunc.getAuthCredential()
    items = GoogleWorkspaceFunc.listFiles(creds)

    if not items:
        print('No file found.')

    else:
        print('Files list:')
        for item in items:
            print(item)

def refreshCmd():

    GoogleWorkspaceFunc.refreshAuthToken()

def exitCmd(cmd):
    pat = '^exit|quit$'
    if re.match(pat, cmd, re.IGNORECASE):
        return True
    
    return False

def mainCmd(cmd):
    pat = '^\A(exit|quit|clear|refresh|list)$'
    mat = re.match(pat, cmd, re.IGNORECASE)
    if mat:
        return mat.group().lower()
    return 'void'

def initialFunc():
    command = ''
    while True:
        command = input('>>> ')
        command = mainCmd(command)

        if exitCmd(command):
            break
        
        func = globals()[ command +'Cmd' ]
        func()

# author:
# - Muhammad Burhan Bin Din
# reference(s): 
# - https://stackoverflow.com/questions/3987041/run-function-from-the-command-line
if __name__ == '__main__':
    initialFunc()