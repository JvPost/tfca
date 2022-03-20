from typing import DefaultDict
from Models.LocatedObjects import LocatedObjects
from Models.Map import Map
from Models.Agent import Agent, AgentState, Orientation
from Models.Plane import Plane
from Models.World import World
from Models.Statistics import Statistics
from Window import Window

from Graphics.graphics import *

import numpy as np
from collections import defaultdict
import random
import time
import math

class Simulation:
    def __init__(self, world : World, stepsPerMove:int,
     simulationLength:int, timeStepsInDay:int, visualize: bool):
        self.World = world
        self.StepsPerMove = stepsPerMove
        self.SimulationLength = simulationLength
        self.TimeStepsInDay = timeStepsInDay
        self.CurrentTimeStep = 0
        self.Day = 1
        self.Visualize = visualize
        if visualize:
            self.Window = Window(world.Width, world.Height, world.Agents, 3)
                
        

    def Iterate(self, wait = False) -> Statistics: 
        while(self.CurrentTimeStep < self.TimeStepsInDay):
            self.TimeStep(wait)
        
        self.DayEnd()
        return Statistics(self.Day, agents=self.World.Agents)
        
    
    def TimeStep(self, wait = False) -> bool:
        self.UpdateAgentMap(self.World, self.StepsPerMove)
        self.UpdateFoodMap(self.World)
        self.CurrentTimeStep+=1
        if (self.Visualize and wait):
            time.sleep(0.1)
    
    def DayEnd(self) -> bool:
        self.Day +=1
        self.CurrentTimeStep = 0
        self.World.EndOfDay()
        self.RemoveDeadAgents()
        self.AddNewAgents()

    def UpdateAgentMap(self, world : World, speed: int):
        agentMap = Map(world, world.Agents)
        foodMap = Map(world, world.Food)

        # dict with new locations as key and values is the list of locations of agents that want to move to the location that is the key
        proposedMoves = defaultdict(list)

        for loc in agentMap.LocatedObjects.Objects.keys():
            agent = agentMap.LocatedObjects.Objects[loc][0] # this is possible because there is always only one agent at location at this time
            perceptionPlane = Plane(loc, agent.SenseDistance)
            detectedFood = foodMap.GetDetectedObjects(loc, perceptionPlane)
            if len(detectedFood) > 0:
                agent.ChooseNextLocation(detectedFood)
                agentNewLocation = agent.GetNewLocation(loc)
            else:
                agent.ChooseRandomNextLocation(speed)
            agentNewLocation = agent.GetNewLocation(loc)
            
            if self.WithinBounds(agentNewLocation): # TODO: make OO
                proposedMoves[agentNewLocation].append(loc)
            else:
                agent.Angle = (agent.Angle + math.pi) % 2*math.pi
            

        # work out collisions
        winningAgents = LocatedObjects() # agents that are actualy going to move
        losingAgents = LocatedObjects() # agents that will lose out ot stronger agents and stay put
    
        for new_loc in proposedMoves.keys():            
            movingAgents = LocatedObjects(locatedObjectList=[[origin,
                                                              self.World.Agents.Objects[origin][0]] for origin in proposedMoves[new_loc]])
            winningAgentOrigin, winningAgent = None, None
            energies = []
            
            if len(movingAgents) == 1: # no colision
                origin = proposedMoves[new_loc][0]
                agent = self.World.Agents.Objects[origin][0]
                winningAgents.add(origin, agent)
            else: # collision
                for origin in proposedMoves[new_loc]:
                    agent = self.World.Agents.Objects[origin][0]
                    if len(energies) > 0:
                        if agent.Energy == max(energies) and random.randint(0, 1) == 1:
                            losingAgents.add(winningAgentOrigin, winningAgent)
                            winningAgentOrigin = origin
                            winningAgent = agent
                        elif agent.Energy > max(energies):
                            losingAgents.add(winningAgentOrigin, winningAgent)
                            winningAgentOrigin = origin
                            winningAgent = agent
                        else:
                            losingAgents.add(origin, agent)
                    else:
                        winningAgentOrigin = origin
                        winningAgent = agent
                    energies.append(agent.Energy)
                winningAgents.add(winningAgentOrigin, winningAgent)
            
                            
        # actually move winning agents
        for origin in winningAgents.keys():
            self.MoveAgent(origin)
        
        # reset not moving agents intent to zero
        for origin in losingAgents.keys():
            agent = losingAgents.Objects[origin][0]
            newLocation = (origin[0] + agent.Intention[0], origin[1] + agent.Intention[1])
            neighborCells = agentMap.FindClosestEmptyCells(newLocation)
            neighborCell = neighborCells[np.random.randint(0, len(neighborCells))]
            agent.Intention = (neighborCell[0] + agent.Intention[0], neighborCell[1] + agent.Intention[1])
            self.MoveAgent(origin)
            
        for loc in self.World.Agents.keys():
            agents = self.World.Agents.Objects[loc]
            if len(agents) > 1:
                continue # TODO: fix dit probleem, more than on ehsould never be possible here.
        
    def MoveAgent(self, location: tuple):
        agent = self.World.Agents.Objects.pop(location)[0]
        newLocation = tuple(np.array(location) + np.array(agent.Intention))
        self.World.Agents.Objects[newLocation].append(agent)
        
        # visualize
        if self.Visualize:
            dx, dy = agent.Intention
            self.Window.Move(location, dx, dy)
        agent.Intention = (0,0)
        
            
        
    def RemoveDeadAgents(self):
        if len(self.World.DyingAgents) > 0:
            for location, agent in self.World.DyingAgents:
                self.World.Agents.Objects.pop(location)
                if self.Visualize:
                    self.Window.Delete(location)
            self.World.DyingAgents = []
        
        
    def AddNewAgents(self):
        for agent in self.World.NewAgents:
            x = random.randint(0, self.World.Width-1)
            y = random.randint(0, self.World.Height-1)
            while (x, y) in self.World.Agents.Objects:
                x = random.randint(0, self.World.Width-1)
                y = random.randint(0, self.World.Height-1)
            self.World.Agents.Objects[(x,y)].append(agent)
            
            if self.Visualize:
                self.Window.Draw((x, y))
            
        self.World.NewAgents = []

    def WithinBounds(self, location: tuple):
        x = location[0]
        y = location[1]
        withinBounds = x >= 0 and x < self.World.Width and y >= 0 and y < self.World.Height
        return withinBounds

    def UpdateFoodMap(self, world: World):
        for agent_location in world.Agents.keys():
            if agent_location in world.Food.keys():
                # increase agents' energy by one
                world.Agents.Objects[agent_location][0].Eat()
                
                # remove food
                world.Food.Objects.pop(agent_location)
                