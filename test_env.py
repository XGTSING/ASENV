from environment import Env
import time

# 一个测试环境的脚步，测试环境渲染是否正常

env = Env(agent_num = [0, 20], contact_num = [0, 5], render_mode = "human")

for i in range(10):
    obs = env.reset()

    for j in range(1000):
        action = [env.action_space.sample() for _ in range(env.agent_num[0]+env.agent_num[1])]
        env.step(action)
        time.sleep(0.1)

env.close()
