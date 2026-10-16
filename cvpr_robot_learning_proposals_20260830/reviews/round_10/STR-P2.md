# Round 10 Review — STR-P2

- Proposal-ID: STR-P2
- Reviewed-Revision: r09
- File: `proposals/STR-P2_deadline_anytime_flow/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 唯一主张为 standard conditional chunk flow 的 deadline-valid complete-chunk exits；明确不把SFP checkpoint、动态horizon、CAS或chance scheduler本身当新意。standard multi-exit+same scheduler是最危险基线，runtime-only降级稿已预置。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 截止时间下动作完整性直接关系闭环安全。 |
| D2 失败模式清晰度 | 4.5 | burst/stale/CAS/prefix fault可复现。 |
| D3 创新性/最近邻 | 4.5 | complete-chunk multi-cutoff contract区别RTC/SFP。 |
| D4 机制因果闭环 | 4.5 | cutoff distribution→scheduler→atomic commit闭合。 |
| D5 技术正确性 | 4.5 | per-k conformal/union bound与状态机一致。 |
| D6 可观测性/泄漏 | 4.5 | cutoff只用当前solver state/age/deadline。 |
| D7 数据可得性 | 4.5 | paired trace replay无需新大规模标注。 |
| D8 算力/工程 | 4.5 | 硬件clock/energy/CAS成本完整。 |
| D9 可证伪性 | 4.5 | budgeted success+miss/jerk硬约束明确。 |
| D10 基线强度 | 4.5 | standard/proposed exit×scheduler 2×2。 |
| D11 消融充分性 | 4.5 | age/CAS/fallback共享，隔离exit机制。 |
| D12 OOD/真机 | 4.5 | device/trace轴与开放/闭环边界清楚。 |
| D13 复现性 | 4.5 | trace manifest、ACF/ESS、计时协议齐全。 |
| D14 CVPR契合度 | 4.5 | 视觉动作生成的实时系统问题成立。 |
| D15 风险/负结果 | 4.5 | runtime benchmark负结果仍可复用。 |

平均分：**4.50/5.00**；所有维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **standard multi-exit持平：** 删除distillation claim，保留deadline/runtime protocol。
- **success <3pp但miss下降：** 只报告系统reliability trade-off，不称policy质量提升。
- **held-out device失败：** 删除设备泛化，仅保留校准设备内经验结论。

## 未决非致命风险与最终修改

complete exit可能通过共享训练图或缓存间接依赖later solver state。r10 必须加入 serialization/replay 单测：保存cutoff k状态后在无later state进程中重建完全相同chunk，并报告host-sync最坏延迟；追加 round_10/r10 log。当前只有9次refine，生命周期门槛未过。
