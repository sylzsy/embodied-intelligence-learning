# Embodied Intelligence Learning

具身智能数据工程与仿真数据管线学习项目。

本仓库用于记录我从数据产品 / 数据工程背景切入具身智能方向的学习过程，重点关注机器人公开数据集、数据质量评估、仿真数据管线和模仿学习方法。

## 目标方向

- 具身智能数据工程师
- 仿真数据管线工程师
- 机器人数据产品 / 系统工程方向

## 当前进度

| 模块 | 当前状态 | 产出 |
| --- | --- | --- |
| 数据集调研 | 已启动 | [Open X-Embodiment 初探](datasets/oxe-overview.md) / [BridgeData V2 字段结构](datasets/bridge-v2-field-schema.md) |
| 论文阅读 | 已启动 | [RT-2 论文笔记](papers/rt-2-notes.md) |
| 学习日志 | 已启动 | [daily-log](notes/daily-log.md) |
| 数据质量检测 | 已形成阶段成果 | [质量检查脚本](scripts/check_dataset_quality.py) / [BridgeData V2 项目报告](reports/bridge-data-quality-project-report.md) |
| 仿真实践 | 待开始 | 计划完成 ROS2 / Isaac Sim 基础 demo |

## 阶段成果：BridgeData V2 数据质量检查

当前已完成一个可展示的数据工程闭环：

```text
BridgeData V2 schema 调研
-> BridgeData-style mock episode 构造
-> 统一 JSONL 格式转换
-> schema 和质量阈值检查
-> Markdown / JSON 报告输出
```

核心产出：

- [BridgeData V2 字段结构笔记](datasets/bridge-v2-field-schema.md)
- [BridgeData V2 数据质量检查项目报告](reports/bridge-data-quality-project-report.md)
- [简历项目描述](reports/resume-project-brief.md)
- [数据质量检查脚本](scripts/check_dataset_quality.py)

当前脚本支持字段完整性、action/state 维度、图像尺寸、timestamp 递增、轨迹长度阈值、action 极端值和缺失率统计。

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

## 近期计划

1. 选择 Open X-Embodiment / BridgeData V2 的小规模子集，完成真实数据加载。
2. 编写数据质量检查脚本，覆盖字段缺失、轨迹长度、图像尺寸、动作维度和语言指令质量。
3. 输出第一版数据质量分析报告，形成可放入简历的项目成果。
4. 继续阅读 RT-1、RT-2、Diffusion Policy、ACT、OpenVLA 等论文，并补充工程落地视角。

## 简历表达目标

最终希望该仓库能够支撑以下简历表述：

> 围绕具身智能公开数据集搭建数据分析与质量检测流程，完成 Open X-Embodiment / BridgeData V2 等数据集结构调研，编写数据质量检查脚本并输出分析报告，熟悉机器人学习数据中 observation、action、language instruction、episode / step 等核心字段。
