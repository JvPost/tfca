import uuid

class WorldObject:
    def __init__(self, width, height, orientation = None):            
        self.Width = width
        if self.Width%2 == 0:
            self.Width = self.Width + 1
            
        self.Height = height
        if self.Height%2 == 0:
            self.Height = self.Height + 1

        self.Orientation = orientation
        self.Id = uuid.uuid4()
