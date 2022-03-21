from typing import DefaultDict
from Models.LocatedObjects import LocatedObjects, LocatedObject
from Models.Map import Map
from Models.Agent import Agent, AgentState, Orientation
from Models.Plane import Plane
from Models.World import World
from Models.Statistics import Statistics
from Models.MoveCommand import MoveCommand
from Graphics.Window import Window

from Graphics.graphics import *

import numpy as np
from collections import defaultdict
import random
import time
import math

class Simulation:
    def __init__(self, world : World, stepsPerMove:int,
     simulationLength:int, timeStepsInDay:int, visualize: bool, visualizationScale: int = 1):
        self.World = world
        self.StepsPerMove = stepsPerMove
        self.SimulationLength = simulationLength
        self.TimeStepsInDay = timeStepsInDay
        self.CurrentTimeStep = 0
        self.Day = 1
        self.Visualize = visualize
        if visualize:
            self.Window = Window(world.Width, world.Height, world.Agents, visualizationScale)
                
    def AddFood(self, food: LocatedObjects):
        self.World.Food = food
        if self.Visualize:
            self.Window.DeleteOldFood()            
            for loc in food.keys():
                self.Window.DrawFood(loc)

    def Iterate(self, wait = False) -> Statistics: 
        while(self.CurrentTimeStep < self.TimeStepsInDay):
            self.TimeStep(wait)
        
        self.DayEnd()
        return Statistics(self.Day, agents=self.World.Agents)
        
    
    def TimeStep(self, wait = False):
        """TODO

        Args:
            wait (bool, optional): _description_. Defaults to False.

        Returns:
            bool: _description_
        """
        self.UpdateAgents(self.World)
        self.UpdateFood(self.World)
        self.CurrentTimeStep+=1
        if (self.Visualize and wait):
            time.sleep(0.1)
    
    def DayEnd(self) -> bool:
        """TODO

        Returns:
            bool: _description_
        """
        self.Day +=1
        self.CurrentTimeStep = 0
        self.World.EndOfDay()
        self.RemoveDeadAgents()
        self.AddNewAgents()
        
    def UpdateFood(self, world: World):
        """TODO

        Args:
            world (World): _description_
        """
        for agent_location in world.Agents.keys():
            if agent_location in world.Food.keys():
                # increase agents' energy by one
                world.Agents.Objects[agent_location].Eat()
                
                # remove food
                world.Food.Objects.pop(agent_location)
                
    def UpdateAgents(self, world : World):
        """TODO

        Args:
            world (World): _description_

        Returns:
            _type_: _description_
        """
        agentMap = Map(world, world.Agents)
        foodMap = Map(world, world.Food)
        for loc in agentMap.LocatedObjects.Objects.keys():
            agent = agentMap.LocatedObjects.Objects[loc]            
            detectedFood = foodMap.GetDetectedObjects(loc, agent)
            detectedAgents = agentMap.GetDetectedObjects(loc, agent)
            
            if len(detectedFood) > 0:
                agent.ChooseMove(detectedFood)
            else:
                agent.ChooseRandomMove()
                
            agentNewLocation = agent.GetNewLocation(loc)
            if not self.WithinBounds(agentNewLocation):
                agent.Angle = (agent.Angle + math.pi) % 2*math.pi

        self.MoveAgents(agentMap)
        return agentMap
    
        
    def SortMoves(self, agents: LocatedObjects) -> LocatedObjects:
        """TODO

        Args:
            agents (LocatedObjects): _description_

        Returns:
            LocatedObjects: _description_
        """
        agents = agents.Objects.items()
        delta = np.random.uniform(0, 0.01) # to add randomness in case 2 agents travel the same distance and have the same amount of energy
        sorted_items = sorted(agents, key = lambda x: x[1].Move.dist + x[1].Energy + delta)
        return LocatedObjects(locatedObjectList=sorted_items) 
            
        
    def MoveAgents(self, agentMap: Map):
        """_summary_ TODO

        Args:
            proposedMoves (defaultdict): default new locations as keys and locatedobjects as value
        """
        # work out collisions
        winningAgents = LocatedObjects() # agents that are actualy going to move
        losingAgents = LocatedObjects() # agents that will lose out ot stronger agents and stay put
        
        # sorted
        queue = self.SortMoves(self.World.Agents)
        queue_hist = []
        
        while queue.count() != 0:
            loc, agent = queue.pop_at(0)
            moved = self.MoveAgent(loc, agentMap)
            if not moved:
                queue.add(loc, agent)
            queue_hist.append(queue.count())           
        
        
    def MoveAgent(self, location: tuple, agentMap: Map) -> bool:
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
                self.Window.DeleteFood(newLocation) # must be done first to net get conflicts
                dx, dy = agent.Move.get()
                self.Window.Move(location, dx, dy)
            agent.Move = MoveCommand(0, 0)
            return True
        elif (agent.Move.get() == (0, 0)): # this happens sometimes, idk why
            return True 
        elif (newLocation in self.World.Agents.Objects): # blocker
            neighborCells = agentMap.FindClosestEmptyCells(newLocation)
            neighborCell = neighborCells[np.random.randint(0, len(neighborCells))]
            dx, dy = agent.Move.get()
            agent.Move.add(dx, dy)
            return False
            
    def RemoveDeadAgents(self):
        """TODO
        """
        if len(self.World.DyingAgents) > 0:
            for location, agent in self.World.DyingAgents:
                self.World.Agents.Objects.pop(location)
                if self.Visualize:
                    self.Window.DeleteAgent(location)
            self.World.DyingAgents = []
        
        
    def AddNewAgents(self):
        """TODO
        """
        for agent in self.World.NewAgents:
            x = random.randint(0, self.World.Width-1)
            y = random.randint(0, self.World.Height-1)
            while (x, y) in self.World.Agents.Objects:
                x = random.randint(0, self.World.Width-1)
                y = random.randint(0, self.World.Height-1)
            self.World.Agents.add((x,y), agent)
            
            if self.Visualize:
                self.Window.DrawAgent((x, y))
            
        self.World.NewAgents = []

    def WithinBounds(self, location: tuple):
        """TODO

        Args:
            location (tuple): _description_

        Returns:
            _type_: _description_
        """
        x = location[0]
        y = location[1]
        withinBounds = x >= 0 and x < self.World.Width and y >= 0 and y < self.World.Height
        return withinBounds


        