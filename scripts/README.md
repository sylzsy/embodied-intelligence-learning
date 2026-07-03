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

按 BridgeData V2 官方 schema 检查：

```bash
python scripts/check_dataset_quality.py --input scripts/bridge_mock_episodes.jsonl --expected-action-dim 7 --expected-state-dim 7 --expected-image-shape 256x256x3
```

按 schema 和质量阈值检查：

```bash
python scripts/check_dataset_quality.py --input scripts/bridge_mock_episodes.jsonl --expected-action-dim 7 --expected-state-dim 7 --expected-image-shape 256x256x3 --min-trajectory-length 2 --max-trajectory-length 200 --action-abs-limit 1.0
```

### `bridge_sample_to_jsonl.py`

将一个 BridgeData-style 小样本转换为本项目统一的 JSONL episode 格式。该脚本不下载完整 BridgeData V2，只用于验证字段映射逻辑。

运行示例：

```bash
python scripts/bridge_sample_to_jsonl.py --output scripts/bridge_mock_episodes.jsonl
python scripts/check_dataset_quality.py --input scripts/bridge_mock_episodes.jsonl
```

### `inspect_tfds_builder.py`

读取 TFDS dataset builder 的 metadata，用于在不下载完整数据集的情况下确认数据集名称、版本、features 和 splits。

运行示例：

```bash
python scripts/inspect_tfds_builder.py --dataset bridge
```

### `summarize_dataset.py`

统计机器人 episode 数据中 action / state 每一维的 min、max、mean 和 std，用于发现分布异常。

运行示例：

```bash
python scripts/summarize_dataset.py --input scripts/bridge_mock_episodes.jsonl --output reports/bridge_mock_distribution_summary.json
```

### `plot_distribution.py`

将 action / state 分布统计结果绘制为 PNG 图表。

运行示例：

```bash
python scripts/plot_distribution.py --input reports/bridge_mock_distribution_summary.json --output-dir assets/distributions
```

## 计划优先实现

- `load_rlds_sample.py`: 加载公开机器人数据集小样本。
- `summarize_dataset.py`: 输出数据集统计摘要，供报告和 README 使用。

脚本应尽量支持命令行参数，方便复现实验结果。
