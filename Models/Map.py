from collections import defaultdict
import numpy as np

from Models.WorldObject import WorldObject
from Models.LocatedObjects import LocatedObjects
from Models.World import World
from Models.Plane import Plane

class Map:
    def __init__(self, world: World = None, locatedObjects: LocatedObjects = LocatedObjects()):
        self.LocatedObjects = locatedObjects
        if world is not None:
            self.Width = world.Width
            self.Height = world.Height
            
    def GetMatrix(self):
        matrix = np.zeros((self.Height, self.Width))
        for x,y in self.LocatedObjects.Objects.keys():
            matrix[y,x] = 1
        return matrix

    def GetDetectedObjects(self, location: tuple, plane: Plane) -> LocatedObjects:
        """Gets LocatedObjects relative to agent

        Args:
            location (tuple): location to detect from.
            plane (Plane): plane object being perceived

        Returns:
            LocatedObjects: objects located relative to agent.
        """
        # rel = relative
        relPlane = plane.Cartesian
        relIndeces = relPlane.reshape(-1, relPlane.shape[-1])
        
        mapPlane = plane.Cartesian + location
        mapIndeces = mapPlane.reshape(-1, mapPlane.shape[-1])

        relLocatedObjects = []
        for i, _ in enumerate(mapIndeces):
            mapIndex = tuple(mapIndeces[i])
            if mapIndex in self.LocatedObjects.Objects.keys():
                relativePositionIndex = tuple(relIndeces[i])
                obj = self.LocatedObjects.Objects[mapIndex][0]
                relLocatedObjects.append((relativePositionIndex, obj))
        locatedObjects = LocatedObjects(locatedObjectList=relLocatedObjects)
        return locatedObjects

    def FindClosestEmptyCells(self, location: tuple) -> tuple:
        """_summary_

        Args:
            location (tuple): _description_

        Returns:
            tuple: _description_
        """
        locationFound = False
        relEmptyCells = []
        searchBreadth = 1
        while len(relEmptyCells) == 0:
            relPlane = Plane(location, searchBreadth).Cartesian
            relIndeces = relPlane.reshape(-1, relPlane.shape[-1])
            
            mapPlane = relPlane + location
            mapIndeces = mapPlane.reshape(-1, mapPlane.shape[-1])
            for idx, _ in enumerate(mapIndeces):
                mapIndex = tuple(mapIndeces[idx])
                if mapIndex not in self.LocatedObjects.Objects.keys():
                    relativePositionIndex = tuple(relIndeces[idx])
                    if relativePositionIndex is not (0,0):
                        relEmptyCells.append(relativePositionIndex)
            locationFound = len(relEmptyCells) == 0
            searchBreadth += 1
            
        relEmptyCells = np.array(relEmptyCells)
        relEmptyCellDists = np.array([np.sqrt(x**2 + y**2) for x, y in relEmptyCells])
        relEmptyCells = relEmptyCells[relEmptyCellDists == np.min(relEmptyCellDists)]
        
        return relEmptyCells
        
    
        
            
    def GetMovementPlane(self, location: tuple, speed: int) -> Plane:
        """Should only be used if locatedObjects in this map are of type agents
        

        Args:
            location (tuple): _description_
            speed (int): _description_

        Returns:
            Plane: _description_
        """        
        plane = Plane(location, speed).Cartesian
        # relPositionIndeces = relPositionsPlain.reshape(-1, relPositionsPlain.shape[-1])

        mapPlane = plane + location
        # absPositionsIndeces = absPositionsPlain.reshape(-1, absPositionsPlain.shape[-1])
        
        mapPlane = mapPlane[ mapPlane[:,:, 0] >= 0 ]    
        
        return