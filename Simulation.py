from Models.Map import Map
from Models.Agent import Agent
from Models.World import World

import numpy as np

class Simulation:
    def __init__(self, world : World, stepsPerMove:int,
     simulationLength:int, timeStepsInDay:int):
        self.World = world
        self.StepsPerMove = stepsPerMove
        self.SimulationLength = simulationLength
        self.CurrentDay = 0
        self.CurrentTimeStep = 0
        self.TimeStepsInDay = timeStepsInDay


    def Iterate(self) -> bool: 
        agentMap = Map(self.World, self.World.Agents)
        foodMap = Map(self.World, self.World.Food)
        # current map
        for agent in self.World.Agents:
            seesFood, foodLocations = agent.SeesFoodAt(foodMap)
            if (seesFood):
                continue

        # day end
        if self.CurrentTimeStep > self.TimeStepsInDay:
            self.TimeStepsInDay = 0
            self.CurrentDay = self.CurrentDay + 1
            self.World.EndOfDay()
        self.IncreaseTimeStep()
        
        return self.CurrentDay <= self.SimulationLength

    def IncreaseTimeStep(self):
        self.TimeStepsInDay = self.TimeStepsInDay + 1

    
