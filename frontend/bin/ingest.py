#!/usr/bin/env python
# add lib to search path
import sys, os
if sys.argv[0] == '' : sys.argv[0] = './'
basepath = '%s/../' % os.path.abspath(
    os.path.dirname(sys.argv[0])
)
sys.path.append('%s/lib' % basepath)

import time
def sleep() : time.sleep(1.0)

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

def ingest_grids() :
    from sqlalchemy.exc import OperationalError
    dangling = {}
    for g in grids :
        sleep()
        
        p = g['parent']
        
        parent = None
        if Grid.query.filter_by(name=p).count() == 1 :
            parent = Grid.query.filter_by(name=p).first()
        else :
            if p not in dangling : dangling[p] = []
            dangling[p].append(g['name'])
        
        print(g)
        
        if Grid.query.filter_by(name=g['name']).count() == 0 :
            # grid doesn't exist, create a new one
            print("Creating new grid")
            grid = Grid()
        else :
            print("Updating existing grid")
            grid = Grid.query.filter_by(name=g['name']).first()
        
        grid.name = g['name']
        grid.description = g['readme'][0]
        
        if grid.points :
            # don't add duplicate points
            prev_ext = [ (p.lat,p.lon) for p in grid.points ]
            if sort(prev_ext) == sort(g['extent']) :
                grid.points=[
                    Point(latitude=lat, longitude=lon)
                    for (lat,lon) in g['extent']
                ]
        
        grid.parent = parent
        grid.west, grid.east, grid.south, grid.north = g['mm']
        
        session.merge(grid)
        session.commit()
    
    for (parent,names) in dangling.items() :
        for name in names :
            Grid.query.filter_by(name=name).first().parent = \
                Grid.query.filter_by(name=parent).first()
    
    session.commit()
    session.flush()

def ingest_deformations() :
    from sqlalchemy.exc import OperationalError
    import time
    dangling = []
    for d in deformations :
        sleep()
        extent = d['extent']
        
        for p in d['param'] :
            print(p)
            if Deformation.query.filter_by(name=d['name']).count() == 0 :
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
            name, grid_name, group_name, desc = params[2:]
            
            group = Group.query.filter_by(name=group_name).first()
            if not group : group = Group(name=group_name)
            grid = Grid.query.filter_by(name=grid_name).first()
            
            marker = Marker(
                name=name,
                description=desc,
                grid=grid,
                group=group,
                longitude=lon,
                latitude=lat,
            )
            session.add(marker)
        session.commit()
        sleep()
    session.flush()

def ingest() :
    #ingest_grids()
    ingest_deformations()
    #ingest_markers()
    print(
        'Ingest complete:\n    %d grids, %d deformations, %d markers, %d groups'
        % tuple(x.query.count() for x in [Grid,Deformation,Marker,Group])
    )

if __name__ == '__main__' :
    import sys, os
    app = TsunamiApp(basepath)
    bind_db(app.root('data/tsunami.sqlite3'))
    ingest()
