##NOTES FOR JIM'S WORK...NOT TO BE USED
##
#Note: look through monitor.sh and figure out what is being sent when and where

import simplejson as json
from StringIO import StringIO	
import urllib

raw_points = urllib.urlopen("http://localhost:8081/data/points").read()
points = json.loads(raw_points)

raw_defs = urllib.urlopen("http://localhost:8081/data/points").read()
deformations = json.loads(raw_defs)

raw_grids = urllib.urlopen("http://localhost:8081/data/points").read()
grids = json.loads(raw_grids)

status = urllib.urlopen("http://localhost:8081/control/jobs/status").read()
pending = json.loads(status)

#removing = urllib.urlopen("http://localhost:8081/data").read()
#removed = urllib.urlopen("http://localhost:8081/data").read()
#archiving = urllib.urlopen("http://localhost:8081/data").read()
#archived = urllib.urlopen("http://localhost:8081/data").read()
#resuming = urllib.urlopen("http://localhost:8081/data").read()
#paused = urllib.urlopen("http://localhost:8081/data").read()

#handle every file in the above lists (by id assumed)
#need to create status file?
    #for each status type?




