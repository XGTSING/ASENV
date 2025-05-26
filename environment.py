import gymnasium as gym
import numpy as np
from gymnasium import spaces

class AirShipEnv(gym.Env):

    def __init__(self, agent_num = 1, window_size = [800, 600]):
        
        self.state_space  = spaces.Box(
            low   = np.array([0, 0, 0]),
            high  = np.array([window_size[0], window_size[1], 2*np.pi]),
            shape = (3,),
            dtype = np.float32
        )
        self.action_space = spaces.Box(
            low   = np.array([-np.pi/6]),
            high  = np.array([np.pi/6]),
            shape = (1,),
            dtype = np.float32
        )

        

    def reset(self):
        super().reset()


        pass

    def step(self):
        
        pass

    def show_frame():
        
        pass

    def close():

        pass