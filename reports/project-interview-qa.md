# 面试问答手册：BridgeData V2 数据质量 Pipeline

## 60 秒项目介绍

这个项目是我面向具身智能数据工程方向做的第一阶段实践。目标不是直接训练机器人模型，而是先解决训练前的数据质量问题。

我以 BridgeData V2 / Open X-Embodiment 风格数据为对象，先整理 episode-step 结构，理解每个 step 中的 image、state、language instruction、action 和 timestamp。然后我写了转换脚本，把 BridgeData-style 字段映射到统一 JSONL 格式，例如把 `image_0` 映射为统一的 `observation.image`。

在质量检查部分，我实现了 schema 检查和质量指标统计，包括字段缺失、action/state 维度、图像尺寸、timestamp 递增、轨迹长度、action 越界和缺失率。后续又加入 action/state 每一维的分布统计和可视化。最后我把数据集规则抽象成 profile，并用一键 pipeline 自动生成 JSON、图表、manifest 和 Markdown 报告，保证整个分析流程可复现、可切换数据集。

## 高频问题

### 1. 你这个项目解决什么问题？

解决机器人训练数据进入模仿学习或 VLA 训练前的数据质量验证问题。机器人数据不是普通表格数据，它需要保证图像、语言、状态、动作和时间顺序对齐。如果这些字段有缺失或错位，模型会学到错误的状态到动作映射。

### 2. 为什么不直接训练模型？

因为模型训练前最重要的是确认数据可用。action 维度不一致、图像尺寸不一致、timestamp 不递增、语言指令缺失都会影响训练稳定性。先做质量检查，可以减少后续训练失败和调参的不确定性。

### 3. BridgeData V2 的核心字段是什么？

核心是 episode-step 结构。每个 step 里通常包含 `steps/action`、`steps/observation/state`、`steps/observation/image_0`、`steps/language_instruction`，以及 `is_first`、`is_last` 等轨迹边界字段。BridgeData V2 中 action 和 state 常见为 7 维，主视角图像是 256 x 256 x 3。

### 4. 为什么要做统一 JSONL 格式？

不同机器人数据集字段命名不一致。如果每个数据集都单独写质检逻辑，代码很难复用。我把 BridgeData V2 的 `image_0`、`state`、`language_instruction`、`action` 映射到统一字段，后续换数据集时只需要改转换层或 profile，主质检逻辑可以复用。

### 5. `issue_types` 和 `quality_rates` 有什么区别？

`issue_types` 统计每类问题出现了多少次，适合定位异常类型。`quality_rates` 把缺失类问题按 step 总数转成比例，适合写质量报告。例如 5 个 step 中 1 个缺少语言指令，缺失率就是 20%。

### 6. 为什么要检查 action 越界？

action 是机器人执行动作的监督信号。如果 action 数值异常大，可能是单位转换、坐标系转换、归一化或日志解析问题。这类异常会污染训练分布，让模型学到不稳定动作，严重时在仿真或真机执行中可能带来安全风险。

### 7. 为什么要看 action/state 的 mean 和 std？

mean、std 可以帮助判断每个自由度是否正常变化。如果某一维 std 长期为 0，可能说明任务本身没有使用该自由度，也可能说明采集或字段映射有问题。如果某一维 range 异常大，就要排查单位、归一化或异常值。

### 8. profile 的作用是什么？

profile 用来记录具体数据集的 schema 规则，比如 action 维度、state 维度、图像尺寸、轨迹长度阈值、action 数值阈值和字段映射。这样 pipeline 和数据集解耦，后续切换到其他机器人数据集时，只需要新增 profile。

### 9. manifest 的作用是什么？

manifest 记录一次 pipeline 运行的输入、配置和输出产物，包括输入文件、profile、质量检查 JSON、分布统计 JSON、图表路径和 report 路径。它让结果可追踪，也方便自动生成报告。

### 10. 这个项目目前的不足是什么？

目前主要在 BridgeData-style mock episode 上验证，真实 BridgeData V2 小样本还需要在更稳定的网络或 Colab 环境中接入。下一步会把当前 pipeline 迁移到真实 Open X-Embodiment / BridgeData V2 小样本，并和仿真数据采集流程结合。

## 简历 Bullet

- 调研 BridgeData V2 / Open X-Embodiment 机器人数据结构，梳理 episode-step 层级下的 observation、action、state、image、language instruction 和 timestamp 等核心字段。
- 设计统一 JSONL episode 格式，将 BridgeData-style 字段映射到统一 schema，提升跨数据集质量检查流程的复用性。
- 开发机器人数据质量检查脚本，支持字段缺失、action/state 维度、图像尺寸、timestamp 递增、轨迹长度、action 越界和缺失率统计。
- 实现 action/state 每一维 min、max、mean、std 分布统计与可视化，用于发现自由度异常、数值范围异常和字段映射问题。
- 构建基于 dataset profile 的一键 pipeline，自动输出 quality summary、distribution summary、可视化图表、manifest 和 Markdown 数据质量报告。

## 追问回答模板

### 如果被问：你怎么证明脚本真的能抓异常？

我不仅在正常 BridgeData-style mock episode 上跑出了 `issue_count=0`，也用异常样例验证过脚本。异常样例能识别语言指令缺失、state 缺失、timestamp 不递增、action 维度不一致、图像尺寸不一致、轨迹过短和 action 越界等问题，所以它不是只打印统计，而是真的根据 schema 和阈值做质量校验。

### 如果被问：你怎么把数据产品实习经验迁移到这个项目？

我把原来做数据产品时关注的数据口径、字段定义、异常指标和报告交付，迁移到了机器人数据集场景。区别是这里的数据对象从业务表变成 episode-step 轨迹，质量指标从普通缺失值扩展到了 action/state 维度、图像尺寸、时间顺序和机器人动作分布。

### 如果被问：下一步你会怎么做？

我会先接入真实 BridgeData V2 / Open X-Embodiment 小样本，验证当前 pipeline 在真实数据上的适配性。然后进入仿真数据管线，跑通一个轻量仿真 demo，比较仿真数据和真实机器人数据在 observation、action、state 和 episode 边界上的差异。
