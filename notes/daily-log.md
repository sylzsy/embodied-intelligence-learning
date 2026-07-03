# 学习日志

## 2026-07-03 Day 13

- **今日完成**：新增 `app.py`，使用 Streamlit 将机器人数据质量 pipeline 包装成可交互页面。页面支持使用内置 BridgeData-style 样例或上传 JSON / JSONL 文件，选择 dataset profile 后一键运行质量检查、分布统计、图表生成和 Markdown 报告生成。

- **今日理解**：Streamlit 页面没有重写质检逻辑，而是复用已有 pipeline。这样做的好处是命令行能力和页面能力保持一致，后续继续增强脚本时，页面也能同步受益。

- **运行结果**：页面运行后可以展示 Episodes、Steps、Issue Count、Language Tasks，并在不同 tab 中查看 quality summary、distribution summary、action/state 图表、report 和运行日志。

- **下一步行动**：Day 14 继续增强页面展示和下载体验，并准备加入 LLM 报告解释模块。

## 2026-07-03 Day 10

- **今日完成**：新增 `generate_pipeline_report.py`，让 pipeline 可以根据 `manifest.json`、`quality_summary.json`、`distribution_summary.json` 和图表自动生成 `report.md`。同时补充第一阶段总结报告，明确 Day 1-10 已经形成 BridgeData-style 机器人数据质量分析闭环。

- **今日理解**：自动报告的价值在于可复现和可交付。它不是手动复制粘贴结果，而是由 pipeline 产物自动生成，能把输入数据、profile 配置、质量检查、分布统计、图表和结论组织成一份可展示的 Markdown 报告。

- **运行结果**：使用 `configs/bridge_v2_profile.json` 运行 pipeline 后，成功生成 `reports/bridge_profile_pipeline/report.md`。当前样例数据共有 1 个 episode、2 个 step，action/state 均为 7 维，图像尺寸为 256 x 256 x 3，`issue_count` 为 0。

- **阶段总结**：第一阶段完成了从 schema 调研、统一字段映射、质量检查、质量指标增强、分布统计、可视化、profile 配置化到自动报告生成的完整链路。下一阶段进入仿真与数据管线实践，并准备接入真实 BridgeData V2 / Open X-Embodiment 小样本。

## 2026-07-03 Day 11

- **今日完成**：整理根目录 `README.md`，将仓库从学习记录升级为项目展示页，补充项目定位、pipeline 流程、快速运行命令、输出产物、样例结果、技术栈、第一阶段结论和下一阶段计划。

- **今日理解**：README 是项目的入口。对面试官来说，README 需要快速回答“你做了什么、怎么运行、结果是什么、有什么工程价值”，而不是只记录学习过程。

- **运行结果**：README 现在可以直接说明 BridgeData-style 数据质量 pipeline 的输入、处理流程和输出报告。

## 2026-07-03 Day 12

- **今日完成**：新增 `reports/project-interview-qa.md`，整理 60 秒项目介绍、高频面试问题、简历 bullet 和追问回答模板。

- **今日理解**：项目做完之后，还需要把工程实现转化成面试表达。重点不是背脚本，而是能解释为什么要做数据质量、为什么要统一字段、profile 和 manifest 的工程价值，以及这些检查如何影响机器人模型训练。

- **阶段收口**：Day 10、Day 11、Day 12 完成后，第一阶段形成了代码、报告、README 和面试表达四类成果，可以作为简历项目基础。

## 2026-07-03 Day 9

- **今日完成**：新增 `configs/bridge_v2_profile.json`，将 BridgeData V2 的 action/state 维度、图像尺寸、轨迹长度阈值、action 数值阈值和字段映射关系配置化；改造 `run_quality_pipeline.py` 支持 `--profile` 参数。

- **今日理解**：把参数放进 profile 是为了让 pipeline 和具体数据集解耦。后续切换到新的机器人数据集时，只需要新增 profile，不需要改主流程代码，也避免手动写长命令导致参数不一致。

- **运行结果**：使用 `configs/bridge_v2_profile.json` 运行 pipeline 后，成功生成 `quality_summary.json`、`distribution_summary.json`、4 张分布图和 `manifest.json`。`manifest.json` 中记录了输入数据、profile 配置和输出产物路径。

- **下一步行动**：继续扩展 profile 机制，后续可以为其他机器人数据集新增 profile，并尝试接入真实 BridgeData V2 小样本。

## 2026-07-03 Day 8

- **今日完成**：新增 `run_quality_pipeline.py`，将质量检查、action/state 分布统计和分布图生成整合为一键 pipeline。输入 `bridge_mock_episodes.jsonl` 后，可自动输出 `quality_summary.json`、`distribution_summary.json`、4 张分布图和 `manifest.json`。

