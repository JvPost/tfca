from typing import DefaultDict
from Models.LocatedObjects import LocatedObjects
from Models.Map import Map
from Models.Agent import Agent, AgentState, Orientation
from Models.PerceptionField import PerceptionField
from Models.World import World
from Models.Statistics import Statistics

import numpy as np
from collections import defaultdict
import random

class Simulation:
    def __init__(self, world : World, stepsPerMove:int,
     simulationLength:int, timeStepsInDay:int):
        self.World = world
        self.StepsPerMove = stepsPerMove
        self.SimulationLength = simulationLength
        self.TimeStepsInDay = timeStepsInDay
        self.CurrentTimeStep = 0
        self.Day = 1
        

    def Iterate(self) -> Statistics: 
        while(self.CurrentTimeStep < self.TimeStepsInDay):
            self.TimeStep()
        
        self.DayEnd()
        # new statistics
        # return statistics
        return Statistics(self.Day, agents=self.World.Agents)
        
    
    def TimeStep(self) -> bool:
        self.UpdateAgentMap(self.World, self.StepsPerMove)
        self.UpdateFoodMap(self.World)
        self.CurrentTimeStep+=1
    
    def DayEnd(self) -> bool:
        self.Day +=1
        self.CurrentTimeStep = 0
        self.World.EndOfDay()
        self.RemoveDeadAgents()        
        return False        

    def UpdateAgentMap(self, world : World, stepsCount: int): # TODO: Remove stepsCount as variable, stepsCount is specific to agent
        agentMap = Map(world, world.Agents)
        foodMap = Map(world, world.Food)

        proposedAgentLocations = LocatedObjects()
        finalAgentLocations = LocatedObjects()

        for loc in agentMap.LocatedObjects.Objects.keys():
            agent = agentMap.LocatedObjects.Objects[loc][0] # this is possible because there is always only one agent at location at this time
            perceptionField = PerceptionField(loc, agent)
            detectedFood = foodMap.GetDetectedObjects(loc, perceptionField)
            if len(detectedFood) > 0:
                nextLocation = agent.ChooseNextLocation(detectedFood)
                agentNewLocation = agent.Move(loc, nextLocation, Orientation.RANDOM)
            else:
                agentNewLocation = agent.MoveRandom(loc, stepsCount)
            
            # move if location within bounds of world
            if self.WithinBounds(agentNewLocation):
                agent.State = AgentState.MOVING
                proposedAgentLocations.add(agentNewLocation, agent)
            else:
                proposedAgentLocations.add(loc, agent)
            

        # work out collisions after moving to the same cell
        for loc in proposedAgentLocations.keys():
            agentsAtLocation = proposedAgentLocations.Objects[loc]
            energies = []
            winning_agent = None
            losing_agents = []

            # move agents
            for agent in agentsAtLocation:
                if len(energies) > 0:
                    if agent.Energy == max(energies) and random.randint(0, 1) == 0: #if 2 agents have same amount of energy, randomly pick one to win the collision
                        losing_agents.append(winning_agent)
                        winning_agent = agent
                    elif agent.Energy > max(energies):
                        losing_agents.append(winning_agent)
                        winning_agent = agent
                    else: #when agent has less energy
                        losing_agents.append(agent)
                else:
                    winning_agent = agent
                energies.append(agent.Energy)
            
            
            winning_agent.State = AgentState.EATING
            finalAgentLocations.add(loc, winning_agent)

            # move back losing agents
            for losing_agent in losing_agents:
                location, located_losing_Agent = None, None
                for loc in agentMap.LocatedObjects.keys():
                    agent = agentMap.LocatedObjects.Objects[loc][0]
                    if agent.Id == losing_agent.Id:
                        location = loc
                        located_losing_Agent = agent
                        break
                if location == None or located_losing_Agent == None:
                    raise("Something went wrong here")
                finalAgentLocations.add(loc, located_losing_Agent)

        world.Agents = finalAgentLocations
        
        
    def RemoveDeadAgents(self):
        for location, agent in self.World.DyingAgents:
            self.World.Agents.Objects.pop(location)
        self.World.DyingAgents = []

    def WithinBounds(self, location: tuple):
        x = location[0]
        y = location[1]
        return x >= 0 and x < self.World.Width and y >= 0 and y < self.World.Height

    def UpdateFoodMap(self, world: World):
        for agent_location in world.Agents.keys():
            if agent_location in world.Food.keys():
                # increase agents' energy by one
                world.Agents.Objects[agent_location][0].Eat()
                
                # remove food
                world.Food.Objects.pop(agent_location)
                
    def InitStatistics(self):
        seeingAgentsCount = 0
        blindAgentsCount = 0
        foodCount = len(self.World.Food.ObjectsList)
        dayCount = 0
        for agent in self.World.Agents.ObjectsList:
            if type(agent) is SeeingAgent:
                seeingAgentsCount += 1
            else:
                blindAgentsCount+=1
                
        return Statistics(seeingAgentsCount, blindAgentsCount, foodCount, dayCount, 0, 0)