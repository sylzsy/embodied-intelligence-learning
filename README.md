# Embodied Intelligence Data Quality Pipeline

面向 BridgeData V2 / Open X-Embodiment 风格机器人数据的质量分析与报告生成项目。

本仓库记录我从数据产品 / 数据工程背景切入具身智能方向的第一阶段实践，重点是理解机器人训练数据结构，并搭建一条可复现的数据质量分析 pipeline。

## 项目定位

机器人模仿学习和 VLA 模型训练依赖高质量 episode 数据。一个 episode 通常由多个 step 组成，每个 step 包含图像 observation、机器人 state、语言指令、action 和时间信息。

本项目不直接训练模型，而是先解决训练前的数据工程问题：

- 机器人数据字段是否完整。
- action / state 维度是否符合 schema。
- 图像尺寸是否一致。
- timestamp 是否递增。
- 轨迹长度和 action 数值是否异常。
- action / state 每一维分布是否可解释。
- 分析结果是否能自动生成报告并复现。

## 当前进度

| 模块 | 当前状态 | 产出 |
| --- | --- | --- |
| 数据集调研 | 已启动 | [Open X-Embodiment 初探](datasets/oxe-overview.md) / [BridgeData V2 字段结构](datasets/bridge-v2-field-schema.md) |
| 论文阅读 | 已启动 | [RT-2 论文笔记](papers/rt-2-notes.md) |
| 学习日志 | 已启动 | [daily-log](notes/daily-log.md) |
| 数据质量检测 | 第一阶段完成 | [质量检查脚本](scripts/check_dataset_quality.py) / [自动 Pipeline 报告](reports/bridge_profile_pipeline/report.md) / [第一阶段总结](reports/stage1-bridge-data-quality-summary.md) |
| 仿真实践 | 待开始 | 计划完成 ROS2 / Isaac Sim 基础 demo |

## Pipeline 流程

当前已完成一个可展示的数据工程闭环：

```text
BridgeData V2 schema 调研
-> BridgeData-style mock episode 构造
-> 统一 JSONL 格式转换
-> schema 和质量阈值检查
-> action/state 分布统计与可视化
-> profile 配置化
-> 一键 pipeline 自动生成 Markdown / JSON / 图表报告
```

## 快速运行

命令行 pipeline：

```powershell
python scripts\run_quality_pipeline.py --input scripts\bridge_mock_episodes.jsonl --profile configs\bridge_v2_profile.json --output-dir reports\bridge_profile_pipeline
```

运行后会生成：

- `reports/bridge_profile_pipeline/quality_summary.json`
- `reports/bridge_profile_pipeline/distribution_summary.json`
- `reports/bridge_profile_pipeline/plots/*.png`
- `reports/bridge_profile_pipeline/manifest.json`
- `reports/bridge_profile_pipeline/report.md`

Streamlit 页面：

```powershell
streamlit run app.py
```

页面支持上传 JSON / JSONL episode 文件，选择 dataset profile，并展示质量检查结果、action/state 分布图和自动生成的 Markdown 报告。

## 项目结果

当前 BridgeData-style mock episode 的检查结果：

| 指标 | 结果 |
| --- | --- |
| episodes | 1 |
| steps | 2 |
| action_dim | 7 |
| state_dim | 7 |
| image_shape | 256 x 256 x 3 |
| issue_count | 0 |

核心产出：

- [BridgeData V2 字段结构笔记](datasets/bridge-v2-field-schema.md)
- [BridgeData V2 数据质量检查项目报告](reports/bridge-data-quality-project-report.md)
- [BridgeData V2 Profile Pipeline 自动报告](reports/bridge_profile_pipeline/report.md)
- [第一阶段成果总结](reports/stage1-bridge-data-quality-summary.md)
- [简历项目描述](reports/resume-project-brief.md)
- [数据质量检查脚本](scripts/check_dataset_quality.py)

当前脚本支持字段完整性、action/state 维度、图像尺寸、timestamp 递增、轨迹长度阈值、action 极端值、缺失率统计、action/state 分布统计、可视化图表和自动 Markdown 报告生成。

## 技术栈

- Python
- JSON / JSONL
- TensorFlow Datasets metadata inspection
- Matplotlib
- Streamlit
- Markdown report generation
- GitHub 项目文档组织

## 仓库结构

```text
.
├── assets/       # 图片、截图、实验可视化结果
├── datasets/     # 机器人公开数据集调研与数据结构分析
├── notes/        # 日常学习日志、问题记录、阶段复盘
├── papers/       # 具身智能论文阅读笔记
├── reports/      # 数据质量分析报告、阶段性总结
└── scripts/      # 数据加载、质量检查、统计分析脚本
```

## 第一阶段结论

第一阶段已经完成“机器人数据集结构理解 + 统一字段映射 + 数据质量检测 + 分布统计与可视化 + 自动报告生成”的闭环。当前项目可以支撑具身智能数据工程、机器人数据集工程、仿真数据管线方向的简历表达。

## 下一阶段计划

1. 将当前 pipeline 迁移到真实 BridgeData V2 / Open X-Embodiment 小样本。
2. 开始第二阶段仿真与数据管线实践，优先跑通一个轻量仿真或机器人控制 demo。
3. 对比仿真数据和真实机器人数据的字段差异。
4. 继续阅读 RT-1、RT-2、Diffusion Policy、ACT、OpenVLA 等论文，并补充工程落地视角。

## 简历表达目标

最终希望该仓库能够支撑以下简历表述：

> 围绕 BridgeData V2 / Open X-Embodiment 风格机器人数据搭建数据质量分析 pipeline，完成 episode-step 数据结构调研、统一字段映射、schema 规则检查、action/state 分布统计、可视化图表和自动 Markdown 报告生成，熟悉具身智能训练数据中 observation、action、state、language instruction 和 timestamp 等核心字段。
