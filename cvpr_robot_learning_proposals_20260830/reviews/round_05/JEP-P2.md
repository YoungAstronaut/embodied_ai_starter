# Round 05 Review — JEP-P2

- Proposal-ID: JEP-P2
- Reviewed-Revision: r04
- File: `proposals/JEP-P2_object_contact_slots/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r04 已把transaction改为co-membership矩阵、probe改经验上界、abstain纳入90%coverage AURC/fallback，并拆开score与selection success。R4技术建议均响应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.5 | topology重要。 |
| D2 | 4.5 | transient/transaction清楚。 |
| D3 | 4.0 | event增量待证。 |
| D4 | 4.5 | event→planner闭合。 |
| D5 | 4.5 | permutation/abstain修复。 |
| D6 | 4.5 | target-only正确。 |
| D7 | 4.0 | 数据可得。 |
| D8 | 4.0 | MVP可行。 |
| D9 | 3.5 | primary是event F1，而H1是candidate ranking/planning收益。 |
| D10 | 4.5 | 同标签NRI/C-SWM强。 |
| D11 | 4.5 | 消融足。 |
| D12 | 4.0 | 真机合理。 |
| D13 | 4.0 | matching清楚，power缺。 |
| D14 | 4.5 | 契合CVPR。 |
| D15 | 4.5 | topology benchmark有价值。 |

平均分：**4.27/5.00**。D9=3.5；R5不通过。

## 实验攻击面

1. **primary不能证H1。** 90%coverage event F1≥.80可在candidate ranking/success完全无改善时通过；H1明确声称更好排序拓扑动作。
2. **absolute F1无baseline差。** NRI+同labels若F1=.82、本法.80仍满足primary；需relative comparator。
3. **event cluster伪重复。** 同snapshot的8 candidates/4 seeds及同transaction多events相关，snapshot/task才是cluster。
4. **coverage阈值的calibration/test分割未说明。** 必须避免test调到90%。

## 修改与R6验收

1. primary改为90% event coverage下同候选集selection regret，要求相对NRI+same labels降≥20%；event F1为mechanism endpoint。
2. closed-loop success为key secondary，若<3pp则只保留representation/benchmark claim。
3. calibration split冻结abstain threshold；snapshot-cluster/task-stratified CI与power。
4. NRI/C-SWM共享event confidence/fallback，不只共享labels/executor。

