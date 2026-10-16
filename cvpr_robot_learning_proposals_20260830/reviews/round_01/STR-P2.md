# Round 01 Review — STR-P2

- Proposal-ID: STR-P2
- Reviewed-Revision: r00
- File: `proposals/STR-P2_deadline_anytime_flow/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / REVISE**（round<10；科学命题需与 scheduler/系统贡献隔离）

## 文件变更核验

r00 确认研究单次生成内部的 multi-cutoff validity，而非 execution horizon；包含 observation age、atomic commit、RTC-style prefix、多硬件 trace、同 p95 compute 和 cutoff 违规判负。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 任意时刻可用动作是实时 VLA 的真实部署缺口；现有方法 deadline failure 频率未量化。 |
| D2 失败模式清晰度 | 4.0 | 未完成采样/旧动作/观测变老/long-tail jitter 明确；缺最小 trace 和动作后果示例。 |
| D3 创新性/最近邻 | 3.5 | 与 RTC/PACE/DEHP 的对象差异清楚；SFP 中间态可执行、多出口 diffusion/flow 已可能覆盖核心技术。 |
| D4 机制因果闭环 | 3.5 | multi-cutoff/age→atomic output→deadline/action quality；scheduler 与表示学习贡献混合。 |
| D5 技术正确性 | 3.5 | 原子提交正确；multi-cutoff distillation 与 flow consistency/高 NFE 上限的关系、硬前缀下训练目标未推导。 |
| D6 可观测性/泄漏 | 4.5 | deadline/clock/queue 可部署，future latency 不可见且设 oracle 阳性对照。 |
| D7 数据可得性 | 3.5 | 任务与 trace 可收集；Kinetix/RoboTwin checkpoint compatibility、trace schema/许可未写。 |
| D8 算力/工程 | 4.0 | runtime、三硬件、日志字段和两档预算较具体；真实 atomic runtime/控制器集成待验证。 |
| D9 可证伪性 | 4.0 | 同 p95、per-cutoff violation、trace-retuned fixed NFE/one-step 判负明确。 |
| D10 基线强度 | 4.5 | RTC/REMAC/PACE/DEHP/CheckVLA/SFP/DMPO/two-step/oracle 覆盖强。 |
| D11 消融充分性 | 4.0 | age/cutoff/teacher/commit/scheduler/prefix/deadline 均拆；mean compute 与 scheduler overhead 未拆。 |
| D12 OOD/真机 | 4.5 | unseen GPU/network traces、6×100 真机、完整 latency logging；真实视觉 OOD 不突出。 |
| D13 复现性 | 3.0 | 无 runtime state machine、deadline clock origin、trace format、checkpoint/seed/artifact 清单。 |
| D14 CVPR 契合度 | 3.5 | 可能成为系统/runtime 论文；需证明 flow representation 的 multi-cutoff learning产生一般视觉生成结论。 |
| D15 风险/负结果 | 4.0 | 高 NFE 损伤、unseen traces、安全暂停与 benchmark 产出明确。 |

平均分：**3.87/5.00**。关键门槛：D3=3.5、D5=3.5、D6=4.5、D9=4.0；未达 hardened gate。

## Top 问题

1. **major — 新意可能只剩 multi-exit distillation + scheduler**：SFP 已宣称 flow 中间状态可执行；需要最小反例证明“可执行”不等于“deadline-calibrated optimal”。
2. **major — 公平预算只匹配 p95 不够**：可通过降低大多数 episode 的 NFE 换取 tail 改善；应同时报告 mean/p50/p95 compute、energy、age 与成功 Pareto。
3. **major — observation age 的因果作用未隔离**：age 既影响 scheduler 选 k，也可能应改变动作内容；现方法把两者放进一个模型，无法知道收益来源。

## 最近邻冲突与证据缺口

- [RTC 2506.07339v2](https://arxiv.org/abs/2506.07339)、[REMAC 2601.20130v1](https://arxiv.org/abs/2601.20130) 已覆盖异步 prefix 与 chunk consistency。
- [DMPO 2601.20701](https://arxiv.org/abs/2601.20701) 及 fixed one/two-step models 是质量—延迟 Pareto 的直接攻击。
- 必须核查 SFP 对“中间 flow state 可执行”的实际训练目标；若已 multi-time supervision，当前差异可能只剩系统标定。

## 必须修改的动作

1. 构造最小 trace：相同 p95、不同 burst structure 导致固定 NFE/RTC 失败而 deadline-conditioned cutoff 成功；给出动作/时序图。
2. 同时匹配或完整画出 mean、p50/p95/p99 compute/energy 与成功 Pareto；scheduler overhead 纳入 deadline。
3. 做 2×2：age 只调 scheduler、age 只进 policy、二者都进、都不进；固定 k 下测试 age-conditioned action validity。
4. 明确 multi-cutoff teacher 的 consistency：各 cutoff 是否同一 conditional distribution、如何避免互相矛盾、如何评价 calibration 而非仅约束违规。

## Round 02 验收条件

- [ ] 给出 SFP/RTC/one-step 无法覆盖的最小 deadline 反例。
- [ ] 公平性同时报告 mean 和 tail compute，包含 scheduler/atomic commit overhead。
- [ ] age 对 scheduler 与 action content 的作用正交拆分。
- [ ] 最近邻表核查 SFP multi-time objective 与多出口生成工作，若重合则主动收缩 claim。
- [ ] refinement log 记录改动并升为 r01。

