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

    def EndOfDay(self):
        pass

    
            

    



    

