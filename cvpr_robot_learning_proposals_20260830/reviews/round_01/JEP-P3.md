# Round 01 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r00
- File: `proposals/JEP-P3_stochastic_exogenous/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / FATAL-IN-r00**（主 factorization 约束与所选交互任务矛盾）

## 文件变更核验

r00 已完全放弃被 JEPA Safety/CheckVLA 覆盖的 risk calibration，改为 action×exogenous factorial interventions、controllable/exogenous/stochastic latent、marginalized planning、factor leakage probes 和非安全声明。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 任务相关但不可控的动态会淹没 action effect，确定性均值 planning 失败，问题重要。 |
| D2 失败模式清晰度 | 4.0 | conveyor/滚动物/双臂与 action attribution 错误具体；interaction 情形恰未被定义。 |
| D3 创新性/最近邻 | 4.0 | 已实质换题，区别 Invariant JEPA/VLA-JEPA/CoCo/JEPA Safety；stochastic causal representation 邻居缺失。 |
| D4 机制因果闭环 | 3.0 | factorial pair→factor latent→marginal planner→regret；错误 independence 约束使核心箭头不成立。 |
| D5 技术正确性 | 2.5 | 固定 action 改 exogenous 时要求 `z^c` 不变，但接触时间/相对位姿会改变 robot-caused outcome；主任务含强 action×exo interaction，分解不可识别。 |
| D6 可观测性/泄漏 | 4.5 | exogenous seed/未来 target 不进 student，candidate action 和 sampled future 可部署，泄漏对照完整。 |
| D7 数据可得性 | 4.0 | factorial simulator groups 与 OOD split 具体；15k×16 rollout 及真机外生 seed 控制精度待算。 |
| D8 算力/工程 | 3.5 | 两档预算和 planner sample matching 有；latent diffusion、多候选、多 sample 与双臂真机成本高。 |
| D9 可证伪性 | 4.5 | regret/probes/NLL/OOD、single stochastic、oracle upper bound 均有明确判负。 |
| D10 基线强度 | 4.0 | deterministic/stochastic/ensemble/RSSM/VLA-JEPA/CoCo/CheckVLA/oracle 全面。 |
| D11 消融充分性 | 4.0 | factor/stochastic/capacity/samples/independence/masks/swaps/planning 均拆；interaction 不是正式组件。 |
| D12 OOD/真机 | 4.5 | 速度/相位/对象拆分，conveyor+第二臂真机；外生 seed 真机可重复性未说明。 |
| D13 复现性 | 3.0 | 无 structural equations、factor dimensionality allocation、seed synchronization、版本/seed/artifact 清单。 |
| D14 CVPR 契合度 | 4.5 | 随机视频 latent 的可控/外生因果分解具有强视觉学习贡献。 |
| D15 风险/负结果 | 4.5 | 已指出 independence 可能删交互并保留 mean-failure benchmark；但“采用 residual”尚未实现。 |

平均分：**3.93/5.00**。关键门槛：D3=4.0、D5=2.5、D6=4.5、D9=4.5。当前有定义级 fatal flaw。

## Top 问题

1. **fatal-in-r00 — 交互违背 factorization**：传送带相位/第二机械臂位置会改变同一 action 的接触结果，故 action-caused component 不可能在改 e 时保持；把 interaction 塞入未定义 residual 不能修复损失主约束。
2. **major — 分解不可识别**：在无结构约束下，`z^c/z^e/ξ` 可任意旋转/交换而保持 likelihood；低 cross-probe 也可能只是 adversarial hiding。
3. **major — “action-invariant but task-relevant”表述错误**：外生状态本身不随当前 action 改变，但其**后果和最优动作**会与 action 交互；planner 需要联合分布而非简单边缘独立。

## 最近邻冲突与证据缺口

- [JEPA-WM study 2512.24497v3](https://arxiv.org/abs/2512.24497) 已系统揭示 deterministic predictor/planner 选择；应复现其 strongest stochastic/rollout settings。
- [CoCo 2608.04653v1](https://arxiv.org/abs/2608.04653) 有 action×observation counterfactual consistency，可能已覆盖部分 factorial loss。
- Independent mechanisms、causal representation learning、stochastic video/world models、controllable/uncontrollable dynamics decomposition 是关键直接邻域，当前引用不足。
- [JEPA Safety 2608.17496v1](https://arxiv.org/abs/2608.17496) 只用于说明旧种子已放弃，不应作为新机制主基线，除非比较 candidate selection 后果。

## 必须修改的动作

1. 用 potential-outcome/ANOVA 式结构：action main effect、exogenous main effect、action×exogenous interaction 与 stochastic noise；不再要求改 e 时整个 controllable outcome 不变。
2. 定义 planner 需要的量，例如 `p(y|s,a)` 在 e 未观测/部分观测时的 mixture，并说明 factorization 如何降低 ranking regret，而非追求表征独立本身。
3. 给出可识别性假设：matched factorial interventions、共享 decoder/区域约束、minimality 或只声称 functional decomposition；probe 不作为因果证明。
4. 先用一个最小 conveyor counterexample 展示 deterministic mean 和 naive independent factorization 都失败，interaction model 成功，再扩到双臂。

## Round 02 验收条件

- [ ] 主公式包含 action×exogenous interaction，删除与任务矛盾的 invariance 约束。
- [ ] 明确可识别性假设和只允许的 claim，不以低 probe 代替因果证据。
- [ ] 有一个数值/图示最小反例同时攻击 deterministic mean 与 naive independent factorization。
- [ ] 最近邻表补 causal/stochastic world representation，并逐项对比 CoCo/JEPA-WM study。
- [ ] refinement log 记录旧风险题放弃和本轮 fatal 修复，升为 r01。

