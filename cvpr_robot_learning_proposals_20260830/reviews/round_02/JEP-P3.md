# Round 02 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r01
- File: `proposals/JEP-P3_stochastic_exogenous/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（R1 independence fatal 已解除；function ANOVA本身不是创新）

## 实际变更核验

r01 已删除independence，改为 `μ+f_a+f_e+f_ae+ε` row/column-centered functional ANOVA，planner积分`p(Y|a,e)q(e|h)`，给XOR/conveyor反例、held-out cells、Sawada/strong stochastic baselines与functional-only claim。R1 fatal解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | action×external dynamics交互是动态操作核心。 |
| D2 失败模式清晰度 | 4.5 | XOR/conveyor最小例和任务族清楚。 |
| D3 创新性/最近邻 | 4.0 | 相对Sawada/CoCo的explicit interaction+mixture planning有可检验增量；ANOVA/causal factors本身经典。 |
| D4 机制因果闭环 | 4.5 | factorial data→interaction predictor→mixture ranking→OOD success。 |
| D5 技术正确性 | 4.0 | independence错误已修；continuous e/partial posterior与latent JEPA target对应待R4。 |
| D6 可观测性/泄漏 | 4.5 | e/seed/future只target，部署估q(e|history)。 |
| D7 数据可得性 | 4.0 | 2×2 go/no-go和4×4 groups具体。 |
| D8 算力/工程 | 3.5 | 15k×64 cells/sample与双臂真机仍重。 |
| D9 可证伪性 | 4.5 | main-only/single stochastic/Sawada/strong JEPA/mean-failure判负强。 |
| D10 基线强度 | 4.5 | Sawada、CoCo、JEPA-WM strongest、RSSM/ensemble/oracle齐全。 |
| D11 消融充分性 | 4.5 | interaction/stochastic/capacity/posterior/planning/centering全面。 |
| D12 OOD/真机 | 4.5 | held-out action×e、speed/phase/object、conveyor/双臂。 |
| D13 复现性 | 3.5 | measure/centering/generator增强；仍缺同步/version/seed/artifact。 |
| D14 CVPR 契合度 | 4.5 | stochastic visual prediction与causal interaction强。 |
| D15 风险/负结果 | 4.5 | functional-only claim和additive/mean失效边界价值强。 |

平均分：**4.27/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；仍未过 hardened gate/mean 4.30。

## Top 问题

1. **major — ANOVA不是新方法**：[Sawada 1804.06955](https://arxiv.org/abs/1804.06955) 已分controllable/uncontrollable；functional ANOVA与interaction decomposition是经典统计工具。唯一可保留的新命题是“balanced factorial visual JEPA interaction improves manipulation planner regret”。
2. **major — CoCo overlap仍可能更深**：[CoCo 2608.04653v1](https://arxiv.org/abs/2608.04653) 已有action/observation counterfactual consistency和same-state multi-action benchmark；必须逐公式比较其spatial counterfactual是否隐式估interaction。
3. **major — JEPA必要性未证**：同ANOVA可训练pixel/latent stochastic WM；若RSSM或普通object-centric predictor等效，题目不应强调JEPA。

## 具体修改动作

1. 将贡献限定为 factorial benchmark + action×exogenous interaction-aware predictive objective + mixture planning consequence，不宣称发明factor separation/ANOVA。
2. 对CoCo逐公式/数据cell/metric比较，并在相同4×4 groups运行CoCo。
3. 加non-JEPA stochastic object WM + identical ANOVA loss，分离JEPA encoder/target的增量。
4. 明确连续e和partial observation时centering measure、q(e|h) calibration与train/test intervention shift。

## Round 03 验收条件

- [ ] ANOVA/两latent本身不再列为创新，claim集中planner-relevant interaction。
- [ ] CoCo逐公式及同factorial数据基线完成。
- [ ] JEPA vs non-JEPA同objective基线进入判负。
- [ ] `e target→q(e|h)→mixture planner`信息路径和连续measure完整。

