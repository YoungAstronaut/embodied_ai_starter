# Round 05 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r04
- File: `proposals/JEP-P1_action_equivalence/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r04 已定义deploy role-instance slots、同类orbit、fixed node+一次global edge/contact+collision product metric，GT UUID仅oracle，并加入duplicate/missing adversarial例。R4 metric问题已响应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.0 | action metric重要。 |
| D2 | 4.5 | 反例清楚。 |
| D3 | 4.0 | 最近邻密集。 |
| D4 | 4.5 | metric→planner闭合。 |
| D5 | 4.0 | role assignment进入train target还是仅eval仍不清。 |
| D6 | 4.5 | GT UUID隔离。 |
| D7 | 4.0 | MVP可得。 |
| D8 | 3.5 | full OT/seed成本高。 |
| D9 | 4.0 | primary清楚但无power/secondary控制价值门槛。 |
| D10 | 4.5 | Action-Bisim/non-JEPA强。 |
| D11 | 4.5 | 消融足。 |
| D12 | 4.0 | OOD/真机合理。 |
| D13 | 4.0 | schema增强，统计缺。 |
| D14 | 4.5 | 契合CVPR。 |
| D15 | 4.5 | dataset/metric负价值。 |

平均分：**4.20/5.00**。D8=3.5、D3/D5/D9=4.0；R5不通过。

## 实验攻击面

1. **primary regret依赖value head而非纯metric。** metric可改善但`L_rank`单独带来regret；必须用2×2 `metric loss on/off × JEPA/non-JEPA`分离。
2. **role assignment噪声的公平性。** training `d_phys`若用GT UUID canonicalization而test用deploy assignment，domain gap；若主target也用deploy assignment，需明确错误标签如何处理。
3. **20%效应无功效。** states内action pairs高度相关，不能把`32 choose 2`当独立；state才是cluster。
4. **跨embodiment可能稀释primary。** 应预注册单平台primary、跨embodiment key secondary或反之。

## 修改与R6验收

1. 完整2×2分解metric supervision与JEPA structure，primary comparator为Action-Bisim direct同input。
2. 主target/eval使用同deploy canonicalizer；GT UUID只noise oracle，并报assignment分层。
3. state-cluster power分析检测20% regret下降，task/embodiment层级CI。
4. primary域与跨embodiment层级冻结，不能失败后收缩而仍称原claim通过。

