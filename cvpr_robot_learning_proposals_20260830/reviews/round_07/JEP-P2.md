# Round 07 Review — JEP-P2

- Proposal-ID: JEP-P2
- Reviewed-Revision: r06
- File: `proposals/JEP-P2_object_contact_slots/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已加入NRI/JEPA×flat/typed 2×2、endpoint/ordered same-cost target、native/adapter winner与三层claim deletion，并设置event/resource gate。R6训练因素已正交，actual pilot=0明确。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 接触拓扑对操作预测重要。 |
| D2 失败模式清晰度 | 4.5 | transient/transaction失败具体。 |
| D3 创新性/最近邻 | 4.0 | 主要增量在ordered transaction。 |
| D4 机制因果闭环 | 4.5 | event→executor→prediction/scoring闭合。 |
| D5 技术正确性 | 4.5 | matching/transaction定义稳定。 |
| D6 可观测性/泄漏 | 4.5 | target与部署图分开。 |
| D7 数据可得性 | 3.5 | event coverage/abstain为0未知。 |
| D8 算力/工程 | 4.0 | 1.024M公式正确，完整训练网格未计。 |
| D9 可证伪性 | 4.5 | claim ladder充分。 |
| D10 基线强度 | 4.5 | NRI/C-SWM近同构强。 |
| D11 消融充分性 | 4.5 | representation×event-use闭合。 |
| D12 OOD/真机 | 4.0 | OOD/真机细节仍少。 |
| D13 复现性 | 4.0 | extractor schema好，ontology/split欠冻结。 |
| D14 CVPR契合度 | 4.5 | object-centric WAM契合。 |
| D15 风险/负结果 | 4.5 | benchmark-only降级明确。 |

平均分：**4.30/5.00**。D3/D7/D8/D13未过最终门槛；round<10，不通过。

## 数据/资源攻击面

1. `2k×8×4×16=1.024M`正确，但没有full stage或功效驱动的snapshot上限；200 smoke不能决定task-level primary样本数。
2. event extractor读sim causal body IDs/joints/force并做current/past matching；需明确GT body ID只定义label endpoint，association teacher用何输入，否则复现者会用完整GT association而产生过强target。
3. ordered event、endpoint压缩、flat tensor和typed executor共享label-generation cost合理，但四格+native/adapter的训练seed/GPU总量没计。
4. 数据缺task/asset/contact ontology split，尤其同一种gripper-object transaction跨task近重复；support overlap≥90%还可能与OOD冲突，需区分action support和asset OOD。

## 具体修改动作

1. 200 smoke后用snapshot/task ICC计算confirmatory N，设full env-step hard cap；列四格/seed训练GPU-hours。
2. 冻结target schema字段来源：sim ID/force仅target，current/past teacher输入、association confidence与oracle gap单独列；加单测拒绝future/full-track字段。
3. 发布ontology版本、edge/event枚举、null/abstain/censor code与partial-order序列化canonical form。
4. split按task template+asset+contact program family分组；action support overlap只在候选空间检验，不要求OOD asset重合。

## Round 08 验收条件

需给功效驱动full上限、target来源表、ontology canonical schema与family split。R8再压力测试遮挡、复合接触和真机外部有效性。
