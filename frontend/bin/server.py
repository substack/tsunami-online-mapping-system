#!/usr/bin/env python

from itty import *
from jinja2 import Environment, Template, FileSystemLoader

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
        
        run_itty()
    
    def render(self, filename, *args, **kwargs) :
        template = self.env.get_template(filename)
        kwargs['layout'] = self.env.get_template(filename)
        return str(template.render(*args, **kwargs))

app = None

@get('/')
def index(web) :
    return app.render('index.html')

if __name__ == '__main__' :
    import sys, os
    if sys.argv[0] == '' : sys.argv[0] = './'
    basepath = '%s/../' % os.path.abspath(
        os.path.dirname(sys.argv[0])
    )
    app = TsunamiApp(basepath)
    app.run()
