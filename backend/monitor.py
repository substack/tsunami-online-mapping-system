# replacement for monitor.sh

from control import *

for job in Jobs.status('pending') :
    print(job)
