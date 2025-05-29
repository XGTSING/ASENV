import numpy as np
import pygame

class FANC():
    def __init__(self, x = 595, y = 400):

        self.x = x
        self.y = y

        self.is_alive = True

        self.attack_range = 250

        # fancility can not move
        self.image = pygame.image.load("images/icons/trcb.png").convert_alpha()
        self.rotated_image = pygame.transform.rotate(self.image, 0)
        self.rotated_rect = self.rotated_image.get_rect(center = (self.x, self.y))