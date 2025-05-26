import numpy as np
import pygame

class SHIP():

    def __init__(self, x=1000, y=200, theta=np.pi/2):

        self.x = x
        self.y = y
        self.theta = theta

        self.is_alive = True
        self.speed = 2

        self.detect_range = 50
        self.attack_range = 30

        self.image = pygame.image.load("icons/shipb.png").convert_alpha()
        self.rotated_image = pygame.transform.rotate(self.image, np.degrees(self.theta)-90)
        self.rotated_rect = self.rotated_image.get_rect(center = (self.x, self.y))

    def move(self, action, window_size):

        self.theta += action

        self.x += self.speed * np.cos(self.theta)
        self.y -= self.speed * np.sin(self.theta)
        
        if self.x > window_size[0]:
            self.x = window_size[0]
        elif self.x < 0:
            self.x = 0

        if self.y > window_size[1]:
            self.y = window_size[1]
        elif self.y < 0:
            self.y = 0
        
        self.rotated_image = pygame.transform.rotate(self.image, np.degrees(self.theta)-90)
        self.rotated_rect = self.rotated_image.get_rect(center=(self.x, self.y))