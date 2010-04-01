class DB(object) :
    def __init__(self, filename) :
        from sqlalchemy import create_engine, \
            Table, Column, MetaData, ForeignKey, \
            Integer, Boolean, Float, String
        
        self.engine = create_engine('sqlite:///%s' % filename, echo=True)
        self.meta = MetaData()
        
        self.scenarios = Table('scenarios', self.meta,
            Column('id', Integer,  primary_key=True),
            Column('modeling_time', Float, nullable=False), # hours
            Column('time_step', Float, nullable=False), # seconds
            Column('output_step', Float, nullable=False), # seconds
            Column('sea_level', Float, nullable=False), # meters
            Column('bottom_friction', Float, nullable=False), # coefficient
            Column('earth_radius', Float, nullable=False), # meters
            Column('earth_gravity', Float, nullable=False), # m/(s*s)
            Column('earth_rotation', Float, nullable=False), # Hz
            Column('grid', None, ForeignKey('grids.id')),
        )
        
        self.jobs = Table('jobs', self.meta,
            Column('id', Integer,  primary_key=True),
            Column('scenarios', None, ForeignKey('scenarios.id')),
            Column('status', String, nullable=False), # pending running complete failed
            Column('person', String), # the "Investigator" of the senario
            Column('name', String),
            Column('cputime', Integer),
            Column('deformation', String, nullable=False), # the deformation to select
            Column('nodes', String, nullable=False),
            Column('node_type', String, nullable=False), # type of node on HPC to use
            Column('qtype', String), # Queue type
        )
        
        self.grids = Table('grids', self.meta,
            Column('id', Integer, primary_key=True),
            Column('name', String, nullable=False)
        )
        
        self.points = Table('points', self.meta,
            Column('id', Integer, primary_key=True),
            Column('longitude', Float, nullable=False),
            Column('latitude', Float, nullable=False),
            Column('grid', None, ForeignKey('grids.id')),
        )
        
        self.deformations = Table('deformations', self.meta,
            Column('id', Integer, primary_key=True),
            Column('name', String, nullable=False),
        )
        
        self.meta.create_all(self.engine)

class Grids(object):
    def _init_(self, id, name):
        self.id = id
        self.name = name

    def _repr_(self):
        return "<User('%s', '%s')>" % (self.id, self.name)

#from sqlalchemy.orm import mapper
#mapper(Grids,grids)

