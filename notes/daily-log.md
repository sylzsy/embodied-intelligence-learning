# 学习日志

  ## 2026-06-26

  - **今日收获**：完成了 Open X-Embodiment
  数据集初探——搞清楚了它的规模（100万+轨迹、60个数据集、22种机器人）和数据格式（Episode → Step → observation + action
  的层级结构），数据长什么样心里有数了。精读了 RT-2 论文，理解了 VLA 的核心逻辑——拿大 VLM 做 co-fine-tuning、把 action
  转成 token 跟文字混着训，让机器人既有常识又能动手。顺便把 VLM/VLA/co-fine-tuning/泛化层次 这些基础概念都捋清了。

  - **卡点/疑问**：Open X-Embodiment 还没实际下载数据，RLDS 格式到底怎么用还没上手。RT-2 的 chain-of-thought
  推理具体是怎么触发的、tokenization 的细节（action 离散化到 256 个 bin 具体怎么映射）还需要后面深入看。

  - **明天计划**：下载 Open X-Embodiment 一个小子集（比如 Bridge V2），用 Python 加载数据看看实际长什么样。开第二篇论文
  Diffusion Policy，和 RT-2 对比着看。

## 2026-07-01

- **今日完成**：按照 Day 1 操作手册跑通了机器人 episode 数据质量检查流程。进入项目目录后，查看了 `sample_robot_episodes.jsonl`，理解了 episode、steps、observation、action、timestamp 的基本结构；运行 `check_dataset_quality.py` 后，看到样例数据共有 2 个 episode、5 个 step，并检测出 5 类数据质量问题。

- **今日理解**：`issue_types` 用来统计每类问题出现了多少次，`issues` 用来定位问题具体发生在哪个 episode 和 step。今天理解了语言指令缺失、机器人状态缺失、时间戳不递增、动作维度不一致、图像尺寸不一致这 5 类问题，以及它们对机器人模仿学习 / VLA 模型训练的影响。

- **卡点 / 疑问**：目前使用的是手写样例数据，还没有加载真实的 Open X-Embodiment 或 BridgeData V2 数据。下一步需要学习真实数据集的 RLDS / TFDS 格式，并把真实 episode 转换成脚本可检查的结构。

- **下一步行动**：继续做 Day 2，目标是研究 BridgeData V2 或 Open X-Embodiment 小样本的数据加载方式，打印真实 episode 字段结构，并尝试复用当前质量检查脚本。
