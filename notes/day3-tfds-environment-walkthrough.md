# Day 3：搭建 TFDS/RLDS 环境

## 目标

Day 3 的目标是搭建一个干净的 TensorFlow Datasets 环境，为后续读取 BridgeData V2 / RLDS 数据做准备。

今天不下载完整 BridgeData V2。完整数据约 387GB，直接下载不适合学习初期。今天只做：

- 创建独立 conda 环境。
- 安装 TensorFlow 和 TensorFlow Datasets。
- 验证版本。
- 尝试读取 TFDS builder metadata。

## 第一步：创建独立环境

不要污染 `base` 环境。当前 `base` 是 Python 3.13，不适合作为 TensorFlow 主环境。

执行：

```powershell
conda create -n ei-tfds python=3.11 -y
conda activate ei-tfds
python --version
```

期望结果：

```text
Python 3.11.x
```

本次实际结果：

```text
Python 3.11.15
```

## 第二步：安装依赖

在 `(ei-tfds)` 环境中执行：

```powershell
pip install tensorflow-datasets tensorflow
```

验证：

```powershell
python -c "import tensorflow as tf; import tensorflow_datasets as tfds; print('tensorflow', tf.__version__); print('tensorflow_datasets', tfds.__version__)"
```

本次实际结果：

```text
tensorflow 2.21.0
tensorflow_datasets 4.9.10
```

如果看到 oneDNN 相关 warning，不是报错。它只是说明 TensorFlow 启用了 CPU 计算优化，不影响数据加载。

## 第三步：读取 TFDS builder 信息

执行：

```powershell
python scripts\inspect_tfds_builder.py --dataset bridge
```

这个脚本只读取 TFDS builder metadata，不应该完整下载 387GB 数据。

你需要重点观察：

- `name`
- `full_name`
- `version`
- `features`
- `splits`
- `download_size`
- `dataset_size`

面试表达：

> 我没有直接下载完整 BridgeData V2，而是先用 TFDS builder 读取 metadata，确认数据集名称、版本、split 和 feature 结构。这是数据工程里比较稳妥的做法：先确认 schema 和规模，再决定是否下载样本。

## 第四步：如果 `bridge` metadata 读取超时

本次在本地执行：

```powershell
conda run -n ei-tfds python scripts\inspect_tfds_builder.py --dataset bridge
```

出现了超时。这说明当前环境中 TensorFlow / TFDS 已安装成功，但读取 `bridge` 相关远程 metadata 受网络或 TFDS catalog 初始化影响。

为了确认脚本本身可用，可以先用小数据集验证：

```powershell
conda run -n ei-tfds python scripts\inspect_tfds_builder.py --dataset mnist
```

本次 `mnist` 能成功输出：

```text
name: mnist
full_name: mnist/3.0.1
features: image, label
```

工程判断：

- 环境安装成功。
- `inspect_tfds_builder.py` 脚本可用。
- `bridge` metadata 读取卡在网络 / TFDS 远程初始化，不是 Python 环境问题。
- 后续可以换更稳定网络，或使用 Google Colab 尝试读取 `bridge` metadata。

## 今天完成标准

- 能解释为什么不用 Python 3.13 的 base 环境。
- 能创建并激活 `ei-tfds` 环境。
- 能验证 TensorFlow 和 TFDS 版本。
- 能解释 oneDNN warning 不是报错。
- 能运行 `inspect_tfds_builder.py` 查看 TFDS metadata。
- 能说明本地读取 `bridge` metadata 超时的原因和下一步处理方案。
