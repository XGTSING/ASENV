import numpy as np
import pygame

class SHIP():

    def __init__(self, x=0.0, y=0.0, theta=0.0, image='shipr', speed=1, detect_range=100, attack_range=70):

        self.x = x
        self.y = y
        self.theta = theta
        self.image = image

        self.is_alive = True
        self.speed = speed

        self.detect_range = detect_range
        self.attack_range = attack_range

        self.image = pygame.image.load("images/icons/%s.png" % self.image).convert_alpha()
        width = self.image.get_width() * 1.2
        height = self.image.get_height() * 1.2
        self.scaled_image = pygame.transform.scale(self.image, (width, height))
        self.flipped_image = pygame.transform.flip(self.scaled_image, True, False)
        self.flipped_rect = self.flipped_image.get_rect(center=(self.x, self.y))
    
    def change_icon(self):
        self.image = pygame.image.load("images/icons/%s.png" % self.image).convert_alpha()
        width = self.image.get_width() * 1.2
        height = self.image.get_height() * 1.2
        self.scaled_image = pygame.transform.scale(self.image, (width, height))
        # self.flipped_image = pygame.transform.flip(self.scaled_image, True, False)
        self.flipped_rect = self.flipped_image.get_rect(center=(self.x, self.y))

    def move(self, action, window_size):

        self.theta += action
        self.theta = self.theta%(2 * np.pi)

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
        
        if np.cos(self.theta) > 0:
            self.flipped_image = pygame.transform.flip(self.scaled_image, True, False)
        else:
            self.flipped_image = self.scaled_image
        self.flipped_rect = self.flipped_image.get_rect(center=(self.x, self.y))
