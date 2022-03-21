from Graphics.graphics import *
from Models.LocatedObjects import LocatedObjects
from Models.Agent import Agent

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
        self.FoodPoints = {}
        for agent_loc in agents.keys():
            self.DrawAgent(agent_loc)
            
    def Move(self, location: tuple, dx: int, dy: int):
        pt = self.AgentPoints[location]
        pt.move(self.Scale*dx, self.Scale*dy)
        location_new = tuple(np.array(location) + np.array((dx, dy)))
        self.AgentPoints[location_new] = self.AgentPoints.pop(location)
        
    def DeleteAgent(self, location: tuple):
        if location in self.AgentPoints:
            pt = self.AgentPoints[location]
            pt.undraw()
            self.AgentPoints.pop(location)
            
    def DeleteFood(self, location: tuple):
        if location in self.FoodPoints:
            pt = self.FoodPoints[location]
            pt.undraw()
            self.FoodPoints.pop(location)
            
    def DrawAgent(self, location: tuple):
        x, y = location
        pt = Point(x * self.Scale + self.Margin, y * self.Scale + self.Margin)
        self.AgentPoints[location] = pt
        pt.draw(self.Win)
            
    def DrawFood(self, location: tuple):
        if location not in self.AgentPoints and location not in self.FoodPoints:
            x, y = location
            pt = Point(x * self.Scale + self.Margin, y * self.Scale + self.Margin)
            self.FoodPoints[location] = pt
            pt.setOutline('red')
            pt.draw(self.Win)
            
    def DeleteOldFood(self):
        for k in self.FoodPoints:
            pt = self.FoodPoints[k].undraw()
        self.FoodPoints = {}
        
    