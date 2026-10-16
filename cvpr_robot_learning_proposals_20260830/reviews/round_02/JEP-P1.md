# Round 02 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r01
- File: `proposals/JEP-P1_action_equivalence/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（R1 非传递 fatal 已解除；Action-Bisimulation 使“pseudometric”本身不能算新）

## 实际变更核验

r01 已废弃 equivalence class，改为 `W1+TV` action-effect pseudometric，物理/value分离，S=8 matched seeds+CI abstain，metric/triplet/rank loss、三动作反例与Action-Bisimulation直接基线。定义级fatal解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | action-effect geometry与planner regret重要。 |
| D2 失败模式清晰度 | 4.5 | 0/0.6/1.2反例清楚攻击旧类定义和过度分离。 |
| D3 创新性/最近邻 | 3.5 | [Action-Bisimulation 2403.16369](https://arxiv.org/abs/2403.16369) 已是multi-step controllability pseudometric；增量可能只是JEPA/contact应用。 |
| D4 机制因果闭环 | 4.0 | metric target→latent distance→ranking→success，label shuffle/value swap强。 |
| D5 技术正确性 | 4.0 | 非传递错误已修；SE(3)/contact mixed ground metric和state-local性质待形式化。 |
| D6 可观测性/泄漏 | 4.5 | matched outcomes仅target、student causal。 |
| D7 数据可得性 | 3.5 | variance MVP合理，但完整20k×32×seeds巨大。 |
| D8 算力/工程 | 3.5 | go/no-go存在；reset/rollout成本仍未乘算。 |
| D9 可证伪性 | 4.5 | Action-Bisim direct、distortion/regret/value leak判负明确。 |
| D10 基线强度 | 4.5 | JEPA、CoCo、Action-Bisim、smoothing、oracle全面。 |
| D11 消融充分性 | 4.5 | seeds/CI/H/schema/canonical/metric/value/noise全面。 |
| D12 OOD/真机 | 4.0 | object/camera/embodiment与真机局部微扰。 |
| D13 复现性 | 3.5 | estimator/CI增强；仍缺metric units/version/seed/artifact。 |
| D14 CVPR 契合度 | 4.5 | latent geometry与视觉预测联系强。 |
| D15 风险/负结果 | 4.5 | proxy-control脱钩与局部metric边界有价值。 |

平均分：**4.10/5.00**。D3=3.5、D5=4.0、D6=4.5、D9=4.5；未过创新/技术/mean gate。

## Top 问题

1. **major — Action-Bisimulation 是概念级正面邻居**：不能以“outcome pseudometric”或“multi-step controllability metric”作为创新；必须证明 same-state action-distribution metric 相对其state/action-bisim直接实现产生新的理论/实证结论。
2. **major — JEPA是否必要未证**：同一 metric supervision 可训练任意 action-conditioned predictor；若普通contrastive/dynamics encoder等效，JEPA只是backbone名。
3. **major — physical/value分离与bisimulation定义可能不同**：Action-Bisimulation的reward-free递归metric、goal-conditioned bisimulation等需要逐公式而非摘要比较。

## 具体修改动作

1. 逐公式对比 Action-Bisimulation：domain(state vs action)、递归/horizon、transition distribution、reward/value、metric fixed point、视觉输入、planner终点。
2. 加非JEPA action-conditioned encoder与same metric loss；只有target-encoder/predictive structure带来独立收益才能称JEPA contribution。
3. 补goal-conditioned/action abstraction/bisimulation metric邻域；把新意锁在 matched-seed contact-rich action metric + physical/value cross-task test（若足够）。
4. 给SE(3)+contact ground cost单位归一、triangle property与empirical estimator误差。

## Round 03 验收条件

- [ ] Action-Bisimulation逐公式差异表完成，pseudometric本身不再列为贡献。
- [ ] JEPA vs non-JEPA同metric监督基线进入判负。
- [ ] physical/value separation相对bisimulation/goal abstraction的边界准确。
- [ ] metric target/target encoder/student/planner信息路径完整。

