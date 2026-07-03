# Day 9：数据集 Profile 配置化

## 目标

Day 9 将 Day 8 的 pipeline 从“命令行手写参数”升级为“数据集 profile 配置”。

这样后续切换数据集时，只需要新增配置文件，不需要改 pipeline 代码。

## 第一步：查看 BridgeData V2 profile

执行：

```powershell
Get-Content configs\bridge_v2_profile.json
```

重点字段：

```text
expected_action_dim: 7
expected_state_dim: 7
expected_image_shape: 256x256x3
min_trajectory_length: 2
max_trajectory_length: 200
action_abs_limit: 1.0
```

## 第二步：使用 profile 运行 pipeline

执行：

```powershell
python scripts\run_quality_pipeline.py --input scripts\bridge_mock_episodes.jsonl --profile configs\bridge_v2_profile.json --output-dir reports\bridge_profile_pipeline
```

## 第三步：检查 manifest

执行：

```powershell
Get-Content reports\bridge_profile_pipeline\manifest.json
```

你应该能看到：

- `profile_path`
- `profile`
- `quality_summary`
- `distribution_summary`
- `plots`

## 面试表达

> Day 9 我把 pipeline 参数配置化，新增 BridgeData V2 profile。这样 action/state 维度、图像尺寸、轨迹长度阈值和 action 数值阈值都写在配置文件里。后续如果接入新的机器人数据集，只需要新增 profile，不需要改 pipeline 主逻辑。

## 今天完成标准

- 能解释 profile 文件解决什么问题。
- 能运行带 `--profile` 的 pipeline。
- 能打开 `manifest.json`，说明其中记录了输入、profile 和输出产物。
- 能说明配置化为什么比硬编码更适合数据工程项目。
