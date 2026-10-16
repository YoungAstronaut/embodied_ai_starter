# Round 08 Review — JEP-P2

- Proposal-ID: JEP-P2
- Reviewed-Revision: r07
- File: `proposals/JEP-P2_object_contact_slots/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已加入smoke→ICC/100M cap、target来源/future拒绝、`topo_event_v1`及task/asset/contact-program split；R7数据复现问题基本解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 接触拓扑重要。 |
| D2 失败模式清晰度 | 4.5 | transaction/cancellation具体。 |
| D3 创新性/最近邻 | 4.0 | ordered event是有限增量。 |
| D4 机制因果闭环 | 4.5 | event→executor→selection闭合。 |
| D5 技术正确性 | 4.5 | schema/资源/匹配一致。 |
| D6 可观测性/泄漏 | 4.5 | future拒绝明确。 |
| D7 数据可得性 | 4.0 | TopoManip可生成。 |
| D8 算力/工程 | 4.0 | cap与power gate合理。 |
| D9 可证伪性 | 4.5 | 三层claim deletion充分。 |
| D10 基线强度 | 4.5 | NRI same-label强。 |
| D11 消融充分性 | 4.5 | representation×event-use完整。 |
| D12 OOD/真机 | 3.5 | 4×80有规模，sim-real ontology未闭合。 |
| D13 复现性 | 4.5 | topo schema/family split具体。 |
| D14 CVPR契合度 | 4.5 | object-centric预测与操作强。 |
| D15 风险/负结果 | 4.5 | benchmark-only价值明确。 |

平均分：**4.33/5.00**。D3/D12未达门槛；round<10，不通过。

## OOD/真机攻击面

1. contact-program family holdout很好，但需要说明new program是否仍由`topo_event_v1`可表达；否则是ontology open-set，不应按普通OOD评分。
2. 真机4×80 marker只评graph GT合理，但marker应不进入model RGB；contact/ownership GT与仿真body-ID event的语义对齐未审计。
3. event coverage/fallback在遮挡和detector failure下可能急剧上升；primary90% coverage若真机达不到，不能只报成功样本。
4. handover/开盖/插拔有双臂/力风险，缺共享force/collision/transaction legality在线guard。

## 修改与R9验收

1. OOD分closed-ontology new program、open-ontology new edge/event；后者只报unknown/abstain与failure atlas。
2. 真机marker置于独立视角/裁除，人工双标event time/type/transaction，给sim-real confusion与同步CI。
3. 报coverage/abstain/fallback、conditional regret/success；coverage<预设区间即真机不可确认。
4. 所有方法共享force/workspace/collision guard与illegal transaction rejection，计入latency/success。

R9叙事应优先“transient event sequence避免endpoint cancellation”，JEPA仅在N×T vs J×T过关后保留，避免把图/slot包装成创新。
