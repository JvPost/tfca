from ast import Or
from .WorldObject import WorldObject
from .LocatedObjects import LocatedObjects

from enum import IntEnum
import random
import numpy as np
import math

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

    def __init__(self, width, height, energy, receptiveDistance, moveDistance:int):
        super().__init__(width, height)
        self.Energy = energy
        self.ReceptiveDistance = receptiveDistance
        self.Alive = True
        self.State = AgentState.IDLE
        self.EnergyCost = receptiveDistance
        self.moveDistance = moveDistance

    def GetPerceptionX(self):
        return [x for x in range(-self.ReceptiveDistance, self.ReceptiveDistance+1)]
    
    def GetPerceptionY(self):
        return [y for y in range(-self.ReceptiveDistance, self.ReceptiveDistance+1)]

    def Eat(self) -> None:
        if (self.State == AgentState.EATING):
            self.Energy = self.Energy+1
            self.State = AgentState.IDLE

    def EndOfDay(self):
        self.Energy -= self.EnergyCost
        if self.Energy<0:
            self.Alive = False

    def ChooseNextLocation(self, locatedObjects: LocatedObjects) -> tuple:
        """_summary_

        Args:
            locatedObjects (LocatedObjects): _description_

        Returns:
            tuple: _description_
        """
        locations = locatedObjects.Objects.keys()
        distances = [np.sqrt(x**2 + y**2) for x,y in locations]
        x,y = list(locations)[np.argmin(distances)]
        # if the distance is above max, find the next best allowed location
        dist = math.sqrt(x**2 + y**2)
        if dist > self.moveDistance: 
            rad = math.atan((-y)/x)
            x_allowed = round(self.moveDistance * math.cos(rad))
            y_allowed = -round(self.moveDistance * math.sin(rad))
            if x < 0:
                x_allowed *= -1
            if y < 0:
                y_allowed *= -1
            x, y = x_allowed, y_allowed
            
        return (x,y)

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

    def Replicate(self) -> list:
        return []