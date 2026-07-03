# Roadmap

## Phase 1: 数据集结构与质量分析

- [x] 创建学习仓库
- [x] 整理 Open X-Embodiment 数据集初探
- [x] 整理 RT-2 论文笔记
- [x] 搭建 TFDS/RLDS 环境并验证 metadata 检查流程
- [x] 构造 BridgeData-style 小样本并跑通统一质检 pipeline
- [x] 编写数据质量检查脚本
- [x] 输出第一版样例数据质量分析报告
- [x] 输出第一版公开数据集质量分析报告
- [x] 输出一键 pipeline 自动 Markdown 报告

## Phase 2: 仿真与数据管线

- [ ] 将 pipeline 迁移到真实 BridgeData V2 / Open X-Embodiment 小样本
- [ ] 跑通 ROS2 基础 demo
- [ ] 跑通 Isaac Sim 或 Gazebo 基础场景
- [ ] 记录仿真数据采集流程
- [ ] 对比仿真数据和真实数据字段差异

## Phase 3: 模仿学习方法理解

- [ ] 阅读 Diffusion Policy
- [ ] 阅读 ACT
- [ ] 阅读 OpenVLA
- [ ] 复现一个轻量 demo 或整理可运行环境记录

## 阶段成果目标

短期目标不是把所有方向都学完，而是先形成一个可展示项目：

> 机器人数据集结构理解 + 统一字段映射 + 数据质量检测 + 分布统计与可视化 + 自动分析报告。
