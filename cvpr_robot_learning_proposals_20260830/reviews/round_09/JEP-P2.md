# Round 09 Review — JEP-P2

- Proposal-ID: JEP-P2
- Reviewed-Revision: r08
- File: `proposals/JEP-P2_object_contact_slots/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已把唯一主线锁为closed-ontology transient ordered events，open ontology只atlas，加入marker双标、coverage/fallback、transaction/safety guard与JEPA/executor删除规则；R8 overclaim已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | contact topology重要。 |
| D2 失败模式清晰度 | 4.5 | endpoint cancellation具体。 |
| D3 创新性/最近邻 | 4.5 | ordered partial-order transaction相对NRI endpoint差异明确。 |
| D4 机制因果闭环 | 4.5 | event→executor→future ranking闭合。 |
| D5 技术正确性 | 4.5 | transaction/schema严谨。 |
| D6 可观测性/泄漏 | 4.5 | target/logger隔离。 |
| D7 数据可得性 | 4.0 | TopoManip可生成。 |
| D8 算力/工程 | 4.0 | 100M cap。 |
| D9 可证伪性 | 4.5 | claim ladder明确。 |
| D10 基线强度 | 4.5 | NRI same-label强。 |
| D11 消融充分性 | 4.5 | representation×event-use完整。 |
| D12 OOD/真机 | 4.0 | closed/open边界合理。 |
| D13 复现性 | 4.5 | ontology/canonical serialization完整。 |
| D14 CVPR契合度 | 4.5 | 对象图预测与操作强契合。 |
| D15 风险/负结果 | 4.5 | event benchmark独立成立。 |

平均分：**4.40/5.00**。round<10，不通过。

## 模拟审稿攻击

1. **“NRI with richer labels.”** 正是最危险基线；N×T vs J×T决定JEPA是否存在，J×F vs J×T决定executor是否存在。
2. **“Ontology is engineered and closed.”** 摘要主动写closed ontology；open event只unknown/atlas，不包装zero-shot。
3. **“Slots/graphs/JEPA are all old.”** 标题应围绕transient ordered transaction，不能再叫object-contact slots创新。

## 修改与R10验收

标题建议 **TopoManip: Ordered Contact Transactions beyond Endpoint Graph Prediction**。主图以同一event sequence对比endpoint压缩与typed executor。主表先NRI same-label。R10准备N×T持平时删除JEPA、J×F持平时删除executor的两版摘要/标题，不允许只在结论脚注降级。
