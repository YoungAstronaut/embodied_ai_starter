# Round 11 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r10
- Responds-To: round_10
- Checked: 2026-08-30
- Lifecycle: `round_01`…`round_10`，10次实际refine
- Verdict: **PASS**

## Actual-diff核验

r10 加入student/target shard只经opaque key连接、future/reward/success/event/seed/task-ID字段拒绝、泄漏阳性CI测试，以及flicker/low-visual true event盲评混淆矩阵；metadata预测event family>60%即重建shard。

| 维度 | 分数 | 最终理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 历史惯性恢复重要。 |
| D2 失败模式清晰度 | 4.5 | false/missed reset与RMRT清楚。 |
| D3 创新性/最近邻 | 4.5 | change×value reset-worthiness边界明确。 |
| D4 机制因果闭环 | 4.5 | innovation→reset→action时序正确。 |
| D5 技术正确性 | 4.5 | LCB/FWER/censor定义合理。 |
| D6 可观测性/泄漏 | 4.5 | schema reject与阳性测试充分。 |
| D7 数据可得性 | 4.0 | event family target较重。 |
| D8 算力/工程 | 4.0 | proposer与recovery成本清楚。 |
| D9 可证伪性 | 4.5 | 盲评/metadata probe会否定机制。 |
| D10 基线强度 | 4.5 | label-equal pure gates。 |
| D11 消融充分性 | 4.5 | change×value 2×2。 |
| D12 OOD/真机 | 4.0 | seen-family主线、real secondary。 |
| D13 复现性 | 4.5 | shard/root/CI schema固定。 |
| D14 CVPR契合度 | 4.5 | streaming视觉控制明确。 |
| D15 风险/负结果 | 4.5 | EventAlias/detector降级可用。 |

平均分：**4.40/5.00**。最近邻已审：IntentVLA、PACE、REMAC、BOCPD/event-triggered MPC、CheckVLA。未决非致命风险：稀有真事件power可能不足。硬门槛全过：**PASS**。
