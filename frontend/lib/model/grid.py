from model.util import *
from model.point import *

class Grid(Entity) :
    name = Column(String)
    box = ManyToOne('Box') # each grid has one bounding box
    points = OneToMany('GridPoint') # each grid has many boundary points
    parent = ManyToOne('Grid') # each grid may have one parent

class GridPoint(Point) :
    grid = ManyToOne('Grid')
