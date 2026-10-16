# Round 09 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r08
- File: `proposals/STR-P1_event_intent_reset/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已将唯一主线收敛到reset-worthiness，限定seen-family cross-task，加入compositional stress、root events、collision/jerk/false-reset约束与detector降级；R8安全/OOD边界已闭合。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 重置时机重要。 |
| D2 失败模式清晰度 | 4.5 | novelty≠reset反例强。 |
| D3 创新性/最近邻 | 4.5 | paired ΔQ reset-worthiness相对change gate差异明确。 |
| D4 机制因果闭环 | 4.5 | change/value→reset→RMRT闭合。 |
| D5 技术正确性 | 4.5 | coverage/censor/safety一致。 |
| D6 可观测性/泄漏 | 4.5 | oracle target隔离。 |
| D7 数据可得性 | 4.0 | 16 tasks可生成。 |
| D8 算力/工程 | 4.0 | 640-step分账可执行。 |
| D9 可证伪性 | 4.5 | 2×2与安全降级强。 |
| D10 基线强度 | 4.5 | BOCPD/CheckVLA/equal gates齐。 |
| D11 消融充分性 | 4.5 | change×value完整。 |
| D12 OOD/真机 | 4.5 | task OOD与4×100外测合理。 |
| D13 复现性 | 4.5 | root/split/threshold完整。 |
| D14 CVPR契合度 | 4.5 | 长时程VLA事件控制契合。 |
| D15 风险/负结果 | 4.5 | detector benchmark有价值。 |

平均分：**4.43/5.00**。round<10，不通过。

## 模拟审稿攻击

1. **“BOCPD/event-triggered replanning is old.”** 标题与摘要不要把event/change detection当贡献；唯一差异是paired intervention utility判定“该不该reset”。
2. **“ΔQ oracle supervision explains everything.”** pure ΔQ、pure change、generic concat、proposed四格必须主表，native/equal并列。
3. **“RMRT tube is hand-tuned.”** δp/δx/H冻结、敏感性和success/jerk约束需正文；不能只报更短恢复。

## 修改与R10验收

标题建议 **Reset-Worthiness from Change and Intervention Value for Long-Horizon VLA**，删除“intent”以免读者寻找未部署的intent posterior。摘要明确seen-family cross-task。R10准备ΔQ head无增益时的**EventAlias Reset-Worthiness Benchmark**版本，并将安全可行条件放primary同句。
