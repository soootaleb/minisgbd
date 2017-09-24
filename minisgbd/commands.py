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
    The creation involves creating the attached file
    '''
    manager.dbdef.create_relation(args[0], args[1], args[2:])