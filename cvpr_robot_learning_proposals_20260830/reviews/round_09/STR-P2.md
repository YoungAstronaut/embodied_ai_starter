# Round 09 Review — STR-P2

- Proposal-ID: STR-P2
- Reviewed-Revision: r08
- File: `proposals/STR-P2_deadline_anytime_flow/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已把唯一主线锁定standard chunk multi-exit，held-out device仅empirical，加入commit前guard、fallback/CAS/stale条件与runtime降级；R8叙事已显著收敛。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | deadline控制重要。 |
| D2 失败模式清晰度 | 4.5 | partial exit/stale chunk具体。 |
| D3 创新性/最近邻 | 4.5 | complete-chunk multi-cutoff+age/scheduler边界清楚。 |
| D4 机制因果闭环 | 4.5 | exits→chance scheduler→atomic commit闭合。 |
| D5 技术正确性 | 4.5 | 两时间轴/guard/ESS正确。 |
| D6 可观测性/泄漏 | 4.5 | future latency/device guarantee边界清楚。 |
| D7 数据可得性 | 4.5 | 多硬件trace可采。 |
| D8 算力/工程 | 4.5 | profiler/训练合同完整。 |
| D9 可证伪性 | 4.5 | standard multi-exit持平即降级。 |
| D10 基线强度 | 4.5 | best fixed/multi-exit/DMPO齐。 |
| D11 消融充分性 | 4.5 | exit×scheduler×age完整。 |
| D12 OOD/真机 | 4.5 | held-out device+6×100强。 |
| D13 复现性 | 4.5 | clock/power/trace/guard完整。 |
| D14 CVPR契合度 | 4.5 | 算法系统结合强。 |
| D15 风险/负结果 | 4.5 | runtime benchmark独立成立。 |

平均分：**4.50/5.00**。round<10，不通过。

## 模拟审稿攻击

1. **“Standard consistency distillation already gives multi-exit.”** 主2×2必须证明shared-noise multi-cutoff objective在同chance scheduler下仍赢。
2. **“This is systems engineering.”** 回应是complete-chunk validity、age-conditioned content和closed-loop deadline constraints的联合可证伪命题；atomic CAS是必要实现，不是唯一贡献。
3. **“SFP is the real comparison.”** SFP输出对象不同，只留secondary；不要让跨范式表占摘要/主图。

## 修改与R10验收

标题建议 **Deadline-Valid Complete-Chunk Exits for Conditional Flow Policies**。主图仅standard flow的1/2/4/8 exits、age与atomic commit。主表第一行standard multi-exit+same scheduler。R10准备P×C与S×C持平时的**Atomic Multi-Exit Runtime Benchmark**版本，并确保SFP只出现related work/secondary表。
