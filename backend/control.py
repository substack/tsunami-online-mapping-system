import simplejson as json
import urllib

class Data(object) :
    base = "http://localhost:8081/data"
    @classmethod
    def get(cself,name) :
        uri = "%s/%s/get/%s" % (cself.base,cself.name(),name)
        return json.loads(urllib.urlopen(uri).read())
    
    def set(cself,id,value) :
        uri = "%s/%s/set/%d/%s" % (cself.base,cself.name(),id,value)
        ok = urllib.urlopen(uri).read()
        if ok != "ok" : raise "Response not OK: %s" % ok
    
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
