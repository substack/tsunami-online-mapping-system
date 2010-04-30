from __common__ import *

@get('/data/deformations')
def deformations(request) :
    return Deformation.json()

@get('/data/deformations/names')
def deformation_names(request) :
    return js.dumps([ x[0] for x in session.query(Deformation.name).all() ])

@get('/data/deformations/name/(?P<name>.+)')
def deformation_from_name(request, name) :
    return Deformation.json(Deformation.query.filter_by(name=name))
