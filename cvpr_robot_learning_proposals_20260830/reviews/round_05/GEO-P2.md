# Round 05 Review — GEO-P2

- Proposal-ID: GEO-P2
- Reviewed-Revision: r04
- File: `proposals/GEO-P2_contact_transition/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r04 已给cause-specific survival NLL及event/no-event/truncate手算，删除`L_cons`，拆开fixed-candidate score与argmax selection/success，并把probe上界改为GT-field经验accuracy。技术合同成立。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.5 | 接触候选排序重要。 |
| D2 | 4.5 | event/censor失败清楚。 |
| D3 | 4.0 | ontology增量待证。 |
| D4 | 4.5 | field→score闭合。 |
| D5 | 4.5 | survival/干预语义已修。 |
| D6 | 4.5 | target-only正确。 |
| D7 | 4.0 | 仿真标签可得。 |
| D8 | 4.0 | 1.024M MVP/latency合同可行。 |
| D9 | 4.0 | 仍列success/ranking/timing多个“主要终点”，无唯一检验。 |
| D10 | 4.5 | contact强基线足。 |
| D11 | 4.5 | 消融完整。 |
| D12 | 4.0 | OOD/真机合理。 |
| D13 | 4.0 | loss明确，统计计划缺。 |
| D14 | 4.5 | CVPR契合。 |
| D15 | 4.5 | benchmark负结果有价值。 |

平均分：**4.30/5.00**。D3/D9=4.0；round<10，R5不通过。

## 实验攻击面

1. **多primary导致可选择性报告。** success≥6pp、timing MAE≥20%、ranking≥5pp与combined≥2pp并列，未说明哪个失败会否定H1。
2. **统计单元不清。** “3 seeds/episode CI”会重复计算同snapshot的8 candidates×4 seeds；正确cluster应是snapshot/episode，task作更高层。
3. **数据规模矛盾。** MVP写2k snapshots，数据段又写6类task各5k episode；需区分label generation、training与full。
4. **真机100 trials/task功效未知。** 6pp绝对提升通常需远多于100次才能窄CI，除非paired/block设计显著降方差。

## 修改与R6验收

1. 锁定primary为同候选集的normalized selection regret或closed-loop success二选一；建议selection regret，success为key secondary。
2. snapshot cluster bootstrap+task-stratified CI；预注册多事件类型Holm/FDR。
3. 给MVP/full数据漏斗和训练/评测拆分。
4. 真机采用paired reset/block并做二项/配对功效；不足时明确仅外效度，不设6pp confirmatory门槛。

