# Round 06 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r05
- File: `proposals/WAM-P2_value_of_imagination/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已把 S=16 cross-fit 的 steps/records/storage 改为 10.24M/40.96M、640k/2.56M、5.2/21GB，并冻结单一资源 operating point、episode/task 功效和 success 降级。R5 的预算算术问题解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 实时想象分配对 WAM 部署关键。 |
| D2 失败模式清晰度 | 4.5 | harmful compute 与 non-myopic continuation 反例明确。 |
| D3 创新性/最近邻 | 4.0 | VOC/halting 既有，增量靠视觉 CRN target。 |
| D4 机制因果闭环 | 4.5 | paired path→Bellman target→stop gate 闭合。 |
| D5 技术正确性 | 4.5 | cross-fit 与增量成本已合理。 |
| D6 可观测性/泄漏 | 4.5 | exact-reset Y 仅 target。 |
| D7 数据可得性 | 4.0 | 可生成但 40.96M steps 风险大。 |
| D8 算力/工程 | 3.5 | 21GB 只是 records，sim/WAM 总成本仍可能超限。 |
| D9 可证伪性 | 4.5 | 单资源点与 control 降级明确。 |
| D10 基线强度 | 3.5 | 未证明 myopic VOC 是 validation 最强 deployable gate。 |
| D11 消融充分性 | 3.5 | paired target 与 continuation policy 未正交。 |
| D12 OOD/真机 | 4.0 | unseen task 有，真机只校准 gate。 |
| D13 复现性 | 4.5 | CRN hash、全路径 record 和 cost 定义细。 |
| D14 CVPR契合度 | 4.5 | 视觉世界模型与实时决策问题契合。 |
| D15 风险/负结果 | 4.5 | prevalence/oracle/compute-only 均有早停。 |

平均分：**4.20/5.00**。D3/D10/D11 与均分均未达门槛；round<10，不通过。

## Top 问题与证据缺口

1. **“固定 myopic VOC 为最强”没有证据。** When-to-Trust、CheckVLA、PonderNet/ACT 或 compute-only scheduler 可能在 validation 上更强。先验指定 myopic 可把 primary 变成对容易基线的胜利。
2. **共享 labels 会抹平或偏置比较。** 原生 gates 不使用 S16 exact-reset continuation target；若全部给该 label，它们已不再是原方法；若不给，本法多拿大量监督。需要 native/equal-target 两条赛道。
3. **当前消融没有隔离两项主张。** 收益可能来自 paired CRN label，也可能来自 finite-horizon Bellman stopping，而不是两者组合。compute-only/visual shuffle不能回答这个问题。

## 具体修改动作

1. 最强 deployable comparator 改为 validation winner `max{myopic VOC, Ponder/ACT, When-to-Trust proxy, CheckVLA-style risk gate, compute-only scheduler}`，同一冻结资源点；primary 用 closed testing 同时超过 winner 与 myopic direct baseline。
2. 建 `target {ordinary/unpaired or shuffled-seed, paired CRN cross-fit}` × `stopping {myopic one-step, finite-horizon continuation}` 2×2；四格同输入、K、head 宽度、候选、planner calls、label count。另保留 native baselines 表。
3. 每个 baseline 分开报告原生 target 与 target-equal adapter，禁止一句“共享 labels”带过。finite-horizon oracle 不参与 deployable winner。
4. 预算表增加每格 target generation、WAM forward、GPU-hours、CPU sim-hours、peak I/O；fallback 的执行收益必须共享。

## Round 07 验收条件

必须把 comparator 改为 validation winner，补 target×stopping 2×2 和 native/adapter 双表，并给 5k pilot 的 aggregate sim throughput 与 wall-clock 测量计划；否则 D10/D11 维持 3.5。
