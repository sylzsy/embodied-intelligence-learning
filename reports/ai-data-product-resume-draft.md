# 邵叶隆 - AI 数据产品 / 数据平台产品实习生

> 目标岗位：AI 数据产品实习生 / 数据平台产品实习生 / 多模态数据产品实习生

## 个人概况

温州大学计算机科学与技术硕士在读，获校一等奖学金，具备数据产品、OCR / 图像识别、多模态数据质量分析和机器学习项目经验。熟悉需求分析、PRD 撰写、数据指标设计、数据质量评估和跨角色协作，能够从业务场景出发梳理数据问题，并推动产品方案落地。近期围绕 BridgeData V2 / Open X-Embodiment 风格机器人数据搭建数据质量分析 pipeline，强化了 AI 数据集工程、质量规则和自动化报告能力。

## 教育背景

**温州大学｜计算机科学与技术｜硕士** 
2024.09 - 2027.09

- 主修课程：机器学习、深度学习、人工智能原理与应用、优化理论、计算机应用数学、高级计算机网络等。
- 研究方向：特征选择、智能优化、机器学习实验评估。

## 实习 / 产品项目经历

### 手写体 OCR 数据产品方案设计｜AI 数据产品 / OCR 图像识别方向

- 基于真实教学材料场景，梳理材料上传、自动分页、任务分发、标注工作台、OCR 识别、字段检查和质检流转等现有业务流程，识别“手写答案 / 批注无法稳定结构化”的核心痛点。
- 使用真实手写样例完成多厂商 OCR 横评，覆盖 500 条有效样本，对比豆包、讯飞、阿里、百度、有道和 PaddleOCR 等方案，评估成功率、字符准确率、完全正确率、平均耗时和 P95 耗时。
- 输出手写体 OCR 接入 PRD，明确“不改变主流程、在原 OCR 按钮旁新增手写体 OCR 入口、识别结果回填原字段”的低成本改造方案。
- 设计 OCR 结果数据记录字段，包括 `ocr_source`、`ocr_vendor`、`ocr_text_raw`、`ocr_text_final`、`ocr_confidence`、`ocr_status`、`ocr_error_code`、`ocr_reviewed` 等，支持结果追踪、质检复核和后续数据分析。
- 设计字段检查和质检联动规则，包括手写识别待复核、识别失败、识别结果为空、OCR 后未确认、LaTeX 渲染失败等问题项，降低低质量识别结果直接进入生产流程的风险。
- 基于厂商评测结果提出“豆包主识别 + 讯飞备选 + 失败转人工”的服务策略，兼顾准确率、稳定性、长尾耗时和业务可用性。

**可量化结果：**

- 评测原始图片 177 张、标注区域 1709 个、有效评测样本 1242 条。
- 本轮厂商横评样本 500 条。
- 豆包字符准确率 91.05%，超过手写试卷场景 88% 的目标线。
- 讯飞成功率 97.50%，作为备选厂商提升兜底稳定性。

## AI 数据工程项目

### BridgeData V2 机器人数据质量分析 Pipeline｜具身智能数据集工程

- 调研 BridgeData V2 / Open X-Embodiment 机器人数据结构，梳理 episode-step 层级下的 observation、action、state、image、language instruction 和 timestamp 等核心字段。
- 设计统一 JSONL episode 格式，将 BridgeData-style 字段映射到统一 schema，例如将 `steps/observation/image_0` 映射为 `steps/observation/image`，提升跨数据集质量检查流程的复用性。
- 开发机器人数据质量检查脚本，支持字段缺失、action/state 维度、图像尺寸、timestamp 递增、轨迹长度、action 越界和缺失率统计。
- 实现 action/state 每一维 min、max、mean、std 分布统计与可视化，用于发现自由度异常、数值范围异常和字段映射问题。
- 构建基于 dataset profile 的一键 pipeline，自动输出 quality summary、distribution summary、可视化图表、manifest 和 Markdown 数据质量报告。

**项目产出：**

- 支持 BridgeData V2 profile：`action_dim=7`、`state_dim=7`、`image_shape=256x256x3`。
- 当前 mock episode 检查结果：1 个 episode、2 个 step、`issue_count=0`。
- 自动生成质量检查 JSON、分布统计 JSON、4 张分布图和 Markdown 报告。

## 科研经历

### 元启发式进化算法在医学数据集特征选择中的应用｜硕士课题

- 面向高维小样本医学数据，研究特征冗余、噪声大、过拟合和泛化性能下降问题。
- 将特征选择建模为二进制组合优化问题，设计包含分类性能和特征数惩罚的适应度函数。
- 在元启发式搜索基础上探索强化学习策略和代理模型，以降低模型评估成本。
- 优化目标包括分类性能提升、特征数量减少和结果稳定性提升。
- 科研产出：1 篇论文在投，1 篇论文修改中。

## 技能

- **产品能力**：需求分析、PRD 撰写、竞品 / 厂商评测、用户流程梳理、指标设计、质检规则设计、产品方案汇报。
- **数据能力**：数据口径设计、数据质量检查、字段映射、缺失率统计、异常值分析、JSON / JSONL 数据处理、自动化报告生成。
- **AI / 算法理解**：OCR、图像识别、多模态数据、机器学习、特征工程、特征选择、交叉验证、AUC / F1 等评估指标。
- **编程工具**：Python、Matlab、C++、Java、Excel、PPT、Markdown、Git。
- **工程工具**：Python 脚本、Matplotlib 可视化、TensorFlow Datasets metadata inspection。
