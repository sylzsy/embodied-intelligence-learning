# Day 5 数据质量指标增强报告

## 1. 目标

本报告记录 Day 5 对数据质量检查脚本的增强：在 schema 检查基础上，增加轨迹长度阈值、缺失率统计和 action 极端值检查。

## 2. 新增检查项

| 参数 | 作用 |
| --- | --- |
| `--min-trajectory-length` | 检查 episode 是否过短 |
| `--max-trajectory-length` | 检查 episode 是否过长 |
| `--action-abs-limit` | 检查 action 数值是否超过绝对值阈值 |

新增输出：

| 字段 | 作用 |
| --- | --- |
| `quality_rates` | 按 step 数计算缺失率 |

## 3. BridgeData-style 样例检查

运行命令：

```powershell
python scripts\check_dataset_quality.py --input scripts\bridge_mock_episodes.jsonl --expected-action-dim 7 --expected-state-dim 7 --expected-image-shape 256x256x3 --min-trajectory-length 2 --max-trajectory-length 200 --action-abs-limit 1.0
```

结果：

| 指标 | 结果 |
| --- | --- |
| issue_count | 0 |
| action 维度 | 7 |
| image shape | 256 x 256 x 3 |
| 轨迹长度 | 2 |

结论：BridgeData-style mock episode 符合当前 schema 和质量阈值。

## 4. 异常样例检查

运行命令：

```powershell
python scripts\check_dataset_quality.py --input scripts\sample_robot_episodes.jsonl --min-trajectory-length 3 --max-trajectory-length 3 --action-abs-limit 0.5
```

识别出的问题包括：

- `trajectory_too_short`
- `missing_language_instruction`
- `invalid_state`
- `action_value_out_of_range`
- `non_increasing_timestamp`
- `inconsistent_action_dim`
- `inconsistent_image_shape`

缺失率示例：

| 指标 | 数量 | 比例 |
| --- | --- | --- |
| missing_language_instruction | 1 | 0.2 |
| missing_or_invalid_state | 1 | 0.2 |

## 5. 工程意义

Day 5 后，质量检查脚本不只输出异常列表，还能输出可用于报告的数据质量指标。后续接入真实 BridgeData V2 episode 后，可以用这些指标形成更完整的数据集质量分析报告。
