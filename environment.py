import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces
from uav import UAV
from ship import SHIP
from fanc import FANC


class AirShipEnv(gym.Env):

    def __init__(self, render_mode = None, agent_num = 1, window_size = [1200, 800]):
        
        self.window_size = window_size
        self.agent_num = agent_num
        
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            high=np.array([float(window_size[0]), float(window_size[1]), float(2*np.pi)], dtype=np.float32),
            shape=(3,),
            dtype=np.float32
        )
        self.action_space = spaces.Box(
            low=np.array([-np.pi/6], dtype=np.float32),
            high=np.array([np.pi/6], dtype=np.float32),
            shape=(1,),
            dtype=np.float32
        )

        self.screen = None
        self.clock  = None
        self.bg = pygame.image.load("bg.png")
        self.render_mode = render_mode
        if self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode(window_size)
            self.clock  = pygame.time.Clock()
            pygame.display.set_caption("MISSION01")

        self.uav = [UAV() for _ in range(agent_num)]
        self.tgt = SHIP()
        self.fanc = FANC()

    # RESET
    def reset(self):
        super().reset()

        for uav in self.uav:
            uav.x = self.window_size[0] / 2
            uav.y = self.window_size[1] - 50
            uav.theta = np.pi / 2
        
        self.tgt.x = self.window_size[0] - 200
        self.tgt.y = 200
        self.tgt.theta = np.pi / 2

        self.render()
        return self.get_obs()

    # STEP
    def step(self, action):

        for i, uav in enumerate(self.uav):
            uav.move(action[i], self.window_size)

        self.render()
        return self.get_obs()
    
    # get observation {all}
    def get_obs(self):
        obs = []
        for i, uav in enumerate(self.uav):
            obs.append([uav.x, uav.y, uav.theta])

        return obs
    
    # render or not
    def render(self):
        if self.render_mode == "human":
            self._render_frame()

    # render one frame
    def _render_frame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return
        # flip background
        self.screen.blit(self.bg, (0, 0))

        # draw uav
        for uav in self.uav:
            if uav.is_alive:
                self.screen.blit(uav.rotated_image, uav.rotated_rect)
                pygame.draw.circle(self.screen, (200, 200, 200), (int(uav.x), int(uav.y)), uav.detect_range, 1)
                pygame.draw.circle(self.screen, (255, 55, 55), (int(uav.x), int(uav.y)), uav.attack_range, 1)
        
        # draw target
        if self.tgt.is_alive:
            self.screen.blit(self.tgt.rotated_image, self.tgt.rotated_rect)
            pygame.draw.circle(self.screen, (200, 200, 200), (int(self.tgt.x), int(self.tgt.y)), self.tgt.detect_range, 1)
            pygame.draw.circle(self.screen, (255, 55, 55), (int(self.tgt.x), int(self.tgt.y)), self.tgt.attack_range, 1)
        
        # draw fanc
        if self.fanc.is_alive:
            self.screen.blit(self.fanc.rotated_image, self.fanc.rotated_rect)
            pygame.draw.circle(self.screen, (255, 55, 55), (int(self.fanc.x), int(self.fanc.y)), self.fanc.attack_range, 1)
        
        # draw missile

        # flip all 
        pygame.display.flip()

    # Close Render windows
    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()
