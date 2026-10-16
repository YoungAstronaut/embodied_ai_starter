# Round 08 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r07
- File: `proposals/GEO-P3_geometry_confidence/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已保留真实rollout-regret B并将资源改为`[3+N_valid repair]×S4×H16`，拆validity/router split，补corruption cells与repair smoke；R7资源P0解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 几何置信路由有价值。 |
| D2 失败模式清晰度 | 4.5 | corruption/hard pairs明确。 |
| D3 创新性/最近邻 | 4.0 | relation B增量待实证。 |
| D4 机制因果闭环 | 4.5 | repair→risk→route闭合。 |
| D5 技术正确性 | 4.5 | repair成本与语义一致。 |
| D6 可观测性/泄漏 | 4.5 | 三split隔离。 |
| D7 数据可得性 | 4.0 | corruption generator可做。 |
| D8 算力/工程 | 4.0 | Nrelation gate后可控。 |
| D9 可证伪性 | 4.5 | B/fallback失败均可判负。 |
| D10 基线强度 | 4.5 | label-equal winner充分。 |
| D11 消融充分性 | 4.5 | supervision×structure强。 |
| D12 OOD/真机 | 3.5 | unseen family与真机协议不完整。 |
| D13 复现性 | 4.5 | cell/split/repair公式具体。 |
| D14 CVPR契合度 | 4.0 | 外部效度决定贡献强度。 |
| D15 风险/负结果 | 4.5 | calibration-only产出明确。 |

平均分：**4.27/5.00**。D3/D12未达门槛；round<10，不通过。

## OOD/真机攻击面

1. “未见corruption family”和“已见family未见severity”需明确leave-one-family-out；只有四轴时，若所有轴均参与训练就没有family-zero-shot。
2. test不插值回90%是正确防泄漏，但各方法achieved coverage若差很多，selected risk不可直接公平。需把coverage偏差作为硬可行约束。
3. RGB/stop fallback可能在最坏域占主导；若success来自大量stop，risk降低不等于任务价值。要同时报告abort、progress和conditional branch performance。
4. Franka三任务没有trial/root数、corruption实现、顺序随机化与安全规则；50-shot recalibration也需独立real calibration/test拆分。

## 修改与R9验收

1. 定义LOFO矩阵：每轮hold一family，seen-family unseen severity另表；hard A/B按asset group隔离。
2. primary可行条件加入test coverage CI含预设区间（如[.85,.95]）；不满足则方法失败而非按不同coverage比risk。
3. 报full/coarse/RGB/stop路由比例、conditional risk/success、fallback-only和progress-adjusted utility。
4. 真机至少3 tasks×预注册root blocks，corruption与50-shot split不重合；共享force/workspace stop，trial不足只外测。

R9需要把“可靠性selector、非省算系统”放在题目/摘要首位，并主动承认zero-shot calibration不保证跨新family有效。
