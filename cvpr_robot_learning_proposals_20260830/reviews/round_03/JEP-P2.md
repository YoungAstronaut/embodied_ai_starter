# Round 03 Review — JEP-P2

- Proposal-ID: JEP-P2
- Reviewed-Revision: r02
- File: `proposals/JEP-P2_object_contact_slots/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（R1 action-conditioning fatal 持续解除；candidate-level target 支持与梯度防串谋未闭合）

## 实际变更核验

r02 已明确 graph/JEPA 不是创新，把 event 改为带 `τ`、Add/Del、typed-edge、partial order 和 atomic transfer transaction；endpoint cancellation 已通过中间事件序列修复。C-SWM、NRI+同 typed labels 以及三类 contact WM 的版本/代码状态已进入正文。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | attachment/ownership 改变是固定 slot 在 manipulation 中的真实盲点。 |
| D2 失败模式清晰度 | 4.5 | attach-detach、handover transaction 和 illegal cycle 可观察。 |
| D3 创新性/最近邻 | 4.0 | graph/event model已有；增量是 transient typed transaction 对候选规划的价值。 |
| D4 机制因果闭环 | 4.0 | candidate→event sequence→executor→JEPA→score 已闭合。 |
| D5 技术正确性 | 3.5 | event algebra改善明显，但训练是否拥有每个 candidate 的真实 event target 未说明。 |
| D6 可观测性/泄漏 | 4.5 | future graph/event 仅 target，full-trajectory association 仅 oracle。 |
| D7 数据可得性 | 4.0 | 仿真 causal body IDs 可提取；真实 causal teacher gap 仍大。 |
| D8 算力/工程 | 4.0 | typed executor/legality 可实现，partial-order decoder复杂但可控。 |
| D9 可证伪性 | 4.5 | fixed-action wrong-edit 2×2、NRI同标签和 oracle event 强。 |
| D10 基线强度 | 4.5 | NRI/C-SWM/contact WM/persistent slot 均覆盖。 |
| D11 消融充分性 | 4.5 | event字段、legality、cycle、触觉、label shuffle均可拆。 |
| D12 OOD/真机 | 4.0 | 遮挡/同类物体与真机 marker评测合理。 |
| D13 复现性 | 3.5 | 缺 per-candidate rollout manifest、并发事件匹配和联合训练梯度图。 |
| D14 CVPR 契合度 | 4.5 | 对象中心视觉动力学与接触操作高度契合。 |
| D15 风险/负结果 | 4.5 | 可退化为 contact-topology benchmark/graph model结果。 |

平均分：**4.20/5.00**。D3=4.0、D5=3.5、D6=4.5、D9=4.5；round<10 且 D5 未过硬门槛，R3 不通过。

## Top 问题与证据缺口

1. **major — per-candidate target 支持未写出。** operator 对 N 个候选预测 event sequence，但数据段只给“每种 primitive edit≥5k”，没有说明每个同 snapshot candidate 是否 exact-reset 执行并提取 target。若只监督 logged/executed action，部署候选排序大部分是外推。
2. **major — 联合训练可让 event latent 变成 action code。** 后期 scorer→operator 梯度若不截断，decoder 可绕过 typed event fidelity编码 candidate identity；固定 action/wrong edit 干预只有在 event bottleneck 真被使用时才可信。
3. **technical — partial-order loss/matching未定义。** 同一 time bin antichain 的 permutation-invariant loss、不同长度序列、abstain 和 transaction group 的 matching需要唯一算法，否则 F1/MAE 不可复现。

## 具体修改动作

1. 写明 `snapshot×N candidates×seeds×H` 的生成乘法账；主结果要求 candidate support coverage，并报告 proposer shift。
2. 主模型对 discrete typed event tensor stop-gradient后送 scorer/executor；另报 end-to-end 版本与从 event latent 解码 action ID 的 shortcut probe。
3. 定义 sequence matching：time tolerance、edge equality、antichain Hungarian、transaction exact-match、null/abstain 处理，并给单元测试。
4. 让 NRI+同标签共享完全相同 event target、executor和candidate set，只改变 representation/predictor。

## Round 04 验收条件

- [ ] 每个训练候选的 event label来源、exact-reset coverage 和总成本闭合。
- [ ] scorer/operator 梯度边界与 action-code probe 明确。
- [ ] partial-order/transaction metric 有确定匹配算法与最小测试例。
- [ ] NRI/C-SWM 同标签对照不存在数据或 executor 优势。

