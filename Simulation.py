from typing import DefaultDict
from Models.Map import Map
from Models.Agent import Agent, AgentState
from Models.World import World

import numpy as np
from collections import defaultdict

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
        proposedMap = dict;

        proposedLocations = defaultdict([])
        collisions = []
        # current map
        for agent in self.World.Agents:
            seesFood, foodLocations = agent.SeesFoodAt(foodMap.Matrix)
            if agent.State == AgentState.EATING:
                agent.Eat()
            if seesFood: # find food
                print("======= foodmap ========")
                print(foodMap.Matrix)
                print(f"===Agent({agent.X},{agent.Y})===")
                print(agentMap.Matrix)
                x, y = agent.FindNearestFood(foodLocations)
                if len(proposedLocations[(x,y)]) > 0:
                    if (x, y) not in collisions:
                        collisions.append(x,y)
                proposedLocations[x, y].append(agent)

        # work out collisions
        for x,y in collisions:
            energies = []
            for agent in proposedLocations[(x,y)]:
                energies.append(agent.Energy) # TODO: make test foodMap and test agentMap where collision occurs.


        # day end
        if self.CurrentTimeStep > self.TimeStepsInDay:
            self.TimeStepsInDay = 0
            self.CurrentDay = self.CurrentDay + 1
            self.World.EndOfDay()
        self.IncreaseTimeStep()
        
        return self.CurrentDay <= self.SimulationLength

    def IncreaseTimeStep(self):
        self.TimeStepsInDay = self.TimeStepsInDay + 1

    def GetAgentCollisions(self, agentMap:Map) -> list:
        for

    
