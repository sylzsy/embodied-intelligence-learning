# Scripts

数据加载、数据质量检查和统计分析脚本目录。

## 已实现

### `check_dataset_quality.py`

检查小规模机器人 episode 数据的基础质量问题，支持 JSON / JSONL 输入。

当前覆盖：

- episode / step 结构是否存在
- observation 是否缺失
- image 尺寸字段是否合法
- state 是否为空
- action 是否为空，并统计 action 维度
- action 维度是否一致
- language_instruction 是否为空
- timestamp 是否递增
- image shape 是否一致
- trajectory length 统计

运行示例：

```bash
python scripts/check_dataset_quality.py --input scripts/sample_robot_episodes.jsonl
```

保存结果：

```bash
python scripts/check_dataset_quality.py --input scripts/sample_robot_episodes.jsonl --output reports/sample_quality_summary.json
```

## 计划优先实现

- `load_rlds_sample.py`: 加载公开机器人数据集小样本。
- `summarize_dataset.py`: 输出数据集统计摘要，供报告和 README 使用。

脚本应尽量支持命令行参数，方便复现实验结果。
