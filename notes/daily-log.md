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

- **今日收获**：跑通了第一个机器人 episode 数据质量检查脚本，理解了 episode、step、observation、action、language_instruction、timestamp 的基本结构。脚本能够统计轨迹长度、动作维度、图像尺寸，并识别语言指令缺失、state 为空、时间戳不递增、动作维度不一致、图像尺寸不一致等问题。

- **卡点/疑问**：当前使用的是手写样例数据，还没有加载真实 Open X-Embodiment / BridgeData V2 数据。下一步需要学习 RLDS / TFDS 数据格式，并把真实数据转换成统一 JSONL 格式。

- **明天计划**：研究 BridgeData V2 或 Open X-Embodiment 的小样本加载方式，编写 `load_rlds_sample.py`，把真实 episode 的字段结构打印出来。
