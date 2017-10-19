from helpers import *
from settings import *
from functions import *

import uuid, pickle

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

    def create_header(self):
        pid = add_page(self.relation.file_id)
        write_page(pid, ['0'])
        # free_page(pid, True)

class GlobalManager:
    dbdef = None
    files = []

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

    def create_relation(self, name, columns_number, columns_types):
        rel_schema = RelSchema(name, columns_number, columns_types)
        rel_def = RelDef(self.dbdef.counter, rel_schema)
        self.dbdef.relations.append(rel_def)
        self.dbdef.counter += 1
        create_file(rel_def.file_id)
        hf = HeapFile(rel_def)
        hf.create_header()
        self.files.append(hf)

    def insert(self, relation, values):
        rec = Record()
        rec.set_values(values)