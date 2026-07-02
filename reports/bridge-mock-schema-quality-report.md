# BridgeData V2 Mock Schema 质量检查报告

## 1. 目标

本报告用于验证 BridgeData V2 官方 schema 是否可以转化为可执行的数据质量检查规则。

由于完整 BridgeData V2 体量较大，且本地读取 `bridge` metadata 存在超时问题，本次先使用 BridgeData-style mock episode 验证字段映射和质量检查流程。

## 2. 检查规则

根据 BridgeData V2 官方字段结构，本次检查设置：

| 检查项 | 期望值 |
| --- | --- |
| action 维度 | 7 |
| state 维度 | 7 |
| 主图像尺寸 | 256 x 256 x 3 |

运行命令：

```powershell
python scripts\check_dataset_quality.py --input scripts\bridge_mock_episodes.jsonl --expected-action-dim 7 --expected-state-dim 7 --expected-image-shape 256x256x3
```

## 3. 检查结果

| 指标 | 结果 |
| --- | --- |
| episode 数量 | 1 |
| step 数量 | 2 |
| action 维度分布 | 7 维出现 2 次 |
| 图像尺寸分布 | 256 x 256 x 3 出现 2 次 |
| language instruction 数量 | 1 |
| issue_count | 0 |

## 4. 结论

BridgeData-style mock episode 符合当前设置的 schema 规则：

- action 维度符合 BridgeData V2 的 7 维要求。
- state 维度符合 BridgeData V2 的 7 维要求。
- 主图像尺寸符合 256 x 256 x 3 要求。
- language instruction 存在且非空。
- timestamp 正常递增。

## 5. 工程意义

这一步说明项目已经从“理解 BridgeData V2 字段结构”推进到“把 schema 转成可执行质检规则”。后续接入真实 BridgeData V2 episode 时，可以复用同一套脚本检查真实样本是否满足训练数据要求。
