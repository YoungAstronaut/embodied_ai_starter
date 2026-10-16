# Round 05 Review — STR-P3

- Proposal-ID: STR-P3
- Reviewed-Revision: r04
- File: `proposals/STR-P3_counterfactual_history/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r04 已采用pair-local共享library/seed/hash、task-normalized advantage，并重算accepted/attempted/CEM成本，MVP降为2k/M16/S4=4.096M、full 8k=131.072M及7天hard cap。R4成本问题已正面回应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.5 | aliasing重要。 |
| D2 | 4.5 | strict合同清楚。 |
| D3 | 4.5 | 公开commit overlap已核。 |
| D4 | 4.5 | pair→Q→history action闭合。 |
| D5 | 4.0 | library/adv修复，但自然primary的Q标签来源未闭合。 |
| D6 | 4.5 | target隔离。 |
| D7 | 4.0 | 合成可生成。 |
| D8 | 4.0 | 新go/no-go合理。 |
| D9 | 3.5 | primary“自然matched split cross-value regret”在公开AliasBench无pair/Q字段。 |
| D10 | 4.5 | baseline强。 |
| D11 | 4.5 | 模态/架构消融足。 |
| D12 | 4.0 | transfer方向正确。 |
| D13 | 4.0 | artifact好，自然label协议缺。 |
| D14 | 4.5 | 契合CVPR。 |
| D15 | 4.5 | feasibility/audit负价值强。 |

平均分：**4.27/5.00**。D9=3.5；R5不通过。

## 实验攻击面

1. **primary当前不可计算。** 自己的audit证明公开AliasBench无pair index/current tolerance/candidate-Q；若“自然matched split”只是研究者再生成的pairs，就不再是官方natural split，必须明示来源。
2. **transfer措辞含混。** “合成训练transfer降≥15%”应明确是regret相对下降；比较对象是random-pair还是原数据。
3. **MVP M16与full M64定义漂移。** go/no-go方法的action support不同，MVP效应不一定预测full；需要同一小子集上的M16/M64 sensitivity。
4. **自然难度匹配可能用结果变量。** 只能按预动作可见covariates匹配，不能按Q/regret后验匹配。

## 修改与R6验收

1. 二选一：primary改为合成strict held-out pair regret；自然官方任务只外效度。或明确在官方task code上重新采集trajectory/pair/Q的完整协议并称“reconstructed naturalistic split”。
2. 锁定transfer comparator与“15% regret reduction”公式。
3. 在同500 pairs上跑M16/M64/S4/S8 coverage/效应稳定性。
4. matching propensity仅用部署前covariates，冻结后再看outcome。

