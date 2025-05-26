from environment import AirShipEnv
import time

env = AirShipEnv(agent_num = 2, render_mode = "human")

for i in range(10):
    obs = env.reset()

    for j in range(100):
        action = [env.action_space.sample() for _ in range(env.agent_num)]
        env.step(action)
        time.sleep(0.01)

env.close()
