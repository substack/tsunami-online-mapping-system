from model.util import *

class Point(Entity) :
    longitude = Column(Float)
    latitude = Column(Float)

class Box(Entity) :
    west = Column(Float)
    south = Column(Float)
    east = Column(Float)
    north = Column(Float)
