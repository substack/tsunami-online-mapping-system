from __common__ import *

@get('/data/scenarios/get')
def scenarios(request) :
    return Scenario.json()

@get('/data/scenarios/get/id/(?P<sid>.+)')
def scenarios(request, sid) :
    return Scenario.json(Scenario.query.filter_by(id=id))

@get('/data/scenarios/get/(?P<sid>\d+)/markers')
def scenarios(request, sid) :
    return Marker.json(Scenario.get_by(id=sid).markers)

@get('/data/scenarios/get/(?P<sid>\d+)/grids')
def scenarios(request, sid) :
    return Marker.json(Scenario.get_by(id=sid).grids)
