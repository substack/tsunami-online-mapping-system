from __common__ import *

@get('/data/admin/cron-interval/get')
def cron_interval(request) :
    opt = Option.query.filter_by(key='cron-interval').first()
    if opt :
        return str(opt.value)
    else :
        return "5" # default cron frequency

@get(r'/data/admin/cron-interval/set/(?P<interval>\d+)')
def update_cron_interval(request,interval) :
    opt = Option.query.filter_by(key='cron-interval').first()
    if not opt :
        opt = Option(key='cron-interval')
        session.add(opt)
    opt.value = str(int(interval))
    session.commit()
    return 'ok'
