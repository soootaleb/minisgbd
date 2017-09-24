from models import *
from helpers import *

manager = GlobalManager()

def help():
    cprint('This is the help function', 'WARNING')

def create(args):
    manager.dbdef.create_relation(args[0], args[1], args[2:])