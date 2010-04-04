from model.util import *
from model.point import *

class Deformation(Entity) :
    name = Column(String)
    points = OneToMany('DeformationPoint') # one deformation for many points
    extent = ManyToOne('Extent') # many deformations

class DeformationPoint(Point) :
    deformation = ManyToOne('Deformation') # many points in one deformation

class Extent(Entity) :
    west = Column(Float)
    south = Column(Float)
    east = Column(Float)
    north = Column(Float)
    deformations = OneToMany('Deformation')
