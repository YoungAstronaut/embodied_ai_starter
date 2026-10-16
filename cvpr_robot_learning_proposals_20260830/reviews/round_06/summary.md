# Round 06 Summary — 最强基线与正交消融

- Review date: 2026-08-30
- Input revisions: 12/12 r05，`Responds-To-Review: round_05`
- Refinement logs: 12/12 含 `## round_05 / r05`
- Individual reviews: 12/12，均含十五维评分与R7验收条件
- Policy: round<10，全部 **FAIL / REVISE**
- Score range: 4.20–4.40

## 汇总

| ID | 平均分 | Fatal | R6首要缺口 |
|---|---:|---|---|
| GEO-P1 | 4.27 | 否 | checker/Y*标签公平；matching与representation混叠 |
| GEO-P2 | 4.33 | 否 | ContactGuard native/typed-label合同；ontology×executor 2×2 |
| GEO-P3 | 4.23 | 否 | regret-only少拿repair-derived B；structure×supervision 2×2 |
| WAM-P1 | 4.33 | 否 | JPDA完整posterior/marginal control近同构基线缺失 |
| WAM-P2 | 4.20 | 否 | 固定myopic并非validation winner；paired target×stopping未正交 |
| WAM-P3 | 4.33 | 否 | PEARL/RMA信息口径；factorization×belief 2×2 |
| STR-P1 | 4.33 | 否 | innovation与ΔQ reset-worthiness未正交 |
| STR-P2 | 4.40 | 否 | standard multi-exit未共享同chance scheduler/wrapper |
| STR-P3 | 4.20 | 否 | 本法多拿pair/Q数据；pair data×cross-value loss未正交 |
| JEP-P1 | 4.27 | 否 | Action-Bisim native/adapter边界与winner规则 |
| JEP-P2 | 4.30 | 否 | action×edit仅是干预；representation×executor训练2×2缺失 |
| JEP-P3 | 4.27 | 否 | winner遗漏non-JEPA same-objective；oracle-e/true-q混写 |

## Fatal复核

12份r05的R5 endpoint、cluster、功效和预算修订均已实际落盘；此前GEO-P2、STR-P2、JEP-P1、JEP-P2、JEP-P3、GEO-P1、WAM-P1等公式/信息流 fatal 均未复发。本轮**没有新公式级 fatal**。但以下公平性缺口若不修，会构成审稿阶段的 major flaw，不能以“同预算”一句带过。

## R6跨Proposal结论

1. **同数据量不等于同监督。** GEO-P1的`Y*`、GEO-P2 typed contact、GEO-P3 repair-derived `B`、STR-P1的ΔQ、STR-P3的M64/S8 Q-set都来自额外oracle target。强基线必须分为原论文native版与拿同target的label-equal adapter版。
2. **最强比较者必须由冻结规则选出。** WAM-P2不能先验指定myopic VOC；JEP-P3不能把non-JEPA+same objective列在清单却排除出winner；STR-P3不能只用原始history baseline。validation只在同一primary/约束下选一次，test不得重选。
3. **删除一个head不是机制分解。** 应对核心主张做正交2×2：GEO-P2 ontology×executor、WAM-P1 evidence×marginal control、WAM-P2 paired target×continuation、WAM-P3 factorization×belief、STR-P1 innovation×value、STR-P2 exit objective×scheduler、STR-P3 pair data×loss、JEP-P2 representation×executor。
4. **共享系统层。** candidate manifest、detector、role/contact matching、calibration split、scheduler、CAS/fallback、planner samples/calls与p95/p99都必须共享；只共享模型参数量不足以公平。
5. **近同构基线最危险。** WAM-P1的完整JPDA posterior、JEP-P2的NRI+same-label+executor、JEP-P3的non-JEPA+same objective若持平，必须按claim ladder删除对应方法贡献，而不是换secondary指标保结论。
6. **官方代码不可得不构成胜利。** 对正文重实现冻结公式/commit/字段；同时区分paper-faithful native与为了公平输入输出而做的adapter。

## Round 07统一验收 — 数据、算力与复现

1. 每份列 baseline-native 与 label/input-equal 两张逐字段合同；冻结validation winner及closed comparison规则。
2. 核心机制至少一个真正正交2×2；四格共享训练样本、label-seconds、参数±5%、optimizer steps、planner calls、fallback与runtime envelope。
3. 给实际pilot漏斗：attempted→valid/support/accepted→train/test，报告cluster数而非candidate/seed伪样本数。
4. 给逐模块资源账：target/env steps、CPU sim-hours、GPU-hours、peak显存/存储/I/O、mean/p95/p99 latency与失败重试；不能只报A100×天。
5. 冻结manifest：数据生成commit、baseline commit/公式、seed/candidate hash、schema版本、hardware/driver/clock、train/calibration/test边界。
6. 若pilot达不到预注册功效或wall-clock cap，必须明确MVP claim降级，不得把低功效结果写confirmatory。

## R7优先级

- **P0**：WAM-P2、STR-P3、JEP-P3（winner/监督公平直接影响primary有效性）。
- **P1**：GEO-P1/GEO-P2/GEO-P3/WAM-P1/WAM-P3/STR-P1/STR-P2/JEP-P2（需补主2×2与共享系统层）。
- **P2**：JEP-P1（已有完整metric×JEPA 2×2，主要补Action-Bisim native/adapter和资源manifest）。
