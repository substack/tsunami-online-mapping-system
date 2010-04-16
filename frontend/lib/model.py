from elixir import *
# all columns are not nullable, which should be the default
Column = (lambda *args, **kwargs :
    Field(*args, **(dict([('nullable',False)] + kwargs.items())))
)

class Deformation(Entity) :
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    user = Column(Boolean)
    
    # bounding box in degrees from .extent files:
    west = Column(Float)
    south = Column(Float)
    east = Column(Float)
    north = Column(Float)
    
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

class Group(Entity) :
    name = Column(String)
    grids = OneToMany('Grid')

class Grid(Entity) :
    name = Column(String)
    description = Column(String, nullable=True)
    group = ManyToOne('Group')
    
    points = OneToMany('GridPoint') # each grid has many boundary points
    parent = ManyToOne('Grid') # each grid may have one parent
    children = OneToMany('Grid') # and multiple children
    
    # bounding box
    west = Column(Float)
    south = Column(Float)
    east = Column(Float)
    north = Column(Float)

class GridPoint(Entity) :
    grid = ManyToOne('Grid')
    longitude = Column(Float)
    latitude = Column(Float)

class Job(Entity) :
    # a scenario may have many jobs in the case where the job fails
    scenario = ManyToOne('Scenario')
    
    status = Column(String) # pending running complete failed
    person = Column(String) # the "Investigator" of the senario
    name = Column(String)
    cputime = Column(Integer)
    nodes = Column(Integer)
    node_type = ManyToOne('NodeType')
    qtype = Column(String) # Queue type

class NodeType(Entity) :
    value = Column(String)
    
    def __init__(self,value=None) :
        ways = '4-way 16-way'.split()
        if value not in ways :
            raise 'Invalid node type "%s"\nValid types: %s' \
                % (str(value), str(ways))
        self.value = value

class Scenario(Entity) :
    modeling_time = Column(Float) # hours
    time_step = Column(Float) # seconds
    output_step = Column(Float) # seconds
    sea_level = Column(Float) # meters
    bottom_friction = Column(Float) # coefficient
    earth_radius = Column(Float) # meters
    earth_gravity = Column(Float) # m/(s*s)
    earth_rotation = Column(Float) # Hz
    # each scenario has one grid and one earthquake
    grid = ManyToOne('Grid')
    earthquake = ManyToOne('Deformation')
    # a scenario can be submitted multiple times potentially
    # when the processing fails for some reason
    jobs = OneToMany('Job')
