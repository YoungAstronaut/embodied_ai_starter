# Round 05 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r04
- File: `proposals/WAM-P3_hidden_physics_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r04 已把belief shift改为held-out-action predictive MMD/W1/regret，拆分nuisance deploy/target/eval字段，给fractional CVaR和1024 reference、Ljung-Box；functional措辞一致。R4建议已响应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.5 | hidden dynamics重要。 |
| D2 | 4.5 | prior/passive/probe清楚。 |
| D3 | 4.0 | nuisance分解增量待证。 |
| D4 | 4.5 | predictive belief→CVaR闭合。 |
| D5 | 4.5 | shift/CVaR定义清楚。 |
| D6 | 4.5 | deploy/target/eval分离。 |
| D7 | 4.0 | 数据可得。 |
| D8 | 4.0 | 64/1024离线可控。 |
| D9 | 4.0 | success/NLL/coverage/width多重门槛未定primary。 |
| D10 | 4.5 | 组合baseline强。 |
| D11 | 4.5 | factorial充分。 |
| D12 | 4.5 | OOD/真机贴合。 |
| D13 | 4.0 | estimator清楚，统计层级缺。 |
| D14 | 4.5 | 契合CVPR。 |
| D15 | 4.5 | 可辨识负边界强。 |

平均分：**4.33/5.00**。D3/D9=4.0；round<10，R5不通过。

## 实验攻击面

1. **primary过多。** success≥6pp、NLL降10%、coverage范围、width降15%是四重合取；若其中一项失败如何解释未规定。
2. **physics-only≥2× nuisance-only需要功效。** MMD/W1跨task尺度不同，需标准化并在同held-out action set配对。
3. **选择“第2次交互”可能后验。** 已同时报告1/2/4次，应预注册primary时点，其他为学习曲线。
4. **baseline适应信息必须同等。** PEARL/RMA/generic mixture需拿相同controller/detector confidence与history，否则显式nuisance模型多输入。

## 修改与R6验收

1. primary锁定被动第2次交互后的OOD action regret或success二选一；建议normalized action regret，success key secondary。
2. predictive MMD标准化、state/task cluster paired CI及2×effect功效。
3. 1/4次交互为secondary，不用取最好。
4. 所有context baselines共享相同deploy fields/history/sample/planner budget；仅factorization不同。

