from helpers import *
from commands import *
from settings import *

import os

try:
    for o in os.listdir(DATABASE):
        os.remove(os.path.join(DATABASE, o))
except:
    pass

for args in [
    ['user', 'int', 'string3']
]:
    cprint(args)
    create(args)

# INSERT

for args in [
    ['user', '345', 'doe'],
]:
    cprint(args)
    insert(args)

read()

exit(0)