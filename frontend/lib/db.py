from sqlalchemy import create_engine, \
    Table, Column, MetaData, ForeignKey, \
    Integer, Boolean, Float, String

db = create_engine('sqlite:///db.sqlite', echo=True)
meta = MetaData()

scenarios = Table('scenarios', meta,
    Column('id', Integer,  primary_key=True),
    Column('modeling_time', Float), # hours
    Column('time_step', Float), # seconds
    Column('output_step', Float), # seconds
    Column('sea_level', Float), # meters
    Column('bottom_friction', Float), # coefficient
    Column('earth_radius', Float), # meters
    Column('earth_gravity', Float), # m/(s*s)
    Column('earth_rotation', Float), # Hz
    Column('grid', None, ForeignKey('grids.id')),
)

jobs = Table('jobs', meta,
    Column('id', Integer,  primary_key=True),
    Column('scenarios', None, ForeignKey('scenarios.id')),
    Column('status', String), # pending running complete failed
)

grids = Table('grids', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String)
)

points = Table('points', meta,
    Column('id', Integer, primary_key=True),
    Column('longitude', Float),
    Column('latitude', Float),
    Column('grid', None, ForeignKey('grids.id')),
)