- **今日理解**：pipeline 的价值在于工程复现。相比手动依次运行多个脚本，一键 pipeline 能保证输入、参数、输出路径和分析结果可追踪，更接近真实数据工程项目中的自动化分析流程。

- **运行结果**：成功生成 `reports/bridge_mock_pipeline/`，其中包含质量检查结果、分布统计结果、action/state 可视化图表和 manifest 文件。

- **下一步行动**：基于当前 pipeline 继续扩展真实数据接入能力，后续尝试读取真实 BridgeData V2 metadata 或小样本 episode。

## 2026-07-03 Day 7

- **今日完成**：新增 `plot_distribution.py`，将 action/state 每一维的 min-max 范围和 std 生成可视化图表，包括 `action_range.png`、`action_std.png`、`state_range.png`、`state_std.png`。

- **今日理解**：range 图用于观察每一维的最小值、最大值和均值，std 图用于观察每一维的波动程度。相比只看 JSON，图表更适合快速发现某一维是否异常大、是否长期不变。

- **运行结果**：当前 mock 数据中 action 第 6 维变化最明显，std 最大；部分维度 std 为 0，说明这些维度在当前样本中没有变化。

- **下一步行动**：将质量检查、分布统计和图表生成整合成一键 pipeline，提升项目可复现性。

## 2026-07-03 Day 6

- **今日完成**：新增 `summarize_dataset.py`，对 BridgeData-style episode 的 action/state 进行分布统计，输出每一维的 min、max、mean、std，并生成 `bridge_mock_distribution_summary.json`。

- **今日理解**：字段完整和维度正确不代表数据质量一定好，还需要观察 action/state 每一维的数值范围和波动情况。若某一维 std 长期为 0，可能说明该自由度没有被使用，也可能是数据采集或字段映射异常；若 max 异常大，可能是单位转换、归一化或日志解析问题。

- **运行结果**：当前 mock 数据中 action/state 均为 7 维，第 6 维波动最大，部分维度 std 为 0，说明当前小样本中这些维度没有变化。

- **下一步行动**：将 action/state 分布统计结果可视化，生成更适合报告展示的图表。

## 2026-07-03 Day 5

- **今日完成**：增强 `check_dataset_quality.py`，新增轨迹长度阈值、action 极端值检查和缺失率统计，输出 `quality_rates` 用于量化语言指令、state、image、action 等字段问题。

- **今日理解**：`issue_types` 用于统计每类问题出现次数，`quality_rates` 用于把缺失类问题按 step 总数转成比例，适合写数据质量报告。例如 5 个 step 中 1 个缺少语言指令，缺失率就是 20%。

- **运行结果**：BridgeData-style mock 数据在 `action_dim=7`、`state_dim=7`、`image_shape=256x256x3`、轨迹长度阈值和 action 数值阈值下检查结果为 `issue_count=0`；异常样例可识别 `trajectory_too_short`、`action_value_out_of_range`、`missing_language_instruction` 等问题。

- **下一步行动**：继续补充分布统计能力，观察 action/state 每一维的数值范围和波动情况。

## 2026-07-02 Day 4

- **今日完成**：整理 BridgeData V2 官方 schema，明确核心字段包括 `steps/action`、`steps/observation/state`、`steps/observation/image_0`、`steps/language_instruction` 和 `steps/language_embedding`。由于 Google Colab 暂时无法登录，改为基于官方 TFDS 文档和本地 mock 数据继续推进。

- **今日理解**：BridgeData V2 的 action 和 state 都是 7 维，主视角图像字段是 `image_0`，尺寸为 256 x 256 x 3，`language_embedding` 是 512 维。真实数据集字段需要先映射到项目统一 JSONL 格式，再复用统一质量检查脚本。

- **运行结果**：运行 `bridge_sample_to_jsonl.py` 生成 1 个 BridgeData-style episode，共 2 个 step。随后使用增强后的 `check_dataset_quality.py` 设置 `--expected-action-dim 7 --expected-state-dim 7 --expected-image-shape 256x256x3` 进行检查，结果 `issue_count` 为 0。

- **工程收获**：把 BridgeData V2 官方 schema 转成了可执行质检规则。后续接入真实 BridgeData V2 episode 时，可以复用相同规则检查 action/state/image 是否符合训练数据要求。

- **下一步行动**：继续增强质量检查脚本，加入轨迹长度阈值、语言指令缺失率、图像字段缺失率和 action 极端值检查。

## 2026-07-01

