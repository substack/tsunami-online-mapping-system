from elixir import *
from model import *

def bind_db(filename) :
    metadata.bind = 'sqlite:///%s' % filename
    metadata.bind.echo = True
    
    import os
    setup_all()
    if not os.path.exists(filename) : create_all()
