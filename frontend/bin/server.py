#!/usr/bin/env python2.6
from itty import *
from jinja2 import Environment, Template, FileSystemLoader

# add lib to search path
if sys.argv[0] == '' : sys.argv[0] = './'
basepath = '%s/../' % os.path.abspath(
    os.path.dirname(sys.argv[0])
)
sys.path.append('%s/lib' % basepath)

from db import *

host = '0.0.0.0'
port = 8081

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
        
        run_itty(config='__main__')
    
    def root(self,*files) :
        return '%s/%s' % (self.basepath,'/'.join(files))
    
    def render(self, filename, *args, **kwargs) :
        template = self.env.get_template(filename)
        kwargs['layout'] = self.env.get_template(filename)
        return str(template.render(*args, **kwargs))
     
app = None

@get('/')
def index(request) :
    return app.render('index.html',
        deformations=[ d.name for d in Deformation.query.all() ],
    )

@get('/css/(?P<filename>.+)')
def css(request,filename) :
    return Response(
        static_file(filename, root=app.root('css')),
        content_type=content_type(filename)
    )

@get('/js/(?P<filename>.+)')
def js(request,filename) :
    return Response(
        static_file(filename, root=app.root('js')),
        content_type=content_type(filename)
    )

@get('/old_page')
def old_page(request) :
    return app.render('old_page.html',
        # previously from /usr/local/apachedev/htdocs/mapping/status
        # cat $file | awk -F',' '{printf "\
        # addScenario(\"%s\",\"%s\",\"%s\",%f,\"%s\");\n", $1, $2, $3, $4, $5 }'
        jobs=[],
        pending_jobs=[], # keys: cputime, reqtime, nodes, nodetype, qtype, qt
        cron_frequency=15, # in minutes
        # /usr/local/apachedev/htdocs/mapping/current_nodes
        current_nodes=30, # available midnight nodes
        # df -k | grep /dev/dsk/c2d0s7 | awk '{print $3/1000000}' # used
        # df -k | grep /dev/dsk/c2d0s7 | awk '{print $4/1000000}' # avail
        storage={ 'used' : 100, 'available' : 50 } # gigabytes
    )

#@get('/data/jobs/(?P<job_id>)')
#def jobs(request, job_id) :

#@get('/data/jobs')
#def jobs(request) :

if __name__ == '__main__' :
    import sys, os
    app = TsunamiApp(basepath)
    bind_db(app.root('data/tsunami.sqlite3'))
    app.run()
