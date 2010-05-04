import simplejson as json
import urllib

class Data(object) :
    @classmethod
    def get(cself,part) :
        uri = "http://localhost:8081/data/%s/get/%s" % (cself.name(),part)
        return json.loads(urllib.urlopen(uri).read())
    
    @classmethod
    def all(cself) : return cself.get('')
 
class Jobs(Data) :
    @staticmethod
    def name() : return 'jobs'
    
    @classmethod
    def status(cself,name) : return cself.get('status/%s' % name)

class Scenarios(Data) :
    @staticmethod
    def name() : return 'scenarios'

class Points(Data) :
    @staticmethod
    def name() : return 'points'

class Markers(Data) :
    @staticmethod
    def name() : return 'markers'
