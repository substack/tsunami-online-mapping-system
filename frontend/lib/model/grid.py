from model.util import *
from model.point import *

class Grid(Entity) :
    name = Column(String)
    extent = ManyToOne('Extent') # each grid has one deformation
    parent = ManyToOne('Grid') # each grid may have one parent
