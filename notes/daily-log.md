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

## 2026-07-01 Day 2

- **今日完成**：完成了 BridgeData V2 字段结构理解和 BridgeData-style 小样本转换。确认 BridgeData V2 在 TFDS 中的数据集名是 `bridge`，完整数据约 387GB，因此没有直接完整下载，而是先用小样本验证字段映射流程。

- **今日理解**：BridgeData-style 数据中包含 `episode_metadata`、`steps/action`、`steps/language_instruction`、`steps/observation/image_0` 和 `steps/observation/state`。我将 `image_0` 映射为统一的 `observation.image`，将 step 级别的 `language_instruction` 放入 `observation.language_instruction`，从而让不同来源的数据可以复用同一套质量检查脚本。

- **运行结果**：转换后的样例数据共有 1 个 episode、2 个 step；action 维度为 7，图像尺寸为 256 x 256 x 3，`issue_count` 为 0，说明样例数据字段完整且格式一致。

- **卡点 / 疑问**：当前本地 Python 环境没有安装 `tensorflow` 和 `tensorflow_datasets`，因此还没有直接加载真实 TFDS/RLDS 数据。后续需要单独准备兼容环境，再尝试读取真实 BridgeData V2 小样本 metadata。

- **下一步行动**：准备 Day 3，研究如何安装或创建适合 TFDS/RLDS 的 Python 环境，并尝试读取 `bridge` 数据集的 metadata 或小规模样本。

## 2026-07-01 Day 3

- **今日完成**：创建了独立 conda 环境 `ei-tfds`，使用 Python 3.11.15，并安装了 TensorFlow 2.21.0 和 TensorFlow Datasets 4.9.10。完成了 TFDS/RLDS 数据加载环境的基础搭建。

- **今日理解**：没有使用 base 环境，因为 base 是 Python 3.13，不适合作为 TensorFlow 主环境。通过独立环境隔离依赖，可以避免污染已有项目环境，也方便后续复现实验。

- **运行结果**：运行 `inspect_tfds_builder.py --dataset mnist` 成功读取 TFDS metadata，输出了 `mnist/3.0.1`、`image` 和 `label` 等 features，说明 TFDS 环境和 builder 检查脚本可用。

- **卡点 / 疑问**：尝试读取 `bridge` metadata 时本地超时，判断不是 TensorFlow/TFDS 安装问题，而可能是 TFDS catalog 远程初始化或网络访问问题。

- **下一步行动**：Day 4 准备使用 Google Colab 或更稳定网络尝试读取 `bridge` metadata；如果仍然受限，则继续基于 BridgeData-style schema 完善字段报告和质量检查流程。
