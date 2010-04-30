from __common__ import *

@get('/data/points')
def points(request) :
    return Point.json()
