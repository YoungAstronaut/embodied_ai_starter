# Round 10 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r09
- File: `proposals/JEP-P3_stochastic_exogenous/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 已删除JEPA branding，把唯一主张收缩为 balanced action×exogenous factorial interventions 与 interaction-aware action ranking；ANOVA/两latent不计新意，non-JEPA same-objective与CoCo为首组。true-e只用于训练cell/oracle，learned-q是部署primary。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 外生动态会破坏动作归因与规划。 |
| D2 失败模式清晰度 | 4.5 | action×exogenous交互最小反例明确。 |
| D3 创新性/最近邻 | 4.5 | 机器人factorial benchmark与q-planner合同清楚。 |
| D4 机制因果闭环 | 4.5 | balanced cells→interaction embedding→mixture planner闭合。 |
| D5 技术正确性 | 4.5 | conditional kernel embedding/centering与mixture正确。 |
| D6 可观测性/泄漏 | 4.5 | true-e/q-sampled/q-corrupt路径分离。 |
| D7 数据可得性 | 4.0 | 1.408M outcomes的factorial数据较重。 |
| D8 算力/工程 | 4.0 | 22.528M env steps可行但工程复杂。 |
| D9 可证伪性 | 4.5 | additive/interaction×q及K收敛可判负。 |
| D10 基线强度 | 4.5 | MDN-RSSM/non-JEPA/CoCo同目标强。 |
| D11 消融充分性 | 4.5 | observational/factorial×generic/ANOVA完整。 |
| D12 OOD/真机 | 4.0 | ID/combinatorial/μ-shift分层，real secondary。 |
| D13 复现性 | 4.5 | cells、K-prefix、centering与group split明确。 |
| D14 CVPR契合度 | 4.5 | 动态视觉规划benchmark契合。 |
| D15 风险/负结果 | 4.5 | dataset→objective→JEPA降级清楚。 |

平均分：**4.40/5.00**；关键维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **non-JEPA/CoCo持平：** 删除JEPA/model claim，保留ExoManip factorial benchmark。
- **interaction embedding改善但regret<3pp：** 只报告distribution fit，不宣称规划收益。
- **q在μ-shift失校：** 部署切conservative fallback并删除OOD planning claim。

## 未决非致命风险与最终修改

部署时若任何主结果偷用true-e即为fatal。r10 必须把 learned-q primary、true-e oracle、q-corrupt stress 三列固定在同一主表，并预注册q失校触发conservative fallback的阈值；追加 round_10/r10 log。当前只有9次refine。
