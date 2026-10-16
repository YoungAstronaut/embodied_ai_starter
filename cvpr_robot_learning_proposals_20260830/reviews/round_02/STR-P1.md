# Round 02 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r01
- File: `proposals/STR-P1_event_intent_reset/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（无 fatal；paired reset-value 比纯 change detection 有明确增量）

## 实际变更核验

r01 已把 N/F/C 三标签分开，用 paired alternative-intent ΔQ 定义 reset-worthy C，修正 `t−1 prediction→t residual→reset→a_t`，形式化K=4 posterior margin、3+3 hard pairs、severity/prevalence指标并补BOCPD。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | stability-reactivity问题重要。 |
| D2 失败模式清晰度 | 4.5 | novelty/failure/reset-value 与hard pairs清楚。 |
| D3 创新性/最近邻 | 4.0 | 相对IntentVLA/BOCPD/PACE的“change≠reset value”差异成立；event-triggered replanning/control邻域仍缺。 |
| D4 机制因果闭环 | 4.5 | innovation+C posterior→reset→recovery，双oracle和ablation强。 |
| D5 技术正确性 | 4.0 | 时间图修复；K intents/Q oracle定义、density-ratio校准待深审。 |
| D6 可观测性/泄漏 | 4.5 | future values只target，one-cycle latency明确。 |
| D7 数据可得性 | 4.0 | paired value oracle与severity字段可生成。 |
| D8 算力/工程 | 4.0 | 轻量部署、两档预算合理；oracle数据成本未乘算。 |
| D9 可证伪性 | 4.5 | novelty-only、alternative ablation、fixed/oracle判负明确。 |
| D10 基线强度 | 4.0 | IntentVLA/Remember/BOCPD/PACE/forget/oracles齐全；event-triggered MPC缺。 |
| D11 消融充分性 | 4.5 | signal/CUSUM/posterior/hard pairs/threshold/history全面。 |
| D12 OOD/真机 | 4.5 | 多事件类型、severity与真机paired。 |
| D13 复现性 | 3.5 | 标签/time图增强，仍缺oracle planner/version/seed/artifact。 |
| D14 CVPR 契合度 | 4.0 | visual temporal prediction/change representation明确。 |
| D15 风险/负结果 | 4.5 | change detector降级与Pareto负结果有价值。 |

平均分：**4.20/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；未过 hardened gate/mean。

## Top 问题

1. **major — event-triggered replanning邻域不足**：BOCPD只代表检测；robotics/control已有innovation-triggered/event-triggered MPC/replanning，必须说明paired C target超越何处。
2. **major — 与 CheckVLA/When-to-Trust 的“何时介入”边界未列**：即便它们不叫intent reset，也用world consistency/risk触发纠正，可能是更强替代。
3. **major — K=4 alternative proposer可决定全部结果**：若候选不含正确intent，reset detector无机会；若oracle proposer过强，收益来自replanning capacity。

## 具体修改动作

1. 补 event-triggered MPC/replanning、CheckVLA/When-to-Trust/REMAC 的trigger-object表：检测量、干预动作、候选生成、延迟、保证/claim。
2. 固定相同 alternative proposer给全部gate，并加入 oracle-K/current-proposer/random-K，分离trigger与proposal quality。
3. 将唯一新意写成 paired reset-value supervision 把 change evidence 与 intervention utility 联合，而非CUSUM/BOCPD。
4. 在R3列出C target的外生seed、Q horizon、future信息与student隔离。

## Round 03 验收条件

- [ ] event-triggered control与跨方向intervention近邻表完整。
- [ ] 所有gate共享K候选/proposer，trigger增益独立。
- [ ] claim不把change detector/CUSUM当新。
- [ ] C oracle信息路径可逐字段审计。

