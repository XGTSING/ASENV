import pygame
import numpy as np

class MISSILE():

    def __init__(self, x = 0, y = 0, theta = 0):

        self.x = x
        self.y = y
        self.theta = theta

        self.is_alive = True
        self.speed = 20

        self.image = pygame.image.load("images/icons/mslr.png").convert_alpha()
        width = self.image.get_width() * 0.5
        height = self.image.get_height() * 0.5
        self.scaled_image = pygame.transform.scale(self.image, (width, height))
        self.rotated_image = pygame.transform.rotate(self.scaled_image, np.degrees(self.theta)-90)
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
        
        self.rotated_image = pygame.transform.rotate(self.scaled_image, np.degrees(self.theta)-90)
        self.rotated_rect = self.rotated_image.get_rect(center=(self.x, self.y))