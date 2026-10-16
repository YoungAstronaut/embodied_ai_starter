# Round 10 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r09
- File: `proposals/GEO-P1_counterfactual_geometry/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 已固化独立 utility evaluator 下的 relation/generic × SCM/generic 2×2、label-equal 最强基线、三条审稿攻击和 benchmark 降级稿。经 Round 10 独立版本刷新，VGA v2、MECo-WAM v1、CofactVLA v1 均未给出同构的“pair protocol + 独立动作效用评估”合同；D3 可升至 4.5，但 counterfactual/deconfounding 本身不计创新。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | geometry shortcut重要但适用域窄。 |
| D2 失败模式清晰度 | 4.5 | nuisance/causal/hard-negative配对明确。 |
| D3 创新性/最近邻 | 4.5 | 独特对象是独立utility下的relation协议，不是backbone。 |
| D4 机制因果闭环 | 4.5 | pair→关系干预→候选排序闭合。 |
| D5 技术正确性 | 4.5 | 支持集、集合NLL与regret定义一致。 |
| D6 可观测性/泄漏 | 4.5 | checker、selector与部署字段已隔离。 |
| D7 数据可得性 | 4.0 | exact-reset pair仍需较强模拟器。 |
| D8 算力/工程 | 4.0 | 分阶段预算可信但full grid昂贵。 |
| D9 可证伪性 | 4.5 | 2×2、错误swap、<3pp降级可推翻claim。 |
| D10 基线强度 | 4.5 | VGA/Cofact/MECo label-equal winner在首组。 |
| D11 消融充分性 | 4.5 | representation×deconfounding正交。 |
| D12 OOD/真机 | 4.0 | 主claim限sim，真机只secondary。 |
| D13 复现性 | 4.5 | lineage、成本和manifest字段完整。 |
| D14 CVPR契合度 | 4.5 | 可复用benchmark协议契合视觉机器人。 |
| D15 风险/负结果 | 4.5 | benchmark版仍有独立价值。 |

平均分：**4.37/5.00**；D3/D5/D6/D9均4.5，无fatal，内容硬门槛通过。

## 三结果压力测试

- **最强基线持平：** 自动删除新method claim，保留独立 evaluator 的 Geometry Counterfactual Ranking benchmark；不再称“因果几何新模型”。
- **control secondary <3pp：** 机制claim判负，但pair difficulty、support与shortcut测量仍可发表为诊断协议。
- **OOD/真机失败：** 不外推sim排序证据；标题/摘要移除transfer，只报告边界。

## 未决非致命风险与最终修改

独立 evaluator 仍可能和 relation ontology 同偏。r10 必须实际加入：至少两类不同 checkpoint/reward evaluator 的一致性判据、分歧时自动降级规则，以及冻结 evaluator hash/版本字段；并在 log 写 `## round_10 / r10`。当前仅有9次refine，生命周期硬门槛未过；完成后进入R11核验。
