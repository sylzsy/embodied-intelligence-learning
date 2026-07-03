# BridgeData V2 数据质量检查项目报告

## 1. 项目背景

具身智能模型训练依赖高质量机器人数据。和普通业务数据不同，机器人数据通常是 episode-step 层级结构，每个 step 中需要对齐图像、机器人状态、语言指令、动作和时间信息。

本项目围绕 BridgeData V2 / BridgeData-style 数据，搭建了一个轻量的数据质量检查流程，目标是验证：

- 是否能理解公开机器人数据集的字段结构。
- 是否能把不同数据源转换成统一 JSONL episode 格式。
- 是否能将官方 schema 转成可执行的质量检查规则。
- 是否能输出可用于简历和面试的数据质量分析报告。

## 2. 数据结构理解

BridgeData V2 在 TensorFlow Datasets 中的数据集名为：

```text
bridge
```

根据官方 schema，核心字段包括：

| 字段 | 形状 / 类型 | 说明 |
| --- | --- | --- |
| `steps/action` | `(7,)` | 机器人动作向量 |
| `steps/observation/state` | `(7,)` | 机器人状态向量 |
| `steps/observation/image_0` | `(256, 256, 3)` | 主视角 RGB 图像 |
| `steps/language_instruction` | string | 自然语言任务指令 |
| `steps/language_embedding` | `(512,)` | 语言 embedding |

本项目将 BridgeData V2 原始字段映射到统一格式：

| 原始字段 | 统一字段 |
| --- | --- |
| `episode_metadata/episode_id` | `episode_id` |
| `steps/observation/image_0` | `steps/observation/image` |
| `steps/observation/state` | `steps/observation/state` |
| `steps/language_instruction` | `steps/observation/language_instruction` |
| `steps/action` | `steps/action` |

## 3. 工程流程

项目流程如下：

```text
官方 schema 调研
-> BridgeData-style mock episode 构造
-> 统一 JSONL 格式转换
-> schema 规则检查
-> 质量指标统计
-> Markdown / JSON 报告输出
```

核心脚本：

| 脚本 | 作用 |
| --- | --- |
| `scripts/bridge_sample_to_jsonl.py` | 构造 BridgeData-style 样例并转换成统一 JSONL |
| `scripts/check_dataset_quality.py` | 检查字段完整性、schema 一致性和质量指标 |
| `scripts/inspect_tfds_builder.py` | 读取 TFDS builder metadata |

## 4. 质量检查规则

当前质检脚本支持：

| 检查项 | 说明 |
| --- | --- |
| 字段完整性 | 检查 observation、image、state、action、language instruction 是否存在 |
| action 维度 | 检查 action 是否符合期望维度 |
| state 维度 | 检查 state 是否符合期望维度 |
| image shape | 检查图像尺寸是否符合期望 |
| timestamp | 检查时间戳是否递增 |
| 轨迹长度 | 检查 episode 是否过短或过长 |
| action 极端值 | 检查 action 数值是否超过阈值 |
| 缺失率 | 输出语言指令、state、image、action 等缺失率 |

BridgeData V2 mock 样例使用的规则：

```powershell
python scripts\check_dataset_quality.py --input scripts\bridge_mock_episodes.jsonl --expected-action-dim 7 --expected-state-dim 7 --expected-image-shape 256x256x3 --min-trajectory-length 2 --max-trajectory-length 200 --action-abs-limit 1.0
```

## 5. 检查结果

BridgeData-style mock episode 检查结果：

| 指标 | 结果 |
| --- | --- |
| episode 数量 | 1 |
| step 数量 | 2 |
| action 维度 | 7 维，出现 2 次 |
| image shape | 256 x 256 x 3，出现 2 次 |
| language instruction 数量 | 1 |
| issue_count | 0 |
| quality_rates | 无缺失项 |

异常样例检查中，脚本可以识别：

- `trajectory_too_short`
- `missing_language_instruction`
- `invalid_state`
- `action_value_out_of_range`
- `non_increasing_timestamp`
- `inconsistent_action_dim`
- `inconsistent_image_shape`

## 6. 项目价值

该项目证明了一个具身智能数据工程流程的最小闭环：

- 能读懂机器人公开数据集 schema。
- 能将原始字段映射到统一训练数据格式。
- 能把官方 schema 转成可执行质检规则。
- 能输出异常类型、异常位置和缺失率等质量指标。
- 能形成面向模型训练前数据准备的数据质量报告。

## 7. 当前限制

- 当前 BridgeData V2 使用 mock episode 验证流程，尚未下载真实大规模数据。
- 本地读取 `bridge` metadata 时存在超时，推测与网络或 TFDS 远程 catalog 初始化有关。
- 后续需要在稳定网络或 Colab 环境中读取真实 episode，并复用当前质检流程。

## 8. 下一步

1. 继续尝试读取真实 BridgeData V2 metadata。
2. 接入真实小样本 episode。
3. 增加多视角图像缺失检查。
4. 增加 action 分布统计和可视化。
5. 将报告扩展为真实公开数据集质量分析报告。
