# Round 06 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r05
- File: `proposals/JEP-P1_action_equivalence/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已加入 metric supervision×JEPA 完整2×2，把 deploy canonicalizer 下单平台 held-out action ranking regret设为唯一primary，并指定Action-Bisimulation direct、state/task功效和GT UUID oracle边界。R5 的贡献混叠问题明显改善。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 动作冗余与局部后果表示有价值。 |
| D2 失败模式清晰度 | 4.5 | 同state动作后果与metric反例明确。 |
| D3 创新性/最近邻 | 4.0 | Action-Bisim已覆盖pseudometric，增量边界窄。 |
| D4 机制因果闭环 | 4.5 | outcome metric→representation→candidate ranking闭合。 |
| D5 技术正确性 | 4.5 | ground metric、null cost、triangle tests具体。 |
| D6 可观测性/泄漏 | 4.5 | role assignment deploy-only，UUID oracle隔离。 |
| D7 数据可得性 | 4.0 | matched-seed future outcome可生成。 |
| D8 算力/工程 | 4.0 | S32与跨平台adapter有成本。 |
| D9 可证伪性 | 4.5 | direct baseline持平即判负。 |
| D10 基线强度 | 4.0 | Action-Bisim direct 的原生/同target差异未冻结。 |
| D11 消融充分性 | 4.5 | metric×JEPA 2×2已是强设计。 |
| D12 OOD/真机 | 4.0 | 跨embodiment secondary，真机扰动有限。 |
| D13 复现性 | 4.5 | metric、assignment、cluster合同细。 |
| D14 CVPR契合度 | 4.0 | 视觉表征契合，但理论增量需强实验。 |
| D15 风险/负结果 | 4.5 | 可删除JEPA或退化为representation结果。 |

平均分：**4.27/5.00**。D3/D10未达门槛；round<10，不通过。

## Top 问题与证据缺口

1. **“Action-Bisimulation direct”可能被弱化。** 原方法的递归/价值结构与本法 immediate matched-outcome pseudometric并非同target；若只做“direct”简化，审稿人会质疑没有忠实复现最强理论基线。
2. **同metric non-JEPA已有，但最强 comparator 规则忽略它。** validation上 `non-JEPA+same metric`可能强于Action-Bisim direct，primary应对所有deployable格的winner，而非固定论文名。
3. **canonicalizer是共享前提还是贡献尚不清楚。** direct baseline必须拿同role detector/order/tracker与abstain；还应报告assignment错误分层，防metric收益只是匹配质量差异。

## 具体修改动作

1. Action-Bisim做两版：paper-faithful recursive/native objective；same-data adapter（相同RGB/history/candidate/canonicalizer与local ground outcome）。代码/公式差异逐字段冻结。
2. 最强 comparator改为validation winner `max{Action-Bisim-native, Action-Bisim-adapter, non-JEPA+same metric, JEPA without metric}`，test不重选。
3. 扩展2×2报告主效应之外，再加 `target {Action-Bisim recursive, local matched-outcome}` 的危险对照；至少在同一non-JEPA backbone上比较，确认收益不是换target。
4. 所有格共享canonicalizer并按assignment正确/错误/abstain分层；oracle UUID只量上界，不能选择test operating point。

## Round 07 验收条件

需补Action-Bisim native/adapter复现合同、validation winner规则、同backbone target对照和assignment分层；R7还需给S32数据量、triangle测试及adapter runtime预算。
