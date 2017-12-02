from models import *
from helpers import *

import inspect, sys

manager = GlobalManager()

def help():
    '''
    Help function will list available commands & display attached python documentation
    '''
    cprint('Here is a list of available functions', 'OKBLUE')
    members = inspect.getmembers(sys.modules[__name__], lambda o: hasattr(o, '__globals__') and '__file__' in o.__globals__ and o.__globals__['__file__'][-11:-3] == 'commands')
    for o in members:
        cprint('- {}: {}'.format(o[0], o[1].__doc__ if o[1].__doc__ is not None else 'No documentation found'), 'OKBLUE')

def create(args):
    '''
    Creates a relation object using the global manager's DbDef object.
    The creation involves creating the attached file.
    @syntax: create <relname> <field> <field>...
    @param1: relname The relation name to create
    @param2: num_columns The number of columns in the relation
    @paramN: value... The relations values (fields). N must be == to @param2 num_columns + 2
    @example: create user firstname lastname
    '''
    manager.create_relation(args[0], args[1], args[2:])

def insert(args):
    '''
    Insert a record in a relation.
    @syntax: insert <relname> <value> <value>...
    @param1: relname The relation name to insert a record in
    @paramN: value... The record values (fields)
    @example: insert user john doe
    '''
    manager.insert(args[0], args[1:])

def read():
    file = open(os.path.join(DATABASE, 'Data_0.rf'), 'rb')
    file.seek(0)
    print(file.read().decode().strip('\x00'))