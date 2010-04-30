from __common__ import *

@get('/data/scenarios')
def scenarios(request) :
    return Scenario.json()

@get('/data/scenarios/id/(?P<id>.+)')
def scenarios(request, id) :
    return Scenario.json(Scenario.query.filter_by(id=id))
