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

@get('/data/jobs/delete/(?P<job_id>\d+)')
def delete_job(request,job_id) :
    session.delete(Job.get_by(id=job_id))
    session.commit()
    return 'ok'

@post('/submit-job')
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
