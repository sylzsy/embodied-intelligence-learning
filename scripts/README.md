# Scripts

数据加载、数据质量检查和统计分析脚本目录。

计划优先实现：

- `load_rlds_sample.py`: 加载公开机器人数据集小样本。
- `check_dataset_quality.py`: 检查字段缺失、轨迹长度异常、图像尺寸异常、动作维度异常等问题。
- `summarize_dataset.py`: 输出数据集统计摘要，供报告和 README 使用。

脚本应尽量支持命令行参数，方便复现实验结果。
