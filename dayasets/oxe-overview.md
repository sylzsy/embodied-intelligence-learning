# Open X-Embodiment (OXE) 数据集初探

  ## 1. 它是什么？
  Open X-Embodiment 是一个由 Google DeepMind 联合 21 个机构、34 个实验室共同发布的**大规模机器人学习数据集**，
  将 60 个已有的机器人数据集统一整合到一个标准格式下，供机器人基础模型训练使用。
  获得了 ICRA 2024 最佳会议论文奖。Octo、OpenVLA 等开源机器人基础模型都用它训练。

  ## 2. 数据规模

  | 指标 | 数值 |
  |------|------|
  | 真机轨迹总数 | **100万+**（完整集约140万） |
  | 整合数据集数量 | **60个** |
  | 机器人平台种类 | **22种** |
  | 技能数量 | **527种** |
  | 任务实例 | **16万+** |
  | 参与机构 | **21个**（34个实验室） |
  | 原始数据量 | ~32TB（压缩后约3.6TB） |

  ### 主要机器人平台
  - Franka Emika Panda、WidowX、UR5、xArm、Sawyer
  - Google Robot（Everyday Robots）
  - KUKA 工业臂
  - ALOHA 双手系统
  - Hello Robot Stretch 移动操作
  - 宇树 A1、波士顿动力 Spot（足式）

  ### 最大的几个子集
  - Language Table（xArm）：~44万条
  - Fractal / RT-1（Google Robot）：~13万条
  - Bridge V2（WidowX）：~6万条
  - QT-Opt（KUKA）：~6万条

  ## 3. 数据长什么样？

  ### 层级结构
  Dataset（整体数据集）
    └── Episode（一条完整的轨迹）
          └── Step（每个时间步）
                ├── observation（观测）
                │     ├── image：RGB图像 (300×300×3)
                │     ├── state：本体感知状态（关节角度等）
                │     └── language_instruction：自然语言任务描述
                ├── action（动作）
                │     ├── world_vector：末端位置 (x, y, z)
                │     ├── rotation_delta：旋转 (roll, pitch, yaw)
                │     └── gripper：夹爪开合度
                ├── reward（奖励，可选）
                └── discount（折扣因子，可选）

  ### 关键特征
  - 所有数据统一为 **RLDS 格式**（基于 TFDS / Apache Arrow）
  - 图像统一缩放到 320×256
  - 动作空间：7自由度末端执行器（x, y, z, roll, pitch, yaw）+ 夹爪
  - 平均轨迹长度：约 120 个时间步，3-10Hz
  - 任务以自然语言形式标注，如 "pick up the blue block"

  ### 数据样例（概念）
  Episode 1:
    Task: "put the spoon in the drawer"
    Step 0: image=[RGB数组], action=[0.01, 0.02, -0.01, 0, 0, 0, 0.8]
    Step 1: image=[RGB数组], action=[0.02, 0.01, -0.02, 0, 0, 0, 0.7]
    ...
    Step 119: image=[RGB数组], action=[0, 0, 0, 0, 0, 0, 1.0]
