from model.util import *
from model.point import *

class Grid(Entity) :
    name = Column(String)
    box = ManyToOne('Box') # each grid has one bounding box
    points = OneToMany('Point') # each grid has many boundary points
    parent = ManyToOne('Grid', nullable=True) # each grid may have one parent
