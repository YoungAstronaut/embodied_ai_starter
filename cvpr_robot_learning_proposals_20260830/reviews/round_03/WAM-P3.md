# Round 03 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r02
- File: `proposals/WAM-P3_hidden_physics_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（因果时间图合格；nuisance/persistent context 的可区分性仍主要靠经验审计）

## 实际变更核验

r02 已改题为 Hidden-Dynamics Predictive Belief，加入 Robot-Factored+PEARL/RMA、generic recurrent mixture 与 VariBAD 邻域；`z/u/e/innovation` 的时间顺序、stop-gradient、prior/passive/probe 三阶段和 GT physical parameter 仅分层均已实际写入。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | hidden dynamics 导致重复接触失败，重要且常见。 |
| D2 失败模式清晰度 | 4.5 | 首次不可辨识、作用后更新和 probe 成本边界明确。 |
| D3 创新性/最近邻 | 4.0 | belief/context adaptation 已知；增量是显式 nuisance 分解的视觉 WAM 验证。 |
| D4 机制因果闭环 | 4.0 | nominal residual→belief→future set→CVaR 已闭合，但 z/nuisance 仍可重参数化。 |
| D5 技术正确性 | 4.0 | t 到 t+1 的更新无未来回填；i.i.d. innovation 与 KL 训练仍需精确定义。 |
| D6 可观测性/泄漏 | 4.5 | GT dynamics/force 仅评测或 oracle，nominal trajectory 部署可计算。 |
| D7 数据可得性 | 4.0 | exact-reset hidden-physics 数据和真机可换物性可得。 |
| D8 算力/工程 | 4.0 | 50k episode/mixture sampling 可行，组合基线成本较高但可控。 |
| D9 可证伪性 | 4.5 | t=0 leak、factorial noise、generic mixture 与 oracle gap 判负强。 |
| D10 基线强度 | 4.5 | Robot-Factored+PEARL/RMA 和 generic recurrent mixture 是正确组合强基线。 |
| D11 消融充分性 | 4.5 | prior/passive/probe、nuisance、risk objective 与传感 oracle 分解充分。 |
| D12 OOD/真机 | 4.5 | 参数区间外、两模拟器与可控真机物性契合主张。 |
| D13 复现性 | 3.5 | 缺 nuisance supervision target、mixture family 和 innovation test 的 schema。 |
| D14 CVPR 契合度 | 4.5 | 视觉动力学、不确定性与操作适应契合。 |
| D15 风险/负结果 | 4.5 | 不解释 latent 为物理参数，并保留可辨识边界负结果。 |

平均分：**4.27/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10 且 D3/D5 未达硬门槛，R3 不通过。

## Top 问题与证据缺口

1. **major — stop-gradient 不等于 nuisance 已分离。** 即便 `g(u_t)` stop-gradient，q 仍可从 residual/history 重新编码 controller/vision/contact-location error。现有 2×2×2×2 是必要审计，但“机制分离”必须用 intervention 结果而不是结构名字证明。
2. **technical — innovation 假设过强。** `ε_dyn` 被写成跨时 i.i.d.，真实 stick-slip/contact noise 常有状态相关与时间相关；若错误，persistent z 会吸收 correlated innovation，造成伪 adaptation。
3. **technical — CVaR 的采样/校准合同缺失。** mixture z 与 innovation 各采多少样本、CVaR0.2 的 estimator bias/variance、与所有基线同 sample budget 尚未定义。

## 具体修改动作

1. 为每个 nuisance 写可观测监督 target 与 intervention；加 nuisance-only change、physics-only change、二者同时变的 belief-shift confusion matrix，而非只报平均 ratio。
2. 比较 i.i.d.、AR(1)/state-dependent innovation 与 persistent z；若 correlated innovation baseline 持平，收缩“persistent dynamics”解释。
3. 规定 q mixture 数、innovation samples、CVaR estimator/CI 与 planner call 数，所有强基线同预算。
4. 做 posterior predictive check：在 held-out action 上检验 coverage、autocorrelation residual 与 calibration，而非用 latent probe 支撑分离。

## Round 04 验收条件

- [ ] nuisance target、stop-gradient 和 q 输入的字段级图完整。
- [ ] correlated/state-dependent innovation 强基线及 residual autocorrelation 判据存在。
- [ ] CVaR sampling/estimator/预算合同可复现。
- [ ] 分离结论由 factorial intervention 和 predictive check 支持，不依赖 latent 可解释性。

