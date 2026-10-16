# Round 03 Summary — 机制因果链与信息路径

- Review date: 2026-08-30
- Input revisions: 12/12 均为 r02，且 `Responds-To-Review: round_02`
- Refinement logs: 12/12 均含 `## round_02 / r02`
- Individual reviews: 12/12 已完成
- Round policy: round<10，全部 **FAIL / REVISE**
- Score range: 3.97–4.27

## 汇总表

| Proposal-ID | Revision | 平均分 | 关键低维 | Fatal flaw | R3 结论 | 下一轮首要动作 |
|---|---:|---:|---|---|---|---|
| GEO-P1 | r02 | 3.97 | D6=3.0, D4/D8/D13=3.5 | **是** | FAIL / FATAL-IN-r02 | 证明 `type_embedding` 部署来源；checker type 严禁进 student |
| GEO-P2 | r02 | 4.23 | D13=3.5 | 否 | FAIL | field/scorer stop-gradient、action-code probe、全候选 target support |
| GEO-P3 | r02 | 4.23 | D13=3.5 | 否 | FAIL | on-manifold relation repair；三分支全链路成本 |
| WAM-P1 | r02 | 4.20 | D5=3.5, D13=3.5 | 否 | FAIL | 消除 `A_mj·ℓ_mj` 重复计似然；完整 proper score |
| WAM-P2 | r02 | 4.17 | D4/D5/D13=3.5 | 否 | FAIL | myopic VOC 与非单调收益一致化；continuation-value baseline |
| WAM-P3 | r02 | 4.27 | D13=3.5 | 否 | FAIL | correlated innovation 与 nuisance intervention；CVaR estimator |
| STR-P1 | r02 | 4.17 | D4/D5/D13=3.5 | 否 | FAIL | deployed gate 必须直接使用 paired reset value |
| STR-P2 | r02 | 4.27 | D13=3.5 | 否（R2 fatal解除） | FAIL | 可部署 latency quantile/chance-constrained scheduler |
| STR-P3 | r02 | 4.20 | D5/D13=3.5 | 否 | FAIL | 闭合连续 policy 与离散 Q-library 支持域；运行 AliasBench audit |
| JEP-P1 | r02 | 4.17 | D8/D13=3.5 | 否 | FAIL | 可变对象/dustbin 下 metric 性；排 action-code shortcut |
| JEP-P2 | r02 | 4.20 | D5/D13=3.5 | 否 | FAIL | per-candidate event target；partial-order matching；梯度边界 |
| JEP-P3 | r02 | 4.23 | D5/D13=3.5 | 否 | FAIL | 从 mean ANOVA 升级/收缩为明确 distributional object |

## 本轮独立结论

R2 的 STR-P2 fatal 已通过真正改变模型范式而解除：r02 只使用标准 conditional chunk flow 的完整 chunk multi-exit，明确 solver-time 与 physical-time 两轴，SFP 不再承担不相容的 checkpoint/teacher 角色。

R3 新发现 GEO-P1 的信息路径 fatal。正文由 full-state checker 产生 typed entity pair，relation adapter 又直接使用 `type_embedding`，但只为 masks 给出部署 detector 替代，没有给 relation type 的部署来源。按当前可实现解释，checker type 会进入 student/action query；这不是训练 target 的正常 privileged supervision，而是部署不可得字段直接旁路。必须在 r03 中删除该旁路或把 type 改为部署可预测的 soft variable。

其余 11 份未发现未来帧、GT state、reward、seed、evaluator stratum 直接进入部署 action 的致命泄漏；但出现多处“target-only 已隔离、机制仍未闭合”的技术问题：

1. **训练目标与部署决策量不一致。** STR-P1 训练 paired reset value，部署却比较 intent log-probability；WAM-P2 允许边际收益负后再正，却用一步负 VOC 立即停止。
2. **中间变量可与 action 串谋。** GEO-P2 contact field、JEP-P2 event sequence 在后期联合训练时可能编码 candidate identity；需要 typed/discrete bottleneck、stop-gradient 和 fixed-action/wrong-intermediate intervention。
3. **oracle 筛选不等于泄漏，但会造成选择偏差。** GEO-P1 的 accepted pairs、STR-P3 的 strict pairs 都由 full-state/future value 过滤；student 字段虽干净，仍需 matched rejected/natural-domain controls。
4. **数学对象必须唯一。** WAM-P1 association likelihood 可能被 `A·ℓ` 重复计；JEP-P1 的 dustbin/对象匹配未证明保持 triangle；JEP-P3 在条件均值 ANOVA 与 stochastic NLL 之间摇摆。
5. **所有 candidate-conditioned 方法都要证明 target 支持。** GEO-P2、JEP-P2、STR-P3 需要明确同 snapshot 下哪些候选被真实 exact-reset rollout，不能用 executed-action 标签外推覆盖部署候选。

## Round 04 统一验收条件 — 技术正确性压力测试

1. GEO-P1 先解除 relation-type fatal；任何 checker/evaluator 字段进入 student batch 均直接拒绝。
2. 每份给一个可手算/逐步模拟的最小例，验证核心公式：Bayes update、stopping rule、reset gate、runtime scheduler、OT metric、partial-order matching或distributional ANOVA。
3. 所有中间表征进入 scorer/planner 前标注梯度边界，并加入 action-code/metadata shortcut probe。
4. 所有 oracle-generated target 列出 estimand、采样单元、support、stop-gradient、部署替代与阳性泄漏控制。
5. 技术修复不得用收缩措辞掩盖：若改 estimand/decision rule，必须同步标题、H1、loss、部署伪代码、实验和判负条件。

## Round 04 优先级

- **P0**：GEO-P1（relation type fatal）。
- **P1**：WAM-P2、STR-P1、STR-P3、WAM-P1、JEP-P3（公式/决策量不一致）。
- **P2**：GEO-P2、GEO-P3、WAM-P3、STR-P2、JEP-P1、JEP-P2（梯度、support、metric/runtime合同）。

