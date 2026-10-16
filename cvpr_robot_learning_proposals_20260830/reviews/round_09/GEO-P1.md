# Round 09 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r08
- File: `proposals/GEO-P1_counterfactual_geometry/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已把主claim限为sim exact-intervention ranking，加入asset/task/renderer/severity矩阵、逐域support、3×30 root真机、GT/guard与benchmark降级；R8的伪OOD/真机过度claim已压住。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | geometry shortcut重要。 |
| D2 失败模式清晰度 | 4.5 | paired failure具体。 |
| D3 创新性/最近邻 | 4.0 | VGA/MECo/Cofact组合边界仍窄。 |
| D4 机制因果闭环 | 4.5 | relation supervision到ranking闭合。 |
| D5 技术正确性 | 4.5 | 公式/资源/支持域一致。 |
| D6 可观测性/泄漏 | 4.5 | checker/GT隔离。 |
| D7 数据可得性 | 4.0 | staged gate合理。 |
| D8 算力/工程 | 4.0 | 上限明确。 |
| D9 可证伪性 | 4.5 | 2×2与降级充分。 |
| D10 基线强度 | 4.5 | label-equal winner强。 |
| D11 消融充分性 | 4.5 | representation×objective完整。 |
| D12 OOD/真机 | 4.0 | claim边界已诚实。 |
| D13 复现性 | 4.5 | manifest完整。 |
| D14 CVPR契合度 | 4.0 | 需避免“合成因果”叙事反噬。 |
| D15 风险/负结果 | 4.5 | benchmark title可切换。 |

平均分：**4.30/5.00**。D3/D14未达门槛；round<10，不通过。

## 模拟审稿攻击

1. **“Self-fulfilling checker benchmark.”** `Y*`同时筛pair和训练，审稿人会认为primary只奖励checker ontology。正文首图要分开：checker只筛/辅训，primary由独立short-horizon utility；独立reward/checkpoint sensitivity放主表。
2. **“VGA + Cofact/CAST with geometry tokens.”** 标题若含“causal geometry”会被直接判组合创新。必须把贡献写成可证伪的relation-vs-generic 2×2与pair dataset，而非新因果理论。
3. **“Oracle supervision buys the gain.”** 主表第一组必须是label-equal winner；native baselines第二组，不得反过来。

## 修改与R10验收

建议主标题采用 **Geometry Counterfactual Ranking: Do Relation Tokens Beat Generic Deconfounding?**；摘要第一段明确“不识别现实因果效应”。贡献只列：pair protocol、2×2 falsification、ranking evidence。主图用实线deploy/虚线checker target。R10需出现一页“Reviewer attack→正文证据”表，并准备success<3pp的benchmark版标题/摘要。
