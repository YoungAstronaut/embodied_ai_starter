# Round 04 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r03
- File: `proposals/WAM-P3_hidden_physics_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / REVISE**（innovation/CVaR审计增强；belief-shift与nuisance target的可观测定义仍不唯一）

## 实际变更核验

r03 已加入nuisance可观察target、四类belief-shift confusion、i.i.d./AR(1)/state-dependent innovation、64-sample同预算CVaR、128-reference bias门槛及PIT/coverage/ACF checks。R3建议均有实际响应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | hidden dynamics适应重要。 |
| D2 失败模式清晰度 | 4.5 | prior/passive/probe和nuisance factorial清楚。 |
| D3 创新性/最近邻 | 4.0 | 显式nuisance分解需超组合baseline。 |
| D4 机制因果闭环 | 4.0 | residual→belief→predictive set→CVaR闭合。 |
| D5 技术正确性 | 4.0 | innovation家族合理；belief-shift metric/CVaR reference仍不稳。 |
| D6 可观测性/泄漏 | 4.5 | GT dynamics/force仅评测或oracle。 |
| D7 数据可得性 | 4.0 | simulation/真机物性可控。 |
| D8 算力/工程 | 4.0 | 64 samples同预算可行。 |
| D9 可证伪性 | 4.5 | noise factorial/组合baseline/ACF拒绝强。 |
| D10 基线强度 | 4.5 | PEARL/RMA/recurrent mixture齐全。 |
| D11 消融充分性 | 4.5 | innovation、risk、nuisance、probe全面。 |
| D12 OOD/真机 | 4.5 | 参数区间外和实物切换贴合。 |
| D13 复现性 | 4.0 | sampling合同增强；shift/target定义缺。 |
| D14 CVPR 契合度 | 4.5 | 视觉世界模型和物理适应契合。 |
| D15 风险/负结果 | 4.5 | 可辨识边界明确。 |

平均分：**4.30/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10且D3/D5未达门槛，R4不通过。

## Top 问题与技术证据

1. **major — belief-shift没有表示不变定义。** mixture latent的均值/KL会受component permutation和可逆重参数化影响；既然不解释z，confusion matrix必须基于held-out action的posterior predictive distribution距离/utility变化，而不是latent shift。
2. **major — contact localization residual并非天然部署可观测。** 真正residual需要GT contact location；部署只有detector prediction/confidence。需区分`u_t`可见输入与训练监督target，不能把target误称在线可见。
3. **technical — 128 samples不是可靠“reference”。** 对tail CVaR，128仍高方差；“bias<5%”应相对更大离线样本/收敛外推，并定义12.8个最差样本如何插值。
4. **minor — 相关工作段仍写“物理参数后验”。** 与functional predictive-equivalence边界不一致，应清理。

## 具体修改动作

1. belief-shift定义为固定held-out action set上的predictive MMD/Wasserstein、coverage或decision regret，并做component permutation不变单测。
2. 为每个nuisance列`deploy input / train target / evaluator GT`三列；contact GT不得进入q更新。
3. CVaR用fractional order-statistic明确公式，参考样本提升到≥1024或画64/128/256/1024收敛。
4. ACF阈值按有效样本数给CI/whiteness test，不固定任意0.1。

## Round 05 验收条件

- [ ] belief-shift完全在predictive/decision空间定义并对latent重参数化不变。
- [ ] nuisance deploy input与supervision target分离。
- [ ] CVaR estimator、fractional tail和reference convergence可复算。
- [ ] 全文不再把functional latent称作物理参数posterior。

