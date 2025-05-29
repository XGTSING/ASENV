import gymnasium as gym
import numpy     as np
import pygame
from gymnasium  import spaces

from units.uav  import UAV
from units.usv  import USV
from units.ship import SHIP

class Env(gym.Env):

    def __init__(self, render_mode = None, agent_num = [1, 1], contact_num = [1, 1], window_size = [1200, 800]):
        
        self.window_size = window_size
        self.agent_num   = agent_num
        self.contact_num = contact_num

        # 标志位
        self.no_circle = True

        # 定义空间
        self.observation_space = spaces.Box(
            low  =np.array([0.0, 0.0, 0.0], dtype=np.float32),
            high =np.array([float(window_size[0]), float(window_size[1]), float(2*np.pi)], dtype=np.float32),
            shape=(3,),
            dtype=np.float32
        )
        self.action_space = spaces.Box(
            low  =np.array([-np.pi/6], dtype=np.float32),
            high =np.array([np.pi/6], dtype=np.float32),
            shape=(1,),
            dtype=np.float32
        )

        # 初始化Pygame
        self.screen = None
        self.clock  = None
        self.bg = pygame.image.load("images/bg.png")
        self.render_mode = render_mode
        if self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode(window_size)
            self.clock  = pygame.time.Clock()
            pygame.display.set_caption("MISSION01")

        # 实例化单位
        self.uav  = [UAV(image='uavr') for _ in range(self.agent_num[0])]
        self.usv  = [USV(image='usvr') for _ in range(self.agent_num[1])]

        self.DES  = SHIP(x = 1100, y = 100,detect_range=80, attack_range=50)
        self.BUJI = SHIP()

        self.uavb = [UAV(image='uavy') for _ in range(self.contact_num[0])]
        self.usvb = [USV(image='usvy') for _ in range(self.contact_num[1])]

    # RESET
    def reset(self):
        super().reset()
        # 驱逐舰方位初始化
        self.DES.x     = self.window_size[0] - 100
        self.DES.y     = 100
        self.DES.theta = 0
        # 补给舰方位初始化
        self.BUJI.x     = 200
        self.BUJI.y     = self.window_size[1] - 200
        self.BUJI.theta = np.arctan2(self.BUJI.y - self.DES.y, self.DES.x - self.BUJI.x)
        # 无人机方位初始化
        for uav in self.uav:
            uav.x     = 150
            uav.y     = self.window_size[1] - 150
            uav.theta = np.arctan2(self.BUJI.y - self.DES.y, self.DES.x - self.BUJI.x)
        # 无人艇方位初始化
        for usv in self.usv:
            usv.x     = 150
            usv.y     = self.window_size[1] - 150
            usv.theta = np.arctan2(self.BUJI.y - self.DES.y, self.DES.x - self.BUJI.x)

        # 蓝无人单位方位初始化
        for uavb in self.uavb:
            uavb.x     = 800
            uavb.y     = 600
            uavb.theta = np.arctan2(uavb.y - self.BUJI.y, self.BUJI.x - uavb.x)
        for usvb in self.usvb:
            usvb.x     = 800
            usvb.y     = 600
            usvb.theta = np.arctan2(usvb.y - self.BUJI.y, self.BUJI.x - usvb.x)

        self.render()
        return self.get_obs()

    # STEP
    def step(self, action):
        
        # 按键检测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.no_circle = not self.no_circle

        # 移动
        for i, uav in enumerate(self.uav):
            if uav.is_alive:
                uav.move(action[i], self.window_size)

        for i, usv in enumerate(self.usv):
            if usv.is_alive:
                usv.move(action[i+len(self.uav)], self.window_size)

        if self.BUJI.is_alive:
            self.BUJI.move(0, self.window_size)
        
        for i, uavb in enumerate(self.uavb):
            if uavb.is_alive:
                angle = np.arctan2(uavb.y - self.BUJI.y, self.BUJI.x - uavb.x)
                uavb.move(angle - uavb.theta + np.random.normal(0, np.pi/12), self.window_size)
        for i, usvb in enumerate(self.usvb):
            if usvb.is_alive:
                angle = np.arctan2(usvb.y - self.BUJI.y, self.BUJI.x - usvb.x)
                usvb.move(angle - usvb.theta + np.random.normal(0, np.pi/6), self.window_size)

        # 死亡逻辑
        for uav in self.uav:
            if uav.is_alive:
                for usvb in self.usvb:
                    if usvb.is_alive:
                        distance = np.sqrt((uav.x - usvb.x)**2 + (uav.y - usvb.y)**2)
                        if distance < uav.attack_range:
                            usvb.is_alive = False

        for usv in self.usv:
            if usv.is_alive:
                for usvb in self.usvb:
                    if usvb.is_alive:
                        distance = np.sqrt((usv.x - usvb.x)**2 + (usv.y - usvb.y)**2)
                        if distance < usv.bomb_range:
                            usvb.is_alive = False
                            usv.is_alive = False
        for uavb in self.uavb:
            if uavb.is_alive:
                for uav in self.uav:
                    if uav.is_alive:
                        distance = np.sqrt((uavb.x - uav.x)**2 + (uavb.y - uav.y)**2)
                        if distance < uavb.attack_range:
                            uav.is_alive = False
                            
        for usvb in self.usvb:
            if usvb.is_alive and self.BUJI.is_alive:
                distance = np.sqrt((usvb.x - self.BUJI.x)**2 + (usvb.y - self.BUJI.y)**2)
                if distance < usvb.bomb_range:
                    usvb.is_alive = False
                    self.BUJI.is_alive = False

        self.render()
        next_states = self.get_obs()
        rewards     = self.get_rewards()
        dones       = self.get_dones()
        return next_states, rewards, dones
    
    # get observation {all}
    def get_obs(self):
        obs = []
        for i, uav in enumerate(self.uav):
            obs.append([uav.x, uav.y, uav.theta])
        for i, usv in enumerate(self.usv):
            obs.append([usv.x, usv.y, usv.theta])
        return obs
    
    # get rewards {all}
    def get_rewards(self):

        pass

    # get_dones {all}
    def get_dones(self):
        
        pass

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

        # draw uavr
        for uav in self.uav:
            if uav.is_alive:
                self.screen.blit(uav.rotated_image, uav.rotated_rect)
                if not self.no_circle:
                    pygame.draw.circle(self.screen, (200, 200, 200), (int(uav.x), int(uav.y)), uav.detect_range, 1)
                    pygame.draw.circle(self.screen, (255, 55, 55), (int(uav.x), int(uav.y)), uav.attack_range, 1)
        
        # draw usvr
        for usv in self.usv:
            if usv.is_alive:
                pygame.draw.circle(self.screen, (255,255,0), (int(usv.x), int(usv.y)), usv.bomb_range, 1)
                self.screen.blit(usv.flipped_image, usv.flipped_rect)
                if not self.no_circle:
                    pygame.draw.circle(self.screen, (200,200,200), (int(usv.x), int(usv.y)), usv.detect_range, 1)
                    pygame.draw.circle(self.screen, (255,55,55), (int(usv.x), int(usv.y)), usv.attack_range, 1)
                
        # draw uavb
        for uavb in self.uavb:
            if uavb.is_alive:
                self.screen.blit(uavb.rotated_image, uavb.rotated_rect)
                if not self.no_circle:
                    pygame.draw.circle(self.screen, (200,200,200), (int(uavb.x), int(uavb.y)), uavb.detect_range, 1)
                    pygame.draw.circle(self.screen, (255,55,55), (int(uavb.x), int(uavb.y)), uavb.attack_range, 1)

        # draw usvb
        for usvb in self.usvb:
            if usvb.is_alive:
                pygame.draw.circle(self.screen, (255,255,0), (int(usvb.x), int(usvb.y)), usvb.bomb_range, 1)
                self.screen.blit(usvb.flipped_image, usvb.flipped_rect)
                if not self.no_circle:
                    pygame.draw.circle(self.screen, (200,200,200), (int(usvb.x), int(usvb.y)), usvb.detect_range, 1)
                    pygame.draw.circle(self.screen, (255,55,55), (int(usvb.x), int(usvb.y)), usvb.attack_range, 1)
                
        # draw Destroyer
        if self.DES.is_alive:
            self.screen.blit(self.DES.flipped_image, self.DES.flipped_rect)
            pygame.draw.circle(self.screen, (200, 200, 200), (int(self.DES.x), int(self.DES.y)), self.DES.detect_range, 1)
            pygame.draw.circle(self.screen, (255, 55, 55), (int(self.DES.x), int(self.DES.y)), self.DES.attack_range, 1)
        
        # draw BUJI
        if self.BUJI.is_alive:
            self.screen.blit(self.BUJI.flipped_image, self.BUJI.flipped_rect)
            pygame.draw.circle(self.screen, (200, 200, 200), (int(self.BUJI.x), int(self.BUJI.y)), self.BUJI.detect_range, 1)
            # pygame.draw.circle(self.screen, (255, 55, 55), (int(self.BUJI.x), int(self.BUJI.y)), self.BUJI.attack_range, 1)
        
        # flip all 
        pygame.display.flip()

    # Close Render windows
    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()
