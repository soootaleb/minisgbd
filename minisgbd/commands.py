from models import RelSchema
from helpers import cprint, c

def help():
    cprint('This is the help function', 'WARNING')

def create(args):
    rel = RelSchema(args[0], args[2:], args[1])
    print(rel)