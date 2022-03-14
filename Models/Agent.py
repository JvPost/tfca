from ast import Or
from .WorldObject import WorldObject
from .LocatedObjects import LocatedObjects

from enum import IntEnum
import random
import numpy as np

class Orientation(IntEnum):
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3,
    RANDOM = 5

class AgentState(IntEnum):
    IDLE = 0,
    EATING = 1,
    MOVING = 2

class Agent(WorldObject):
    HorizontalEnumValues = [1, 3]
    VerticalEnumVals = [0, 2]

    def __init__(self, width, height, energy, receptiveDistance):
        super().__init__(width, height)
        self.Energy = energy
        self.ReceptiveDistance = receptiveDistance
        self.Alive = True
        self.State = AgentState.IDLE

    def GetPerceptionX(self):
        return [x for x in range(-self.ReceptiveDistance, self.ReceptiveDistance+1)]
    
    def GetPerceptionY(self):
        return [y for y in range(-self.ReceptiveDistance, self.ReceptiveDistance+1)]

    def Eat(self) -> None:
        if (self.State == AgentState.EATING):
            self.Energy = self.Energy+1
            self.State = AgentState.IDLE

    def ChooseNextLocation(self, locatedObjects: LocatedObjects) -> tuple:
        """_summary_

        Args:
            locatedObjects (LocatedObjects): _description_

        Returns:
            tuple: _description_
        """
        locations = locatedObjects.Objects.keys()
        distances = [np.sqrt(x**2 + y**2) for x,y in locations]
        chosenLocation =list(locations)[np.argmin(distances)]
        return chosenLocation

    def Move(self, currentLocation: tuple, movement: tuple, orientation : Orientation = None) -> tuple:
        """Calculate new location, change orientation, return new location.

        Args:
            currentLocation (tuple): agents current location coordinates tuple
            movement (tuple): agents movement tuple
            orienation (Orientation, optional): Changes orientation if not None. Defaults to None.

        Returns:
            tuple: new location
        """
        if orientation is not None and orientation is not Orientation.RANDOM:
            self.Orientation = orientation
        elif orientation == Orientation.RANDOM:
            self.Orientation = Orientation(random.randint(0, 3))

        return tuple(np.array(currentLocation) + np.array(movement))

    def MoveRandom(self, currentLocation: tuple, stepsCount: int) -> tuple:
        """ Calculates a new random location for agent and return is

        Args:
            currentLocation (tuple): _description_
            stepsCount (int): _description_

        Returns:
            tuple: _description_
        """
        x_stepsCount = random.randint(0, stepsCount)
        rand_idx_x = random.randint(0, 1)
        moveOrientation_x = Orientation(Agent.HorizontalEnumValues[rand_idx_x]) # get orientation east or west
        curr_x, curr_y = currentLocation
        new_x, new_y = 0,0 
        if moveOrientation_x == Orientation.EAST:
            new_x = curr_x+x_stepsCount
        elif moveOrientation_x == Orientation.WEST:
            new_x = curr_x-x_stepsCount
        # move y
        y_stepsCount = stepsCount - x_stepsCount
        rand_idx_y = random.randint(0, 1)
        moveOrientation_y = Orientation(Agent.VerticalEnumVals[rand_idx_y]) # get orientation north or south
        if moveOrientation_y == Orientation.NORTH:
            new_y = curr_y-y_stepsCount
        elif moveOrientation_y == Orientation.SOUTH:
            new_y = curr_y+y_stepsCount
        self.Orientation = Orientation(random.randint(0, 3))
        return new_x, new_y

