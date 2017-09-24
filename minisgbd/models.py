from helpers import *
from functions import *

import uuid

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

    def create_relation(self, name, columns_number, columns_types):
        rel_schema = RelSchema(name, columns_number, columns_types)
        rel_def = RelDef(self.counter, rel_schema)
        self.relations.append(rel_def)
        self.counter += 1
        create_file(rel_def.file_id)

class GlobalManager:
    dbdef = None

    def __init__(self):
        self.dbdef = DbDef()

class PageId:
    idx = None
    file_id = None

    def __init__(self, file_id):
        check_file_id(file_id)
        self.file_id = file_id

    def get_file_name(self):
        return mount_file_name(self.file_id)