from collections import defaultdict
import numpy as np

from Models.WorldObject import WorldObject
from Models.LocatedObjects import LocatedObjects
from Models.World import World
from Models.PerceptionField import PerceptionField

class Map:
    def __init__(self, world: World = None, locatedObjects: LocatedObjects = LocatedObjects()):
        self.LocatedObjects = locatedObjects
        if world is not None:
            self.Width = world.Width
            self.Height = world.Height
        self.Matrix = self.GetMatrix()
        
    def GetMatrix(self):
        matrix = np.zeros((self.Height, self.Width))
        for x,y in self.LocatedObjects.Objects.keys():
            matrix[y,x] = 1
        return matrix

    def GetDetectedObjects(self, location: tuple, field: PerceptionField) -> LocatedObjects:
        """Gets LocatedObjects relative to agent

        Args:
            location (tuple): location to detect from.
            field (PerceptionField): field object being perceived

        Returns:
            LocatedObjects: objects located relative to agent.
        """
        relPositionsPlain = field.Cartesian
        relPositionIndeces = relPositionsPlain.reshape(-1, relPositionsPlain.shape[-1])
        
        absPositionsPlain = field.Cartesian + location
        absPositionIndeces = absPositionsPlain.reshape(-1, absPositionsPlain.shape[-1])

        relativePositionedObjects = []
        for i, _ in enumerate(absPositionIndeces):
            absolutePositionIndex = tuple(absPositionIndeces[i])
            if absolutePositionIndex in self.LocatedObjects.Objects.keys():
                relativePositionIndex = tuple(relPositionIndeces[i])
                obj = self.LocatedObjects.Objects[absolutePositionIndex][0]
                relativePositionedObjects.append((relativePositionIndex, obj))
        locatedObjects = LocatedObjects(locatedObjectList=relativePositionedObjects)
        return locatedObjects
        # return [(loc, item) for loc, item in zip(matrix_indeces, self.Matrix[matrix_indeces_columns])]

    # def GetMapFor(self, objects):
    #     _loc = [(obj.X, obj.Y) for obj in objects]
    #     _map = np.zeros((self.Height, self.Width))
    #     for x, y in _loc:
    #         _map[y, x] = 1
    #     return _map

    # def GetLocatedObjects(self):
    #     objects = defaultdict(list)
    #     for obj in self.Objects:
    #         self.LocatedObjects[(obj.X, obj.Y)].append(obj)

    # def GetObjectList(self):
    #     d = self.LocatedObjects
    #     return [obj for obj in self.Objects]
    

    
        
        