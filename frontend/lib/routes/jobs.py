from __common__ import *
import re
from default_dict import DefaultDict

@get('/data/jobs/get')
def jobs(request) :
    return Job.json()

@get('/data/jobs/get/status/(?P<status>.+)')
def jobs_by_status(request, status) :
    return Job.json(Job.query.filter_by(status=status))

@get('/data/jobs/set/(?P<job_id>\d+)/status/(?P<status>.*)')
def update_job_status(request,job_id,status) :
    Job.get_by(id=job_id).status = status
    session.commit()
    return 'ok'

@get('/data/jobs/set/(?P<job_id>\d+)/start_time/(?P<start_time>.*)')
def update_job_start_time(request,job_id,start_time) :
    Job.get_by(id=job_id).start_time = int(start_time)
    session.commit()
    return 'ok'

@get('/data/jobs/set/(?P<job_id>\d+)/progress/(?P<progress>.*)')
def update_job_progress(request,job_id,progress) :
    Job.get_by(id=job_id).progress = float(progress)
    session.commit()
    return 'ok'

@get('/data/jobs/remove/(?P<job_id>\d+)')
def delete_job(request,job_id) :
    session.delete(Job.get_by(id=job_id))
    session.commit()
    return 'ok'

@get('/data/jobs/start/(?P<job_id>\d+)')
def start_job(request,job_id) :
    Job.get_by(id=job_id).status = 'starting'
    session.commit()
    return 'ok'

@get('/data/jobs/stop/(?P<job_id>\d+)')
def start_job(request,job_id) :
    Job.get_by(id=job_id).status = 'stopping'
    session.commit()
    return 'ok'

@post('/submit-job')
def submit_job(request) :
    params = DefaultDict('', request.POST.items())
    
    # grids
    grid_names = [ x.group(1) for x in
        [ re.match(r'^grid_(.+)',y) for y in params.keys() ] if x
    ]
    grids = [ grid for grid in
        [ Grid.get_by(name=name) for name in grid_names ]
        if grid is not None
    ]
    
    # markers already in the database
    marker_names = [ x.group(1) for x in
        [ re.match(r'^marker_(.+)',y) for y in params.keys() ] if x
    ]
    markers = [ marker for marker in
        [ Marker.get_by(name=name) for name in marker_names ]
        if marker is not None
    ]
    
    user_marker_names = [ x.group(1) for x in
        [ re.match(r'^user_marker_(.+)',y) for y in params.keys() ] if x
    ]
    user_markers = []
    
    keys = """
        time_step output_step sea_level bottom_friction earth_radius
        earth_gravity earth_rotation
        
        person name description nodes node_type queue_type
    """.split()
    
    missing = [ key for key in keys if not params.has_key(key) ]
    if missing : return 'Empty parameters: %s' % ' '.join(missing)
    
    session.add(Scenario(
        grids = grids,
        markers = markers + user_markers,
        jobs = [ Job(
            person=params['person'],
            name=params['name'],
            description=params['description'],
            nodes=int(params['nodes']),
            node_type=NodeType(params['node_type']),
            qtype=params['queue_type'],
            status='pending',
            progress=0.0
        ) ],
        modeling_time = 0.0,
        time_step = float(params['time_step']),
        output_step = float(params['output_step']),
        sea_level = float(params['sea_level']),
        bottom_friction = float(params['bottom_friction']),
        earth_radius = float(params['earth_radius']),
        earth_gravity = float(params['earth_gravity']),
        earth_rotation = float(params['earth_rotation']),
    ))
    session.commit()
    return 'ok'
