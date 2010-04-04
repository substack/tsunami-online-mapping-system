from model.util import *
from model.point import *

class Grid(Entity) :
    name = Column(String)
    points = OneToMany('GridPoint') # one grid for many points

class GridPoint(Point) :
    grid = ManyToOne('Grid') # many points in one grid
