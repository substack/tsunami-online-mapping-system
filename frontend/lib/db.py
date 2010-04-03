from elixir import *
# all columns are not nullable, which should be the default
Column = (lambda *args, **kwargs :
    Field(*args, **(dict([('nullable',False)] + kwargs.items())))
)

class DB(object) :
    def __init__(self,filename) :
        metadata.bind = 'sqlite:///%s' % filename
        metadata.bind.echo = True

class Grid(Entity) :
    name = Column(String)

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
        if value not in ways.split() :
            raise 'Invalid node type "%s"\nValid types: %s' \
                % (str(value), str(ways))
        self.value = value

class Point(Entity) :
    longitude = Column(Float)
    latitude = Column(Float)
    grid = ManyToOne('Grid') # many points in one grid

class Deformation(Entity) :
    name = Column(String)
