# Round 11 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r10
- Responds-To: round_10
- Checked: 2026-08-30
- Lifecycle: `round_01`…`round_10`，10次实际refine
- Verdict: **PASS**

## Actual-diff核验

r10 新增 evaluator-A/B（不同checkpoint与reward schema）、四项冻结hash、方向一致且regret reduction差≤10pp的验收门槛；分歧时自动降为ontology-specific pair benchmark。该修改关闭了独立evaluator与relation ontology同偏的最后风险，不只是metadata改动。

| 维度 | 分数 | 最终理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | geometry shortcut重要、边界诚实。 |
| D2 失败模式清晰度 | 4.5 | 三类pair与hard-negative明确。 |
| D3 创新性/最近邻 | 4.5 | 新对象是双独立utility下的relation protocol。 |
| D4 机制因果闭环 | 4.5 | pair→干预→ranking闭合。 |
| D5 技术正确性 | 4.5 | support/NLL/regret一致。 |
| D6 可观测性/泄漏 | 4.5 | checker、target、deploy隔离。 |
| D7 数据可得性 | 4.0 | exact-reset仍需专门模拟器。 |
| D8 算力/工程 | 4.0 | staged budget可行。 |
| D9 可证伪性 | 4.5 | 双evaluator分歧会自动判负/降级。 |
| D10 基线强度 | 4.5 | VGA/Cofact/MECo label-equal。 |
| D11 消融充分性 | 4.5 | relation/generic×SCM/generic。 |
| D12 OOD/真机 | 4.0 | sim primary、real secondary。 |
| D13 复现性 | 4.5 | evaluator/version/hash与lineage齐全。 |
| D14 CVPR契合度 | 4.5 | 可复用视觉控制benchmark。 |
| D15 风险/负结果 | 4.5 | ontology-specific降级仍有价值。 |

平均分：**4.37/5.00**。最近邻已审：VGA v2、MECo-WAM v1、CofactVLA v1、GAM、ST-VLA。未决非致命风险：真实pair覆盖可能有限。所有维≥4.0、D3/D5/D6/D9=4.5、无fatal、refine=10：**PASS**。
