# Round 10 Review — STR-P3

- Proposal-ID: STR-P3
- Reviewed-Revision: r09
- File: `proposals/STR-P3_counterfactual_history/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 已放弃自然matched seed主线，唯一主张是可达双历史、当前观测/语言/proprio匹配且action-value sets冲突的 synthetic strict protocol；IntentVLA/Remember Smarter只证明历史有用，未提供此pair-Q测量合同。三backbone label-equal winner位于首组。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | history alias是长任务策略关键失效。 |
| D2 失败模式清晰度 | 4.5 | matched-current/conflicting-value定义具体。 |
| D3 创新性/最近邻 | 4.5 | 严格pair-Q benchmark超出历史encoder。 |
| D4 机制因果闭环 | 4.5 | reachable pair→cross-value target→history use闭合。 |
| D5 技术正确性 | 4.5 | Q support、canonical proposer与成本已闭合。 |
| D6 可观测性/泄漏 | 4.5 | task/episode/texture与未来字段控制充分。 |
| D7 数据可得性 | 4.0 | M64 pair-Q成本高且acceptance有限。 |
| D8 算力/工程 | 4.0 | full cap≤1B但仍重。 |
| D9 可证伪性 | 4.5 | swap/delete/cross-value与only-video gate直接。 |
| D10 基线强度 | 4.5 | 三backbone+原历史数据winner。 |
| D11 消融充分性 | 4.5 | control/strict data×ordinary/cross-value 2×2。 |
| D12 OOD/真机 | 4.0 | sim-B/near-match只作外部效度。 |
| D13 复现性 | 4.5 | pair hash、lineage、独立evaluator完整。 |
| D14 CVPR契合度 | 4.5 | 可复用视觉历史benchmark成立。 |
| D15 风险/负结果 | 4.5 | pure-benchmark标题可保留。 |

平均分：**4.40/5.00**；关键维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **三backbone winner持平：** 删除训练objective贡献，保留Counterfactual-Alias数据与评测。
- **natural transfer <3pp：** 不把synthetic改善外推自然数据。
- **真机near-match不足80 roots：** 删除真机段，避免把near-match写成strict pair。

## 未决非致命风险与最终修改

pair generator与Q evaluator若共享归纳偏置会自洽。r10 必须加入第二个不同checkpoint/reward evaluator的一致性门槛、评价分歧率以及rejected-pair manifest，并追加 round_10/r10 log。当前只有9次refine。
