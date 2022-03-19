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
    worldWidth = 100
    worldHeight = 100
    stepsPerMove = 3
    timeStepsPerDay = 40
    slow = False
    
    #agents config    
    agentsCount = 10
    agentWidth = 1
    agentHeight = 1
    startEnergy = 0
    agents = CreateAgents(agentsCount, agentWidth, agentHeight, startEnergy, stepsPerMove)
    agent_locations = CreateLocations(worldWidth, worldHeight, agentsCount)
    # agents = [Agent(1, 1, 1000, 5, 3, 0)]
    # agent_locations = [(0, 50)]    
    locatedAgentsList = zip(agent_locations, agents)
    locatedAgents = LocatedObjects(locatedObjectList=locatedAgentsList)
    
    
    #food config
    foodCount = 1667
    foodWidth = 1
    foodHeight = 1
    foods = CreateFood(foodCount, foodWidth, foodHeight)
    foodsLocations = CreateLocations(worldWidth, worldHeight, foodCount)
    locatedFoodsList = zip(foodsLocations, foods)
    locatedFoods = LocatedObjects(locatedObjectList=locatedFoodsList)

    # world config
    simulationLength = 1000
    world = World(worldWidth, worldHeight, locatedAgents, locatedFoods)

    sim = Simulation(world, stepsPerMove, simulationLength, timeStepsPerDay, True)
    start_statistics = Statistics(1, locatedAgents)
    stop = False
    while(not stop):
        world_statistics = sim.Iterate(slow)
        
        PrintStatistics(world_statistics, 10)
        
        # new food
        foods = CreateFood(foodCount, foodWidth, foodHeight)
        foodsLocations = CreateLocations(worldWidth, worldHeight, foodCount)
        locatedFoodsList = zip(foodsLocations, foods)
        locatedFoods = LocatedObjects(locatedObjectList=locatedFoodsList)
        world.Food = locatedFoods
        
        stop = world_statistics.Day >= simulationLength or len(world.Agents) == 0

def CreateAgents(agentsCount: int, agentWidth: int,
                 agentHeight: int, startEnergy: int,
                 stepsPerMove) -> list:
    agents = []
    while agentsCount > len(agents):
        senseDistance = random.randint(5, 9)
        agent = Agent(agentWidth, agentHeight, startEnergy, senseDistance, stepsPerMove)
        agents.append(agent)
    return agents

def CreateFood(foodCount: int, foodWidth: int, foodHeight: int) -> list:
    return [FoodObject(foodWidth, foodHeight) for _ in range(foodCount+1)]

def CreateLocations(x_max: int, y_max: int, count: int) -> np.array:
    lst = []
    while len(lst) < count:
        x = round(random.randint(0.1*x_max, 0.9*x_max))
        y = round(random.randint(0.1*y_max, 0.9*y_max))
        if (x, y) not in lst:
            lst.append((x, y))
    return lst
    
    
def PrintStatistics(stats: Statistics, stop: int ) -> None:
    print(
        f"Day {stats.Day} - {len(stats.Agents)} agents:\n{stats.AgentHist(stop)}"
    )
    
if __name__ == "__main__":
    main()