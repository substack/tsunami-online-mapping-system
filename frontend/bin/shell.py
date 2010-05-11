# Execute with: python -i shell.py
# alternative script for accessing data in the database

import os,sys
# add lib to search path
if sys.argv[0] == '' : sys.argv[0] = './'
basepath = '%s/../' % os.path.abspath(
    os.path.dirname(sys.argv[0])
)
sys.path.append('%s/lib' % basepath)

from model import *
from db import bind_db
bind_db('../data/tsunami.sqlite3')
