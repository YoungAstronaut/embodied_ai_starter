# Round 06 Review — STR-P3

- Proposal-ID: STR-P3
- Reviewed-Revision: r05
- File: `proposals/STR-P3_counterfactual_history/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已诚实放弃官方 AliasBench 的 natural matched primary，改用 synthetic strict held-out physical pairs；官方任务只作外部效度，并补 pre-action matching、M/S预算敏感性、pair/task功效和控制收益降级。R5 “primary不可计算” fatal 风险解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 历史混叠是长时程VLA核心问题。 |
| D2 失败模式清晰度 | 4.5 | 同当前观测但Q-set不同的定义强。 |
| D3 创新性/最近邻 | 4.0 | 主要创新转为 benchmark/generator+paired supervision。 |
| D4 机制因果闭环 | 4.5 | legal pair→Q-set→cross loss→swap ranking闭合。 |
| D5 技术正确性 | 4.5 | 双向 value-set 与 state-local library 正确。 |
| D6 可观测性/泄漏 | 4.5 | snapshot/Q/future 隔离严格。 |
| D7 数据可得性 | 3.5 | 131M accepted steps且acceptance未知。 |
| D8 算力/工程 | 3.5 | 7天cap下完整8k仍高风险。 |
| D9 可证伪性 | 4.5 | 双backbone、swap与降级明确。 |
| D10 基线强度 | 4.0 | 原始history baseline少拿pair/Q监督。 |
| D11 消融充分性 | 3.5 | strict pair data与cross-value loss未正交。 |
| D12 OOD/真机 | 4.0 | AliasBench只外测，真机near-match较弱。 |
| D13 复现性 | 4.5 | pair/hash/Q schema具体。 |
| D14 CVPR契合度 | 4.5 | benchmark+视觉记忆机制有潜力。 |
| D15 风险/负结果 | 4.5 | architecture/history modality降级边界充分。 |

平均分：**4.20/5.00**。D3/D10/D11及数据工程仍未达门槛；round<10，不通过。

## Top 问题与证据缺口

1. **主比较严重混合数据与目标。** “原始数据 history baseline”既没拿严格 pair，也没拿M64/S8 Q-set labels；本法的胜利可能只是额外131M rollout监督，不是 counterfactual history机制。
2. **random-pair不是充分控制。** 随机pair可能明显off-manifold，太容易失败。需要 pre-action-covariate matched 但 Q-set irrelevant 的 hard control，以及 strict pair + ordinary objective。
3. **最强 comparator 未覆盖 Remember Smarter/IntentVLA 的适配版。** 只比较“各backbone原始数据”不能保证超过 learned memory compression；它们也应拿相同 strict-pair数量和optimizer steps。
4. **generator与评测共用Q定义会自洽偏置。** strict pair由 H16/M64/S8 Q筛选，primary又用同定义；需独立 horizon/reward/checkpoint evaluator或cross-generator holdout。

## 具体修改动作

1. 建 `pair data {covariate-matched irrelevant/control, strict Q-set}` × `objective {ordinary history BC/ranking, cross-value swap}` 2×2；四格同额外pairs、Q计算成本、optimizer steps、backbone与action head。
2. 对 IntentVLA、causal Transformer、Remember-Smarter各跑 native 与 strict-pair label-equal adapter；primary比较 validation winner，不只原始 history。
3. 增加 hard negative：外观/动作历史同等接近、合法可达但 Q-set Jaccard≥0.8；random pair仅保留sanity check。
4. primary evaluator 使用独立 seeds、H32或替代reward/checkpoint，并报告相对生成器H16的结论稳定性；否则只可称“自洽Q benchmark”。

## Round 07 验收条件

必须补 pair-data×objective 2×2、三类backbone的label-equal适配、hard matched controls与独立Q evaluator；同时给MVP实际接受率/steps/s。未完成前 D10/D11 不得升分。
