from model.util import *
from model.point import *

class Deformation(Entity) :
    name = Column(String, nullable=True)
    box = ManyToOne('Box') # one bounding box for each deformation
    # by order of appearance in .param files:
    point = ManyToOne('Point') # lat/lon params
    resolution = Column(Float) # looks like resolution in meters
    max_value = Column(Float) # could be a maximum value of some sort
    arcseconds = Column(Float) # complete guess on this one
    x = Column(Float) # usually 15.0
    y = Column(Float) # usually 90.0
    easting = Column(Float) # possibly
    northing = Column(Float) # possibly
