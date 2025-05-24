import gymnasium as gym
import numpy as np
from gymnasium import spaces

class AirShipEnv():

    def __init__(self, agent_num = 1, window_size = [800, 600]):
        
        self.state_space  = spaces.Box(
            low   = np.array([0, 0, 0]),
            high  = np.array([window_size[0], window_size[1], 2*np.pi]),
            dtype = np.float32
        )
        self.action_space = spaces.Box(
            
        )

    def reset():
        
        pass

    def step():
        
        pass

    def show_frame():
        
        pass

    def close():

        pass