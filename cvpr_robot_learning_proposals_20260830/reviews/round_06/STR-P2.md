# Round 06 Review — STR-P2

- Proposal-ID: STR-P2
- Reviewed-Revision: r05
- File: `proposals/STR-P2_deadline_anytime_flow/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已冻结单一 deadline/energy operating point，把 episode success 设为唯一 primary，并把 miss/jerk 变成硬约束；补 paired trace replay、trace-block×episode 功效及同时超过 best-fixed/multi-exit 的 closed testing。R5 多终点与统计问题已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | deadline miss 对实时VLA直接致命。 |
| D2 失败模式清晰度 | 4.5 | burst trace 与 stale chunk 最小例清楚。 |
| D3 创新性/最近邻 | 4.0 | multi-exit/RTC 已有，增量在完整chunk一致性+age。 |
| D4 机制因果闭环 | 4.5 | cutoff exits→latency scheduler→atomic commit闭合。 |
| D5 技术正确性 | 4.5 | solver time与physical time已严格分离。 |
| D6 可观测性/泄漏 | 4.5 | future latency只作阳性oracle。 |
| D7 数据可得性 | 4.5 | paired trace replay 易于构造。 |
| D8 算力/工程 | 4.0 | runtime实现和fault tests工作量较大。 |
| D9 可证伪性 | 4.5 | 单预算、约束和closed testing明确。 |
| D10 基线强度 | 4.5 | best fixed、standard multi-exit、one-step齐。 |
| D11 消融充分性 | 4.0 | age 2×2好，但 exit objective×scheduler未正交。 |
| D12 OOD/真机 | 4.5 | unseen jitter traces与fault tests强。 |
| D13 复现性 | 4.5 | state machine、CAS与runtime指标具体。 |
| D14 CVPR契合度 | 4.5 | 生成策略与机器人实时系统兼具。 |
| D15 风险/负结果 | 4.5 | multi-exit/DMPO持平即降级。 |

平均分：**4.40/5.00**。D3=4.0、D11=4.0；round<10，不通过。

## Top 问题与证据缺口

1. **standard multi-exit baseline 是否拿同一 latency-chance scheduler 未冻结。** 若它只用固定 cutoff，而本法用 calibrated scheduler，收益可能完全来自 scheduler而非 shared-noise multi-cutoff objective。
2. **atomic commit/fallback 是系统贡献，必须共享。** 正文说 fallback共享，但没有明确 standard multi-exit、RTC early-stop 都经过同 CAS/timestamp/stale rejection layer。
3. **age 2×2只隔离 scheduler/content，不隔离 exit训练。** 核心论文命题至少含 exit validity 与 deadline scheduling两部分，应有主效应/交互。

## 具体修改动作

1. 增加 `exit training {standard consistency/multi-exit, proposed shared-noise multi-cutoff}` × `scheduler {best fixed/ordinary, same conformal latency chance}` 2×2；四格同teacher、data、NFE、output chunk、scheduler features与校准样本。
2. 所有 deployable baselines强制通过同一 CAS/atomic commit/fallback wrapper；另报 wrapper-off diagnostic，不把系统安全层当模型增益。
3. standard multi-exit也获得同 age scheduler/content 2×2；否则 age特性只给本法。
4. validation winner 在同预算 success 且 miss/jerk满足约束的可行集内选；若无基线可行，应报告 constraint frontier而非把 infeasible baseline当0分。

## Round 07 验收条件

需补 exit-objective×scheduler 2×2、共享 wrapper接口、同calibration trace/feature contract及每格实测mean/p95/p99/energy；R7还需冻结硬件/驱动/计时器与trace manifest。
