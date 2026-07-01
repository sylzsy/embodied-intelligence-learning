# Day 2：理解 BridgeData V2 字段结构

## 目标

Day 2 的目标不是完整下载 BridgeData V2，而是理解真实公开机器人数据集的字段结构，并跑通一个 BridgeData-style 样例到项目统一 JSONL 格式的转换流程。

完成后，你应该能解释：

- 为什么不直接下载完整 BridgeData V2。
- BridgeData V2 在 TFDS 里的名字是什么。
- BridgeData V2 的 `action`、`state`、`image` 字段大概长什么样。
- 为什么要把真实数据集字段转换成统一的 episode JSONL 格式。

## 第一步：确认数据集基本信息

BridgeData V2 在 TensorFlow Datasets 中的名字是：

```text
bridge
```

需要记住的字段信息：

| 字段 | 含义 |
| --- | --- |
| `episode_metadata` | episode 的元信息，例如数据来源路径 |
| `steps/action` | 机器人动作，BridgeData V2 中通常是 7 维 |
| `steps/language_instruction` | 当前 episode 或 step 对应的语言任务指令 |
| `steps/observation/image_0` | 主视角 RGB 图像，通常是 256 x 256 x 3 |
| `steps/observation/state` | 机器人状态，通常是 7 维 |

完整 BridgeData V2 约 387GB，不适合第一天直接完整下载。因此 Day 2 先做字段结构理解和小样本转换。

面试表达：

> 我没有一开始完整下载 BridgeData V2，因为完整数据约 387GB。我的做法是先查清楚 TFDS 中 `bridge` 的字段结构，再用小样本验证字段转换和质量检查流程，避免被大数据下载和环境配置卡住。

## 第二步：检查本地环境

执行：

```powershell
python -c "import importlib.util; print('tensorflow_datasets', importlib.util.find_spec('tensorflow_datasets') is not None); print('tensorflow', importlib.util.find_spec('tensorflow') is not None)"
```

如果输出是：

```text
tensorflow_datasets False
tensorflow False
```

说明当前环境还不能直接加载 TFDS 数据。这个结果是正常的，尤其 Python 3.13 环境下 TensorFlow 兼容性可能需要单独处理。

面试表达：

> 我先检查了本地环境，发现当前 Python 环境没有安装 TensorFlow 和 TensorFlow Datasets。因此我没有强行下载真实数据，而是先写了一个 BridgeData-style 的小样本转换脚本，验证字段映射逻辑。

## 第三步：运行 BridgeData-style 转换脚本

执行：

```powershell
python scripts\bridge_sample_to_jsonl.py --output scripts\bridge_mock_episodes.jsonl
```

你应该看到脚本输出一个 episode，结构类似：

```text
episode_id
source_dataset
steps
  observation
    image
    state
    language_instruction
  action
  timestamp
```

这个脚本做的事情是：

| BridgeData-style 字段 | 项目统一字段 |
| --- | --- |
| `episode_metadata.episode_id` | `episode_id` |
| `steps.observation.image_0` | `steps.observation.image` |
| `steps.observation.state` | `steps.observation.state` |
| `steps.language_instruction` | `steps.observation.language_instruction` |
| `steps.action` | `steps.action` |
| `steps.timestamp` | `steps.timestamp` |

面试表达：

> BridgeData V2 原始字段和我的质量检查脚本字段不完全一样，所以我先做字段映射，把 `image_0` 映射成统一的 `image`，把 step 级别的 `language_instruction` 放到 `observation` 里。这样后续不同数据集都可以转换成统一格式，再复用同一套质量检查脚本。

## 第四步：复用 Day 1 质量检查脚本

执行：

```powershell
python scripts\check_dataset_quality.py --input scripts\bridge_mock_episodes.jsonl
```

你应该看到：

- `episodes` 为 1
- `steps` 为 2
- `action_dimensions` 中 7 维 action 出现 2 次
- `image_shapes` 中 256 x 256 x 3 出现 2 次
- `issue_count` 为 0

面试表达：

> Day 2 我验证了 Day 1 写的数据质量检查脚本可以复用到 BridgeData-style 数据上。只要先做字段转换，后续就能统一检查 action 维度、image shape、语言指令、state 和 timestamp。

## 第五步：今天完成标准

- 知道 BridgeData V2 在 TFDS 里叫 `bridge`。
- 知道完整数据约 387GB，所以先做小样本。
- 知道 BridgeData V2 的 action 和 state 通常是 7 维。
- 知道主图像字段是 `image_0`，尺寸通常是 256 x 256 x 3。
- 能运行 `bridge_sample_to_jsonl.py`。
- 能用 Day 1 的 `check_dataset_quality.py` 检查转换后的样例数据。
