# Round 09 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r08
- File: `proposals/WAM-P3_hidden_physics_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已前置functional predictive而非参数识别，加入physics×appearance/t0泄漏、root drift/logger隔离、shared guard与system-ID降级；R8 hidden/真机风险已响应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | dynamics adaptation重要。 |
| D2 失败模式清晰度 | 4.5 | t0/t2与nuisance反例明确。 |
| D3 创新性/最近邻 | 4.5 | nominal-realization predictive belief差异清楚。 |
| D4 机制因果闭环 | 4.5 | residual→belief→CVaR闭合。 |
| D5 技术正确性 | 4.5 | functional claim严谨。 |
| D6 可观测性/泄漏 | 4.5 | θ/logger/appearance审计强。 |
| D7 数据可得性 | 4.0 | 50k可行但重。 |
| D8 算力/工程 | 4.0 | sample grid闭合。 |
| D9 可证伪性 | 4.5 | t0/nuisance/oracle门槛强。 |
| D10 基线强度 | 4.5 | PEARL/RMA/generic mixture充分。 |
| D11 消融充分性 | 4.5 | factorization×belief完整。 |
| D12 OOD/真机 | 4.5 | physics×appearance与4×120强。 |
| D13 复现性 | 4.5 | cell/sample/logger合同完整。 |
| D14 CVPR契合度 | 4.5 | 视觉适应控制强。 |
| D15 风险/负结果 | 4.5 | adaptation/system-ID降级有价值。 |

平均分：**4.43/5.00**。round<10，不通过。

## 模拟审稿攻击

1. **“PEARL/RMA already infer hidden dynamics.”** 主差异必须是nominal action-realization residual、deploy-equal context与t=2 predictive regret，而非“belief”一词。
2. **“Mass/friction is visible.”** physics×appearance全交叉和t0≤3pp是硬门槛，必须主表。
3. **“Latent system identification is not interpretable.”** 主动承认只在predictive equivalence下定义，禁止θ probe庆功。

## 修改与R10验收

标题建议 **Functional Predictive Beliefs from Action-Realization Residuals**，删除“Hidden Physics”强因果暗示。摘要唯一主命题写两次被动交互后的t=2 regret。主图分nominal realization、nuisance、belief和logger。R10准备t0泄漏或generic mixture持平时的**Predictive Adaptation under Dynamics Shift**降级摘要。
