# Day 1：跑通机器人数据质量检查

## 目标

今天不要追求下载大数据集，也不要急着跑模型。目标只有一个：

> 亲手跑通一个机器人 episode 数据质量检查流程，并能解释 observation、action、language instruction、timestamp 为什么重要。

完成后，你在面试里可以说：

> 我先用一个小规模 episode 样例模拟机器人数据结构，写了质量检查脚本，检查字段缺失、动作维度、图像尺寸、语言指令和时间戳问题。这个流程后续可以迁移到 Open X-Embodiment / BridgeData V2 小样本上。

## 第一步：进入项目目录

在 PowerShell 中执行：

```powershell
cd D:\具身智能学习\embodied-intelligence-learning
```

确认当前目录：

```powershell
pwd
```

你应该看到路径类似：

```text
D:\具身智能学习\embodied-intelligence-learning
```

## 第二步：看项目结构

执行：

```powershell
dir
```

你需要知道这些目录分别干什么：

| 目录 | 作用 |
| --- | --- |
| `datasets` | 放公开机器人数据集调研 |
| `scripts` | 放数据加载、质检、统计脚本 |
| `reports` | 放数据质量报告 |
| `papers` | 放论文笔记 |
| `notes` | 放每日学习记录和执行手册 |

面试回答方式：

> 我把这个项目拆成数据集调研、脚本、报告、论文和日志几个模块。这样不是只写零散代码，而是模拟真实的数据工程项目流程：先理解数据结构，再写脚本检查，再输出报告。

## 第三步：打开样例数据

执行：

```powershell
Get-Content scripts\sample_robot_episodes.jsonl
```

你要重点看懂这个结构：

```text
episode
└── steps
    ├── observation
    │   ├── image
    │   ├── state
    │   └── language_instruction
    ├── action
    └── timestamp
```

你需要能解释：

- `episode`：一条完整机器人任务轨迹，例如“拿起红色方块”。
- `step`：轨迹中的一个时间步。
- `observation`：机器人在当前时刻看到和感知到的信息。
- `image`：视觉输入。
- `state`：机器人自身状态，例如关节角、末端位姿等。
- `language_instruction`：任务指令。
- `action`：机器人下一步动作。
- `timestamp`：时间戳，用来判断时序是否正常。

面试回答方式：

> 机器人数据不是普通表格数据，它是 episode-step 的层级结构。每个 step 里通常有 observation 和 action，observation 里包括图像、状态和语言指令。模型训练时其实是在学 observation 到 action 的映射，所以这些字段必须对齐。

## 第四步：运行质量检查脚本

执行：

```powershell
python scripts\check_dataset_quality.py --input scripts\sample_robot_episodes.jsonl
```

你会看到 JSON 输出。重点看这些字段：

| 字段 | 含义 |
| --- | --- |
| `episodes` | 一共有几条轨迹 |
| `steps` | 一共有多少个时间步 |
| `trajectory_length` | 轨迹长度统计 |
| `action_dimensions` | action 维度分布 |
| `image_shapes` | 图像尺寸分布 |
| `issue_count` | 发现的问题总数 |
| `issue_types` | 每类问题的数量 |
| `issues` | 具体异常样本位置 |

面试回答方式：

> 我先统计数据规模和字段分布，再检查质量问题。比如 action 维度如果不一致，训练时模型输出维度就无法统一；image shape 不一致会影响 dataloader；timestamp 不递增说明轨迹时序可能有问题。

## 第五步：保存质量检查结果

执行：

```powershell
python scripts\check_dataset_quality.py --input scripts\sample_robot_episodes.jsonl --output reports\sample_quality_summary.json
```

再确认文件生成：

```powershell
dir reports
```

你应该能看到：

```text
sample_quality_summary.json
sample-quality-report.md
```

面试回答方式：

> 我把脚本输出保存成 JSON，方便后续报告引用，也方便做自动化流程。真实项目里这一步可以接到数据看板、CI 检查或者数据版本管理流程里。

## 第六步：阅读报告

执行：

```powershell
Get-Content reports\sample-quality-report.md
```

你要能说出这 5 类问题：

| 问题 | 为什么重要 |
| --- | --- |
| `missing_language_instruction` | 语言条件缺失，VLA 或语言条件模仿学习不能用 |
| `invalid_state` | 机器人状态为空，状态输入不完整 |
| `non_increasing_timestamp` | 时序异常，说明轨迹顺序可能错了 |
| `inconsistent_action_dim` | 动作维度不一致，模型输出空间无法统一 |
| `inconsistent_image_shape` | 图像尺寸不一致，视觉输入管线会出错 |

## 第七步：写今日学习日志

在 `notes/daily-log.md` 里追加一段：

```markdown
## 2026-06-30

- **今日收获**：跑通了第一个机器人 episode 数据质量检查脚本，理解了 episode、step、observation、action、language_instruction、timestamp 的基本结构。脚本能够统计轨迹长度、动作维度、图像尺寸，并识别语言指令缺失、state 为空、时间戳不递增、动作维度不一致、图像尺寸不一致等问题。

- **卡点/疑问**：当前使用的是手写样例数据，还没有加载真实 Open X-Embodiment / BridgeData V2 数据。下一步需要学习 RLDS / TFDS 数据格式，并把真实数据转换成统一 JSONL 格式。

- **明天计划**：研究 BridgeData V2 或 Open X-Embodiment 的小样本加载方式，编写 `load_rlds_sample.py`，把真实 episode 的字段结构打印出来。
```

## 你今天必须真正理解的 3 个问题

### 1. 为什么要做数据质量检查？

因为机器人模型训练依赖状态、图像、语言和动作之间的严格对齐。如果数据有缺帧、动作维度不一致、时间戳错乱或语言指令缺失，模型会学到错误的状态-动作关系。

### 2. 这个项目和数据产品实习有什么关系？

数据产品实习训练的是需求拆解、指标口径、数据清洗、异常定位和跨团队沟通。迁移到具身智能里，就是把“业务数据质量”换成“机器人训练数据质量”，检查对象从订单、用户、指标变成 episode、observation、action 和 language instruction。

### 3. 为什么不一上来就训练模型？

因为没有高质量数据，训练模型没有意义。对于具身智能数据工程岗位，能把数据采集、清洗、质检、报告和训练样本准备好，本身就是重要工作。

## 今天完成标准

- 能独立进入项目目录。
- 能打开并解释 `sample_robot_episodes.jsonl`。
- 能运行 `check_dataset_quality.py`。
- 能看懂 `issue_types` 和 `issues`。
- 能用自己的话解释 5 类数据质量问题。
- 能把今天做的事写进 `daily-log.md`。
