from collections import defaultdict

class LocatedObjects():
    def __init__(self, locatedObjectDict: defaultdict = None, locatedObjectList: list = None):
        """Wrapper for located objects where default dict where the key is the location and the value is the list of object on that location.
        If both parameters are None Objects is empty defaultdict with list default item.

        Args:
            locatedObjectDict (defaultdict, optional): key: locations, values: list of object at location. Defaults to None.
            locatedObjectList (list, optional): Every item in list should be a 2-tuple where first item is a 2-tuple containin the location and the second item is a list containing the object at said location. Defaults to None.
        """
        if locatedObjectList != None:
            locatedObjectList = list(locatedObjectList)
            if len(locatedObjectList) > 0 and len(locatedObjectList[0]) != 2:
                raise("If using locatedObjectList as initializer each item must be list with 2 items")
            
        
        self.Objects = defaultdict(list)
        if locatedObjectDict is not None:
            self.Objects = locatedObjectDict
        elif locatedObjectList is not None:
            for location, obj in locatedObjectList:
                self.Objects[tuple(location)].append(obj)
        self.ObjectsList = self.ToList()
        
    def ToList(self):
        l = []
        for val in self.Objects.values():
            for obj in val:
                l.append(obj)
        return l
    
    def __len__(self):
        return len(self.Objects)

    def keys(self):
        return self.Objects.keys()

    def add(self, key: tuple, value):
        self.Objects[key].append(value)
        self.ObjectsList.append(value)
