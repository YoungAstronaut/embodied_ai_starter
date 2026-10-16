# Round 09 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r08
- File: `proposals/JEP-P3_stochastic_exogenous/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已将唯一主线改为balanced factorial+interaction，分ID/combinatorial/μshift，加入q失校conservative切换、real logger/guard与balanced→ANOVA→JEPA层级；R8 OOD/安全边界已响应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 外生交互归因重要。 |
| D2 失败模式清晰度 | 4.5 | mean/variance/mode反例强。 |
| D3 创新性/最近邻 | 4.5 | balanced manipulation benchmark+deploy mixture命题明确。 |
| D4 机制因果闭环 | 4.5 | factorial→q→ranking闭合。 |
| D5 技术正确性 | 4.5 | functional ANOVA/measure严谨。 |
| D6 可观测性/泄漏 | 4.5 | e/logger隔离。 |
| D7 数据可得性 | 4.0 | ExoManip可生成。 |
| D8 算力/工程 | 4.0 | model grid重但闭合。 |
| D9 可证伪性 | 4.5 | 三层claim ladder强。 |
| D10 基线强度 | 4.5 | CoCo/Sawada/non-JEPA齐。 |
| D11 消融充分性 | 4.5 | data×objective与deploy 2×2完整。 |
| D12 OOD/真机 | 4.0 | μshift/guard合理，真机仍secondary。 |
| D13 复现性 | 4.5 | cell/kernel/measure/seed完整。 |
| D14 CVPR契合度 | 4.5 | 动态视觉世界模型契合。 |
| D15 风险/负结果 | 4.5 | benchmark可独立成立。 |

平均分：**4.40/5.00**。round<10，不通过。

## 模拟审稿攻击

1. **“Functional ANOVA and two-latent models are old.”** 主张只在balanced action×e benchmark与learned-q planning，不宣称理论新。
2. **“CoCo already does counterfactual controllability.”** 同4×4 groups、公式/target差异与CoCo持平判负必须主表。
3. **“JEPA is branding.”** non-JEPA same-objective进入winner；持平时标题、摘要、图都删JEPA，而非只降一句。

## 修改与R10验收

标题建议 **ExoManip: Balanced Action–Exogenous Interventions for Interaction-Aware World Models**，不把JEPA写标题。贡献层级严格是dataset→interaction objective→JEPA optional。主图画true-e target、learned-q deploy和conservative fallback。R10准备generic conditional持平时纯factorial benchmark版本。
