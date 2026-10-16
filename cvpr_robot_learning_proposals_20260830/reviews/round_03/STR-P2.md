# Round 03 Review — STR-P2

- Proposal-ID: STR-P2
- Reviewed-Revision: r02
- File: `proposals/STR-P2_deadline_anytime_flow/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（R2 fatal 已解除；deadline scheduler 的可部署决策规则仍未形式化）

## 实际变更核验

r02 已实质选择标准 conditional chunk flow 的完整 `[B,H,D_a]` multi-NFE exits，不再加载或改写 SFP checkpoint；solver-time 与 physical control-time 分离，CAS commit、version、hard prefix 和逐步状态机均存在。SFP 仅作不同输出对象的外部闭环参照，旧 fatal 解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 尾延迟与陈旧观测是流策略真机部署的核心系统问题。 |
| D2 失败模式清晰度 | 4.5 | 80ms burst 反例和 stale chunk 序列可逐步模拟。 |
| D3 创新性/最近邻 | 4.0 | multi-exit/consistency 已知；增量是 chunk-flow+age+deadline 的机器人验证。 |
| D4 机制因果闭环 | 4.0 | exits→scheduler→atomic commit→physical execution 已闭合。 |
| D5 技术正确性 | 4.0 | 双时间轴正确；“最大可完成 NFE”需要运行时分布而非已知未来。 |
| D6 可观测性/泄漏 | 4.5 | future latency trace 不进部署，teacher action 仅 distillation target。 |
| D7 数据可得性 | 4.0 | 三硬件 trace 和两 benchmark 可采集。 |
| D8 算力/工程 | 4.0 | runtime state machine具体；全链路实现仍有较高工程风险。 |
| D9 可证伪性 | 4.5 | 同对象 multi-exit、fixed NFE、DMPO/HybridFlow 和 SFP 分范式比较合理。 |
| D10 基线强度 | 4.5 | 同 checkpoint/output/cost 的关键基线齐全。 |
| D11 消融充分性 | 4.5 | age scheduler×policy 2×2、atomic/prefix/teacher 消融充分。 |
| D12 OOD/真机 | 4.5 | unseen jitter/device 与真机 deadline 直接对应主 claim。 |
| D13 复现性 | 3.5 | 缺 runtime quantile predictor、deadline chance constraint 和 fallback 伪代码。 |
| D14 CVPR 契合度 | 4.5 | 生成策略与实时控制的视觉机器人系统贡献清楚。 |
| D15 风险/负结果 | 4.5 | 失败仍产出 wall-clock benchmark/cutoff-validity suite。 |

平均分：**4.27/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10 且 D3/D5 未达硬门槛，R3 不通过。

## Top 问题与证据缺口

1. **major — scheduler 不能预知“可完成”。** 部署只知道当前 deadline/queue/load，未来单次 exit latency 随机；“选择最大可完成 NFE”必须定义为基于条件延迟分布的 chance constraint，而不能暗含 future trace oracle。
2. **major — teacher sample alignment 可能损害多模态。** 对同一 `ξ` 对齐单个 K-step teacher 是合理 CRN，但需证明 1-NFE exit 仍保留跨 ξ 的分布，而不是在 distillation 权重下 mode collapse。
3. **minor — commit feasibility 的边界。** 完整 tensor 通过约束才 commit，但当任何新 exit 均未在 deadline 前完成时，执行 old suffix 的 observation age/safety 上限未定义。

## 具体修改动作

1. 训练/校准 `P(T_k≤d | device,queue,load,age)`，用预注册 `≥1-α` chance constraint 选 k；与 mean-latency heuristic、future-latency oracle 分开。
2. 按 k 报跨 noise seeds 的 MMD/energy distance、mode coverage 和 per-mode success，控制 teacher/student sample 数一致。
3. 给出 last-completed chunk 过龄上限与 safe fallback（stop/hold/reactive one-step），并计入 miss/success/jerk。
4. 用 trace replay 单测证明 CAS 不提交 stale version、不覆盖 executed prefix、所有 overhead 被 timestamp 捕获。

## Round 04 验收条件

- [ ] scheduler 使用可部署 latency quantile/chance constraint，不读取 future trace。
- [ ] multi-exit 分布保真按多个 ξ/模式而非单样本 L2 验收。
- [ ] old suffix 过龄后的安全 fallback 与最大 age 明确。
- [ ] CAS/prefix/version 有逐事件单测和故障注入。

