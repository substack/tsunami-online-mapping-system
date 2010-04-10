from model.util import *
from model.point import *

class Earthquake(Entity) :
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    # by order of appearance in .param files:
    longitude = Column(Float) # longitude of quake
    latitude = Column(Float) # latitude of quake
    depth = Column(Float) # depth of quake in meters
    strike = Column(Float)
    dip = Column(Float) # in degrees
    rake = Column(Float)
    slip = Column(Float)
    length = Column(Float) # fault length in meters
    width = Column(Float) # fault width in meters
    
    # Moment and moment magnitudes explained in:
    # http://www.earth.northwestern.edu/people/seth/research/sumatra.html
    
    def mw(self) :
        "Compute the quake's moment magnitude Mw"
        from math import log
        return log( self.m0() ) / log(10) / 1.5 - 10.73
    
    def m0(self) :
        "Compute the quake's seismic moment m0 in dyn-cm"
        from math import cos, radians
        mu = 3.6e+11
        area = self.width * self.length / cos(radians(self.dip)) * 1e+6 * 1e+6
        return self.slip * mu * area
    
    def param_format(self) :
        'Output the deformation data in .param format'
        return ' '.join([
            self.longitude,
            self.latitude,
            self.depth,
            self.strike,
            self.dip,
            self.rake,
            self.slip,
            self.length,
            self.width,
        ])
