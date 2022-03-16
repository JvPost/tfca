from Models.LocatedObjects import LocatedObjects
from Models.World import World
from Models.Agent import Agent, Orientation, SeeingAgent
from Models.FoodObject import FoodObject
from Simulation import Simulation
from Models.Statistics import Statistics

import numpy as np

import random

def main():
    # world config
    worldWidth = 1000
    worldHeight = 1000
    stepsPerMove = 6
    timeStepsPerDay = 12

    #agents config    
    agentsCount = 100
    agentWidth = 1
    agentHeight = 1
    startEnergy = 10
    agents = CreateAgents(agentsCount, agentWidth, agentHeight, startEnergy)
    agent_locations = CreateLocations(worldWidth, worldHeight, agentsCount)
    locatedAgentsList = zip(agent_locations, agents)
    locatedAgents = LocatedObjects(locatedObjectList=locatedAgentsList)
    
    #food config
    foodCount = 5000
    foodWidth = 1
    foodHeight = 1
    foods = CreateFood(foodCount, foodWidth, foodHeight)
    foodsLocations = CreateLocations(worldWidth, worldHeight, foodCount)
    locatedFoodsList = zip(foodsLocations, foods)
    locatedFoods = LocatedObjects(locatedObjectList=locatedFoodsList)

    # world config
    simulationLength = 100
    world = World(worldWidth, worldHeight, locatedAgents, locatedFoods)

    sim = Simulation(world, stepsPerMove, simulationLength, timeStepsPerDay)
    while(sim.Iterate()):
        PrintStatistics(sim.Statistics)
        
def CreateAgents(agentsCount: int, agentWidth: int, agentHeight: int, startEnergy: int) -> list:
    agents = []
    while agentsCount > len(agents):
        seeing = random.randint(0, 1)
        if seeing == 1:
            agent = SeeingAgent(agentWidth, agentHeight, startEnergy, 4)
        else:
            agent = Agent(agentWidth, agentHeight, startEnergy, 1)
        agents.append(agent)
    return agents

def CreateFood(foodCount: int, foodWidth: int, foodHeight: int) -> list:
    return [FoodObject(foodWidth, foodHeight) for _ in range(foodCount+1)]

def CreateLocations(x_max: int, y_max: int, count: int) -> np.array:
    random_X = np.random.randint(0, x_max, size=count)
    random_Y = np.random.randint(0, y_max, size=count)
    zipped = zip(random_X, random_Y)    
    return [(x,y) for x,y in zipped]
    
def PrintStatistics(stats: Statistics):
    if (stats.CurrentTimeStep == 0):
        print(f"Day{stats.DayCount}:\t",
                    stats.BlindAgentsCount,
                    stats.SeeingAgentsCount,
                    stats.FoodCount
              )

if __name__ == "__main__":
    main()