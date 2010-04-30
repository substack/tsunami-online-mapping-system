#!/usr/bin/env python2.6
from itty import *
from jinja2 import Environment, Template, FileSystemLoader

import re

# add lib to search path
if sys.argv[0] == '' : sys.argv[0] = './'
basepath = '%s/../' % os.path.abspath(
    os.path.dirname(sys.argv[0])
)
sys.path.append('%s/lib' % basepath)

from db import *
from default_dict import DefaultDict

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
        json=dict(zip(
            'deformations markers groups grids points'.split(),
            [ x.json() for x in [Deformation,Marker,Group,Grid,Point] ]
        ))
    )

@get('/images/(?P<filename>.+)')
def images(request,filename) :
    return Response(
        static_file(filename, root=app.root('images')),
        content_type=content_type(filename)
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

@get('/overlays/(?P<filename>.+)')
def overlays(request,filename) :
    return Response(
        static_file(filename, root=app.root('overlays')),
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

import simplejson as js

# markers
@get('/data/markers')
def markers(request) :
    return Marker.json()
@get('/data/markers/names')
def marker_names(request) :
    return js.dumps([ x[0] for x in session.query(Marker.name).all() ])
@get('/data/markers/name/(?P<name>.+)')
def marker_from_name(request, name) :
    return Marker.json(Marker.query.filter_by(name=name))

# deformations
@get('/data/deformations')
def deformations(request) :
    return Deformation.json()
@get('/data/deformations/names')
def deformation_names(request) :
    return js.dumps([ x[0] for x in session.query(Deformation.name).all() ])
@get('/data/deformations/name/(?P<name>.+)')
def deformation_from_name(request, name) :
    return Deformation.json(Deformation.query.filter_by(name=name))

# grids
@get('/data/grids')
def grids(request) :
    return Grid.json()
@get('/data/grids/names')
def grid_names(request) :
    return js.dumps([ x[0] for x in session.query(Grid.name).all() ])
@get('/data/grids/name/(?P<name>.+)')
def grid_from_name(request, name) :
    return Grid.json(Grid.query.filter_by(name=name))

# points
@get('/data/points')
def points(request) :
    return Point.json()

# scenarios
@get('/data/scenarios')
def scenarios(request) :
    return Scenario.json()
@get('/data/scenarios/id/(?P<id>.+)')
def scenarios(request, id) :
    return Scenario.json(Scenario.query.filter_by(id=id))

#jobs
@get('/data/jobs')
def jobs(request) :
    return Job.json()
@get('/data/jobs/pending')
def pending_jobs(request) :
    return Job.json(Job.query.filter_by(status='pending'))
@get('/data/jobs/pending')
def pending_jobs(request) :
    return Job.json(Job.query.filter_by(status='pending'))
@get('/data/jobs/(?P<job_id>\d+)/update/status/(?P<status>.*)')
def update_job_status(request,job_id,status) :
    Job.get_by(id=job_id).status = status
    session.commit()
    return 'ok'
@get('/data/jobs/(?P<job_id>\d+)/update/start_time/(?P<start_time>.*)')
def update_job_start_time(request,job_id,start_time) :
    Job.get_by(id=job_id).start_time = int(start_time)
    session.commit()
    return 'ok'
@get('/data/jobs/(?P<job_id>\d+)/update/progress/(?P<progress>.*)')
def update_job_progress(request,job_id,progress) :
    Job.get_by(id=job_id).progress = float(progress)
    session.commit()
    return 'ok'
@get('/data/jobs/status')
def status(request) :
    return Job.json()

@post('/submit_job')
def submit_job(request) :
    params = DefaultDict('', request.POST.items())
    grids = [
        x.group(1) for x in
            [ re.match(r'^grid_(.+)',y) for y in params.keys() ]
        if x
    ]
    markers = [
        x.group(1) for x in
            [ re.match(r'^marker_(.+)',y) for y in params.keys() ]
        if x
    ]
    session.add(Scenario(
        grids=[ Grid.query.filter_by(name=key) for key in grids ],
        markers=[ Marker.query.filter_by(name=key) for key in markers ],
        jobs=[ Job(
            person=params['person'],
            name=params['name'],
            description=params['description'],
            nodes=int(params['nodes']),
            node_type=NodeType(params['node_type']),
            qtype=params['qtype'],
            status='pending',
            progress=0.0
        ) ],
        modeling_time=0.0,
        **dict((key,float(params[key])) for key in """
            time_step output_step sea_level bottom_friction
            earth_radius earth_gravity earth_rotation
        """.split())
    ))
    session.commit()
    return 'ok'

if __name__ == '__main__' :
    import sys, os
    app = TsunamiApp(basepath)
    bind_db(app.root('data/tsunami.sqlite3'))
    app.run()
