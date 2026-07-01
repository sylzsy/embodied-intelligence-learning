# 样例机器人数据质量检查报告

## 1. 目标

本报告用于验证机器人 episode 数据质量检查脚本的基础能力。当前使用一份小规模 JSONL 样例数据，模拟具身智能数据集中常见的 observation、action、language instruction、timestamp 等字段。

后续可将同一套检查逻辑迁移到 Open X-Embodiment、BridgeData V2 或 RH20T 的小规模子集上，用于生成真实公开数据集的质量分析报告。

## 2. 数据概况

| 指标 | 结果 |
| --- | --- |
| episode 数量 | 2 |
| step 总数 | 5 |
| 最短轨迹长度 | 2 |
| 最长轨迹长度 | 3 |
| 平均轨迹长度 | 2.5 |
| language instruction 去重数量 | 2 |

## 3. 字段分布

### Action 维度

| action 维度 | step 数 |
| --- | --- |
| 4 | 4 |
| 2 | 1 |

正常样本中 action 维度为 4，异常样本中出现了维度为 2 的 action。真实机器人数据中，action 维度不一致通常意味着不同机器人平台、不同动作表示方式或数据转换过程存在问题，需要在训练前完成统一映射。

### 图像尺寸

| 图像尺寸 | step 数 |
| --- | --- |
| 256 x 256 x 3 | 4 |
| 128 x 128 x 3 | 1 |

样例数据中存在不同图像尺寸。对于模仿学习或 VLA 模型训练，这类问题通常需要通过 resize、padding 或按数据源分组处理，否则容易导致 dataloader 或模型输入维度报错。

## 4. 发现的问题

| 问题类型 | 数量 | 影响 |
| --- | --- | --- |
| missing_language_instruction | 1 | 语言条件缺失，影响语言指令到动作的监督学习 |
| invalid_state | 1 | 机器人本体状态为空，影响状态输入或轨迹分析 |
| non_increasing_timestamp | 1 | 时间戳不递增，说明 step 顺序或采集时间存在异常 |
| inconsistent_action_dim | 1 | 动作维度不一致，影响训练样本拼接和模型输出定义 |
| inconsistent_image_shape | 1 | 图像尺寸不一致，影响 dataloader 和视觉编码器输入 |

## 5. 对具身智能数据工程的意义

机器人学习数据和普通业务数据相比，更强调多模态字段之间的对齐关系。一个 step 中的图像、机器人状态、动作、语言指令和时间戳必须保持一致，否则模型会学到错误的状态-动作对应关系。

本次样例检查虽然规模很小，但已经覆盖了具身智能数据工程中最基础的质量问题：

- observation 字段是否完整
- action 维度是否统一
- language instruction 是否缺失
- timestamp 是否保持时序一致
- 图像尺寸是否可进入统一训练管线

## 6. 下一步

1. 编写 `load_rlds_sample.py`，加载 RLDS / TFDS 格式的小规模公开数据样本。
2. 将公开数据集样本转换为当前脚本可读取的 JSONL episode 格式。
3. 将检查结果用于 Open X-Embodiment 或 BridgeData V2 小样本，并输出第一版真实数据集质量报告。
4. 增加黑帧、空帧、动作极端值和轨迹长度异常阈值等更细粒度检查。
