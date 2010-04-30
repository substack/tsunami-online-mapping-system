from itty import *
from db import *

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
