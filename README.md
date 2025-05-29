# 无人机任务模拟环境

## 项目简介
这是一个基于Pygame和Gymnasium的无人机任务模拟环境，用于强化学习训练。环境模拟了无人机(UAV)与敌方舰船(SHIP)以及固定防空系统(FANC)之间的交互场景。

## 环境组件

### 主要对象
- **无人机(UAV)**: 可控制的智能体，具有探测和攻击能力
- **敌方舰船(SHIP)**: 移动目标，具有探测和攻击能力
- **防空系统(FANC)**: 固定防御设施，具有较大的攻击范围
- **导弹(MISSILE)**: 可发射的武器系统

### 文件结构
- `environment.py`: 主要环境类，基于Gymnasium实现
- `uav.py`: 无人机类定义
- `ship.py`: 敌方舰船类定义
- `fanc.py`: 固定防空系统类定义
- `missile.py`: 导弹类定义
- `test_env.py`: 环境测试示例
- `icons/`: 包含各种游戏图标
- `bg.png`: 游戏背景图

## 使用方法

### 环境初始化
```python
from environment import AirShipEnv

# 创建环境，设置智能体数量和渲染模式
env = AirShipEnv(agent_num=2, render_mode="human")

# 重置环境
obs = env.reset()
```

### 交互示例
```python
# 执行动作
action = [env.action_space.sample() for _ in range(env.agent_num)]
next_states, rewards, dones = env.step(action)

# 关闭环境
env.close()
```

## 环境参数

- **观察空间**: 每个智能体的位置(x, y)和方向角(theta)
- **动作空间**: 方向控制，范围为[-π/6, π/6]
- **智能体数量**: 可自定义
- **窗口大小**: 默认为1200×800像素

## 待完成功能
- 奖励函数实现
- 终止条件判断
- 导弹发射与追踪
- 多智能体协作策略

## 许可证
本项目使用MIT许可证，Copyright (c) 2025 XGTSING