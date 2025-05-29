import numpy as np
import pygame

class USV():

    def __init__(self, x = 0, y = 0, theta = 0, image = 'usvr', speed = 2, detect_range = 30, attack_range = 15, bomb_range = 5):

        self.x = x
        self.y = y
        self.theta = theta
        self.image = image

        self.is_alive = True
        self.speed = speed

        self.detect_range = detect_range
        self.attack_range = attack_range
        self.bomb_range   = bomb_range

        self.image = pygame.image.load("images/icons/%s.png" % self.image).convert_alpha()
        width = self.image.get_width() * 0.8
        height = self.image.get_height() * 0.8
        self.scaled_image = pygame.transform.scale(self.image, (width, height))
        self.flipped_image = pygame.transform.flip(self.scaled_image, True, False)
        self.flipped_rect = self.flipped_image.get_rect(center=(self.x, self.y))

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
        
        if 0 < self.theta < np.pi/2 or 3*np.pi/2 < self.theta < 2*np.pi:
            self.flipped_image = pygame.transform.flip(self.scaled_image, True, False)
        else:
            self.flipped_image = self.scaled_image
        self.flipped_rect = self.flipped_image.get_rect(center=(self.x, self.y))
