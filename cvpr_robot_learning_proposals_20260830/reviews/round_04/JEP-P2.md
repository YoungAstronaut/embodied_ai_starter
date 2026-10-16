# Round 04 Review — JEP-P2

- Proposal-ID: JEP-P2
- Reviewed-Revision: r03
- File: `proposals/JEP-P2_object_contact_slots/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / REVISE**（candidate support/stop-gradient/matching显著增强；transaction标签置换与probe上界仍未定义）

## 实际变更核验

r03 已闭合`2k×8×4×16=1.024M`全候选event target，typed tensor stop-gradient后送scorer，加入action-ID probe，定义±1frame typed Hungarian/null/transaction/abstain matching及并发/contact/attach-detach/handover单测；NRI/C-SWM共享target/executor/scorer。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 接触拓扑变化是固定slot真实盲点。 |
| D2 失败模式清晰度 | 4.5 | transient/transaction/illegal edit清楚。 |
| D3 创新性/最近邻 | 4.0 | event transaction的独立价值待实证。 |
| D4 机制因果闭环 | 4.5 | candidate→event→executor→future→score闭合。 |
| D5 技术正确性 | 4.0 | support/matching改善；transaction ID permutation和probe基准有歧义。 |
| D6 可观测性/泄漏 | 4.5 | future event仅target，full trajectory只oracle。 |
| D7 数据可得性 | 4.0 | 1.024M-step MVP可行。 |
| D8 算力/工程 | 4.0 | decoder/executor复杂但有单测。 |
| D9 可证伪性 | 4.5 | fixed-action edit干预/同标签baseline强。 |
| D10 基线强度 | 4.5 | NRI/C-SWM/contact WM/persistent slots充分。 |
| D11 消融充分性 | 4.5 | event/legality/cycle/触觉/labels全面。 |
| D12 OOD/真机 | 4.0 | 遮挡/同类实例/marker评测合理。 |
| D13 复现性 | 4.0 | matching显著增强；group label规范缺。 |
| D14 CVPR 契合度 | 4.5 | object-centric contact dynamics强契合。 |
| D15 风险/负结果 | 4.5 | topology benchmark边界有价值。 |

平均分：**4.30/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10且D3/D5未达门槛，R4不通过。

## Top 问题与技术证据

1. **major — transaction-id是任意标签。** 预测group ID=2与GT group ID=7可以表示同一分区；若直接typed tensor监督/匹配ID，会引入无意义label permutation。应以event co-membership矩阵或canonical group ordering表达事务。
2. **major — “GT event可解释Bayes accuracy”不可知。** 与GEO-P2同样，应改为held-out probe在GT event tensor上的经验上界，而非Bayes最优。
3. **technical — abstain造成选择偏差。** ambiguous/tie不训练且评测只作coverage，若恰好是最难handover，F1可被抬高；必须固定coverage或按abstain风险报告selective curve。
4. **minor — fixed-action success表述仍需拆分。** 固定candidate时wrong event只能改score；closed-loop success变化来自最终候选选择。

## 具体修改动作

1. transaction用pairwise same-group relation或按最早τ/最小edge canonical排序，loss对group label置换不变。
2. probe比较predicted-event与GT-event输入，同模型/同split；阈值写经验差。
3. 报event risk-coverage/AURC，并让abstain样本进入closed-loop主结果的fallback成本。
4. 分开candidate score intervention和argmax selection intervention。

## Round 05 验收条件

- [ ] transaction表示与loss对group-ID置换不变。
- [ ] action-ID shortcut probe使用可计算经验上界。
- [ ] abstain按fixed coverage/risk计入，不可静默删除难例。
- [ ] fixed candidate与closed-loop selection指标语义一致。

