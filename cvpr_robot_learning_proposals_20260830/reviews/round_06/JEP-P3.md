# Round 06 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r05
- File: `proposals/JEP-P3_stochastic_exogenous/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已把全量固定K4并将K8/16/32限制在500-group校准子集，唯一primary为learned-q held-out action×e regret；加入additive/interaction×belief 2×2、factorial cluster功效。R5 的预算与多终点问题解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 任务相关外生动态会破坏action attribution。 |
| D2 失败模式清晰度 | 4.5 | XOR、方差与mode-weight三类反例强。 |
| D3 创新性/最近邻 | 4.0 | ANOVA/two-latent/stochastic WM既有，组合创新待证。 |
| D4 机制因果闭环 | 4.5 | factorial cells→conditional model→q mixture→ranking闭合。 |
| D5 技术正确性 | 4.5 | true-e conditional与q边缘路径已分开。 |
| D6 可观测性/泄漏 | 4.5 | e label部署不可见且路径审计明确。 |
| D7 数据可得性 | 4.0 | 1.408M outcomes可做但任务构建重。 |
| D8 算力/工程 | 4.0 | 8×A100/10天较重。 |
| D9 可证伪性 | 4.5 | strong baselines持平、q gap和control降级明确。 |
| D10 基线强度 | 3.5 | 最强 comparator 的max遗漏non-JEPA same-objective模型。 |
| D11 消融充分性 | 4.0 | 2×2有价值，但oracle-e/true-q混写且数据贡献未隔离。 |
| D12 OOD/真机 | 4.0 | exogenous OOD合理，真机只外测。 |
| D13 复现性 | 4.5 | measure/kernel/K预算与梯度路径具体。 |
| D14 CVPR契合度 | 4.5 | 视觉JEPA与动态操作问题契合。 |
| D15 风险/负结果 | 4.5 | 可删除JEPA/interaction/deploy claim。 |

平均分：**4.27/5.00**。D3/D10/D11未达门槛；round<10，不通过。

## Top 问题与证据缺口

1. **最强 comparator 定义自相矛盾。** baseline清单有 `non-JEPA stochastic object WM+相同ANOVA/q-cal/mixture loss`，但winner只取 `max(CoCo,Sawada,JEPA-WM)`；若non-JEPA更强，当前primary会避开真正最强者。
2. **2×2把 `oracle e/true q` 合并，信息条件不同。** 观测真实e、知道真实posterior q、用learned q是三种不同上界；混成一格会使interaction主效应不可解释。
3. **balanced factorial data本身可能是主要贡献。** 所有强baseline拿相同4×4数据是公平的，但无法分辨收益来自数据覆盖还是RKHS interaction objective；至少要有parameter-matched generic conditional MDN/cross-attention。
4. **同target non-JEPA需要进入claim gate。** 若它持平，应删除JEPA，但还应决定是否保留interaction-aware benchmark/objective，而不是只写一句降级。

## 具体修改动作

1. winner改为validation上的 `max{CoCo, Sawada, JEPA-WM strongest stochastic, non-JEPA+same objective, parameter-matched conditional MDN/RSSM}`，所有格同4×4×K、q、planner和fallback。
2. 主deploy 2×2只用 `outcome {additive,interaction}` × `posterior {learned q, calibrated generic q}`；另将 oracle-e、oracle-q、learned-q作为三角上界，不与2×2混写。
3. 增 `data {unbalanced observational subsample, balanced factorial}` × `objective {generic conditional stochastic, RKHS-ANOVA interaction}` 的MVP 2×2，预算按相同outcome数下采样；完整实验至少做generic-vs-ANOVA同balanced data。
4. 预注册claim ladder：non-JEPA同目标持平→删除JEPA；generic conditional持平→删除ANOVA objective；balanced data仍改善→只保留benchmark/data结论。

## Round 07 验收条件

必须把non-JEPA same-objective纳入winner，拆开oracle-e/oracle-q/learned-q，补generic conditional同数据对照与claim ladder；R7再给500-group K收敛pilot及每模型GPU/样本调用账。
