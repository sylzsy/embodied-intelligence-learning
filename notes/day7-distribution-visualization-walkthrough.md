# Day 7：Action / State 分布可视化

## 目标

Day 7 将 Day 6 的 action/state 数值统计转成图表，形成更直观的数据质量分析结果。

本日目标：

- 读取 `bridge_mock_distribution_summary.json`
- 绘制 action/state 每一维的 min-max 范围图
- 绘制 action/state 每一维的 std 柱状图
- 学会解释“分布图对机器人数据质量有什么用”

## 第一步：生成图表

执行：

```powershell
python scripts\plot_distribution.py --input reports\bridge_mock_distribution_summary.json --output-dir assets\distributions
```

生成文件：

```text
assets/distributions/action_range.png
assets/distributions/action_std.png
assets/distributions/state_range.png
assets/distributions/state_std.png
```

## 第二步：看懂 range 图

range 图展示每一维的最小值、最大值和平均值。

它可以帮助判断：

- 某一维是否出现异常大值。
- 某一维是否长期保持不变。
- action/state 的数值范围是否符合预期。

## 第三步：看懂 std 图

std 图展示每一维的波动程度。

- `std` 越大，说明这一维变化越明显。
- `std = 0`，说明当前样本中这一维没有变化。

面试表达：

> 我把 action/state 每一维的 min、max、mean、std 转成图表，是为了更直观地发现数据分布异常。比如某一维 max 异常大，可能是单位转换或归一化问题；某一维 std 长期为 0，可能说明该自由度没有被使用，或者字段映射有问题。

## 今天完成标准

- 能运行 `plot_distribution.py`。
- 能找到 4 张分布图。
- 能解释 range 图和 std 图分别表示什么。
- 能说明为什么分布可视化比只看 JSON 更适合写报告。
