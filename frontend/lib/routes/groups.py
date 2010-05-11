from __common__ import *

@get('/data/groups')
def groups(request) :
    return Group.json()

@get('/data/groups/names')
def group_names(request) :
    return js.dumps([ x[0] for x in session.query(Group.name).all() ])

@get('/data/groups/name/(?P<name>.+)')
def group_from_name(request, name) :
    return Group.json(Group.query.filter_by(name=name))
