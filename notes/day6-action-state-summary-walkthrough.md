# Day 6：Action / State 分布统计

## 目标

Day 6 的目标是从“规则检查”推进到“分布分析”。

Day 1-5 已经能回答：

- 字段是否缺失
- action/state 维度是否符合 schema
- 图像尺寸是否正确
- timestamp 是否递增
- 缺失率是多少

Day 6 增加：

- action 每一维的 min / max / mean / std
- state 每一维的 min / max / mean / std
- 判断动作和状态分布是否存在明显异常

## 第一步：运行分布统计脚本

执行：

```powershell
python scripts\summarize_dataset.py --input scripts\bridge_mock_episodes.jsonl --output reports\bridge_mock_distribution_summary.json
```

你应该看到：

```text
action_summary
state_summary
per_dim
min / max / mean / std
```

## 第二步：理解 action 分布

BridgeData V2 的 action 是 7 维。每一维通常对应机器人末端位姿变化、旋转变化或夹爪控制等动作信息。

分布统计的意义：

- `min` / `max`：看某一维是否出现极端值。
- `mean`：看动作整体是否偏向某个方向。
- `std`：看动作变化是否过大或过小。

面试表达：

> 只检查 action 是 7 维还不够，还需要看每一维的数值分布。如果某一维 max 特别大，可能是坐标系、单位转换或归一化出了问题；如果 std 接近 0，可能说明这一维几乎没有变化，对模型训练贡献有限。

## 第三步：理解 state 分布

state 也是 7 维，通常代表机器人当前状态，例如末端位姿、夹爪状态或关节相关信息。

state 分布检查可以帮助发现：

- 状态是否长期不变。
- 状态是否出现异常跳变。
- state 和 action 的维度是否一致但数值范围异常。

## 今天完成标准

- 能运行 `summarize_dataset.py`。
- 能解释 action/state 每一维 min、max、mean、std 的含义。
- 能说明为什么“维度正确”不等于“数据质量一定好”。
- 能把分布统计结果写进数据质量报告。
