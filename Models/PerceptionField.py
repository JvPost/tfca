import enum
import numpy as np
from .Agent import Agent

class PerceptionField():
    def __init__(self, location: tuple, agent: Agent):
        self.x = location[0]
        self.y = location[1]
        self.agent = agent
        self.Cartesian = self.AsCartesian()

    def AsCartesian(self) -> np.ndarray:
        matrix = []
        x_detected = self.agent.GetPerceptionX()
        y_detected = self.agent.GetPerceptionY()
        for i, x in enumerate(x_detected):
            row = []
            for j, y in enumerate(y_detected):
                row.append([x,y])
            matrix.append(row)
        return np.array(matrix)

    