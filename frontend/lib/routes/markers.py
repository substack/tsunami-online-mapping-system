from __common__ import *

@get('/data/markers/get')
def markers(request) :
    return Marker.json()

@get('/data/markers/get/system')
def markers(request) :
    return Marker.json(Marker.query.filter_by(user=False))

@get('/data/markers/get/system/names')
def marker_names(request) :
    return js.dumps([
        x[0] for x in
        session.query(Marker.name).filter_by(user=False)
    ])

@get('/data/markers/get/system/name/(?P<name>.+)')
def marker_from_name(request, name) :
    return Marker.json(Marker.query.filter_by(name=name, user=False))

@get('/data/markers/get/user')
def markers(request) :
    return Marker.json(Marker.query.filter_by(user=True))

@get('/data/markers/get/user/name/(?P<name>.+)')
def marker_from_name(request, name) :
    return Marker.json(Marker.query.filter_by(name=name, user=True))
