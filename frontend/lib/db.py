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
