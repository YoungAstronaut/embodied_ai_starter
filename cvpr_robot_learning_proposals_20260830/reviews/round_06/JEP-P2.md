# Round 06 Review — JEP-P2

- Proposal-ID: JEP-P2
- Reviewed-Revision: r05
- File: `proposals/JEP-P2_object_contact_slots/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已将唯一primary改为90% coverage selection regret，相对NRI+same-label比较；event F1降为机制指标，并共享confidence/fallback/runtime、snapshot/task功效与success降级。R5 的“F1不能证明planning”问题解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 接触关系转移对操作世界模型重要。 |
| D2 失败模式清晰度 | 4.5 | attach/detach/transfer/compound错序明确。 |
| D3 创新性/最近邻 | 4.0 | NRI/C-SWM/ContactWorld后创新主要在transaction sequence。 |
| D4 机制因果闭环 | 4.5 | action→typed edits→executor→JEPA/scorer闭合。 |
| D5 技术正确性 | 4.5 | partial-order transaction与matching已闭合。 |
| D6 可观测性/泄漏 | 4.5 | event tensor stop-grad且action-ID probe。 |
| D7 数据可得性 | 4.0 | 全候选event target可生成。 |
| D8 算力/工程 | 4.0 | typed matching/executor工作量可控。 |
| D9 可证伪性 | 4.5 | regret、F1、fixed-action干预与降级明确。 |
| D10 基线强度 | 4.5 | NRI+完全同标签/executor是近同构强基线。 |
| D11 消融充分性 | 3.5 | action×edit是干预，不是representation×operator训练消融。 |
| D12 OOD/真机 | 4.0 | contact tasks强，真机/跨ontology仍薄。 |
| D13 复现性 | 4.5 | event schema、matching与fallback具体。 |
| D14 CVPR契合度 | 4.5 | object-centric视觉预测与操作结合强。 |
| D15 风险/负结果 | 4.5 | NRI持平即删除JEPA贡献。 |

平均分：**4.30/5.00**。D3=4.0、D11=3.5；round<10，不通过。

## Top 问题与证据缺口

1. **NRI comparator几乎拿走全部核心机制。** 它共享typed timestamp/partial-order labels、executor、scorer和fallback；若仍有差异，只剩representation/predictor。正文必须明确论文在NRI持平时保留什么：benchmark/operator，还是整个方法失效。
2. **当前“right/wrong action×edit”是因果攻击，不是训练因子消融。** 它能排除action-ID捷径，却不能区分收益来自typed transaction、executor或JEPA。
3. **event labels与executor不可分。** flat model若少拿顺序/transaction labels，比较不公平；若拿同label但不经executor，才可测结构执行的贡献。

## 具体修改动作

1. 建 `representation {NRI/C-SWM dynamics, JEPA predictor}` × `event use {flat same-label tensor scorer, typed transaction executor}` 2×2；四格同event targets、matching、confidence、candidate、future loss、参数±5%和planner calls。
2. 再加 endpoint-edge target 与 ordered-event target 的同表示对照；两者训练样本和label生成成本相同，endpoint由同event序列确定性压缩。
3. 写清claim ladder：NRI+executor持平→删除JEPA；flat same-label持平→删除typed executor；两者都持平→仅发布benchmark/evaluator，不声称方法。
4. 对NRI/C-SWM official-native与same-label adapter分表，避免“强行改造成本文”后又称超过原作。

## Round 07 验收条件

需补representation×event-use 2×2、endpoint/sequence target对照、claim ladder与每格runtime/参数/label成本；R7同时给event覆盖、null/abstain和action-ID probe pilot。
