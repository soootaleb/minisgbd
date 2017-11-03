from helpers import *
from commands import *
from settings import *

import os

try:
    os.remove(os.path.join(DATABASE, 'Data_0.rf'))
except:
    pass

# CREATE

for args in [
    ['create', 'user', 'string', 'string']
]:
    cprint(args)
    create(args)

# INSERT

for args in [
    ['insert', 'user', 'john', 'doe'],
]:
    cprint(args)
    insert(args)


exit(0)