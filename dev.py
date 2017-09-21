from minisgbd.models import *
from minisgbd.helpers import *
from minisgbd.settings import *
from minisgbd.functions import *
from minisgbd.exceptions import *
import uuid, os, shutil

shutil.rmtree(DATABASE)
os.mkdir(DATABASE)

FILE_ID = 1995

content1 = []
content2 = []

create_file(FILE_ID)

pid1 = add_page(FILE_ID)
write_page(pid1, PAGE_CONTENT)

pid2 = add_page(FILE_ID)
write_page(pid2, map(str.upper, PAGE_CONTENT))

read_page(pid1, content1)
read_page(pid2, content2)

exit(0)