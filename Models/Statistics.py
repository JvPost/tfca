from collections import defaultdict
from .LocatedObjects import LocatedObjects

class Statistics():
    def __init__(self, day: int, agents: LocatedObjects):
        self.Day = day
        self.Agents = agents
        
    def AgentHist(self):
        hist = defaultdict(int)
        for k in self.Agents.keys():
            agent = self.Agents.Objects[k][0]
            hist[agent.ReceptiveDistance]+=1
            