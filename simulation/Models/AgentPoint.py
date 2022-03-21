from .Agent import Agent
from Graphics.graphics import Point

class AgentPoint:
    def __init__(self, x: int, y: int, agent: Agent, point: Point):
        self.X = x
        self.Y = y
        self.Agent = agent
        self.Point = Point(x, y)