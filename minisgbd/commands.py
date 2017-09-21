from models import *
from helpers import *

def help():
    cprint('This is the help function', 'WARNING')

def create(args):
    rel = RelSchema(args[0], args[2:], args[1])
    print(rel)    