class SeeingAgent(Agent):
    def __init__(self,width, height, energy, receptiveDistance, orientation = None):
        super().__init__(width, height, energy, receptiveDistance)
        if orientation == None:
            orientationInt = random.randint(0, 3)
            self.Orientation = Orientation(orientationInt)
        else:
            self.Orientation = orientation

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

    

    # ########## #
    # Deperacate #
    # ########## #
    # def FindNearestFood(self, relativeFoodLocations : np.ndarray) -> tuple:
    #     """Find nearest food given relative food locations

    #     Args:
    #         relativeFoodLocation (np.ndarray): food locations relative to agent

    #     Returns:
    #         tuple: indeces of object relative to agent
    #     """
    #     distances = []
    #     idx = -1
    #     for loc in relativeFoodLocations:
    #         distances.append(np.sqrt(loc[0]**2 + loc[1]**2))
    #     idx = np.argmin(distances)
    #     if (idx > -1):
    #         loc = relativeFoodLocations[idx]
    #         return (loc[0], loc[1])
    #     else:
    #         return None

    # def ProposeMove(self, relativePosition: tuple) -> tuple:
    #     """Returns the new position of the agent after moving from current position to relative position

    #     Args:
    #         relativePosition (tuple): position relative to agent

    #     Returns:
    #         tuple: tuple containing X and Y coordinate after moving.
    #     """
    #     x = self.X + relativePosition[0]
    #     y = self.Y + relativePosition[1]
    #     return x, y

    # def MoveTo(self, relativePosition: tuple, finishState: AgentState) -> None:
    #     """Changes absolute position according to relativePosition

    #     Args:
    #         relativePosition (tuple): position relative to agent
    #         finishState (AgentState): state after moving
    #     """
    #     self.X = self.X + relativePosition[0]
    #     self.Y = self.Y + relativePosition[1]
    #     self.State = finishState
        
        

    # def MoveRandom(self, stepsCount):
    #     """Proposes and random move at time step

    #     Args:
    #         stepsCount (int): nro steps

    #     Returns:
    #         2-tuple: proposed x to move to, proposed y to move to
    #     """
    #     # move x
    #     x_stepsCount = random.randint(0, stepsCount)
    #     rand_idx_x = random.randint(0, 1)
    #     moveOrientation_x = Orientation(Agent.HorizontalEnumValues[rand_idx_x]) # get orientation east or west
    #     new_x, new_y = 0
    #     if moveOrientation_x == Orientation.EAST:
    #         new_x = self.X+x_stepsCount
    #     elif moveOrientation_x == Orientation.WEST:
    #         new_x = self.X-x_stepsCount
    #     # move y
    #     y_stepsCount = stepsCount - x_stepsCount
    #     rand_idx_y = random.randint(0, 1)
    #     moveOrientation_y = Orientation(Agent.VerticalEnumVals[rand_idx_y]) # get orientation north or south
    #     if moveOrientation_y == Orientation.NORTH:
    #         new_y = self.Y-y_stepsCount
    #     elif moveOrientation_y == Orientation.SOUTH:
    #         new_y = self.Y+y_stepsCount
        
    #     return new_x, new_y

      # def DetectsFoodAt(self, visionArray : np.ndarray, verbose = False) -> tuple:
        
    #     return

    # def SeesFoodAt(self, foodMap:np.array, verbose = False) -> tuple:
    #     """Trys and sees food in agents perception field.
    #     If sees food, the location relative to the agent is returned, empty list otherwise

    #     Args:
    #         foodMap (np.array): World bitmap (from Map.Map), 1 if food in location, 0 otherwise.

    #     Returns:
    #         tuple: 2-tuple containing bool indicating whether agents sees food and location of food.
    #         Location is relative to agent, where agent location is (0,0)
    #     """
        # Should not be able to know self.X and self.Y
        # relativePositions = self.Cartesian # cartesian coordinates describing the vision of the agent relative to the position of the agent
        # absolutePositions = relativePositions + [self.X, self.Y] # cartesian coordinates decribing the vision of agent on entire map as a whole
        # indeces = absolutePositions.reshape(-1, absolutePositions.shape[-1]) # indeces of absolute positions
        # index_columns = tuple([indeces[:, 1], indeces[:, 0]]) # 2D array, axis 0 = y coordinates of vision in food map, axis 1 = x cooridaation of vision food map 
        # foodPresentOnIndex = foodMap[index_columns].astype(bool) # checks which index food is present
        # seesFood = np.any(foodPresentOnIndex)
        # foodPresentRelativePositions = []

        # if verbose:
        #     mask = np.zeros_like(foodMap)
        #     mask[index_columns] = 1
        #     print(foodMap)
        #     print('=====')
        #     print(mask)
        # if seesFood:
        #     location_indeces = np.where(foodPresentOnIndex)
        #     relativePositionIndeces = relativePositions.reshape(-1, relativePositions.shape[-1])
        #     for loc in location_indeces:
        #         foodPresentRelativePositions.append(relativePositionIndeces[loc])
            
        # return seesFood, np.array(foodPresentRelativePositions).squeeze(0)
