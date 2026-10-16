# Round 09 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r08
- File: `proposals/JEP-P1_action_equivalence/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已前置pseudometric不新，拆adapter regimes与asset/camera/morphology轴，设置coverage<90%、GT/guard和JEPA/metric删claim ladder；R8跨embodiment overclaim已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | action-effect表示有价值。 |
| D2 失败模式清晰度 | 4.5 | proxy与metric反例明确。 |
| D3 创新性/最近邻 | 4.0 | Action-Bisim覆盖理论核心。 |
| D4 机制因果闭环 | 4.5 | outcome metric→ranking闭合。 |
| D5 技术正确性 | 4.5 | pseudometric/OT严谨。 |
| D6 可观测性/泄漏 | 4.5 | GT/UUID隔离。 |
| D7 数据可得性 | 4.0 | ActMetric可生成。 |
| D8 算力/工程 | 4.0 | S32/OT gate明确。 |
| D9 可证伪性 | 4.5 | Action-Bisim/JEPA删除规则强。 |
| D10 基线强度 | 4.5 | native/adapter危险基线齐。 |
| D11 消融充分性 | 4.5 | backbone×metric+target充分。 |
| D12 OOD/真机 | 4.0 | adapter边界诚实。 |
| D13 复现性 | 4.5 | metric/lineage完整。 |
| D14 CVPR契合度 | 4.0 | 更像benchmark，控制增量需谨慎。 |
| D15 风险/负结果 | 4.5 | ActMetric benchmark有价值。 |

平均分：**4.30/5.00**。D3/D14未达门槛；round<10，不通过。

## 模拟审稿攻击

1. **“Action-Bisimulation already solves this.”** 相关工作不能只做字段表；必须说明recursive controllability target vs local matched physical outcome，并用same backbone target对照。
2. **“Equivalence was abandoned, so what is new?”** 标题/文件夹可保ID，但论文一律使用local action-effect pseudometric，不再出现class/equivalence贡献。
3. **“Canonicalization does all the work.”** 所有基线共享canonicalizer，assignment strata与oracle UUID gap进主表。

## 修改与R10验收

标题建议 **ActMetric-3D: Matched-Outcome Action Pseudometrics for Visual Planning**，JEPA放副标题或方法格。贡献只列dataset/metric supervision/2×2。R10准备Action-Bisim持平时纯benchmark版本，并确保cross-embodiment只secondary。
