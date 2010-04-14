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

def ingest(uri, **kw) :
    soup = BeautifulSoup(urllib.urlopen(uri).read())
    keys = kw.keys()
    cdefs = [ # candidate definitions gathered from the first key extension
        '.'.join(str(link['href']).split('.')[:-1])
        for link in soup.findAll('a', href=re.compile(r'\.%s$' % keys[0]))
    ]
    defs = [ # definitions have files for all the keys
        d for d in cdefs if all(
            soup.find('a', href='%s.%s' % (d,key))
            for key in keys
        )
    ]
    for d in defs :
        yield dict([('name',d)] + [(
            key,
            f(urllib.urlopen('%s%s.%s' % (uri,d,key)).read())
        ) for (key,f) in kw.items()]
    )

deformations = ingest(
    'http://burn.giseis.alaska.edu/deformations/',
    extent=lambda s : map(float, s.split()),
    param=lambda s : [ # trick for where-style DRY:
        (lambda xs :
            { 'type' : '', 'params' : map(float,xs) }
                if len(xs) == 9 else 
            { 'type' : xs[0], 'params' : map(float,xs[1:]) }
        )(line.split())
        for line in s.splitlines()
    ],
)

grids = ingest(
    'http://burn.giseis.alaska.edu/grids/',
    extent=lambda s : list(chunkby(2,map(float,s.split()))),
    mm=lambda s : map(float, s.split()),
    parent=lambda s : s.strip(),
    readme=lambda s : s.splitlines()[0].split(', '),
)

from math import ceil
def chunkby(n,xs) :
    for i in range(0, int(ceil(float(len(xs)) / 2.0))) :
        yield xs[i*n:(i+1)*n]

if __name__ == '__main__' :
    import sys, os
    app = TsunamiApp(basepath)
    bind_db(app.root('data/tsunami.sqlite3'))

def populate_grids() :
    from sqlalchemy.exc import OperationalError
    import time
    dangling = []
    for g in grids :
        time.sleep(5.0)
        
        mm = g['mm']
        
        parent = None
        try :
            parent = session.query(Grid).filter(Grid.name == g['parent']).first()
        except OperationalError :
            dangling.append((g['name'],g['parent']))
        
        if session.query(Grid).filter(Grid.name == g['name']).count() > 0 :
            continue
        
        grid = Grid(
            name=g['name'],
            description=g['readme'][0],
            group=Group(
                name=g['readme'][1]
            ),
            points=[
                GridPoint(latitude=lat, longitude=lon)
                for (lat,lon) in g['extent']
            ],
            parent=parent,
            west=mm[0], east=mm[1], south=mm[2], north=mm[3],
        )
        session.add(grid)
        session.commit()
    
    for (name,parent) in dangling :
        session.query(Grid).filter(Grid.name == name).first() \
            . parent = session.query(Grid).filter(Grid.name == parent).first()
    
    session.flush()
