# Round 11 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r10
- Responds-To: round_10
- Checked: 2026-08-30
- Lifecycle: `round_01`…`round_10`，10次实际refine
- Verdict: **PASS**

## Actual-diff核验

r10 固定learned-q deployment、true-e oracle、q-corrupt三列共享candidates/samples/planner；部署schema拒绝true_e/e_label/intervention_seed，进入student/planner即fatal；q ECE或coverage失校则切冻结conservative baseline并删除mixture-planning claim。

| 维度 | 分数 | 最终理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 外生动态破坏动作归因。 |
| D2 失败模式清晰度 | 4.5 | interaction最小反例明确。 |
| D3 创新性/最近邻 | 4.5 | ExoManip factorial protocol边界清楚。 |
| D4 机制因果闭环 | 4.5 | cells→interaction→q-mixture planner。 |
| D5 技术正确性 | 4.5 | kernel embedding/centering正确。 |
| D6 可观测性/泄漏 | 4.5 | true-e schema fatal guard。 |
| D7 数据可得性 | 4.0 | factorial outcomes较重。 |
| D8 算力/工程 | 4.0 | 22.528M steps与grid复杂。 |
| D9 可证伪性 | 4.5 | q corruption/calibration触发删除claim。 |
| D10 基线强度 | 4.5 | non-JEPA/MDN-RSSM/CoCo。 |
| D11 消融充分性 | 4.5 | data×objective与additive×interaction。 |
| D12 OOD/真机 | 4.0 | μ-shift/real仅secondary。 |
| D13 复现性 | 4.5 | cell/K/q schema与fallback冻结。 |
| D14 CVPR契合度 | 4.5 | 动态视觉规划benchmark成立。 |
| D15 风险/负结果 | 4.5 | dataset/objective降级路径清楚。 |

平均分：**4.40/5.00**。最近邻已审：CoCo v1、JEPA Safety v1、Sawada et al. 2018、JEPA-WM study、MDN-RSSM。未决非致命风险：balanced factorial data与自然μ-shift存在分布差。硬门槛全过：**PASS**。
