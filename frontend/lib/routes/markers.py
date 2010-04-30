from __common__ import *

@get('/data/markers')
def markers(request) :
    return Marker.json()

@get('/data/markers/names')
def marker_names(request) :
    return js.dumps([ x[0] for x in session.query(Marker.name).all() ])

@get('/data/markers/name/(?P<name>.+)')
def marker_from_name(request, name) :
    return Marker.json(Marker.query.filter_by(name=name))
