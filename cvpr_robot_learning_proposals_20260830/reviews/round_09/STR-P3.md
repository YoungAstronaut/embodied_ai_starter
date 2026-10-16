# Round 09 Review — STR-P3

- Proposal-ID: STR-P3
- Reviewed-Revision: r08
- File: `proposals/STR-P3_counterfactual_history/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已把唯一主线锁定sim-A history-alias benchmark，加入sim-B zero-shot、AliasBench无pair-Q声明、真机≥80 roots或删除及共享guard；R8外部效度过度claim已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | history aliasing重要。 |
| D2 失败模式清晰度 | 4.5 | strict reachable pair定义强。 |
| D3 创新性/最近邻 | 4.5 | reachable Q-set pair benchmark差异明确。 |
| D4 机制因果闭环 | 4.5 | pair→Q-set→cross-value闭合。 |
| D5 技术正确性 | 4.5 | independent evaluator/资源稳定。 |
| D6 可观测性/泄漏 | 4.5 | target shard严格。 |
| D7 数据可得性 | 4.0 | 高风险但有MVP/1B gate。 |
| D8 算力/工程 | 4.0 | cap明确，完整规模重。 |
| D9 可证伪性 | 4.5 | data×objective/跨backbone强。 |
| D10 基线强度 | 4.5 | IntentVLA/Remember/Transformer齐。 |
| D11 消融充分性 | 4.5 | 2×2与modal split完整。 |
| D12 OOD/真机 | 4.0 | sim-B/可删真机边界诚实。 |
| D13 复现性 | 4.5 | lineage/hash/evaluator完整。 |
| D14 CVPR契合度 | 4.5 | benchmark+history机制契合。 |
| D15 风险/负结果 | 4.5 | generator/audit独立有价值。 |

平均分：**4.40/5.00**。round<10，不通过。

## 模拟审稿攻击

1. **“Synthetic self-consistency.”** independent H32/reward/checkpoint与sim-B必须放主结果；AliasBench不能当机制验证。
2. **“Extra 1B simulator steps.”** 2×2所有格同Q成本、M16只feasibility和资源cap需正文首表，不能藏附录。
3. **“Current observations are never truly identical.”** 论文应说tolerance-matched、reachable alias pairs，不说identical state；matching sensitivity与hard irrelevant controls是核心。

## 修改与R10验收

标题建议 **Counterfactual-Alias: Reachable History Pairs with Conflicting Action Values**。贡献顺序benchmark/generator→paired supervision→跨backbone，方法encoder不列创新。R10准备acceptance不足或closed-loop<3pp时纯benchmark摘要，并删除任何“natural memory”泛化措辞。
