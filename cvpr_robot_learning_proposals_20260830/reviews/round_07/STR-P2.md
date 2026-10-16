# Round 07 Review — STR-P2

- Proposal-ID: STR-P2
- Reviewed-Revision: r06
- File: `proposals/STR-P2_deadline_anytime_flow/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已加入standard/proposed exit×fixed/chance scheduler 2×2，共享age/CAS/fallback/calibration、feasible-set winner及hardware/clock/trace manifest。R6系统公平问题已响应，actual replay=0明确。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 实时deadline是部署硬约束。 |
| D2 失败模式清晰度 | 4.5 | burst/stale/CAS故障具体。 |
| D3 创新性/最近邻 | 4.0 | multi-exit增量仍需实验。 |
| D4 机制因果闭环 | 4.5 | exit→scheduler→commit闭合。 |
| D5 技术正确性 | 4.5 | 两时间轴与chance calibration正确。 |
| D6 可观测性/泄漏 | 4.5 | future latency仅oracle。 |
| D7 数据可得性 | 4.0 | traces易采但目前0，block定义缺。 |
| D8 算力/工程 | 4.0 | profiler合同强，训练/episode总量未闭合。 |
| D9 可证伪性 | 4.5 | infeasible frontier与benchmark降级明确。 |
| D10 基线强度 | 4.5 | 2×2同wrapper充分。 |
| D11 消融充分性 | 4.5 | exit×scheduler与age分解完整。 |
| D12 OOD/真机 | 4.5 | unseen traces/三硬件有价值。 |
| D13 复现性 | 4.5 | clock/driver/power/trace manifest详细。 |
| D14 CVPR契合度 | 4.5 | 视觉生成策略与系统实证契合。 |
| D15 风险/负结果 | 4.5 | runtime benchmark仍有负结果价值。 |

平均分：**4.40/5.00**。D3/D7/D8未全达最终门槛；round<10，不通过。

## 数据/资源攻击面

1. “每硬件≥100 blocks”缺block时长、采样频率、自相关cutoff和每block replay episodes；100不等于100独立cluster。
2. paired trace replay只能共享外生latency trace/seed；closed-loop动作不同后observation会分叉，不能继续声称共享observations。需区分open-loop chunk质量与closed-loop success数据路径。
3. 2×2训练资源未给dataset episodes、teacher forward/NFE、四格训练seed与calibration episode数；只有部署profiling ledger。
4. power sampler/Joule对短burst的时间分辨率和GPU异步同步点未定义，energy ±5%公平可能不可复现。

## 具体修改动作

1. 定义trace block：持续时间、sampling interval、ACF阈值、block boundary、device state/warm-up；以有效sample size而非raw block计power。
2. 两条路径分开：open-loop共享observation/chunk target；closed-loop只共享reset、task和环境seed，允许轨迹分叉并以episode cluster。
3. 给训练公式与manifest：demonstration数、teacher calls、各cutoff loss、model×seed GPU-hours、calibration/test episode数。
4. 冻结CUDA event/monotonic clock同步、power sampling Hz、idle baseline和energy integration；CAS retry/queue wait全部计入。

## Round 08 验收条件

需闭合trace block/ESS、open-vs-closed数据路径、训练总账与energy测量协议。R8重点审查unseen device/jitter和真机安全fallback是否支持主claim。
