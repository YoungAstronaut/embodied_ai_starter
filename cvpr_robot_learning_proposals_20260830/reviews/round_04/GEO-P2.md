# Round 04 Review — GEO-P2

- Proposal-ID: GEO-P2
- Reviewed-Revision: r03
- File: `proposals/GEO-P2_contact_transition/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / REVISE**（target support/梯度边界已闭合；censor likelihood 与 fixed-action intervention需形式化）

## 实际变更核验

r03 已将 typed field stop-gradient 后送 scorer，加入 action-ID probe，明确 `snapshot×8×4×16=1.024M` env steps、所有候选 exact-reset、censor/support≥90%、fixed-action wrong-field阈值和全链路 p95/p99。R3 的串谋/support问题得到实质回应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 接触转移直接决定精细操作成败。 |
| D2 失败模式清晰度 | 4.5 | event ontology/censor/候选分叉清楚。 |
| D3 创新性/最近邻 | 4.0 | explicit typed field对latent rollout的增量仍需实验。 |
| D4 机制因果闭环 | 4.5 | candidate→stop-grad field→score链已闭合。 |
| D5 技术正确性 | 4.0 | 支持域已补；survival likelihood、`L_cons`和干预执行语义仍不唯一。 |
| D6 可观测性/泄漏 | 4.5 | GT contact/pose只作target/oracle。 |
| D7 数据可得性 | 4.0 | 1.024M steps MVP可行，真机标签仍需audit。 |
| D8 算力/工程 | 4.0 | 全链路尾延迟合同合理。 |
| D9 可证伪性 | 4.5 | fixed-action wrong-field、latent/field四路和probe强。 |
| D10 基线强度 | 4.5 | ContactGuard/ContactWorld/触觉等强基线充分。 |
| D11 消融充分性 | 4.5 | field字段、frame、teacher noise和组合均可拆。 |
| D12 OOD/真机 | 4.0 | 摩擦/材质/pose noise/fallback覆盖。 |
| D13 复现性 | 4.0 | manifest与单位明显加强；loss细节仍缺。 |
| D14 CVPR 契合度 | 4.5 | 视觉接触和候选规划契合。 |
| D15 风险/负结果 | 4.5 | 可退化为ontology/benchmark而不强保方法claim。 |

平均分：**4.30/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10 且 D3/D5 未达硬门槛，R4 不通过。

## Top 问题与技术证据

1. **major — right-censor 不能只写一个名字。** event hazard、first-event time、多事件、无event与truncated episode共同存在；需要离散 survival likelihood，明确 risk set和每类event竞争关系，不能对censored τ回归。
2. **major — fixed-action/wrong-field 的“success下降”语义混淆。** 若实际执行动作固定，field只改内部score而不会改变物理success；若field改变被选候选，则最终执行动作并未固定。应分别报告固定candidate的score变化与经过argmax后的selection/success。
3. **technical — “GT field可解释Bayes accuracy”不可直接观测。** 应改为同样probe在GT typed field上的held-out accuracy上界，而不是声称知道Bayes最优值。
4. **technical — `L_cons` 未定义。** 它可能重复SE(3)/mode约束或引入未来路径，需给公式。

## 具体修改动作

1. 写出 cause-specific discrete hazard NLL、censor mask与多事件处理；用`event@3`、`no event through H`、`truncated@5`三个最小序列手算loss。
2. 把机制干预拆成 `fixed candidate score intervention` 与 `candidate-set selection intervention`，只后者评价closed-loop success。
3. 将probe阈值改为“student predicted field probe相对GT-field probe+10pp”，同split/同容量。
4. 明确 `L_cons` 的输入、target、梯度和与其他loss不重复之处。

## Round 05 验收条件

- [ ] survival/censor loss可逐序列计算，多事件与truncation无歧义。
- [ ] fixed-action score效应与selection后success效应不混写。
- [ ] action-ID probe上界可经验计算，不使用不可知Bayes accuracy。
- [ ] `L_cons`公式与字段路径完整。

