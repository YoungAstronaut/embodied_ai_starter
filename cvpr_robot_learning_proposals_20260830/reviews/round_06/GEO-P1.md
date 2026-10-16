# Round 06 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r05
- File: `proposals/GEO-P1_counterfactual_geometry/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已把唯一 primary 锁为 held-out pair selection regret，补出共享 `M=64` 候选、效用公式、pair→task 两级推断、20% 功效目标及控制收益不足时降级规则；R5 的 endpoint/统计缺口基本解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 几何捷径会直接影响部署。 |
| D2 失败模式清晰度 | 4.5 | causal/nuisance/hard-negative 对清楚。 |
| D3 创新性/最近邻 | 4.0 | VGA/MECo/Cofact/CAST 后仅剩 geometry-specific SCM 组合增量。 |
| D4 机制因果闭环 | 4.5 | pair→directional target→同库排序闭合。 |
| D5 技术正确性 | 4.5 | set mass、matching 与 regret 已一致。 |
| D6 可观测性/泄漏 | 4.5 | checker/type 均有 deploy/target 隔离。 |
| D7 数据可得性 | 4.0 | exact-reset pair 可造但接受率未知。 |
| D8 算力/工程 | 4.0 | M64 与分层评估可做，成本仍高。 |
| D9 可证伪性 | 4.5 | 唯一 primary 与自动降级明确。 |
| D10 基线强度 | 4.0 | 强邻居齐，但 generic baseline 的标签等价尚未闭合。 |
| D11 消融充分性 | 4.5 | representation×objective 2×2 已成形。 |
| D12 OOD/真机 | 4.0 | OOD 为 key secondary，真机仍外测。 |
| D13 复现性 | 4.5 | candidate/hash/utility/cluster 已明确。 |
| D14 CVPR契合度 | 4.0 | 视觉几何与机器人决策契合。 |
| D15 风险/负结果 | 4.5 | 持平、低控制收益与不可匹配均可降级。 |

平均分：**4.27/5.00**。D3=4.0、D10=4.0；round<10，不通过。

## Top 问题与证据缺口

1. **“同 accepted labels”仍不等于同监督预算。** 本法使用 checker 导出的 `Y*`、pair type 与 directional loss；`VGA+generic deconfounding`若只拿普通正负 pair，就少拿了动作集合监督。相反，若 generic feature 也拿完整 `Y*`，才真正检验结构几何是否必要。
2. **最强 comparator 是手工拼接而非验证集 winner。** `VGA+CAST/Cofact-style`可能弱于 full-token GFM+同 SCM、MECo+同 objective 或 object-token+SCM。预先固定一个未经 pilot 验证的组合会留下 cherry-pick 攻击面。
3. **2×2 尚缺 matching 因素隔离。** structured token 与 generic feature 的集合大小/匹配难度不同；收益可能来自 Hungarian+null 对齐而非 geometry relation。需要把 deploy matching 作为共享模块或额外因子。

## 具体修改动作

1. 建立两层 comparator：`baseline-native` 按原论文 loss，`label-equal` 给每个 baseline 相同 `Y*`/pair/type 标签；primary 对 validation winner 做 closed comparison，二者都报告。
2. 把候选最强集合写成 validation 冻结的 `max{VGA+generic deconfounding, full-token GFM+SCM, objectness-token+SCM, MECo/CAST重实现}`，同 backbone、M64、训练步、label-seconds、planner calls、fallback、p95。
3. 加 `representation {relation,generic} × objective {generic,SCM} × matching {shared-Hungarian,oracle/none diagnostic}`；至少主 2×2 的两类 representation 都使用同 cardinality、同 matching 代码。
4. 给每个无法获得官方代码的 baseline 冻结公式、输入字段和版本；重实现失败不得计作方法胜利。

## Round 07 验收条件

正文必须列出 baseline-native/label-equal 两张合同、validation winner 规则、matching 公平对照及每格额外 label-seconds/存储/训练步；否则 D10 不得升至 4.5。R7 还需给 pair 生成漏斗与数据 manifest。
