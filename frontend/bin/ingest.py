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

def ingest_builder(uri, pattern=None, **kw) :
    soup = BeautifulSoup(urllib.urlopen(uri).read())
    keys = kw.keys()
    if pattern is None :
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
    else :
        defs = [
            '.'.join(str(link['href']).split('.')[:-1])
            for link in soup.findAll('a', href=pattern)
        ]
    for d in defs :
        yield dict([('name',d)] + [(
            key,
            f(urllib.urlopen('%s%s.%s' % (uri,d,key)).read())
        ) for (key,f) in kw.items()]
    )

deformations = ingest_builder(
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

grids = ingest_builder(
    'http://burn.giseis.alaska.edu/grids/',
    extent=lambda s : list(chunkby(2,map(float,s.split()))),
    mm=lambda s : map(float, s.split()),
    parent=lambda s : s.strip(),
    readme=lambda s : re.split(r'\s*,\s*', s.splitlines()[0], 1)
)

markers = ingest_builder(
    'http://burn.giseis.alaska.edu/scripts/',
    pattern=re.compile(r'^list_.+\.js$'),
    js=lambda js : [
        re.split(r'\s*,\s*',
            re.sub(r'"','',
                re.sub(r'^.+?\(\s*|\s*\).*','',x)
            ), 5
        ) for x in js.splitlines() if re.search(r'^\s+nm\[\d+\]', x)
    ],
)

from math import ceil
def chunkby(n,xs) :
    for i in range(0, int(ceil(float(len(xs)) / 2.0))) :
        yield xs[i*n:(i+1)*n]

if __name__ == '__main__' :
    import sys, os
    app = TsunamiApp(basepath)
    bind_db(app.root('data/tsunami.sqlite3'))

def ingest_grids() :
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
        
        print(g)
        
        group = None
        if len(g['readme']) == 2 :
            name = g['readme'][1]
            try :
                group = session.query(Group).filter(Group.name == name).first()
            except OperationalError :
                group = Group(name=name)
        
        grid = Grid(
            name=g['name'],
            description=g['readme'][0],
            group=group,
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

def ingest_deformations() :
    from sqlalchemy.exc import OperationalError
    import time
    dangling = []
    for d in deformations :
        time.sleep(5.0)
        extent = d['extent']
        
        for p in d['param'] :
            print(p)
            deformation = Deformation(
                name=d['name'],
                description='',
                user=(p['type'] != ''),
                # bounding box:
                west=extent[1],
                south=extent[2],
                east=extent[0],
                north=extent[3],
                # deformation parameters:
                **dict(zip("""
                    longitude latitude depth
                    strike dip rake
                    slip length width
                """.split(), p['params']))
            )
            session.add(deformation)
        session.commit()
    session.flush()

def ingest_markers() :
    import time
    for m in markers :
        for params in m['js'] :
            print(params)
            lon, lat = map(float, params[:2])
            name, grid, group, desc = params[2:]
            g = session.query(Grid).filter(Grid.name == grid).first()
            marker = Marker(
                name=name,
                description=desc,
                grid=g,
                longitude=lon,
                latitude=lat,
            )
            session.add(marker)
        session.commit()
        time.sleep(5.0)
    session.flush()
