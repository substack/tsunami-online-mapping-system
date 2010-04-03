#!/usr/bin/env python
# add lib to search path
import sys, os
if sys.argv[0] == '' : sys.argv[0] = './'
basepath = '%s/../' % os.path.abspath(
    os.path.dirname(sys.argv[0])
)
sys.path.append('%s/lib' % basepath)

from db import *
from server import *
from BeautifulSoup import BeautifulSoup
import re, urllib

def deformations() :
    def_uri = 'http://burn.giseis.alaska.edu/deformations/'
    soup = BeautifulSoup(urllib.urlopen(def_uri).read())
    links = soup.findAll('a', href=re.compile('\.extent$'))
    for href in [ str(x['href']) for x in links ] :
        name = '.'.join(href.split('.')[:-1])
        extents = map(float, urllib.urlopen(def_uri + href).read().split())
        yield (name,extents)

if __name__ == '__main__' :
    import sys, os
    app = TsunamiApp(basepath)
    bind_db(app.root('data/tsunami.sqlite3'))
