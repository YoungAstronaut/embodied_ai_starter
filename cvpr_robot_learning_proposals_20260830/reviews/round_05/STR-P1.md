# Round 05 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r04
- File: `proposals/STR-P1_event_intent_reset/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r04 已用5-head+独立split conformal、α/4 simultaneous LCB后选max；target CI只作权重，oracle coverage仅evaluator，八格truth table删除冗余direct-S。R4技术问题已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.5 | reset问题重要。 |
| D2 | 4.5 | N/F/C和反例清楚。 |
| D3 | 4.0 | paired utility增量待证。 |
| D4 | 4.5 | evidence→LCB→reset闭合。 |
| D5 | 4.5 | simultaneous selection正确。 |
| D6 | 4.5 | oracle移出部署。 |
| D7 | 4.0 | 数据可得。 |
| D8 | 4.0 | K/S/H可控。 |
| D9 | 4.5 | primary已锁恢复步数，kill criteria强。 |
| D10 | 4.5 | gate baseline充分。 |
| D11 | 4.5 | 消融足。 |
| D12 | 4.0 | 真机外测合理。 |
| D13 | 4.0 | 区间合同好，recovery定义/功效缺。 |
| D14 | 4.5 | 契合CVPR。 |
| D15 | 4.5 | benchmark负价值强。 |

平均分：**4.33/5.00**。D3=4.0；round<10，R5不通过。

## 实验攻击面

1. **恢复步数未操作化。** 必须定义从event到何种状态算“恢复”（首次成功动作、回到轨迹tube、持续L步无失败），否则可后验挑最有利定义。
2. **event family/prevalence。** 汇总步数会由高频易事件主导；应以family-macro primary或预注册权重。
3. **interval目标与判定不一致。** 名义FWER95%，判负却容许empirical coverage≥93%；需给有限样本CI而非点估计宽松2pp。
4. **30k episode功效不等于独立event数。** 同snapshot的3+3 hard pairs相关，需snapshot/event cluster及task层级。

## 修改与R6验收

1. recovery定义和censor规则冻结；未恢复episode作为right-censored并用survival/mean restricted recovery time。
2. primary用event-family macro restricted recovery time，success/false reset secondary。
3. 对FWER coverage给binomial/cluster CI，lower bound≥.93或名义误差解释。
4. 按snapshot/event cluster、task-stratified paired CI与30%效应功效。

