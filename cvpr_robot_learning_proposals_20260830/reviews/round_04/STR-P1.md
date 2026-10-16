# Round 04 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r03
- File: `proposals/STR-P1_event_intent_reset/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / REVISE**（paired value已进入部署决策；selected-max CI与coverage字段仍未闭合）

## 实际变更核验

r03 已让部署直接使用predicted `ΔQ`/lower CI-cost，不再比较intent log-probability；visual与proprio/contact evidence用OR，统一cost/threshold/latency伪代码，并把`s`改为部署`q_prop/contact`字段。R3核心断链已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | event后错误意图惯性重要。 |
| D2 失败模式清晰度 | 4.5 | N/F/C和双向hard pairs明确。 |
| D3 创新性/最近邻 | 4.0 | 唯一增量是paired reset utility。 |
| D4 机制因果闭环 | 4.5 | evidence+ΔQ→reset→action已闭合。 |
| D5 技术正确性 | 4.0 | decision score修正；winner CI/coverage仍有问题。 |
| D6 可观测性/泄漏 | 4.0 | 主字段可部署，但伪代码“check coverage”若指oracle-K coverage则部署不可得。 |
| D7 数据可得性 | 4.0 | paired rollout可生成。 |
| D8 算力/工程 | 4.0 | K=4,S=8,H=16可控，需总乘法账。 |
| D9 可证伪性 | 4.5 | value删除、low-visual、shared proposer强。 |
| D10 基线强度 | 4.5 | event/risk/memory控制充分。 |
| D11 消融充分性 | 4.5 | evidence/value/candidate分解全面。 |
| D12 OOD/真机 | 4.0 | 可重复event合理。 |
| D13 复现性 | 4.0 | 伪代码增强；CI estimator未定义。 |
| D14 CVPR 契合度 | 4.5 | 视觉时序与控制契合。 |
| D15 风险/负结果 | 4.5 | stability-reactivity benchmark有价值。 |

平均分：**4.27/5.00**。D3=4.0、D5=4.0、D6=4.0、D9=4.5；round<10且关键维未达门槛，R4不通过。

## Top 问题与技术证据

1. **major — `lowerCI(max_j ΔQ_j)`有winner's curse。** 若先从K=4选最大再用该候选的单独CI，覆盖率不再是名义值；需 simultaneous bootstrap/Bonferroni或在独立fold选候选与估CI。
2. **major — student如何输出CI未定义。** target bootstrap CI不等于部署预测CI。需要quantile/ensemble/conformal residual calibration，并说明跨event OOD时保证范围。
3. **major — deploy“check coverage”可能引用oracle。** current proposer相对oracle-K的coverage只能离线评估，不能部署时决定keep-old；部署只能用可观察的proposal confidence/abstention proxy。
4. **minor — evidence逻辑可简化。** `(gv∨gf∨S>κ_direct)∧S>κ_Q`中S分支在阈值关系下可能冗余，需给阈值排序和真值表。

## 具体修改动作

1. 对K候选构造simultaneous lower confidence bounds，预注册family-wise coverage。
2. 定义student predictive interval与独立calibration split；target CI仅作label noise权重。
3. 从部署伪代码删除oracle candidate coverage，改为offline stratum；若用proxy，单独评其校准。
4. 给`gv,gf,S`八格真值表，验证novelty-no-reset与low-visual-reset均符合H1。

## Round 05 验收条件

- [ ] max候选后的lower CI保持同时覆盖或用独立选择/估计。
- [ ] student CI来源、校准split和OOD边界明确。
- [ ] oracle coverage只在evaluator，部署无不可得字段。
- [ ] evidence gate真值表无冗余/反例。

