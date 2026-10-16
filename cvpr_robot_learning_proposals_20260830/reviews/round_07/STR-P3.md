# Round 07 Review — STR-P3

- Proposal-ID: STR-P3
- Reviewed-Revision: r06
- File: `proposals/STR-P3_counterfactual_history/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已加入control/strict data×ordinary/cross-value 2×2、三backbone native/adapter、hard Jaccard control、独立seed/H32/reward/checkpoint evaluator及resource gate。R6数据/目标混叠已正交，actual pairs=0如实标注。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | history aliasing重要。 |
| D2 失败模式清晰度 | 4.5 | legal pair与Q-set交叉清楚。 |
| D3 创新性/最近邻 | 4.0 | generator/benchmark贡献突出。 |
| D4 机制因果闭环 | 4.5 | pair→Q-set→cross-value闭合。 |
| D5 技术正确性 | 4.5 |独立evaluator方向正确。 |
| D6 可观测性/泄漏 | 4.5 | target shard隔离严格。 |
| D7 数据可得性 | 3.0 | acceptance=0，8k strict pairs风险极高。 |
| D8 算力/工程 | 3.0 | 生成历史与多档H32 evaluator未计全。 |
| D9 可证伪性 | 4.5 | self-consistency降级明确。 |
| D10 基线强度 | 4.5 | 三backbone label-equal winner强。 |
| D11 消融充分性 | 4.5 | data×objective 2×2闭合。 |
| D12 OOD/真机 | 4.0 | AliasBench外测，真机near-match较薄。 |
| D13 复现性 | 4.0 | hash/schema好，但资源和生成策略未闭合。 |
| D14 CVPR契合度 | 4.5 | benchmark与视觉记忆契合。 |
| D15 风险/负结果 | 4.5 | 低acceptance/自洽失败可降级。 |

平均分：**4.20/5.00**。D3/D7/D8/D13未达门槛；round<10，不通过。

## 数据/资源攻击面

1. 4.096M/131.072M/655.36M的Q rollout算术成立，但**寻找两条合法历史并达到匹配当前观测**的前置history-generation env steps未计；这可能比value stage更昂贵。
2. 独立H32在8k full上单一档就需`8k×2×64×8×32=262.144M` steps。新seed可与H32合并，替代reward可复用轨迹，但独立policy checkpoint通常需新candidate/outcome；当前“四档”没有总账。
3. r06公平合同说四格都拿M64/S8，而MVP仍是M16/S4；需明确MVP只做feasibility、不能产生primary confirmatory结果。
4. 8k accepted在40k attempted hard cap下要求≥20% acceptance，exact current-frame匹配+Q-set交叉可能远低于此；actual=0使full尚不可承诺。

## 具体修改动作

1. 分账history search/reachability/matching与Q value stage，记录每accepted pair前的history steps和reject code；给hard cap总env steps而非只value ceiling。
2. 列evaluator档矩阵及复用：new seeds/H32/reward/checkpoint分别需哪些new rollout，给最坏与共享后总steps。
3. 正文明确MVP M16/S4只验证acceptance/coverage/throughput；primary固定M64/S8且须功效达标后才运行。
4. 加checkpoint/asset/task/pair lineage manifest与near-duplicate detection；三backbone×四格训练GPU-hours/seed数另列。

## Round 08 验收条件

必须闭合history-search与独立evaluator总账、MVP/primary边界及lineage去重。R8再评估synthetic-to-AliasBench/真机迁移是否足以支撑CVPR主张。