- **今日完成**：按照 Day 1 操作手册跑通了机器人 episode 数据质量检查流程。进入项目目录后，查看了 `sample_robot_episodes.jsonl`，理解了 episode、steps、observation、action、timestamp 的基本结构；运行 `check_dataset_quality.py` 后，看到样例数据共有 2 个 episode、5 个 step，并检测出 5 类数据质量问题。

- **今日理解**：`issue_types` 用来统计每类问题出现了多少次，`issues` 用来定位问题具体发生在哪个 episode 和 step。今天理解了语言指令缺失、机器人状态缺失、时间戳不递增、动作维度不一致、图像尺寸不一致这 5 类问题，以及它们对机器人模仿学习 / VLA 模型训练的影响。

- **卡点 / 疑问**：目前使用的是手写样例数据，还没有加载真实的 Open X-Embodiment 或 BridgeData V2 数据。下一步需要学习真实数据集的 RLDS / TFDS 格式，并把真实 episode 转换成脚本可检查的结构。

- **下一步行动**：继续做 Day 2，目标是研究 BridgeData V2 或 Open X-Embodiment 小样本的数据加载方式，打印真实 episode 字段结构，并尝试复用当前质量检查脚本。

## 2026-07-01 Day 2

- **今日完成**：完成了 BridgeData V2 字段结构理解和 BridgeData-style 小样本转换。确认 BridgeData V2 在 TFDS 中的数据集名是 `bridge`，完整数据约 387GB，因此没有直接完整下载，而是先用小样本验证字段映射流程。

- **今日理解**：BridgeData-style 数据中包含 `episode_metadata`、`steps/action`、`steps/language_instruction`、`steps/observation/image_0` 和 `steps/observation/state`。我将 `image_0` 映射为统一的 `observation.image`，将 step 级别的 `language_instruction` 放入 `observation.language_instruction`，从而让不同来源的数据可以复用同一套质量检查脚本。

- **运行结果**：转换后的样例数据共有 1 个 episode、2 个 step；action 维度为 7，图像尺寸为 256 x 256 x 3，`issue_count` 为 0，说明样例数据字段完整且格式一致。

- **卡点 / 疑问**：当前本地 Python 环境没有安装 `tensorflow` 和 `tensorflow_datasets`，因此还没有直接加载真实 TFDS/RLDS 数据。后续需要单独准备兼容环境，再尝试读取真实 BridgeData V2 小样本 metadata。

- **下一步行动**：准备 Day 3，研究如何安装或创建适合 TFDS/RLDS 的 Python 环境，并尝试读取 `bridge` 数据集的 metadata 或小规模样本。

## 2026-06-26

- **今日收获**：完成了 Open X-Embodiment 数据集初探——搞清楚了它的规模（100万+轨迹、60个数据集、22种机器人）和数据格式（Episode → Step → observation + action 的层级结构），数据长什么样心里有数了。精读了 RT-2 论文，理解了 VLA 的核心逻辑——拿大 VLM 做 co-fine-tuning、把 action 转成 token 跟文字混着训，让机器人既有常识又能动手。顺便把 VLM/VLA/co-fine-tuning/泛化层次这些基础概念都捋清了。

- **卡点/疑问**：Open X-Embodiment 还没实际下载数据，RLDS 格式到底怎么用还没上手。RT-2 的 chain-of-thought 推理具体是怎么触发的、tokenization 的细节（action 离散化到 256 个 bin 具体怎么映射）还需要后面深入看。

- **明天计划**：下载 Open X-Embodiment 一个小子集（比如 Bridge V2），用 Python 加载数据看看实际长什么样。开第二篇论文 Diffusion Policy，和 RT-2 对比着看。

## 2026-07-01 Day 3

- **今日完成**：创建了独立 conda 环境 `ei-tfds`，使用 Python 3.11.15，并安装了 TensorFlow 2.21.0 和 TensorFlow Datasets 4.9.10。完成了 TFDS/RLDS 数据加载环境的基础搭建。

- **今日理解**：没有使用 base 环境，因为 base 是 Python 3.13，不适合作为 TensorFlow 主环境。通过独立环境隔离依赖，可以避免污染已有项目环境，也方便后续复现实验。

- **运行结果**：运行 `inspect_tfds_builder.py --dataset mnist` 成功读取 TFDS metadata，输出了 `mnist/3.0.1`、`image` 和 `label` 等 features，说明 TFDS 环境和 builder 检查脚本可用。

- **卡点 / 疑问**：尝试读取 `bridge` metadata 时本地超时，判断不是 TensorFlow/TFDS 安装问题，而可能是 TFDS catalog 远程初始化或网络访问问题。

- **下一步行动**：Day 4 准备使用 Google Colab 或更稳定网络尝试读取 `bridge` metadata；如果仍然受限，则继续基于 BridgeData-style schema 完善字段报告和质量检查流程。
