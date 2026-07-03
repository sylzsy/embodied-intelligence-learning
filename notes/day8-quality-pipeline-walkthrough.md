# Day 8：一键数据质量分析 Pipeline

## 目标

Day 8 将前面分散的脚本整合成一个可复现 pipeline。

输入：

```text
episode JSONL
```

输出：

```text
quality_summary.json
distribution_summary.json
action/state 分布图
manifest.json
```

## 第一步：运行 pipeline

执行：

```powershell
python scripts\run_quality_pipeline.py --input scripts\bridge_mock_episodes.jsonl --output-dir reports\bridge_mock_pipeline
```

## 第二步：检查输出文件

执行：

```powershell
dir reports\bridge_mock_pipeline
dir reports\bridge_mock_pipeline\plots
```

你应该看到：

```text
quality_summary.json
distribution_summary.json
manifest.json
plots/action_range.png
plots/action_std.png
plots/state_range.png
plots/state_std.png
```

## 第三步：理解 pipeline 价值

这个 pipeline 串起了：

```text
质量规则检查
-> action/state 分布统计
-> 分布图生成
-> manifest 记录输出路径
```

面试表达：

> Day 8 我把前面分散的数据质量检查、分布统计和图表生成整合成一键 pipeline。这样只需要输入一个 episode JSONL，就能自动生成质量检查 JSON、action/state 分布统计、可视化图表和 manifest 文件。这个结构更接近真实数据工程里的可复现分析流程。

## 今天完成标准

- 能运行 `run_quality_pipeline.py`。
- 能解释 pipeline 的输入和输出。
- 能说明为什么 pipeline 比手动跑多个脚本更适合工程复现。
- 能打开 `manifest.json` 并说明它记录了哪些产物。
