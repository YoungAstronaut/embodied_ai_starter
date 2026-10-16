# Round 10 Review — JEP-P2

- Proposal-ID: JEP-P2
- Reviewed-Revision: r09
- File: `proposals/JEP-P2_object_contact_slots/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 删除slot/JEPA branding，把唯一主张锁为 transient ordered typed contact transactions beyond endpoint graph；NRI×typed label-equal 为最危险基线，JEPA与executor两层均可从claim删除。该边界避开OA-WAM/POT与普通contact head。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | attach/detach/transfer顺序决定操作状态。 |
| D2 失败模式清晰度 | 4.5 | endpoint cancellation与partial order具体。 |
| D3 创新性/最近邻 | 4.5 | ordered transaction protocol超出NRI/contact slots。 |
| D4 机制因果闭环 | 4.5 | action→events→atomic executor→score完整。 |
| D5 技术正确性 | 4.5 | permutation-invariant group与matching定义正确。 |
| D6 可观测性/泄漏 | 4.5 | future event仅target，typed tensor stop-grad。 |
| D7 数据可得性 | 4.0 | 稠密时序event标注存在coverage风险。 |
| D8 算力/工程 | 4.0 | 100M cap可控但全候选重。 |
| D9 可证伪性 | 4.5 | endpoint/ordered same-cost target可推翻主张。 |
| D10 基线强度 | 4.5 | NRI/JEPA×flat/typed 2×2强。 |
| D11 消融充分性 | 4.5 | target/executor/JEPA层级删除完整。 |
| D12 OOD/真机 | 4.0 | closed ontology主线，open ontology只Atlas。 |
| D13 复现性 | 4.5 | topo_event_v1、matching单测与split清楚。 |
| D14 CVPR契合度 | 4.5 | 时序接触拓扑是视觉操作新benchmark。 |
| D15 风险/负结果 | 4.5 | event benchmark在method失败时仍有价值。 |

平均分：**4.40/5.00**；关键维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **NRI×typed持平：** 删除graph/JEPA method，保留ordered-event target。
- **event F1提高但regret不变：** 不宣称控制价值，只报告表示诊断。
- **real fallback过高：** 删除open-ontology transfer，保留closed ontology结论。

## 未决非致命风险与最终修改

±1 frame matching可能把错误顺序宽容成正确。r10 必须加入0/±1/±2 frame tolerance敏感性、原始sensor-to-event timestamp误差与transaction regret联表，并追加 round_10/r10 log。当前只有9次refine。
