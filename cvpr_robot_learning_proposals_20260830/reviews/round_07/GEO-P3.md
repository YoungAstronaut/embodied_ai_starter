# Round 07 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r06
- File: `proposals/GEO-P3_geometry_confidence/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已加入native/equal defer、final-regret/B×pooled/relation 2×2、每法独立同预算calibration、repair acceptance/noise/cost gate；监督公平已实质响应，repair pilot明确为0。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 几何可靠路由有部署价值。 |
| D2 失败模式清晰度 | 4.5 | corruption与hard pairs明确。 |
| D3 创新性/最近邻 | 4.0 | relation-specific repair target是有限增量。 |
| D4 机制因果闭环 | 4.5 | repair B→router→branch risk闭合。 |
| D5 技术正确性 | 4.5 | coverage/calibration逻辑一致。 |
| D6 可观测性/泄漏 | 4.5 | GT repair严格target-only。 |
| D7 数据可得性 | 3.5 | B acceptance/precision完全未知。 |
| D8 算力/工程 | 3.5 | 现有env账遗漏per-relation repair执行。 |
| D9 可证伪性 | 4.5 | B无效会删除。 |
| D10 基线强度 | 4.5 | native/equal和2×2充分。 |
| D11 消融充分性 | 4.5 | supervision×structure+noise曲线强。 |
| D12 OOD/真机 | 4.0 | unseen corruption设计好，真机薄。 |
| D13 复现性 | 4.0 | repair/editor版本与成本公式未闭合。 |
| D14 CVPR契合度 | 4.0 | 视觉可靠性议题契合。 |
| D15 风险/负结果 | 4.5 | calibration-only降级明确。 |

平均分：**4.20/5.00**。D3/D7/D8/D13未达门槛；round<10，不通过。

## 数据/资源攻击面

1. `2k×3 branches×S4×H16=384k`只覆盖原三分支。每个`B_ij`需替换relation、产生repaired action并与branch regret比较；若repaired action也执行H16，成本还乘每snapshot有效relation数。当前账没有这一主target成本。
2. 若`B_ij`只用action-distance而不执行repaired action，则它不是“regret差”标签，方法定义需改。必须二选一，不能同时用低成本和因果效用措辞。
3. GeometryCorrupt四轴×五级、hard A/B、seen/unseen family/severity和三split没有给最小episode数/asset去重规则；2k总量可能使family-level power远低于计划。
4. editor density、decoder consistency、policy-latent validity三个模型/阈值的训练数据和版本未列，容易让calibration split渗入repair选择。

## 具体修改动作

1. 写公式 `N_snapshot×[3+N_valid_relation repairs]×S×H`；若repair只forward不rollout，改写B定义并给oracle-action-distance的局限。
2. 将editor/decoder/policy validity模型的train-only split、commit、threshold fit过程写入manifest，独立于router calibration。
3. 给corruption cell表：family×severity×task×asset×episode，冻结asset/render seed隔离与最小cluster数。
4. 先做100 snapshot repair smoke，报告每snapshot关系数、各gate acceptance、B重复标注一致性与CPU/GPU/I/O；再据此定2k/10k。

## Round 08 验收条件

必须闭合per-relation repair资源与B语义、四轴数据cell和三套split。R8再审查unseen renderer/真实透明高光是否真正OOD，以及三任务真机结论边界。
