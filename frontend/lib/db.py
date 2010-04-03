from elixir import *
# all columns are not nullable, which should be the default
Column = (lambda *args, **kwargs :
    Field(*args, **(dict([('nullable',False)] + kwargs.items())))
)

def bind_db(filename) :
    metadata.bind = 'sqlite:///%s' % filename
    metadata.bind.echo = True
    
    import os
    setup_all()
    if not os.path.exists(filename) : create_all()

class Point(Entity) :
    longitude = Column(Float)
    latitude = Column(Float)

class Grid(Entity) :
    name = Column(String)
    points = OneToMany('GridPoint') # one grid for many points

class GridPoint(Point) :
    grid = ManyToOne('Grid') # many points in one grid

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

class Scenario(Entity) :
    modeling_time = Column(Float) # hours
    time_step = Column(Float) # seconds
    output_step = Column(Float) # seconds
    sea_level = Column(Float) # meters
    bottom_friction = Column(Float) # coefficient
    earth_radius = Column(Float) # meters
    earth_gravity = Column(Float) # m/(s*s)
    earth_rotation = Column(Float) # Hz
    # each scenario has one grid and one deformation
    grid = ManyToOne('Grid')
    deformation = ManyToOne('Deformation')
    # a scenario can be submitted multiple times potentially
    # when the processing fails for some reason
    jobs = OneToMany('Job')

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
