# Round 04 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r03
- File: `proposals/WAM-P2_value_of_imagination/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / REVISE**（continuation Bellman修复有效；成本递推与有限样本max偏差仍需处理）

## 实际变更核验

r03 已把estimand改为有限时域 `V_k/A_k`，保留myopic为基线，加入`Y=[0,-1,4]`反例，分开deadline后果与ms/J/age成本，并锁定environment/candidate/WAM/tie/evaluator全部CRN随机源。R3核心矛盾已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 实时想象分配重要。 |
| D2 失败模式清晰度 | 4.5 | 非单调收益最小例清楚。 |
| D3 创新性/最近邻 | 4.0 | 贡献仍是robot WAM paired continuation target。 |
| D4 机制因果闭环 | 4.5 | partial state→A_k→continue/stop已闭合。 |
| D5 技术正确性 | 4.0 | Bellman方向正确；age cost和finite-sample max bias未闭合。 |
| D6 可观测性/泄漏 | 4.5 | 所有return仅target。 |
| D7 数据可得性 | 4.0 | 乘法账与降级条件明确。 |
| D8 算力/工程 | 4.0 | 资源较大但有go/no-go。 |
| D9 可证伪性 | 4.5 | myopic/compute-only/shuffle/oracle强。 |
| D10 基线强度 | 4.5 | metareasoning和adaptive compute充分。 |
| D11 消融充分性 | 4.5 | nonmonotonic/visual/time/seed均可拆。 |
| D12 OOD/真机 | 4.0 | task/hardware/真机gate合理。 |
| D13 复现性 | 4.0 | CRN schema增强；nested target estimator仍缺。 |
| D14 CVPR 契合度 | 4.5 | WAM与实时控制契合。 |
| D15 风险/负结果 | 4.5 | harmful compute经验规律有价值。 |

平均分：**4.30/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10且D3/D5未达门槛，R4不通过。

## Top 问题与技术证据

1. **major — observation age cost可能累加绝对值。** Bellman每步减`c_k`，而`c_k`写`λ_age·observation_age_ms`。若age依次20/40/60ms，会减20+40+60，而不是本次扩展新增的20ms；除非明确这是刻意的running cost。需用incremental `Δage`或terminal age cost。
2. **major — max+S=8带乐观偏差。** `V_k=max(Y_k, estimated E[V_{k+1}]-c)`在同8 seeds上递推，噪声经max向上偏；CI跨margin的筛选也会改变标签分布。需要sample splitting/cross-fitting或bootstrap bias correction。
3. **minor — 文本合同仍残留myopic表述。** 最近邻表“本方案=E[Y_{k+1}-Y_k]-cost”、判负“VOC AUROC”应同步为continuation advantage，避免方法与评测不一致。

## 具体修改动作

1. 明确cost是incremental还是state running cost；给3步age手算，避免重复惩罚。
2. 用独立seed folds估continuation expectation与决策max，或报告nested bootstrap bias；S=4/8/16/32做label稳定性。
3. target record需保存全`Y_{0:K}`与每步增量cost，不再只称相邻pairs。
4. 全文统一A_k/continuation术语与AUROC/ECE指标。

## Round 05 验收条件

- [ ] age/energy/time cost递推不重复，最小例可核。
- [ ] max operator的有限样本偏差有cross-fit或校正及收敛曲线。
- [ ] target schema保存全路径并支持Bellman重算。
- [ ] 表格、loss、部署和判负统一使用continuation advantage。

