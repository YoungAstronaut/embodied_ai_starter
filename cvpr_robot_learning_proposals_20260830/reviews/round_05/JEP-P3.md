# Round 05 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r04
- File: `proposals/JEP-P3_stochastic_exogenous/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**（R4 conditional-e fatal已解除）

## 实际变更核验

r04 已让conditional `P(Y|a,e)`/ANOVA只读true-e cells，q监督与`-log∫stopgrad(p)q`/planner distillation分开，定义product characteristic kernel并加入K=4/8/16/32收敛。R4 fatal实质解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.5 | 外生交互重要。 |
| D2 | 4.5 | 三类反例清楚。 |
| D3 | 4.0 | benchmark/objective增量待证。 |
| D4 | 4.5 | conditional/q/marginal路径闭合。 |
| D5 | 4.5 | 错误e污染已修。 |
| D6 | 4.5 | e label仅target。 |
| D7 | 4.0 | factorial可生成。 |
| D8 | 3.5 | 数据段仍按K=4，K32收敛/完整预算未重算。 |
| D9 | 4.0 | regret/success/NLL/q coverage多重门槛未锁primary。 |
| D10 | 4.5 | 同factorial强基线足。 |
| D11 | 4.5 | interaction/q/planner消融足。 |
| D12 | 4.5 | OOD/真机贴合。 |
| D13 | 4.0 | kernel清楚，功效/预算缺。 |
| D14 | 4.5 | 契合CVPR。 |
| D15 | 4.5 | 可删JEPA保benchmark。 |

平均分：**4.30/5.00**。D8=3.5、D3/D9=4.0；R5不通过。

## 实验攻击面

1. **K合同漂移。** 15k groups成本按每cell K=4，但方法要求K32 reference/可能升级；需说明仅子集收敛还是全训练K。
2. **primary不唯一。** H1最直接是held-out action×e ranking regret；NLL/interaction norm/q coverage/OOD success应层级化。
3. **f_ae效果与q效果混淆。** oracle-e下interaction增益和learned-q下mixture闭环应做2×2；否则q改进可掩盖interaction无用。
4. **3 seeds/CI不足。** factorial group是cluster，action/e cells和K seeds非独立；task/group双层CI。

## 修改与R6验收

1. K4全数据+K4/8/16/32校准子集，或重算全K预算；阈值冻结。
2. primary锁定learned-q下held-out action×e normalized ranking regret，相对同数据最强baseline降20%。
3. 报`additive/interaction × oracle-e/learned-q` 2×2，分别判objective与deployment闭环。
4. factorial-group cluster、task-stratified CI和20%效应功效；success key secondary。

