# BridgeData V2 字段结构笔记

## 数据集定位

BridgeData V2 是面向机器人学习的大规模操作数据集，主要用于模仿学习、离线强化学习、语言条件策略学习和开放词表多任务机器人学习。

在 TensorFlow Datasets 中，BridgeData V2 的数据集名称是：

```text
bridge
```

## 为什么先看 schema

完整 BridgeData V2 体量很大，不适合学习初期直接完整下载。数据工程上更稳妥的做法是：

1. 先确认数据集名称和字段结构。
2. 再判断需要哪些 split 和样本。
3. 最后再设计下载、转换、质检和报告流程。

## 官方字段结构

根据 TensorFlow Datasets 的 `bridge` 数据集文档，核心结构可以理解为：

```text
episode
├── episode_metadata
└── steps
    ├── action
    ├── discount
    ├── is_first
    ├── is_last
    ├── is_terminal
    ├── language_embedding
    ├── language_instruction
    ├── observation
    │   ├── image_0
    │   ├── image_1
    │   ├── image_2
    │   ├── image_3
    │   └── state
    └── reward
```

## 关键字段表

| 字段 | 类型 / 形状 | 工程含义 |
| --- | --- | --- |
| `episode_metadata/episode_id` | int32 | episode 编号 |
| `episode_metadata/file_path` | string | 原始数据路径 |
| `episode_metadata/has_image_0` | bool | 是否存在主视角图像 |
| `episode_metadata/has_image_1` | bool | 是否存在第 2 路图像 |
| `episode_metadata/has_image_2` | bool | 是否存在第 3 路图像 |
| `episode_metadata/has_image_3` | bool | 是否存在第 4 路图像 |
| `episode_metadata/has_language` | bool | 是否存在语言指令 |
| `steps/action` | float32, `(7,)` | 机器人动作向量 |
| `steps/language_instruction` | string | 自然语言任务指令 |
| `steps/language_embedding` | float32, `(512,)` | 语言指令 embedding |
| `steps/observation/image_0` | uint8, `(256, 256, 3)` | 主视角 RGB 图像 |
| `steps/observation/image_1` | uint8, `(256, 256, 3)` | 辅助视角 RGB 图像 |
| `steps/observation/image_2` | uint8, `(256, 256, 3)` | 辅助视角 RGB 图像 |
| `steps/observation/image_3` | uint8, `(256, 256, 3)` | 辅助视角 RGB 图像 |
| `steps/observation/state` | float32, `(7,)` | 机器人状态向量 |
| `steps/is_first` | bool | 是否为 episode 第一个 step |
| `steps/is_last` | bool | 是否为 episode 最后一个 step |
| `steps/is_terminal` | bool | 是否为终止状态 |
| `steps/reward` | float32 | 奖励 |
| `steps/discount` | float32 | 折扣因子 |

## 和本项目统一 JSONL 格式的映射

| BridgeData V2 字段 | 本项目统一字段 | 说明 |
| --- | --- | --- |
| `episode_metadata/episode_id` | `episode_id` | 保留 episode 标识 |
| `steps/observation/image_0` | `steps/observation/image` | 先使用主视角图像 |
| `steps/observation/state` | `steps/observation/state` | 保留机器人状态 |
| `steps/language_instruction` | `steps/observation/language_instruction` | 放入 observation，方便统一质检 |
| `steps/action` | `steps/action` | 保留动作向量 |
| `steps/is_first/is_last/is_terminal` | 暂不进入统一格式 | 后续可用于轨迹切分和时序检查 |

## 数据质量检查关注点

BridgeData V2 进入质量检查流程时，优先关注：

- `action` 是否始终为 7 维。
- `state` 是否始终为 7 维。
- `image_0` 是否存在，尺寸是否为 256 x 256 x 3。
- `language_instruction` 是否为空。
- `has_language` 和 `language_instruction` 是否一致。
- `is_first` / `is_last` 是否能正确标记 episode 边界。
- 多视角图像 `image_1~image_3` 是否存在缺失或视角不一致。

## 面试表达

> 我先没有直接下载完整 BridgeData V2，而是先整理官方 TFDS schema。BridgeData V2 的核心是 episode-step 结构，每个 step 包含 7 维 action、7 维 state、最多 4 路 256x256 RGB 图像，以及语言指令和语言 embedding。基于这个 schema，我把主视角 `image_0`、`state`、`language_instruction` 和 `action` 映射到项目统一 JSONL 格式，后续可以复用同一套数据质量检查脚本。

## 参考

- TensorFlow Datasets `bridge` catalog: https://www.tensorflow.org/datasets/catalog/bridge
- TensorFlow Datasets GitHub catalog markdown: https://github.com/tensorflow/datasets/blob/master/docs/catalog/bridge.md
- BridgeData V2 project page: https://rail-berkeley.github.io/bridgedata/
