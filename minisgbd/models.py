from helpers import *
from settings import *
from functions import *
from exceptions import *

import uuid, pickle, os, time

class PageId:
    idx = None
    file_id = None

    def __init__(self, file_id):
        check_file_id(file_id)
        self.file_id = file_id

    def get_file_name(self):
        return mount_file_name(self.file_id)

class Record:
    attributes = [] # Strings only

    def set_values(self, values):
        self.attributes = values

class RelDef:
    file_id = None
    rel_schema = None
    record_size = 0

    def __init__(self, file_id, rel_schema):
        self.file_id = file_id
        self.rel_schema = rel_schema

class RelSchema:
    name = 'DEFAULT_RELSCHEMA_NAME'
    columns_types = []
    columns_number = 0

    def __init__(self, name, columns_number, columns_types):
        self.name = name
        self.columns_types = columns_types
        self.columns_number = columns_number

    def __str__(self):
        return c(self.name) + ' with columns ' + str(self.columns_types)

class DbDef:
    counter = 0
    relations = []

class HeapFile:
    relation = None

    def __init__(self, relation):
        self.relation = relation

    def create_header(self, buffer):
        pid = buffer.disk.add_page(self.relation.file_id)
        page = buffer.get_page(pid)
        page.append(0)
        buffer.free_page(pid, True)

class DiskManager:
    
    def create_file(self, file_id):
        check_file_id(file_id)
        files = os.listdir(DATABASE)
        file_name = mount_file_name(file_id)
        if file_name in files: raise MiniFileExistsError('File {} already exists'.format(file_name))
        else: open(os.path.join(DATABASE, file_name), 'wb')

    def add_page(self, file_id):
        check_file_id(file_id)
        pid = PageId(file_id)
        file_name = mount_file_name(pid.file_id)
        f = open(os.path.join(DATABASE, file_name), 'ab')
        pid.idx = f.tell()
        f.close()
        return pid

    def read_page(self, pid, buffer):
        check_buffer(buffer)
        f = open(os.path.join(DATABASE, pid.get_file_name()), 'rb')
        f.seek(pid.idx)
        content = f.read(PAGE_SIZE)
        buffer.append(content.decode().split(DATA_SEP))
        f.close()

    def write_page(self, pid, buffer):
        f = open(os.path.join(DATABASE, pid.get_file_name()), 'rb+')
        f.seek(pid.idx)
        f.write(bytes(DATA_SEP.join(buffer), 'utf-8'))
        f.close()

class BufferManager:

    F = 2
    disk = DiskManager()
    pages_states = dict()
    
    def get_lru(self):
        lru_pid = None
        lru_time = None
        for k, v in self.pages_states.items():
            if lru_time is None or lru_time > v['used']:
                lru_time = v['used']
                lru_pid = k

        return lru_pid
    
    def get_page(self, pid):
        if pid not in self.pages_states.keys():
            arr = []
            self.disk.read_page(pid, arr)
            if len(self.pages_states.keys()) >= self.F:
                lru_pid = self.get_lru()
                del self.pages_states[lru_pid]
            self.pages_states[pid.idx] = {
                'pin_count': 1,
                'dirty': False,
                'page': arr,
                'used': time.time()
            }
            return arr
        else:
            self.pages_states[pid.idx]['pin_count'] += 1
            self.pages_states[pid.idx]['used'] = time.time()
            return self.pages_states[pid.idx]['page']

    def free_page(self, pid, dirty):
        if dirty:
            self.pages_states[pid.idx]['dirty'] = True
        self.pages_states[pid.idx]['pin_count'] -= 1

class GlobalManager:
    dbdef = None
    files = []
    buffer = BufferManager()

    def __init__(self):
        self.dbdef = DbDef()
        try:
            with open(os.path.join(DATABASE, 'Catalog.def'), 'rb') as obj:
                self.dbdef = pickle.load(obj)
        except Exception:
            pass
        
        self.refresh_heap_files()

    def refresh_heap_files(self):
        for rel_def in self.dbdef.relations:
            self.files.append(HeapFile(rel_def))

    def finish(self):
        with open(os.path.join(DATABASE, 'Catalog.def'), 'wb') as output:
            pickle.dump(self.dbdef, output, pickle.HIGHEST_PROTOCOL)

    def calculate_record_size(self, columns_types):
        count = 0
        for column in columns_types:
            if column == 'int' or column == 'float':
                count += 4
            elif column[:6] == 'string':
                try:
                    count += int(column[6:])
                except Exception:
                    raise MiniColumnTypeError('Type {} is not correct'.format(column))
            else:
                raise MiniColumnTypeError('Type {} is not correct'.format(column))
        return count

    def create_relation(self, name, columns_number, columns_types):
        rel_schema = RelSchema(name, columns_number, columns_types)
        rel_def = RelDef(self.dbdef.counter, rel_schema)
        rel_def.record_size = GlobalManager.calculate_record_size(columns_types)
        self.dbdef.relations.append(rel_def)
        self.dbdef.counter += 1
        self.buffer.disk.create_file(rel_def.file_id)
        hf = HeapFile(rel_def)
        hf.create_header(self.buffer)
        self.files.append(hf)

    def insert(self, relation, values):
        rec = Record()
        rec.set_values(values)