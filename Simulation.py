from typing import DefaultDict
from Models.LocatedObjects import LocatedObjects, LocatedObject
from Models.Map import Map
from Models.Agent import Agent, AgentState, Orientation
from Models.Plane import Plane
from Models.World import World
from Models.Statistics import Statistics
from Models.MoveCommand import MoveCommand
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
        self.UpdateFoodMap(self.World)
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
        proposedMoves = LocatedObjects()

        for loc in agentMap.LocatedObjects.Objects.keys():
            agent = agentMap.LocatedObjects.Objects[loc]            
            detectedFood = foodMap.GetDetectedObjects(loc, agent)
            detectedAgents = agentMap.GetDetectedObjects(loc, agent)
            
            if len(detectedFood) > 0:
                agent.ChooseMove(detectedFood)
            else:
                agent.ChooseRandomMove(speed)
                
            agentNewLocation = agent.GetNewLocation(loc)
            
            
            if self.WithinBounds(agentNewLocation): # TODO: make OO
                if agentNewLocation not in proposedMoves.Objects:
                    newLocatedObjects = LocatedObjects()
                    newLocatedObjects.add(loc, self.World.Agents.Objects[loc])
                    proposedMoves.add(agentNewLocation, newLocatedObjects)
                    # proposedMoves.add(agentNewLocation, LocatedObjects(locatedObjectList=[(loc, self.World.Agents.Objects[loc])]))
                else:
                    proposedMoves.Objects[agentNewLocation].add(loc, agent)
            else:
                agent.Angle = (agent.Angle + math.pi) % 2*math.pi
            
        self.MoveAgents(proposedMoves, agentMap)
        
    def SortMoves(self, proposedMoves: defaultdict) -> list:
        locatedAgents = LocatedObjects()
        for new_loc in proposedMoves.Objects:
            movingAgents = proposedMoves.Objects[new_loc]
            for agentLoc in movingAgents.Objects:
                locatedAgents.add(agentLoc, )
                continue
        return []
        
    def MoveAgents(self, proposedMoves: defaultdict, agentMap: Map):
        """_summary_ TODO

        Args:
            proposedMoves (defaultdict): default new locations as keys and locatedobjects as value
        """
        # work out collisions
        winningAgents = LocatedObjects() # agents that are actualy going to move
        losingAgents = LocatedObjects() # agents that will lose out ot stronger agents and stay put
        
        # sorted
        queue = []
        # queue = self.SortMoves(proposedMoves)
        
        for new_loc in proposedMoves.keys():            
            # movingAgents = LocatedObjects(locatedObjectList=[[origin,
            #                                                   self.World.Agents.Objects[origin]] for origin in proposedMoves[new_loc]])
            movingAgents = proposedMoves.Objects[new_loc]
            if movingAgents.count() == 1: # no colision
                origin = list(proposedMoves.Objects[new_loc].keys())[0]
                agent = self.World.Agents.Objects[origin]
                winningAgents.add(origin, agent)               
            else: # collision
                energies = []
                winningAgentOrigin, winningAgent = None, None
                for origin in proposedMoves.Objects[new_loc].keys():
                    agent = self.World.Agents.Objects[origin]
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
            moved = self.MoveAgent(origin)
            if not moved:
                queue.append(origin)
                
            
        # move losing agents to a cell next to desired location.
        for origin in losingAgents.keys():
            agent = losingAgents.Objects[origin]
            dx, dy = agent.Move.get()
            newLocation = (origin[0] + dx, origin[1] + dy)
            neighborCells = agentMap.FindClosestEmptyCells(newLocation)
            neighborCell = neighborCells[np.random.randint(0, len(neighborCells))]
            agent.Move = MoveCommand(neighborCell[0] + dx, neighborCell[1] + dy)
            moved = self.MoveAgent(origin)
            if not moved:
                queue.append(origin)
                
        
        while len(queue) != 0:
            currLoc = queue.pop(0)
            moved = self.MoveAgent(currLoc)
            if not moved:
                queue.append(currLoc)
            
        
        
    def MoveAgent(self, location: tuple) -> bool:
        """Takes an agent on location and moves it based on it's intent. The visualization module is also updated.

        Args:
            location (tuple): the location of the agent to be moved.

        Returns:
            bool: whether move was succesfull
        """
        agent = self.World.Agents.Objects[location]
        newLocation = tuple(np.array(location) + np.array(agent.Move.get()))
        
        if (newLocation not in self.World.Agents.Objects):
            agent = self.World.Agents.Objects.pop(location)
            self.World.Agents.add(newLocation, agent)
            
            # visualize
            if self.Visualize:
                dx, dy = agent.Move.get()
                self.Window.Move(location, dx, dy)
            agent.Move = MoveCommand(dx, dy)
            return True
        else:
            return False
            
        
            
        
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
            self.World.Agents.add((x,y), agent)
            
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
                world.Agents.Objects[agent_location].Eat()
                
                # remove food
                world.Food.Objects.pop(agent_location)
                
        