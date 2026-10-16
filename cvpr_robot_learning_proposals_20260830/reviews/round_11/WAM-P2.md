# Round 11 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r10
- Responds-To: round_10
- Checked: 2026-08-30
- Lifecycle: `round_01`…`round_10`，10次实际refine
- Verdict: **PASS**

## Actual-diff核验

r10 将target-build compute、teacher quality、deploy decision compute分为三账；oracle rollout虽不计部署时延，但全额计入research/data-generation cost，同时提供training-cost与deploy-cost视图。昂贵target不再被包装成免费部署收益。

| 维度 | 分数 | 最终理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 实时预算下想象价值关键。 |
| D2 失败模式清晰度 | 4.5 | harmful compute/latency cost具体。 |
| D3 创新性/最近邻 | 4.5 | paired continuation-value target边界成立。 |
| D4 机制因果闭环 | 4.5 | CRN outcome→A_k→stop。 |
| D5 技术正确性 | 4.5 | incremental cost/cross-fit正确。 |
| D6 可观测性/泄漏 | 4.5 | future outcomes只进离线target。 |
| D7 数据可得性 | 4.0 | S16 target records成本高。 |
| D8 算力/工程 | 4.0 | 三账透明但总体较重。 |
| D9 可证伪性 | 4.5 | paired-myopic/winner会判负。 |
| D10 基线强度 | 4.5 | Ponder/ACT/When-to-Trust/CheckVLA。 |
| D11 消融充分性 | 4.5 | CRN×target及S敏感性完整。 |
| D12 OOD/真机 | 4.0 | real gate可删除。 |
| D13 复现性 | 4.5 | 三类成本/质量字段固定。 |
| D14 CVPR契合度 | 4.5 | WAM实时控制问题明确。 |
| D15 风险/负结果 | 4.5 | compute-harm诊断可独立成立。 |

平均分：**4.40/5.00**。最近邻已审：When-to-Trust、HarmoWAM、CheckVLA、PonderNet、ACT/Selecting Computations。未决非致命风险：离线target成本可能限制扩展。硬门槛全过：**PASS**。
