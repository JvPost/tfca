from Models.World import World
from Models.Agent import Agent, Orientation, SeeingAgent
from Models.FoodObject import FoodObject
from Simulation import Simulation

import random

def main():
    # world config
    worldWidth = 10 
    worldHeight = 10

    #agents config    
    agentsCount = 10
    agentWidth = 1
    agentHeight = 1
    startEnergy = 10
    # agents = CreateAgents(worldWidth-1, worldHeight-1, agentsCount,
    #  agentWidth, agentHeight, startEnergy)
    agent = SeeingAgent((5,5), 1, 1, 10, 4, Orientation.NORTH)
    agents = [agent]
    
    stepsPerMove = 6
    timeStepsPerDay = 10
    
    #food config
    foodCount = 10
    foodWidth = 1
    foodHeight = 1
    foods = CreateFood(worldWidth-1, worldHeight-1, foodCount,
     foodWidth, foodHeight)

    # world config
    simulationLength = 100
    world = World(worldWidth, worldHeight, agents, foods)

    sim = Simulation(world, stepsPerMove, simulationLength, timeStepsPerDay)
    while(sim.Iterate()):

        print('Hello world')
        
def CreateAgents(x_max, y_max, agentsCount, agentWidth, agentHeight, startEnergy):
    agents = []
    xs = []
    ys = []
    while agentsCount > len(agents):
        rand_x = random.randint(0, x_max)
        rand_y = random.randint(0, y_max)
        if rand_x not in xs and rand_y not in ys:
            seeing = random.randint(0, 1)
            if (seeing == 0):
                agent = Agent((rand_x, rand_y), agentWidth, agentHeight, startEnergy, 1)
            elif(seeing == 1):
                agent = SeeingAgent((rand_x, rand_y), agentWidth, agentHeight, startEnergy, 4)
            xs.append(rand_x)
            ys.append(rand_y)
            agents.append(agent)
    return agents

def CreateFood(x_max, y_max, foodCount, foodWidth, foodHeight):
    foods = []
    xs = []
    ys = []
    while foodCount > len(foods):
        rand_x = random.randint(0, x_max)
        rand_y = random.randint(0, y_max)
        if rand_x not in xs and rand_y not in ys:
            xs.append(rand_x)
            ys.append(rand_y)
            food = FoodObject((rand_x, rand_y), foodWidth, foodHeight)
            foods.append(food)
    return foods

if __name__ == "__main__":
    main()