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
