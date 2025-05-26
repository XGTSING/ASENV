import numpy as np

class UAV():

    def __init__(self, x, y, theta):

        self.x = x
        self.y = y
        self.theta = theta

        self.speed = 10

        self.detect_range = 100
        self.attack_range = 50

    def move(self, action):

        self.theta += action

        self.x += self.speed * np.cos(self.theta)
        self.y += self.speed * np.sin(self.theta)
