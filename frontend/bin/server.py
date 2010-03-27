#!/usr/bin/env python

from itty import *

@get('/')
def index(web) :
    return 'Hello!'

@get('/:')
def moo(web) :
    return 'default route'

if __name__ == '__main__' :
    import sys, os
    if sys.argv[0] == '' : sys.argv[0] = './'
    dbfile = '%s/../data/db.sqlite3' % os.path.abspath(
        os.path.dirname(sys.argv[0])
    )
    run_itty()
