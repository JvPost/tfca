from .Agent import Agent
from .FoodObject import FoodObject
import random

class World:
    def __init__(self, width, height, agents, food):
        self.Width = width
        self.Height = height
        self.Agents = agents
        self.Food = food

    def EndOfDay(self):
        for agent in self.Agents:
            agent.Energy = agent.Energy - 1
            self.Alive = agent.Energy >= -1

    
            

    



    

