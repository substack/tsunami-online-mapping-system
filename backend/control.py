import simplejson as json
import urllib

class Data(object) :
    @classmethod
    def get(cself,part) :
        uri = "http://localhost:8081/data/%s/%s" % (cself.name(),part)
        return json.loads(urllib.urlopen(uri).read())
    
    @classmethod
    def all(cself) : return cself.get('')
 
class Jobs(Data) :
    @staticmethod
    def name() : return 'jobs'
    
    @classmethod
    def pending(cself) : return cself.get('pending')
    
    @classmethod
    def running(cself) : return cself.get('running')
    
    @classmethod
    def finished(cself) : return cself.get('finished')
    
    @classmethod
    def removing(cself) : return cself.get('removing')
    
    @classmethod
    def removed(cself) : return cself.get('removed')
    
    @classmethod
    def archiving(cself) : return cself.get('archiving')
    
    @classmethod
    def archived(cself) : return cself.get('archived')

    @classmethod
    def resuming(cself) : return cself.get('resuming')

    @classmethod
    def resumed(cself) : return cself.get('resumed')

    @classmethod
    def pausing(cself) : return cself.get('pausing')

    @classmethod
    def paused(cself) : return cself.get('paused')

class Scenarios(Data) :
    @staticmethod
    def name() : return 'scenarios'

class Points(Data) :
    @staticmethod
    def name() : return 'points'

class Markers(Data) :
    @staticmethod
    def name() : return 'markers'
