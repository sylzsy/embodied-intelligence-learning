# 第一阶段成果总结：BridgeData V2 数据质量分析 Pipeline

## 阶段目标

第一阶段目标是从具身智能数据工程视角，理解机器人数据集的核心结构，并做出一条可复现的数据质量分析流程。

当前阶段围绕 BridgeData V2 / BridgeData-style 数据完成了从字段理解、样例转换、质量检查、分布统计、可视化到自动报告生成的闭环。

## 已完成能力

1. 理解机器人 episode / step 数据结构。
2. 理解 observation、action、state、language instruction、timestamp 等核心字段。
3. 将 BridgeData V2 的 `image_0`、`state`、`language_instruction`、`action` 映射到项目统一 JSONL 格式。
4. 编写并增强数据质量检查脚本，覆盖字段缺失、维度不一致、图像尺寸异常、timestamp 异常、轨迹长度异常、action 越界和缺失率统计。
5. 统计 action / state 每一维的 min、max、mean、std。
6. 生成 action / state 分布可视化图表。
7. 使用 dataset profile 管理不同数据集的 schema 规则。
8. 使用一键 pipeline 输出质量 JSON、分布 JSON、图表、manifest 和 Markdown 报告。

## 核心产物

- `scripts/check_dataset_quality.py`：机器人 episode 数据质量检查。
- `scripts/summarize_dataset.py`：action / state 分布统计。
- `scripts/plot_distribution.py`：action / state 分布可视化。
- `scripts/run_quality_pipeline.py`：一键运行质量检查、统计和绘图。
- `scripts/generate_pipeline_report.py`：根据 pipeline manifest 自动生成 Markdown 报告。
- `configs/bridge_v2_profile.json`：BridgeData V2 schema profile。
- `reports/bridge_profile_pipeline/report.md`：自动生成的数据质量分析报告。

## 当前样例结果

使用 `scripts/bridge_mock_episodes.jsonl` 和 `configs/bridge_v2_profile.json` 运行 pipeline 后：

- episodes: 1
- steps: 2
- action_dim: 7
- state_dim: 7
- image_shape: 256 x 256 x 3
- issue_count: 0

这说明当前 BridgeData-style mock episode 符合 profile 中定义的基础 schema。

## 面试表达

> 我做了一个面向具身智能数据集的数据质量分析 pipeline。项目以 BridgeData V2 的 episode-step 结构为基础，先整理 schema，再把 action、state、language instruction 和 image 字段映射到统一 JSONL 格式。随后我实现了质量检查脚本，能检查字段缺失、action/state 维度、图像尺寸、timestamp 递增、轨迹长度和 action 越界等问题，并进一步统计 action/state 每一维的分布，生成可视化图表。最后我把数据集 schema 抽象成 profile，并用一键 pipeline 自动输出 JSON、图表、manifest 和 Markdown 报告，保证分析流程可复现、可切换数据集。

## 后续方向

第二阶段建议进入仿真与数据管线方向：

1. 跑通一个轻量仿真或机器人控制 demo。
2. 对比仿真数据和真实机器人数据字段差异。
3. 设计仿真数据采集后的质量检查流程。
4. 将当前质量 pipeline 扩展到真实 BridgeData V2 小样本或其他 Open X-Embodiment 子集。
