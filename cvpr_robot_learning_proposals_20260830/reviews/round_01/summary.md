# Round 01 Summary — 问题定义与最小反例

- Review date: 2026-08-30
- Input revisions: 12/12 均为 r00
- Individual reviews: 12/12 已完成
- Pass policy: 第 10 轮前不得 PASS；本轮全部 **FAIL / REVISE**
- Score range: 3.70–3.93；没有 Proposal 达到 mean≥4.30 与关键维度门槛

## 汇总表

| Proposal-ID | Revision | 平均分 | 最低维 | Fatal flaw | Round 01 结论 | Round 02 优先修复 |
|---|---:|---:|---|---|---|---|
| GEO-P1 | r00 | 3.80 | D5=3.0, D13=3.0 | 否 | FAIL | necessary-geometry 标签循环、directional action loss、中介 claim 形式化 |
| GEO-P2 | r00 | 3.70 | D5=2.5 | **是** | FAIL / FATAL-IN-r00 | contact transition 条件化 candidate action；ontology 与部署 frame |
| GEO-P3 | r00 | 3.77 | D5=3.0, D13=3.0 | 否 | FAIL | 删除不可部署 `L_act`；统一 routing risk/coverage 粒度 |
| WAM-P1 | r00 | 3.87 | D5=3.0, D13=3.0 | 否 | FAIL | 不可辨识对称例、permutation-invariant ID calibration、passive/active 拆分 |
| WAM-P2 | r00 | 3.80 | D5=3.0, D13=3.0 | 否 | FAIL | VOC potential outcomes/reward horizon；移除错误 monotonicity；视觉贡献隔离 |
| WAM-P3 | r00 | 3.90 | D5=3.0, D13=3.0 | 否 | FAIL | θ-NLL 矛盾、首次交互边界、residual confounders、robust objective |
| STR-P1 | r00 | 3.87 | D5=3.0, D13=3.0 | 否 | FAIL | event≠intent-change；时间索引；alternative intent 定义 |
| STR-P2 | r00 | 3.87 | D3=3.5, D4=3.5, D5=3.5, D7=3.5, D14=3.5 | 否 | FAIL | 与 SFP/multi-exit 的核心差异；mean+tail 公平预算；age 作用拆分 |
| STR-P3 | r00 | 3.87 | D13=3.0 | 否 | FAIL | 正确 action set 而非 demo distance；pair reachability；视觉 history vs last-action |
| JEP-P1 | r00 | 3.77 | D5=2.5 | **是** | FAIL / FATAL-IN-r00 | 非传递阈值关系不能称 equivalence class；stochastic outcomes |
| JEP-P2 | r00 | 3.73 | D5=2.5 | **是** | FAIL / FATAL-IN-r00 | graph operator 条件化 candidate action；typed concurrent edit algebra |
| JEP-P3 | r00 | 3.93 | D5=2.5 | **是** | FAIL / FATAL-IN-r00 | 加 action×exogenous interaction；可识别性；最小数值反例 |

## 本轮总判断

r00 的整体质量高于普通 idea list：12 份均有稳定 ID、训练/部署信息表、强基线、反向/泄漏阳性对照与预注册式判负。因此本轮没有把“格式缺失”当主要问题，而是检查每个科学命题的最小生成过程是否真的成立。

发现四个必须先消除的 r00-level fatal：

1. **GEO-P2** 与 **JEP-P2** 都在预测动作导致的未来 contact/topology，却没有把 candidate action 输入 transition/operator；当前不能用于候选动作评估。
2. **JEP-P1** 用距离阈值定义的局部关系通常不传递，却把它当 equivalence class 训练/检索。
3. **JEP-P3** 要求改 exogenous seed 时 controllable latent 不变，但其 conveyor/双臂任务的 action effect 本身与外生状态交互，当前 independence 主约束错误。

其余 Proposal 的主要共同问题是：

- 失败变量虽清楚，但 oracle 标签/数据生成过程仍可能循环定义；
- “中介、校准、belief、VOC、intent、正确动作”多处缺少统计/操作定义；
- 仿真 exact-reset 与真机 paired trial 写出规模，却未给 acceptance rate、功效和容差；
- R2 必须把机器人最近邻之外的直接理论邻域补齐，例如 Bayesian tracking/system ID/metareasoning/change point/action abstraction/causal stochastic representation；
- 所有 r00 的 D13 都≤3.0，后续必须逐步加入 schema、版本、seed、伪代码和 artifact 契约，不能只在最终轮补。

## Round 02 统一验收条件

1. 12 个 Proposal 全部升为 r01，并在 `refinement_log.md` 逐条映射本轮修改。
2. 四个 fatal 必须从公式和信息图上实质消失；改措辞不算修复。
3. 每份新增最近邻逐项表：输入、监督、student/target 可见信息、训练图、部署图、核心实验结论、新 Proposal 的可判重边界。
4. 每份给出至少一个最小正例、一个最小反例和一个替代机制 control。
5. 数据生成/标签 oracle 必须说明是否使用模拟器完整状态、未来帧、执行后状态以及这些信息为何不进 student。
6. 预算公平从“同参数/同 p95”扩展为与该机制相关的完整 matching：数据、teacher、NFE、候选数、mean/tail latency、控制频率。

## Round 02 优先级

- **P0**：GEO-P2、JEP-P1、JEP-P2、JEP-P3（先消 fatal）。
- **P1**：GEO-P1、GEO-P3、WAM-P1、WAM-P2、WAM-P3、STR-P1、STR-P3（补操作定义/最小反例）。
- **P2**：STR-P2（除操作定义外，必须证明不是 SFP/RTC 上的系统化 multi-exit engineering）。

