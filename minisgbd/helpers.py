from minisgbd.settings import *
from minisgbd.exceptions import *

def c(val, color='BOLD'):
    return COLORS[color] + str(val) + COLORS['ENDC']

def cprint(val, color='HEADER'):
    print(c(val, color))

def mount_file_name(file_id):
    return 'Data_{}.rf'.format(file_id)

def check_buffer(buffer):
    if type(buffer) is None: raise MiniBufferValueError('The buffer specified is None')
    if type(buffer) is not list: raise MiniBufferValueError('The buffer specified is not an array')
    if len(buffer) > 0: raise MiniBufferValueError('The buffer specified is not empty')

def check_file_id(file_id):
    '''
    Check if the file_id is OK:
        - file_id is not None
        - type(file_id) is int
        - file_id >= 0
    '''
    if file_id is None: raise MiniFileNameValueError('Trying to create a file with None file_id')
    if type(file_id) is not int: raise MiniFileNameValueError('Trying to create a file with type(file_id) != int')
    if file_id < 0: raise MiniFileNameValueError('Trying to create a file with file_id < 0')
