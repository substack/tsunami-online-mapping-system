from __common__ import *

@get('/data/grids')
def grids(request) :
    return Grid.json()

@get('/data/grids/names')
def grid_names(request) :
    return js.dumps([ x[0] for x in session.query(Grid.name).all() ])

@get('/data/grids/name/(?P<name>.+)')
def grid_from_name(request, name) :
    return Grid.json(Grid.query.filter_by(name=name))
