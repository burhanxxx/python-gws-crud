# author: Muhammad Burhan Bin Din
# description: test function to fix error on the Google Workspace credential function
# Reference:
# https://docs.python.org/3/library/os.path.html 

import os.path


print(os.path.abspath(__file__))
print(os.path.dirname(__file__))
print(os.path.dirname(__file__) + '\\token.json')

print(os.path.abspath('c:\\upload\\sample.txt'))
print(os.path.basename('upload\\sample.txt'))

print(os.path.curdir)

print(os.path.exists(os.path.abspath('c:\\upload\\sample.txt')))