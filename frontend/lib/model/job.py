from model.util import *

class Job(Entity) :
    # a scenario may have many jobs in the case where the job fails
    scenario = ManyToOne('Scenario')
    
    status = Column(String) # pending running complete failed
    person = Column(String) # the "Investigator" of the senario
    name = Column(String)
    cputime = Column(Integer)
    nodes = Column(Integer)
    node_type = ManyToOne('NodeType')
    qtype = Column(String) # Queue type

class NodeType(Entity) :
    value = Column(String)
    
    def __init__(self,value=None) :
        ways = '4-way 16-way'.split()
        if value not in ways :
            raise 'Invalid node type "%s"\nValid types: %s' \
                % (str(value), str(ways))
        self.value = value
