import simplejson as json
import urllib

class Data(object) :
    @classmethod
    def get(cself,part) :
        raw = urllib.urlopen(
            "http://localhost:8081/data/%s/%s" % (cself.name(),part)
        ).read()
        return json.loads(raw)
    
    @classmethod
    def all(cself) : return cself.get('')
 
class Jobs(Data) :
    @staticmethod
    def name() : return 'jobs'
    @classmethod
    def pending(cself) : return cself.get('pending')

class Scenarios(Data) :
    @staticmethod
    def name() : return 'scenarios'

class Points(Data) :
    @staticmethod
    def name() : return 'points'

class Markers(Data) :
    @staticmethod
    def name() : return 'markers'
