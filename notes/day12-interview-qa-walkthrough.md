# Day 12：整理面试问答

## 目标

Day 12 的目标是把第一阶段项目转化成可面试表达的内容，包括：

- 60 秒项目介绍。
- 高频面试问题。
- 简历 bullet。
- 追问回答模板。

## 核心产物

新增：

```text
reports/project-interview-qa.md
```

这份文档围绕 BridgeData V2 数据质量 pipeline，整理了项目背景、技术细节、工程价值、当前不足和下一步计划。

## 必会问题

1. 这个项目解决什么问题？
2. 为什么不直接训练模型？
3. BridgeData V2 的核心字段是什么？
4. 为什么要做统一 JSONL 格式？
5. `issue_types` 和 `quality_rates` 有什么区别？
6. 为什么要检查 action 越界？
7. 为什么要看 action/state 的 mean 和 std？
8. profile 和 manifest 分别有什么作用？
9. 当前项目不足是什么？
10. 下一步怎么扩展到真实数据和仿真数据？

## 60 秒表达

> 这个项目是我面向具身智能数据工程方向做的第一阶段实践。目标不是直接训练机器人模型，而是先解决训练前的数据质量问题。我以 BridgeData V2 / Open X-Embodiment 风格数据为对象，整理 episode-step 结构，理解 image、state、language instruction、action 和 timestamp。然后我把 BridgeData-style 字段映射到统一 JSONL 格式，并实现质量检查、action/state 分布统计、可视化图表和自动 Markdown 报告。最后通过 dataset profile 和 manifest，让 pipeline 可以复现、可追踪，也方便后续切换到其他机器人数据集。

## 今天完成标准

- 能用 60 秒讲清项目。
- 能解释 profile、manifest、issue_types、quality_rates。
- 能说明为什么数据质量会影响机器人模型训练。
- 能说出下一阶段要接入真实数据和仿真数据管线。
