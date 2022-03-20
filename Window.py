from Graphics.graphics import *
from Models.LocatedObjects import LocatedObjects

import numpy as np

class Window:
    def __init__(self, width: int, height: int,
                 agents: LocatedObjects(), scale: int = 1):
        self.Margin = width / 10
        self.Width = scale * width + self.Margin
        self.Height = scale * height + self.Margin
        self.Agents = agents
        self.Scale = scale
        self.Win = GraphWin("World", self.Width, self.Height)
        self.AgentPoints = {}
        for agent_loc in agents.keys():
            self.Draw(agent_loc)
            
    def Move(self, location: tuple, dx: int, dy: int):
        pt = self.AgentPoints[location]
        pt.move(self.Scale*dx, self.Scale*dy)
        location_new = tuple(np.array(location) + np.array((dx, dy)))
        if location_new in self.AgentPoints:
            print("Fishy")
        self.AgentPoints[location_new] = self.AgentPoints.pop(location)
        
    def Delete(self, location: tuple):
        if location in self.AgentPoints:
            pt = self.AgentPoints[location]
            pt.undraw()
            self.AgentPoints.pop(location)
            
    def Draw(self, location: tuple):
        x, y = location
        pt = Point(x * self.Scale + self.Margin, y * self.Scale + self.Margin)
        self.AgentPoints[location] = pt
        pt.draw(self.Win)
            
            