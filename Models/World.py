from Models.LocatedObjects import LocatedObjects
from .Agent import Agent
from .FoodObject import FoodObject
import random

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
            agent.EndOfDay()
            if not agent.Alive:
                self.DyingAgents.append((location, agent))
            
            
        
        

    
            

    



    

