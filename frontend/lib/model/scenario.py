from model.util import *

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
