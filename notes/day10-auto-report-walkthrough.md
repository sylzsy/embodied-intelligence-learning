# Day 10：自动生成 Pipeline Markdown 报告

## 目标

Day 10 将 pipeline 的 JSON 和图表产物自动整合成 Markdown 报告。

Day 8 pipeline 已经能生成：

- `quality_summary.json`
- `distribution_summary.json`
- action/state 分布图
- `manifest.json`

Day 10 新增：

- `report.md`

## 第一步：运行 pipeline

执行：

```powershell
python scripts\run_quality_pipeline.py --input scripts\bridge_mock_episodes.jsonl --profile configs\bridge_v2_profile.json --output-dir reports\bridge_profile_pipeline
```

## 第二步：打开报告

执行：

```powershell
Get-Content reports\bridge_profile_pipeline\report.md
```

或者直接在文件夹中打开：

```text
reports/bridge_profile_pipeline/report.md
```

## 第三步：理解报告内容

自动报告包含：

- 输入数据
- 使用的 profile
- episode / step 数量
- issue count
- expected schema
- issue types
- quality rates
- action/state 每一维统计表
- action/state 分布图

## 面试表达

> Day 10 我把 pipeline 产物自动整合成 Markdown 报告。这样质量检查结果、分布统计和可视化图表都能自动汇总到 `report.md`，不需要手动复制粘贴。这个步骤让项目从“能跑脚本”进一步变成“能自动生成数据质量分析交付物”。

## 今天完成标准

- 能运行 pipeline 并生成 `report.md`。
- 能解释 `report.md` 是从 `manifest.json`、质量检查 JSON、分布统计 JSON 和图表自动生成的。
- 能说明自动报告比手写报告更可复现。
