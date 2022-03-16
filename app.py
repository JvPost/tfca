from Models.LocatedObjects import LocatedObjects
from Models.World import World
from Models.Agent import Agent, Orientation
from Models.FoodObject import FoodObject
from Simulation import Simulation
from Models.Statistics import Statistics

import numpy as np

import random

def main():
    # world config
    worldWidth = 20
    worldHeight = 20
    stepsPerMove = 6
    timeStepsPerDay = 12

    #agents config    
    agentsCount = 20
    agentWidth = 1
    agentHeight = 1
    startEnergy = 0
    agents = CreateAgents(agentsCount, agentWidth, agentHeight, startEnergy, stepsPerMove)
    agent_locations = CreateLocations(worldWidth, worldHeight, agentsCount)
    locatedAgentsList = zip(agent_locations, agents)
    locatedAgents = LocatedObjects(locatedObjectList=locatedAgentsList)
    
    #food config
    foodCount = 40
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
    lastDay = False
    while(not lastDay):
        world_statistics = sim.Iterate()
        
        PrintStatistics(world_statistics)
        
        # new food
        foods = CreateFood(foodCount, foodWidth, foodHeight)
        foodsLocations = CreateLocations(worldWidth, worldHeight, foodCount)
        locatedFoodsList = zip(foodsLocations, foods)
        locatedFoods = LocatedObjects(locatedObjectList=locatedFoodsList)
        world.Food = locatedFoods
        
        lastDay = world_statistics.Day >= simulationLength

def CreateAgents(agentsCount: int, agentWidth: int,
                 agentHeight: int, startEnergy: int,
                 stepsPerMove) -> list:
    agents = []
    while agentsCount > len(agents):
        senseDistance = random.randint(0, 10)
        agent = Agent(agentWidth, agentHeight, startEnergy, senseDistance, stepsPerMove)
        agents.append(agent)
    return agents

def CreateFood(foodCount: int, foodWidth: int, foodHeight: int) -> list:
    return [FoodObject(foodWidth, foodHeight) for _ in range(foodCount+1)]

def CreateLocations(x_max: int, y_max: int, count: int) -> np.array:
    random_X = np.random.randint(0, x_max, size=count)
    random_Y = np.random.randint(0, y_max, size=count)
    zipped = zip(random_X, random_Y)    
    return [(x,y) for x,y in zipped]
    
def PrintStatistics(stats: Statistics) -> None:
    print(
        f"Day {stats.Day}\t {len(stats.Agents)} agents"
    )
    

if __name__ == "__main__":
    main()