# Round 11 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r10
- Responds-To: round_10
- Checked: 2026-08-30
- Lifecycle: `round_01`…`round_10`，10次实际refine
- Verdict: **PASS**

## Actual-diff核验

r10 把orbit构造、support、certification attempted/success/failure codes、null与uniform-on-orbit proper score写入主表，并固定“simulator-certified ε-symmetric”；证书失败样本单列atlas，不再被重标为identifiable。

| 维度 | 分数 | 最终理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 长遮挡身份错误关键。 |
| D2 失败模式清晰度 | 4.5 | 三strata与orbit明确。 |
| D3 创新性/最近邻 | 4.5 | 分层proper-score协议超出persistent slots。 |
| D4 机制因果闭环 | 4.5 | joint posterior→update→decision。 |
| D5 技术正确性 | 4.5 | posterior与symmetry scoring正确。 |
| D6 可观测性/泄漏 | 4.5 | GT evaluator shard隔离。 |
| D7 数据可得性 | 4.0 | certified rerender需专门数据。 |
| D8 算力/工程 | 4.0 | detector/beam/WAM预算可控。 |
| D9 可证伪性 | 4.5 | cert failure与L11胜负直接。 |
| D10 基线强度 | 4.5 | JPDA L11、MHT、OA/POT。 |
| D11 消融充分性 | 4.5 | evidence×inference ladder完整。 |
| D12 OOD/真机 | 4.0 | benchmark主线，control可删。 |
| D13 复现性 | 4.5 | orbit/support/failure code齐全。 |
| D14 CVPR契合度 | 4.5 | identity observability benchmark成立。 |
| D15 风险/负结果 | 4.5 | failure atlas有独立价值。 |

平均分：**4.40/5.00**。最近邻已审：OA-WAM、POT-VLA、3D-ALP、JPDA/MHT、JRDB。未决非致命风险：simulator certificate不能替代现实可识别性。硬门槛全过：**PASS**。
