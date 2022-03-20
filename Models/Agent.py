from ast import Or
from .WorldObject import WorldObject
from .LocatedObjects import LocatedObjects
from .AgentDayResult import AgentDayResult

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

    def __init__(self, width, height, energy, senseDistance, speed:int, angle: int = None):
        super().__init__(width, height)
        self.Energy = energy
        self.SenseDistance = senseDistance
        self.Alive = True
        self.EnergyCost = senseDistance
        self.Speed = speed
        self.Intention = (0, 0)
        if angle == None:
            self.Angle = np.random.uniform(0, math.pi*2)
        else:
            self.Angle = angle

    def Eat(self) -> None:
        self.Energy = self.Energy+1

    def EndOfDay(self) -> AgentDayResult:
        self.Energy -= (round(self.EnergyCost/3) + 1)
        child = None
        if self.Energy < 1:
            self.Alive = False
        elif self.Energy > 1:
            child = self.Replicate()
        self.Energy = 0
        return AgentDayResult(child)

    def ChooseNextLocation(self, locatedObjects: LocatedObjects) -> tuple:
        """_summary_

        Args:
            locatedObjects (LocatedObjects): _description_

        Returns:
            tuple: _description_
        """
        locations = locatedObjects.Objects.keys()
        distances = [np.sqrt(x**2 + y**2) for x,y in locations]
        dx, dy = list(locations)[np.argmin(distances)]
        # if the distance is above max, find the next best allowed location
        dist = math.sqrt(dx**2 + dy**2)
        self.Angle = math.atan2(-dy, dx)
        if dist > self.Speed:     
            dx = round(self.Speed * math.cos(self.Angle))
            dy = -round(self.Speed * math.sin(self.Angle))
                
        self.Intention = (dx, dy)
        
    def ChooseRandomNextLocation(self, speed: int) -> tuple:
        """ Calculates a new random location for agent and return is

        Args:

            speed (int): _description_

        Returns:
            tuple: _description_
        """
        # self.Angle = np.random.normal(self.Angle, 0.1) % 2*math.pi
        
        dx = round(self.Speed * math.cos(self.Angle))
        dy = -round(self.Speed * math.sin(self.Angle))
        self.Intention = (dx, dy)
        

    def GetNewLocation(self, currentLocation: tuple) -> tuple:
        """Calculate new location, return new location.

        Args:
            currentLocation (tuple): agents current location coordinates tuple

        Returns:
            tuple: new location
        """
        return tuple(np.array(currentLocation) + np.array(self.Intention))

    

    def Replicate(self):
        childSenseRange = max(0, round(np.random.normal(self.SenseDistance, 1)))
        child = Agent(self.Width, self.Height, 0,
                      childSenseRange, self.Speed)
        return child