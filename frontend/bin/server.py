#!/usr/bin/env python

from juno import *

@route('/')
def index(web) :
    return str(dir(web))

@route(':')
def moo(web) :
    return 'default'

run()
