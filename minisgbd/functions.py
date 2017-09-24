from models import *
from exceptions import *
import os, uuid

def create_file(file_id):
    check_file_id(file_id)
    files = os.listdir(DATABASE)
    file_name = mount_file_name(file_id)
    if file_name in files: raise MiniFileExistsError('File {} already exists'.format(file_name))
    else: open(os.path.join(DATABASE, file_name), 'wb')

def add_page(file_id):
    check_file_id(file_id)
    pid = PageId(file_id)
    file_name = mount_file_name(pid.file_id)
    f = open(os.path.join(DATABASE, file_name), 'ab')
    pid.idx = f.tell()
    f.close()
    return pid

def read_page(pid, buffer):
    check_buffer(buffer)
    f = open(os.path.join(DATABASE, pid.get_file_name()), 'rb')
    f.seek(pid.idx)
    content = f.read(PAGE_SIZE)
    buffer.append(content.decode().split(DATA_SEP))
    f.close()

def write_page(pid, buffer):
    f = open(os.path.join(DATABASE, pid.get_file_name()), 'rb+')
    f.seek(pid.idx)
    f.write(bytes(DATA_SEP.join(buffer), 'utf-8'))
    f.close()