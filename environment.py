import gymnasium as gym
import numpy     as np
import pygame
from gymnasium  import spaces

from units.uav  import UAV
from units.usv  import USV
from units.ship import SHIP

class Env(gym.Env):

    def __init__(self, render_mode = None, agent_num = [1, 1], window_size = [1200, 800]):
        
        self.window_size = window_size
        self.agent_num   = agent_num

        # 标志位
        self.no_circle = True
        self.no_line = True

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

        self.User = UAV(x=self.window_size[0]/2, y= self.window_size[1]-50, theta=np.pi/2, image='usery', speed=5)
        self.UserAction = 0
        self.DES  = SHIP(x = 900, y = 300, theta=0, image='shipy', speed=0, detect_range=80, attack_range=50)

    # RESET
    def reset(self):
        super().reset()

        # 无人机方位初始化
        for uav in self.uav:
            uav.x     = 250
            uav.y     = self.window_size[1] - 200
            uav.theta = np.arctan2(uav.y - self.DES.y, self.DES.x - uav.x)
        # 无人艇方位初始化
        for usv in self.usv:
            usv.x     = 250
            usv.y     = self.window_size[1] - 250
            usv.theta = np.arctan2(usv.y - self.DES.y, self.DES.x - usv.x)

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
                if event.key == pygame.K_l:
                    self.no_line = not self.no_line
                if event.key == pygame.K_RIGHT:
                    self.UserAction = -np.pi/6
                elif event.key == pygame.K_LEFT:
                    self.UserAction = np.pi/6
                if event.key == pygame.K_UP:
                    self.User.speed += 2
                    self.User.speed = max(self.User.speed, 0)
                elif event.key == pygame.K_DOWN:
                    self.User.speed -= 2
                    self.User.speed = max(self.User.speed, 0)

        # 移动
        self.User.move(self.UserAction, self.window_size)
        self.UserAction = 0

        self.DES.move(0, self.window_size)

        for i, uav in enumerate(self.uav):
            if uav.is_alive:
                uav.move(np.random.normal(0, np.pi/20), self.window_size)

        for i, usv in enumerate(self.usv):
            if usv.is_alive:
                usv.move(np.random.normal(0, np.pi/20), self.window_size)

        for uav in self.uav:
            dx = uav.x - self.DES.x
            dy = uav.y - self.DES.y
            dis = np.sqrt(dx **2 + dy ** 2)
            if dis < uav.detect_range:
                self.DES.image = 'shipb'
                self.DES.change_icon()

        if np.linalg.norm(np.array([self.User.x, self.User.y], dtype= np.float64) - np.array([self.DES.x, self.DES.y], dtype= np.float64)) < self.User.detect_range:
            self.DES.image = 'shipb'
            self.DES.change_icon()

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
        # self.screen.blit(self.bg, (0, 0))
        self.screen.fill((24, 73, 132))
        font = pygame.font.SysFont("Arial", 16)

        # draw line
        if not self.no_line:
            for i in range(3):
                pygame.draw.line(self.screen, (150, 150, 150), (300*(i+1), 0), ( 300*(i+1), 800), width=1)
                pygame.draw.line(self.screen, (150, 150, 150), (0, 200*(i+1)), (1200, 200*(i+1)), width=1)
            for i in range(4):
                for j in range(4):
                    text = font.render(f"A{(i+1)*(j+1)}", True, (255, 255, 255))
                    self.screen.blit(text, (300*i + 275, 200*j + 180))

        # draw user
        self.screen.blit(self.User.rotated_image, self.User.rotated_rect)
        pygame.draw.circle(self.screen, (200, 200, 200), (int(self.User.x), int(self.User.y)), self.User.detect_range, 1)

        # draw area
        fill_area = pygame.Rect(0, 0, 1200, 800)
        pygame.draw.rect(self.screen, (200, 0, 0), fill_area, 1)
        text = font.render("TargetArea", True, (255, 255, 255))
        self.screen.blit(text, (5, 5))

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
                pygame.draw.circle(self.screen, (255,255,0), (int(usv.x), int(usv.y)), usv.bomb_range, 2)
                self.screen.blit(usv.flipped_image, usv.flipped_rect)
                if not self.no_circle:
                    pygame.draw.circle(self.screen, (200,200,200), (int(usv.x), int(usv.y)), usv.detect_range, 1)
                    pygame.draw.circle(self.screen, (255,55,55), (int(usv.x), int(usv.y)), usv.attack_range, 1)
       
        # draw Destroyer
        if self.DES.is_alive:
            self.screen.blit(self.DES.flipped_image, self.DES.flipped_rect)
            pygame.draw.circle(self.screen, (200, 200, 200), (int(self.DES.x), int(self.DES.y)), self.DES.detect_range, 1)
            pygame.draw.circle(self.screen, (255, 55, 55), (int(self.DES.x), int(self.DES.y)), self.DES.attack_range, 1)
        
        
        # flip all 
        pygame.display.flip()

    # Close Render windows
    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()
