# Round 10 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r09
- File: `proposals/JEP-P1_action_equivalence/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 明确 pseudometric/action bisimulation 不新，独特对象是 local 3D contact matched-outcome schema、canonical assignment strata 与 same-backbone recursive-vs-local target protocol；Action-Bisim v3 native/adapter位于首行，原equivalence-class错误未复发。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 局部动作冗余重要但范围受限。 |
| D2 失败模式清晰度 | 4.5 | same-state alternative-action结果差异明确。 |
| D3 创新性/最近邻 | 4.5 | 新意在3D matched-outcome协议而非metric。 |
| D4 机制因果闭环 | 4.5 | outcome metric→target→canonicalizer→regret闭合。 |
| D5 技术正确性 | 4.5 | W1+TV ground metric、null cost和triangle test正确。 |
| D6 可观测性/泄漏 | 4.5 | GT UUID仅oracle，deploy assignment独立。 |
| D7 数据可得性 | 4.0 | S32 matched outcomes资源高。 |
| D8 算力/工程 | 4.0 | OT缓存可行但8-day gate紧。 |
| D9 可证伪性 | 4.5 | metric×JEPA 2×2与planner regret可判负。 |
| D10 基线强度 | 4.5 | Action-Bisim native/adapter及non-JEPA齐全。 |
| D11 消融充分性 | 4.5 | local/recursive target同backbone。 |
| D12 OOD/真机 | 4.0 | morphology/camera外推有coverage gate。 |
| D13 复现性 | 4.5 | 单位、slot、OT和split均闭合。 |
| D14 CVPR契合度 | 4.5 | 3D动作后果测量协议具视觉贡献。 |
| D15 风险/负结果 | 4.5 | ActMetric benchmark可独立成立。 |

平均分：**4.37/5.00**；关键维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **Action-Bisim adapter持平：** 删除local target method，仅保留ActMetric-3D benchmark。
- **control regret <3pp：** metric proxy不可冒充控制收益。
- **跨embodiment coverage<90%：** 删除canonical transfer，仅报告平台内结果。

## 未决非致命风险与最终修改

canonical assignment仍可能借助稳定detector ordering形成shortcut。r10 必须把 duplicate/missing/corrupted detector 的abstention、assignment coverage与regret联合成一张主表，并明确任何GT UUID只出现在oracle列；追加 round_10/r10 log。当前仅9次refine。
