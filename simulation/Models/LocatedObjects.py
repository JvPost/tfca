class LocatedObject():
    def __init__(self, x: int, y: int, obj):
        self.x = x
        self.y = y
        self.object = obj

class LocatedObjects():
    def __init__(self, locatedObjectDict: dict = None, locatedObjectList: list = None):
        """Wrapper for located objects where where the key is the location and the value is the object on that location.
        If both parameters are None Objects is set to an empty dict.

        Args:
            locatedObjectDict (dict, optional): key: locations, values: list of object at location. Defaults to None.
            locatedObjectList (list, optional): Every item in list should be a 2-tuple where first item is a 2-tuple containin the location and the second item is a list containing the object at said location. Defaults to None.
        """
        if locatedObjectList != None:
            if len(locatedObjectList) > 0 and len(locatedObjectList[0]) != 2:
                raise("If using locatedObjectList as initializer each item must be list with 2 items")
            else:
                locatedObjectList = list(locatedObjectList)
            
        
        self.Objects = {}
        if locatedObjectDict is not None:
            self.Objects = locatedObjectDict
        elif locatedObjectList is not None:
            for location, obj in locatedObjectList:
                self.Objects[tuple(location)] = obj
        
    def ToList(self):
        if len(self.Objects) > 0:
            return [self.Objects.values()]
        else:
            return []
    
    def __len__(self):
        return len(self.Objects)

    def keys(self):
        return self.Objects.keys()

    def add(self, key: tuple, value):
        if key in self.Objects:
            raise Exception("Already an object of this type at this location.")
        else:
            self.Objects[key] = value
            
    def count(self):
        return len(self.Objects)
    
    def get(self, index: int):
        return list(self.Objects.items())[0]
    
    def pop_at(self, index: int):
        loc, agent = self.get(0)
        self.Objects.pop(loc)
        return loc, agent
        
