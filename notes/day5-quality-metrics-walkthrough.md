# Day 5：增强数据质量指标

## 目标

Day 5 的目标是把 Day 4 的 schema 检查升级为更完整的数据质量指标。

Day 4 主要检查：

- action 维度是否符合预期
- state 维度是否符合预期
- image shape 是否符合预期

Day 5 增加：

- 轨迹长度阈值
- 缺失率统计
- action 极端值检查
- 更适合写进报告的 `quality_rates`

## 第一步：BridgeData V2 schema + 质量阈值检查

执行：

```powershell
python scripts\check_dataset_quality.py --input scripts\bridge_mock_episodes.jsonl --expected-action-dim 7 --expected-state-dim 7 --expected-image-shape 256x256x3 --min-trajectory-length 2 --max-trajectory-length 200 --action-abs-limit 1.0
```

你应该看到：

```text
issue_count: 0
quality_rates: {}
```

这说明当前 mock episode 满足：

- action 是 7 维
- state 是 7 维
- image 是 256 x 256 x 3
- 轨迹长度在阈值范围内
- action 数值没有超过阈值
- 没有语言、图像、state、action 缺失

## 第二步：用异常样例验证质量指标

执行：

```powershell
python scripts\check_dataset_quality.py --input scripts\sample_robot_episodes.jsonl --min-trajectory-length 3 --max-trajectory-length 3 --action-abs-limit 0.5
```

你会看到脚本识别出：

- `trajectory_too_short`
- `missing_language_instruction`
- `invalid_state`
- `action_value_out_of_range`
- `non_increasing_timestamp`
- `inconsistent_action_dim`
- `inconsistent_image_shape`

并输出类似：

```text
quality_rates:
  missing_language_instruction: count=1, rate=0.2
  missing_or_invalid_state: count=1, rate=0.2
```

## 第三步：理解 `quality_rates`

`issue_types` 用于统计问题类型出现次数。

`quality_rates` 用于把缺失类问题转成比例，方便写报告。例如：

```text
missing_language_instruction rate = 0.2
```

意思是：

> 共有 5 个 step，其中 1 个 step 缺少 language instruction，缺失率为 20%。

## 第四步：面试表达

> Day 5 我把质量检查从单纯的字段维度检查扩展成质量指标检查。除了检查 BridgeData V2 的 action/state/image 是否符合 schema，还增加了轨迹长度阈值、action 极端值检查和缺失率统计。这样输出结果不仅能定位异常样本，还能形成报告里的量化指标，比如语言指令缺失率、state 缺失率和 action 越界数量。

## 今天完成标准

- 能解释 `issue_types` 和 `quality_rates` 的区别。
- 能运行 BridgeData V2 mock 样例的阈值检查。
- 能运行异常样例并看懂 `trajectory_too_short`。
- 能解释为什么 action 极端值需要检查。
- 能把缺失数量转成缺失率写进报告。
