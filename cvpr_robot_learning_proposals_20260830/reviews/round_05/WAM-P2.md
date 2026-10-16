# Round 05 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r04
- File: `proposals/WAM-P2_value_of_imagination/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r04 已改incremental time/J/age cost、两折cross-fit Bellman max、S=4/8/16/32曲线、全`Y_0:K` schema并统一continuation术语。R4技术修复成立。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.5 | computation allocation重要。 |
| D2 | 4.5 | nonmonotonic反例清楚。 |
| D3 | 4.0 | paired continuation target待证。 |
| D4 | 4.5 | Bellman→gate闭合。 |
| D5 | 4.0 | 方法S=16但成本表仍按8 seeds，实验合同不一致。 |
| D6 | 4.5 | target-only正确。 |
| D7 | 4.0 | 可生成。 |
| D8 | 3.5 | seed翻倍后MVP/full成本低估2倍。 |
| D9 | 4.0 | post-hoc mean/p95匹配切片与多λ operating points有选择风险。 |
| D10 | 4.5 | baseline强。 |
| D11 | 4.5 | 消融足。 |
| D12 | 4.0 | OOD/真机合理。 |
| D13 | 4.0 | schema好，预算/analysis rule缺。 |
| D14 | 4.5 | 契合CVPR。 |
| D15 | 4.5 | harmful compute负结果强。 |

平均分：**4.23/5.00**。D8=3.5、D3/D5/D9=4.0；R5不通过。

## 实验攻击面

1. **预算矛盾。** primary cross-fit用S=16，实验仍写`×8 seeds=5.12M/20.48M`；应为10.24M/40.96M（若其他因子不变），records/存储也相应变化。
2. **matched ±5%切片可后验选择。** 不同方法的compute分布可能没有重叠，筛选子集改变task mix；应预先固定预算或用constrained Pareto estimator。
3. **λ灵敏度产生多重尝试。** 必须独立validation选λ与threshold，test只一次。
4. **primary只比myopic不足。** H1还声称优于When-to-Trust/Harmo/CheckVLA等最强gate；primary comparator应是全部deployable baseline中最强者，myopic是机制对照。

## 修改与R6验收

1. 按S=16重算env steps/records/storage/wall-clock并设硬cap。
2. validation冻结一个资源预算/λ，primary为该预算下episode success；Pareto全曲线secondary。
3. comparator取所有deployable baselines中validation最强且同预算者。
4. episode/task cluster paired CI与检测5pp功效；不能用多个operating point取最好test结果。

