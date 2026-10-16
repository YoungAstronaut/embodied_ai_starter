# Round 02 Summary — 最近邻与创新边界

- Review date: 2026-08-30
- Input revisions: 12/12 均为 r01，且 `Responds-To-Review: round_01`
- Individual reviews: 12/12 已完成
- Round policy: round<10，全部 **FAIL / REVISE**
- Score range: 3.93–4.27

## 汇总表

| Proposal-ID | Revision | 平均分 | 最低维 | Fatal flaw | R2 结论 | 下一轮首要动作 |
|---|---:|---:|---|---|---|---|
| GEO-P1 | r01 | 3.93 | D13=3.0 | 否 | FAIL | 加 CofactVLA/CAST；geometry-token vs generic deconfounding |
| GEO-P2 | r01 | 4.23 | D3=3.5, D13=3.5 | 否（R1 fatal解除） | FAIL | ContactGuard latent monitor 强基线；field独立价值 |
| GEO-P3 | r01 | 4.17 | D13=3.5 | 否 | FAIL | generic router/selective prediction；label interaction cost公平 |
| WAM-P1 | r01 | 4.17 | D8=3.5, D13=3.5 | 否 | FAIL | JPDA/MHT+WAM组合基线；OA/POT正文级核验 |
| WAM-P2 | r01 | 4.10 | D7=3.5, D8=3.5, D13=3.5 | 否 | FAIL | claim锁定paired decision-value target；数据算力乘法账 |
| WAM-P3 | r01 | 4.23 | D8=3.5, D13=3.5 | 否 | FAIL | Robot-Factored+PEARL/RMA组合；hidden-dynamics措辞 |
| STR-P1 | r01 | 4.20 | D13=3.5 | 否 | FAIL | event-triggered replanning/CheckVLA邻域；共享proposer |
| STR-P2 | r01 | 3.93 | D5=3.0 | **是** | FAIL / FATAL-IN-r01 | 二选一：SFP physical-time streaming 或 chunk-flow multi-NFE exits |
| STR-P3 | r01 | 4.17 | D8=3.5, D13=3.5 | 否 | FAIL | AliasBench overlap；benchmark/data vs architecture增益 |
| JEP-P1 | r01 | 4.10 | D3=3.5, D7/D8/D13=3.5 | 否（R1 fatal解除） | FAIL | Action-Bisim逐公式；JEPA必要性 |
| JEP-P2 | r01 | 4.20 | D3=3.5, D8/D13=3.5 | 否（R1 fatal解除） | FAIL | C-SWM/graph WM；transient edit events；NRI+same labels |
| JEP-P3 | r01 | 4.27 | D8=3.5, D13=3.5 | 否（R1 fatal解除） | FAIL | CoCo逐公式；non-JEPA同ANOVA；functional-only claim |

## 本轮独立结论

四个 R1 fatal 中，GEO-P2、JEP-P1、JEP-P2、JEP-P3 均通过实际公式/数据图改写而解除，不是文字绕过。与此同时，R2 发现新的 STR-P2 fatal：

- SFP v2 的 flow time 沿 physical action trajectory 前进，Algorithm 2 每积分步生成并立即执行一个动作；
- r01 STR-P2 却把 1/2/4/8 当作同一完整 action chunk 的生成 NFE exits，并要求 atomic commit；
- 当前同时声称使用 SFP checkpoint、完整chunk multi-cutoff和NFE deadline，输出对象/时间轴不相容。必须在 r02 选择一个范式并重画模型。

本轮还独立补出两篇 2026-08 强邻居：

- [CofactVLA 2608.04396v1](https://arxiv.org/abs/2608.04396) 已做 VLA counterfactual deconfounding，压缩 GEO-P1 的“反事实去视觉捷径”空间；
- [ContactGuard 2608.13438v1](https://arxiv.org/abs/2608.13438) 已在 planned action chunk 下做 pre-contact latent prediction/failure monitoring 并真机部署，压缩 GEO-P2 的 action-conditioned pre-contact prediction 空间。

## 跨 Proposal 创新性共性问题

1. **组件名不能当新意**：pseudometric、VOC/halting、JPDA posterior、functional ANOVA、graph dynamics、CUSUM/BOCPD 都有成熟前史。可保留的贡献必须是新的 embodied failure generator、target、干预或 planner consequence。
2. **需要组合强基线**：单独列 Robot-Factored 与 PEARL、JPDA 与 WAM、NRI 与 contact labels 不够；最危险的替代解释恰是这些直接组合。
3. **JEPA/WAM/VLA backbone 必要性必须证**：如果同一 supervision 在普通 stochastic/object-centric predictor 上持平，题目与 claim 应去掉 backbone 品牌。
4. **正文级而非摘要级核验**：多张邻居表仍出现“依原模型/按原协议”，R3 前必须填入准确 input/target/train graph/deploy graph/code status。

## Round 03 统一验收条件

1. 12 份升为 r02，logs 映射每个 R2 动作；STR-P2 必须先消 fatal。
2. 新邻居/组合基线进入 proposal、实验表和判负条件，不能只加 related-work 引用。
3. R3 每份画清 student/teacher/target/planner 的 token、时间戳、梯度与部署成本；任何 evaluator-only 分层字段不得进入模型。
4. 对以 oracle/complete state 生成的 pair、regret、value、contact、edit、metric、exogenous labels，明确 target-only 白名单与故意泄漏阳性对照。
5. 每份至少有一个“同 supervision 非品牌 backbone”基线或说明为何不适用。

## Round 03 优先级

- **P0**：STR-P2（时间语义 fatal）。
- **P1**：GEO-P1、GEO-P2、JEP-P1、JEP-P2（新增/概念级直接碰撞）。
- **P2**：GEO-P3、WAM-P1/P2/P3、STR-P1/P3、JEP-P3（组合强基线与信息路径）。

