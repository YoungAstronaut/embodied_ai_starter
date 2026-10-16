# Round 11 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r10
- Responds-To: round_10
- Checked: 2026-08-30
- Lifecycle: `round_01`…`round_10`，10次实际refine
- Verdict: **PASS**

## Actual-diff核验

r10 在clean/duplicate/missing/corrupted-order四条件下联报abstention、assignment coverage/error与regret，且所有非oracle列只用deploy detector；corrupted-order coverage不降但error/regret恶化>10pp即判stable-order shortcut。GT UUID被硬限于oracle列。

| 维度 | 分数 | 最终理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 局部动作冗余有价值但域窄。 |
| D2 失败模式清晰度 | 4.5 | matched outcome明确。 |
| D3 创新性/最近邻 | 4.5 | ActMetric-3D协议超出Action-Bisim概念。 |
| D4 机制因果闭环 | 4.5 | outcome metric→target→regret。 |
| D5 技术正确性 | 4.5 | W1+TV/null/OT metric正确。 |
| D6 可观测性/泄漏 | 4.5 | GT UUID oracle-only且shortcut probe。 |
| D7 数据可得性 | 4.0 | S32 outcomes成本高。 |
| D8 算力/工程 | 4.0 | OT/cache可行但昂贵。 |
| D9 可证伪性 | 4.5 | detector-order probe直接判负。 |
| D10 基线强度 | 4.5 | Action-Bisim native/adapter。 |
| D11 消融充分性 | 4.5 | metric×JEPA与local/recursive。 |
| D12 OOD/真机 | 4.0 | coverage gate限制外推。 |
| D13 复现性 | 4.5 | role/slot/unit/condition字段齐全。 |
| D14 CVPR契合度 | 4.5 | 3D动作结果benchmark成立。 |
| D15 风险/负结果 | 4.5 | pure benchmark可独立成立。 |

平均分：**4.37/5.00**。最近邻已审：Action-Bisim v3、VLA-JEPA、V-JEPA2-AC、What Matters for Latent Actions、JEPA-WM study。未决非致命风险：跨embodiment canonical roles可能覆盖不足。硬门槛全过：**PASS**。
