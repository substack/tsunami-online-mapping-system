#!/usr/bin/env python

from itty import *
from jinja2 import Environment, Template, FileSystemLoader

class TsunamiApp :
    def __init__(self,basepath) :
        self.basepath = basepath
    
    def run(self) :
        run_itty
        # set up database
        dbfile = self.root('data/db.sqlite3')
        
        # set up jinja2 environment
        self.env = Environment(loader=FileSystemLoader(
            self.root('templates')
        ))
        
        run_itty()
    
    def root(self,*files) :
        return '%s/%s' % (self.basepath,'/'.join(files))
    
    def render(self, filename, *args, **kwargs) :
        template = self.env.get_template(filename)
        kwargs['layout'] = self.env.get_template(filename)
        return str(template.render(*args, **kwargs))
     
app = None

@get('/')
def index(request) :
    return app.render('index.html')

@get('/css/(?P<filename>.+)')
def css(request,filename) :
    return Response(
        static_file(filename, root=app.root('css')),
        content_type=content_type(filename)
    )

if __name__ == '__main__' :
    import sys, os
    if sys.argv[0] == '' : sys.argv[0] = './'
    basepath = '%s/../' % os.path.abspath(
        os.path.dirname(sys.argv[0])
    )
    app = TsunamiApp(basepath)
    app.run()
