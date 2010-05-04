from control import *

for job in Jobs.status('pending') :
    print(job)
