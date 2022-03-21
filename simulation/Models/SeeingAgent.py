    
# depracated
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

