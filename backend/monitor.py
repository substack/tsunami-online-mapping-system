# replacement for monitor.sh

from control import *
from queue import Queue

for job in Jobs.status('pending') :
    # Submit each pending job
    print(job)
