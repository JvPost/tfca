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
    worldWidth = 50
    worldHeight = 50
    speed = np.sqrt(2)
    timeStepsPerDay = 40
    
    #agents config    
    agentsCount = 1
    agentWidth = 1
    agentHeight = 1
    startEnergy = 0
    
    agents = CreateAgents(agentsCount, agentWidth, agentHeight, startEnergy, speed)
    agent_locations = CreateLocations(worldWidth, worldHeight, agentsCount)
    
    locatedAgentsList = [ locatedAgent for locatedAgent in zip(agent_locations, agents)]
    locatedAgents = LocatedObjects(locatedObjectList=locatedAgentsList)
    
    
    #food config
    foodCount = 200
    foodWidth = 1
    foodHeight = 1
    
    foods = CreateFood(foodCount, foodWidth, foodHeight)
    foodsLocations = CreateLocations(worldWidth, worldHeight, foodCount)
        
    locatedFoodsList = [ locatedFood for locatedFood in zip(foodsLocations, foods)]
    locatedFoods = LocatedObjects(locatedObjectList=locatedFoodsList)

    # sim config
    slow = False
    visualize = True
    scale = 10
    simulationLength = 1000
    world = World(worldWidth, worldHeight, locatedAgents, locatedFoods)
    sim = Simulation(world, speed, simulationLength, timeStepsPerDay, visualize, scale)
    start_statistics = Statistics(1, locatedAgents)
    stop = False
    
    while(not stop):
        world_statistics = sim.Iterate(slow)
        
        PrintStatistics(world_statistics, 10)
        
        # new food
        foods = CreateFood(foodCount, foodWidth, foodHeight)
        foodsLocations = CreateLocations(worldWidth, worldHeight, foodCount)
        locatedFoodsList = [ locatedFood for locatedFood in zip(foodsLocations, foods)]
        locatedFoods = LocatedObjects(locatedObjectList=locatedFoodsList)
        sim.AddFood(locatedFoods)
        
        stop = world_statistics.Day >= simulationLength or len(world.Agents) == 0
            
    print("Finish")
    

def CreateAgents(agentsCount: int, agentWidth: int,
                 agentHeight: int, startEnergy: int,
                 stepsPerMove) -> list:
    agents = []
    while agentsCount > len(agents):
        senseDistance = random.randint(0, 9)
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
    
def WriteStatistics(newline: list, file):
    file.write(f"{newline.split(',')}\n")
    
def PrintStatistics(stats: Statistics, stop: int ) -> None:
    print(
        f"Day {stats.Day} - {len(stats.Agents)} agents:\n{stats.AgentHist(stop)}"
    )
    with open('data', 'w') as f:
        string = " ".join([str(y) for y in stats.AgentHist(stop)])
        f.write(string)
    
    
if __name__ == "__main__":
    main()