# 简历项目描述：BridgeData V2 数据质量检查

## 项目名称

面向具身智能训练数据的 BridgeData V2 数据质量检查流程

## 一句话概括

围绕 BridgeData V2 / BridgeData-style 机器人数据，搭建 episode 数据格式转换、schema 规则检查、质量指标统计和报告输出流程，验证机器人训练数据在进入模仿学习管线前的可用性。

## 简历 Bullet 版本

- 调研 BridgeData V2 / Open X-Embodiment 数据结构，梳理 episode-step 层级下的 `observation`、`action`、`state`、`image_0`、`language_instruction` 等核心字段，并整理官方 schema 文档。
- 编写 BridgeData-style 数据转换脚本，将 `image_0`、`state`、`language_instruction`、`action` 等字段映射到统一 JSONL episode 格式，便于后续跨数据集复用质检流程。
- 开发机器人数据质量检查脚本，支持字段完整性、action/state 维度、图像尺寸、timestamp 递增、轨迹长度阈值、action 极端值和缺失率统计等检查。
- 基于 BridgeData V2 schema 设置 `action_dim=7`、`state_dim=7`、`image_shape=256x256x3` 等规则，对 BridgeData-style mock episode 进行验证，输出 `issue_count=0` 的质量检查结果。
- 使用异常样例验证脚本有效性，识别 `missing_language_instruction`、`invalid_state`、`non_increasing_timestamp`、`inconsistent_action_dim`、`inconsistent_image_shape`、`action_value_out_of_range` 等问题，并输出缺失率指标。
- 输出 Markdown / JSON 数据质量报告，形成从数据结构理解、字段转换、质量检查到报告生成的具身智能数据工程闭环。

## 面试项目介绍

这个项目的目标是从数据工程角度理解具身智能训练数据，而不是直接训练模型。我选择 BridgeData V2 作为切入点，因为它是常见的机器人操作数据集，采用 episode-step 结构，每个 step 包含图像、机器人状态、语言指令和动作。

我先整理了官方 TFDS schema，确认 BridgeData V2 的 action 和 state 都是 7 维，主视角图像 `image_0` 是 256x256x3，语言 embedding 是 512 维。然后我写了转换脚本，把 BridgeData-style 数据映射成统一 JSONL 格式，例如把 `image_0` 映射成 `observation.image`，把 step 级别的 `language_instruction` 放入 `observation`。

在质量检查部分，我写了一个可配置脚本，支持检查字段缺失、action/state 维度、图像尺寸、timestamp 是否递增、轨迹长度是否合理、action 是否有极端值，并输出缺失率等质量指标。这样后续接入真实 BridgeData V2 episode 时，可以复用同一套流程判断数据是否适合进入模仿学习训练管线。

## 面试追问准备

### 为什么先做数据质量，不直接训练模型？

因为机器人模型训练高度依赖状态、图像、语言和动作之间的对齐。如果数据存在缺帧、动作维度不一致、时间戳错乱或语言指令缺失，模型会学习到错误的状态-动作映射。先做数据质量检查可以降低后续训练和调参的不确定性。

### 为什么 BridgeData V2 里 `image_0` 要映射成 `observation.image`？

不同机器人数据集的图像字段命名不完全一致。为了让质量检查脚本可以复用，我把具体数据集字段映射到统一字段，例如把 BridgeData V2 的 `image_0` 映射成统一的 `observation.image`。这样后续接入其他数据集时，只需要写适配层，不需要重写质检逻辑。

### `issue_types` 和 `quality_rates` 有什么区别？

`issue_types` 统计每类问题出现了多少次，适合定位异常类型；`quality_rates` 把缺失类问题按 step 总数转成比例，适合写数据质量报告。例如 5 个 step 里 1 个缺少语言指令，缺失率就是 20%。

### 为什么要检查 action 极端值？

action 是机器人执行动作的监督信号。如果 action 数值超过合理范围，可能说明数据采集、单位转换、坐标系转换或归一化过程有问题，也可能污染训练分布，导致模型训练不稳定。严重时，异常动作还可能在仿真或真机执行中造成越界或碰撞风险。

## 当前不足和下一步

- 当前流程已在 BridgeData-style mock episode 上验证，下一步需要接入真实 BridgeData V2 小样本。
- 本地读取 `bridge` metadata 存在网络超时，后续可使用更稳定网络或 Colab 验证。
- 后续计划增加 action 分布可视化、多视角图像缺失检查和真实数据集质量报告。
