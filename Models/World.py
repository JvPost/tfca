from Models.LocatedObjects import LocatedObjects
from .Agent import Agent
from .FoodObject import FoodObject
from Graphics.graphics import Point

import random
from collections import defaultdict

class World:
    def __init__(self, width, height, agents: LocatedObjects, food: LocatedObjects):
        self.Width = width
        self.Height = height
        self.Agents = agents
        self.Food = food
        self.DyingAgents = []
        self.NewAgents = []
        

    def EndOfDay(self):
        for location in self.Agents.keys():
            agent = self.Agents.Objects[location][0]
            result = agent.EndOfDay()
            if not agent.Alive:
                self.DyingAgents.append((location, agent))
            elif result.Child is not None:
                self.NewAgents.append(agent)
            
        
                
            
            
        
        

    
            

    



    

