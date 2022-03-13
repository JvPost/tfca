from .WorldObject import WorldObject
from .ReceptiveField import ReceptiveField
from .Map import Map

import numpy as np


from enum import IntEnum
import random

class Orientation(IntEnum):
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3

class AgentState(IntEnum):
    IDLE = 0,
    EATING = 1

class Agent(WorldObject):
    HorizontalEnumValues = [1, 3]
    VerticalEnumVals = [0, 2]

    def __init__(self, location: tuple, width, height, energy, receptiveDistance):
        super().__init__(location, width, height)
        self.Energy = energy
        self.ReceptiveDistance = receptiveDistance
        self.Alive = True
        self.Cartesian = self.GetPerceptionField().AsCartesian()
        self.State = AgentState.IDLE

    def GetPerceptionField(self)-> ReceptiveField: 
        X = self.GetPerceptionX()
        Y = self.GetPerceptionY();
        field = ReceptiveField(X, Y) 
        return field

    def GetPerceptionX(self):
        return [x for x in range(-self.ReceptiveDistance, self.ReceptiveDistance+1)]
    
    def GetPerceptionY(self):
        return [y for y in range(-self.ReceptiveDistance, self.ReceptiveDistance+1)]
        
    def ProposeMove(self, relativePosition: tuple) -> tuple:
        """Returns the new position of the agent after moving from current position to relative position

        Args:
            relativePosition (tuple): position relative to agent

        Returns:
            tuple: tuple containing X and Y coordinate after moving.
        """
        x = self.X + relativePosition[0]
        y = self.Y + relativePosition[1]
        return x, y

    def MoveTo(self, relativePosition: tuple, finishState: AgentState) -> None:
        """Changes absolute position according to relativePosition

        Args:
            relativePosition (tuple): position relative to agent
            finishState (AgentState): state after moving
        """
        self.X = self.X + relativePosition[0]
        self.Y = self.Y + relativePosition[1]
        self.State = finishState
        
        

    def MoveRandom(self, stepsCount):
        """Proposes and random move at time step

        Args:
            stepsCount (int): nro steps

        Returns:
            2-tuple: proposed x to move to, proposed y to move to
        """
        # move x
        x_stepsCount = random.randint(0, stepsCount)
        rand_idx_x = random.randint(0, 1)
        moveOrientation_x = Orientation(Agent.HorizontalEnumValues[rand_idx_x]) # get orientation east or west
        new_x, new_y = 0
        if moveOrientation_x == Orientation.EAST:
            new_x = self.X+x_stepsCount
        elif moveOrientation_x == Orientation.WEST:
            new_x = self.X-x_stepsCount
        # move y
        y_stepsCount = stepsCount - x_stepsCount
        rand_idx_y = random.randint(0, 1)
        moveOrientation_y = Orientation(Agent.VerticalEnumVals[rand_idx_y]) # get orientation north or south
        if moveOrientation_y == Orientation.NORTH:
            new_y = self.Y-y_stepsCount
        elif moveOrientation_y == Orientation.SOUTH:
            new_y = self.Y+y_stepsCount
        
        return new_x, new_y

    def SeesFoodAt(self, foodMap:np.array, verbose = False) -> tuple:
        """Trys and sees food in agents perception field.
        If sees food, the location relative to the agent is returned, empty list otherwise

        Args:
            foodMap (np.array): World bitmap (from Map.Map), 1 if food in location, 0 otherwise.

        Returns:
            tuple: 2-tuple containing bool indicating whether agents sees food and location of food.
            Location is relative to agent, where agent location is (0,0)
        """
        relativePositions = self.Cartesian # cartesian coordinates describing the vision of the agent relative to the position of the agent
        absolutePositions = relativePositions + [self.X, self.Y] # cartesian coordinates decribing the vision of agent on entire map as a whole
        indeces = absolutePositions.reshape(-1, absolutePositions.shape[-1]) # indeces of absolute positions
        index_columns = tuple([indeces[:, 1], indeces[:, 0]]) # 2D array, axis 0 = y coordinates of vision in food map, axis 1 = x cooridaation of vision food map 
        foodPresentOnIndex = foodMap[index_columns].astype(bool) # checks which index food is present
        seesFood = np.any(foodPresentOnIndex)
        foodPresentRelativePositions = []

        if verbose:
            mask = np.zeros_like(foodMap)
            mask[index_columns] = 1
            print(foodMap)
            print('=====')
            print(mask)
        if seesFood:
            location_indeces = np.where(foodPresentOnIndex)
            relativePositionIndeces = relativePositions.reshape(-1, relativePositions.shape[-1])
            for loc in location_indeces:
                foodPresentRelativePositions.append(relativePositionIndeces[loc])
            
        return seesFood, np.array(foodPresentRelativePositions).squeeze(0)

    def FindNearestFood(self, relativeFoodLocations : np.ndarray) -> tuple:
        """Find nearest food given relative food locations

        Args:
            relativeFoodLocation (np.ndarray): food locations relative to agent

        Returns:
            tuple: indeces of object relative to agent
        """
        distances = []
        idx = -1
        for loc in relativeFoodLocations:
            distances.append(np.sqrt(loc[0]**2 + loc[1]**2))
        idx = np.argmin(distances)
        if (idx > -1):
            loc = relativeFoodLocations[idx]
            return (loc[0], loc[1])
        else:
            return None


    def Eat(self):
        if (self.State == AgentState.EATING):
            self.Energy = self.Energy+1
            self.State = AgentState.IDLE


class SeeingAgent(Agent):
    def __init__(self, location: tuple, width, height, energy, receptiveDistance, orientation = None):
        super().__init__(location, width, height, energy, receptiveDistance)
        if orientation == None:
            orientationInt = random.randint(0, 3)
            self.Orientation = Orientation(orientationInt)
        else:
            self.Orientation = orientation
        self.Cartesian = self.GetPerceptionField().AsCartesian()

    
    def GetPerceptionX(self) -> list:
        X = []
        if self.Orientation == Orientation.NORTH or self.Orientation == Orientation.SOUTH:
            X = [x for x in range(-1, 2)]
        elif self.Orientation == Orientation.EAST:
            X = [x for x in range(0, self.ReceptiveDistance+1)]
        elif self.Orientation == Orientation.WEST:
            X = [x for x in range(-self.ReceptiveDistance, 1)]
        return X

    def GetPerceptionY(self) -> list:
        Y = []
        if self.Orientation == Orientation.EAST or self.Orientation == Orientation.WEST:
            Y = [y for y in range(-1, 2)]
        elif self.Orientation == Orientation.SOUTH:
            Y = [y for y in range(0, self.ReceptiveDistance+1)]
        elif self.Orientation == Orientation.NORTH:
            Y = [y for y in range(-self.ReceptiveDistance, 1)]
        return Y

    def GetPerceptionField(self)-> ReceptiveField: 
        X = self.GetPerceptionX()
        Y = self.GetPerceptionY();
        field = ReceptiveField(X, Y) 
        return field