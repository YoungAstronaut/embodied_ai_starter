# Round 11 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r10
- Responds-To: round_10
- Checked: 2026-08-30
- Lifecycle: `round_01`…`round_10`，10次实际refine
- Verdict: **PASS**

## Actual-diff核验

r10 在同一验收行加入innovation shuffle、wrong-controller residual与held-out-action regret；要求前两者使优势下降≥50%，且held-out action仍比最强基线降regret≥20%，否则删除functional-belief claim。shortcut边界现可证伪。

| 维度 | 分数 | 最终理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 隐动力学导致重复失败。 |
| D2 失败模式清晰度 | 4.5 | same visual/command different outcome。 |
| D3 创新性/最近邻 | 4.5 | residual下predictive-equivalence边界明确。 |
| D4 机制因果闭环 | 4.5 | nominal→residual→belief→planner。 |
| D5 技术正确性 | 4.5 | distribution/CVaR/MMD定义正确。 |
| D6 可观测性/泄漏 | 4.5 | physics/logger仅分层评估。 |
| D7 数据可得性 | 4.0 | physics×nuisance cells较重。 |
| D8 算力/工程 | 4.0 | nested sampling成本可见。 |
| D9 可证伪性 | 4.5 | 三联合负控直接判负。 |
| D10 基线强度 | 4.5 | PEARL/RMA/generic deploy-equal。 |
| D11 消融充分性 | 4.5 | raw/residual×point/distributional。 |
| D12 OOD/真机 | 4.0 | physics drift只secondary。 |
| D13 复现性 | 4.5 | noise/K/reference/负控齐全。 |
| D14 CVPR契合度 | 4.5 | 视觉残差与适应问题成立。 |
| D15 风险/负结果 | 4.5 | generic adaptation降级明确。 |

平均分：**4.40/5.00**。最近邻已审：CoCo v1、Robot-Factored WM、PEARL、RMA、VariBAD、DELE。未决非致命风险：nominal controller误差可能主导residual，但wrong-controller负控会揭示。硬门槛全过：**PASS**。
