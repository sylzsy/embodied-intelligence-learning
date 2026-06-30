# Open X-Embodiment (OXE) 数据集初探

## 1. 数据集简介

Open X-Embodiment 是由 Google DeepMind 联合多家机构发布的大规模机器人学习数据集。它将多个机器人数据集统一整理到标准格式下，便于训练通用机器人策略模型。

该数据集的价值不只在于规模大，更重要的是它尝试统一不同机器人平台、不同任务、不同采集环境下的数据格式，为 RT 系列、Octo、OpenVLA 等机器人基础模型提供数据基础。

## 2. 数据规模

| 指标 | 数值 |
| --- | --- |
| 真机轨迹总数 | 100 万+ |
| 整合数据集数量 | 60 个 |
| 机器人平台种类 | 22 种 |
| 技能数量 | 527 种 |
| 任务实例 | 16 万+ |
| 参与机构 | 21 个机构，34 个实验室 |
| 原始数据量 | 约 32TB，压缩后约 3.6TB |

## 3. 主要机器人平台

- Franka Emika Panda
- WidowX
- UR5
- xArm
- Sawyer
- Google Robot / Everyday Robots
- KUKA 工业臂
- ALOHA 双手系统
- Hello Robot Stretch 移动操作平台
- Unitree A1
- Boston Dynamics Spot

## 4. 典型子集

| 子集 | 机器人平台 | 大致规模 | 特点 |
| --- | --- | --- | --- |
| Language Table | xArm | 约 44 万条 | 桌面操作任务，语言条件明显 |
| Fractal / RT-1 | Google Robot | 约 13 万条 | 移动操作任务，真实环境采集 |
| BridgeData V2 | WidowX | 约 6 万条 | 常用于模仿学习和泛化实验 |
| QT-Opt | KUKA | 约 6 万条 | 抓取任务数据 |

## 5. 数据结构

OXE 使用 RLDS 格式组织数据，可以粗略理解为：

```text
Dataset
└── Episode
    └── Step
        ├── observation
        │   ├── image
        │   ├── state
        │   └── language_instruction
        ├── action
        ├── reward
        └── discount
```

### Observation

- `image`: RGB 图像，记录机器人当前视觉输入。
- `state`: 机器人本体状态，例如关节角度、末端位姿等。
- `language_instruction`: 自然语言任务描述，例如 `pick up the blue block`。

### Action

常见动作表示包括：

- `world_vector`: 末端执行器位置变化。
- `rotation_delta`: 末端执行器旋转变化。
- `gripper`: 夹爪开合状态。

## 6. 数据样例

一个 episode 可以理解为一条完整机器人操作轨迹。每个 step 记录机器人在某一时刻看到什么、状态是什么、执行了什么动作。

任务示例：`put the spoon in the drawer`

| Step | 观测 | 动作 |
| --- | --- | --- |
| 0 | RGB 图像 + 机器人状态 | x=0.01, y=0.02, z=-0.01, gripper=0.8 |
| 1 | RGB 图像 + 机器人状态 | x=0.02, y=0.01, z=-0.02, gripper=0.7 |
| ... | ... | ... |
| 119 | RGB 图像 + 机器人状态 | x=0, y=0, z=0, gripper=1.0 |

## 7. 数据质量关注点

后续做数据质量分析时，优先检查以下问题：

- 字段完整性：是否存在缺失 image、state、action、language_instruction 的 step。
- 轨迹长度：episode 是否过短或过长，是否存在异常中断。
- 图像质量：图像尺寸是否一致，是否存在空帧、黑帧、损坏帧。
- 动作质量：action 维度是否一致，是否存在极端异常值。
- 语言指令质量：指令是否为空，是否过于模板化，是否和实际轨迹不匹配。
- 跨数据集一致性：不同子集的 observation / action 字段命名和语义是否统一。

## 8. 下一步

- 选择一个小规模子集进行实际加载。
- 输出真实字段结构和样本统计。
- 编写数据质量检查脚本。
- 形成第一版数据质量分析报告。
