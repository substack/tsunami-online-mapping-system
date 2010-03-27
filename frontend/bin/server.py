#!/usr/bin/env python

from itty import *
from jinja2 import Environment, FileSystemLoader

class TsunamiApp :
    def __init__(self,basepath) :
        self.basepath = basepath
    
    def run(self) :
        run_itty
        # set up database
        dbfile = '%s/data/db.sqlite3' % self.basepath
        
        # set up jinja2 environment
        self.env = Environment(loader=FileSystemLoader(
                '%s/templates' % self.basepath,
        ))
        
        self.layout = self.env.get_template('layout.html')
        
        run_itty()
    
    def render(self, filename, *args) :
        template = self.env.get_template(filename)
        return app.layout.render(content=template.render(*args))

app = None

@get('/')
def index(web) :
    return str(app.render('index.html'))
    
if __name__ == '__main__' :
    import sys, os
    if sys.argv[0] == '' : sys.argv[0] = './'
    basepath = '%s/../' % os.path.abspath(
        os.path.dirname(sys.argv[0])
    )
    app = TsunamiApp(basepath)
    app.run()
