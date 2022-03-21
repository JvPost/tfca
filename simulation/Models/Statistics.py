from collections import defaultdict
from .LocatedObjects import LocatedObjects

import numpy as np

class Statistics():
    def __init__(self, day: int, agents: LocatedObjects):
        self.Day = day
        self.Agents = agents
        
    def AgentHist(self, stop: int) -> np.array:
        hist = np.zeros(stop)
        for k in self.Agents.keys():
            agent = self.Agents.Objects[k]
            if agent.SenseDistance < stop:
                hist[agent.SenseDistance] += 1
        return hist