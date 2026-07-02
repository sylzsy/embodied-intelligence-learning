# Day 4：BridgeData V2 Metadata 与 Colab 验证路线

## 目标

Day 4 处理 Day 3 的卡点：本地 `ei-tfds` 环境已经可用，但读取 `bridge` metadata 时超时。

今天的目标是：

- 不下载完整 BridgeData V2。
- 根据官方 TFDS 文档整理 `bridge` schema。
- 准备 Google Colab 验证路线。
- 明确本地超时不是环境失败，而是网络 / TFDS 远程 metadata 访问问题。

## 第一步：复盘 Day 3 卡点

本地环境：

```text
conda env: ei-tfds
Python: 3.11.15
tensorflow: 2.21.0
tensorflow_datasets: 4.9.10
```

本地验证结果：

```text
mnist metadata 读取成功
bridge metadata 读取超时
```

工程判断：

- 环境安装成功。
- `inspect_tfds_builder.py` 脚本可用。
- `bridge` 超时更可能是网络或 TFDS 远程 catalog 初始化问题。
- 下一步用 Colab 或更稳定网络验证 `bridge` metadata。

## 第二步：阅读官方 schema 笔记

先打开：

```powershell
Get-Content datasets\bridge-v2-field-schema.md
```

重点记住：

| 字段 | 形状 |
| --- | --- |
| `steps/action` | `(7,)` |
| `steps/observation/state` | `(7,)` |
| `steps/observation/image_0` | `(256, 256, 3)` |
| `steps/language_embedding` | `(512,)` |
| `steps/language_instruction` | string |

面试表达：

> 我在本地 metadata 读取超时后，没有停在报错上，而是先参考官方 TFDS schema 文档整理字段结构。这样即使暂时不能读取真实样本，也能明确后续数据转换和质量检查需要覆盖哪些字段。

## 第三步：Colab 验证代码

在 Google Colab 新建 notebook，执行：

```python
!pip install -q tensorflow-datasets tensorflow
```

然后执行：

```python
import tensorflow_datasets as tfds

builder = tfds.builder("bridge")
info = builder.info

print("name:", info.name)
print("full_name:", info.full_name)
print("version:", info.version)
print("download_size:", info.download_size)
print("dataset_size:", info.dataset_size)
print("features:")
print(info.features)
```

如果这一步成功，说明 Colab 网络能访问 `bridge` metadata。

## 第四步：不要直接下载全量数据

暂时不要执行：

```python
builder.download_and_prepare()
```

原因：

- BridgeData V2 体量很大。
- 下载耗时长。
- 对 Day 4 的目标没有必要。
- 当前只需要 metadata 和字段结构。

面试表达：

> 我明确区分 metadata 验证和数据下载。Day 4 只验证 schema，不执行 `download_and_prepare()`，避免无意义下载全量数据。

## 第五步：如果 Colab 也超时

如果 Colab 执行 `tfds.builder("bridge")` 仍然超时，记录为：

```text
本地和 Colab 均无法稳定读取 bridge metadata，推测是 TFDS 远程访问或数据集 catalog 初始化问题。
```

下一步不阻塞项目，可以继续：

- 使用官方 TFDS schema 文档作为字段依据。
- 完善本项目统一 JSONL schema。
- 增强质量检查脚本。
- 后续再换网络读取真实 episode。

## 第六步：把 schema 转成质量检查规则

根据 BridgeData V2 官方 schema，可以把字段要求变成脚本参数：

```powershell
python scripts\check_dataset_quality.py --input scripts\bridge_mock_episodes.jsonl --expected-action-dim 7 --expected-state-dim 7 --expected-image-shape 256x256x3
```

这条命令表达的是：

- `action` 必须是 7 维。
- `state` 必须是 7 维。
- 主图像必须是 256 x 256 x 3。

面试表达：

> 我把官方 schema 转成了可执行的数据质量规则，而不是只停留在文档理解。例如 BridgeData V2 要求 action 和 state 都是 7 维、主视角图像是 256x256x3，所以我在质检脚本里增加了 expected schema 参数，用来检查数据是否符合预期格式。

## 今天完成标准

- 能解释 Day 3 为什么卡在 `bridge` metadata。
- 能打开并理解 `datasets/bridge-v2-field-schema.md`。
- 能说出 BridgeData V2 的 5 个核心字段：`action`、`state`、`image_0`、`language_instruction`、`language_embedding`。
- 知道 Colab 只验证 metadata，不下载全量数据。
- 能解释为什么暂时不执行 `download_and_prepare()`。
- 能把 BridgeData V2 schema 转成质检命令。
