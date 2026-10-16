# Round 11 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r10
- Responds-To: round_10
- Checked: 2026-08-30
- Lifecycle: `round_01`…`round_10`，10次实际refine
- Verdict: **PASS**

## Actual-diff核验

r10 固定 attempted/valid-selected 三分母、各branch route/fallback以及三branch forward到commit的mean/p95/p99 latency/energy；明确禁止只在accepted子集报告。若attempted-root utility不改善，relation-B claim直接判负。

| 维度 | 分数 | 最终理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 错几何高置信风险重要。 |
| D2 失败模式清晰度 | 4.5 | 失效family/severity明确。 |
| D3 创新性/最近邻 | 4.5 | LOFO Geometry Reliability Atlas独特。 |
| D4 机制因果闭环 | 4.5 | regret→calibration→route完整。 |
| D5 技术正确性 | 4.5 | frozen coverage与三分母正确。 |
| D6 可观测性/泄漏 | 4.5 | GT relation只进target/eval。 |
| D7 数据可得性 | 4.0 | repair/corruption rollouts较重。 |
| D8 算力/工程 | 4.0 | 全pipeline成本已计。 |
| D9 可证伪性 | 4.5 | attempted-root不改善即判负。 |
| D10 基线强度 | 4.5 | pooled/regret-only同预算。 |
| D11 消融充分性 | 4.5 | target×calibrator与placebo充分。 |
| D12 OOD/真机 | 4.0 | LOFO primary、real secondary。 |
| D13 复现性 | 4.5 | 分母、branch、latency字段冻结。 |
| D14 CVPR契合度 | 4.5 | atlas具视觉可靠性价值。 |
| D15 风险/负结果 | 4.5 | repair/router可逐层删除。 |

平均分：**4.37/5.00**。最近邻已审：UAOR、VLA Calibration、VGA、GAM、SelectiveNet/Learning-to-Defer。未决非致命风险：多branch部署成本可能限制实用性，但方案不以省算为claim。硬门槛全过：**PASS**。
