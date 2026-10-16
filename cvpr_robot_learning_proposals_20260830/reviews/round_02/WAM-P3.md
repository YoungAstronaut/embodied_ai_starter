# Round 02 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r01
- File: `proposals/WAM-P3_hidden_physics_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（无 fatal；视觉 residual confounder 分解是合理增量，需压过 system-ID/RMA）

## 实际变更核验

r01 已取消 θ-NLL，改为 predictive-equivalence outcome likelihood/coverage，分 prior/passive/probe，加入 residual nuisance生成式、2×2×2×2、CVaR0.2与PEARL/RMA。R1矛盾实质修复。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 视觉不可见动力学导致重复失败很关键。 |
| D2 失败模式清晰度 | 4.5 | t0不可辨识、被动更新、probe和四类confounders明确。 |
| D3 创新性/最近邻 | 4.0 | 相对Robot-Factored/DELE的视觉posterior增量成立；RMA/PEARL/system-ID已覆盖快速context adaptation。 |
| D4 机制因果闭环 | 4.0 | residual→belief→outcome set→CVaR→success，factorial confounder干预。 |
| D5 技术正确性 | 4.0 | metric/阶段矛盾已修；生成式中z与ε_dyn可交换、set calibration细节待R4。 |
| D6 可观测性/泄漏 | 4.5 | t0泄漏反证、下一周期更新、GTθ oracle隔离清楚。 |
| D7 数据可得性 | 4.0 | exact physics/factorial与真机材料可得；独立操控四confounders有难度。 |
| D8 算力/工程 | 3.5 | 两档预算有，480真机和16-cell干预仍重。 |
| D9 可证伪性 | 4.5 | prior leak、coverage/width、confounder ratio、strong-baseline判负全面。 |
| D10 基线强度 | 4.5 | Robot-Factored、DELE、RSSM、PEARL/RMA、supervised/tactile oracle齐全。 |
| D11 消融充分性 | 4.5 | stage/objective/context/confounder/sensor/θ oracle完整。 |
| D12 OOD/真机 | 4.5 | mass/friction/compliance、跨sim与真机配对。 |
| D13 复现性 | 3.5 | generative schema已加；仍缺measurement/version/seed/artifact。 |
| D14 CVPR 契合度 | 4.5 | visual world-model可辨识性/outcome calibration有强视觉结论。 |
| D15 风险/负结果 | 4.5 | sensor-identifiability边界与functional latent claim审慎。 |

平均分：**4.23/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；未过 hardened gate/mean。

## Top 问题

1. **major — RMA/PEARL增量仍可能是应用组合**：[RMA 2107.04034](https://arxiv.org/abs/2107.04034) 已从近期历史估计环境context快速适应；PEARL已做posterior context。新意需严格定位在 visual WAM residual confounder attribution 与 calibrated future-set planning。
2. **major — Robot-Factored+PEARL组合是关键未写基线**：单独列两者不够；最强替代解释就是 nominal realization factor + generic latent context posterior。
3. **major — “physics”标题仍可能过度**：主latent只predictive equivalence，若不对齐物理量，标题/claim应避免暗示辨识质量/摩擦本体。

## 具体修改动作

1. 增加 `Robot-Factored+PEARL/RMA-context` 组合基线，同history/latent/action objective。
2. 最近邻表逐项比较 context input、privileged training、posterior、uncertainty calibration、visual prediction、planner；补近期 visual system identification。
3. 将主标题/abstract contribution固定为 hidden-dynamics predictive belief，不把z解释为physics parameter；GT physics只分层。
4. 加generic recurrent mixture baseline，验证四confounder显式模型而非更多参数带来收益。

## Round 03 验收条件

- [ ] Robot-Factored+PEARL/RMA组合与generic recurrent mixture进入强基线/判负。
- [ ] RMA/PEARL/system-ID最近邻逐字段准确。
- [ ] 物理参数识别与predictive-equivalence措辞完全一致。
- [ ] R3信息图解释z、ε_dyn与可观测nuisance的梯度/时序边界。

