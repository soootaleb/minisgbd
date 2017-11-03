# from helpers import *
# from exceptions import *

# import os, uuid, time

# F = 2

# pages_states = dict()

# def get_lru():
#     lru_pid = None
#     lru_time = None
#     for k, v in pages_states.items():
#         if lru_time is None or lru_time > v['used']:
#             lru_time = v['used']
#             lru_pid = k

#     return lru_pid

# def create_file(file_id):
#     check_file_id(file_id)
#     files = os.listdir(DATABASE)
#     file_name = mount_file_name(file_id)
#     if file_name in files: raise MiniFileExistsError('File {} already exists'.format(file_name))
#     else: open(os.path.join(DATABASE, file_name), 'wb')

# def add_page(file_id):
#     from models import PageId
#     check_file_id(file_id)
#     pid = PageId(file_id)
#     file_name = mount_file_name(pid.file_id)
#     f = open(os.path.join(DATABASE, file_name), 'ab')
#     pid.idx = f.tell()
#     f.close()
#     return pid

# def read_page(pid, buffer):
#     check_buffer(buffer)
#     f = open(os.path.join(DATABASE, pid.get_file_name()), 'rb')
#     f.seek(pid.idx)
#     content = f.read(PAGE_SIZE)
#     buffer.append(content.decode().split(DATA_SEP))
#     f.close()

# def write_page(pid, buffer):
#     f = open(os.path.join(DATABASE, pid.get_file_name()), 'rb+')
#     f.seek(pid.idx)
#     f.write(bytes(DATA_SEP.join(buffer), 'utf-8'))
#     f.close()

# def get_page(pid):
#     if pid not in pages_states.keys():
#         arr = []
#         read_page(pid, arr)
#         if len(pages_states.keys()) >= F:
#             lru_pid = get_lru()
#             del pages_states[lru_pid]
#         pages_states[pid.idx] = {
#             'pin_count': 1,
#             'dirty': False,
#             'page': arr,
#             'used': time.time()
#         }
#         return arr
#     else:
#         pages_states[pid.idx]['pin_count'] += 1
#         pages_states[pid.idx]['used'] = time.time()
#         return pages_states[pid.idx]['page']

# def free_page(pid, dirty):
#     if dirty:
#         pages_states[pid.idx]['dirty'] = True
#     pages_states[pid.idx]['pin_count'] -= 1