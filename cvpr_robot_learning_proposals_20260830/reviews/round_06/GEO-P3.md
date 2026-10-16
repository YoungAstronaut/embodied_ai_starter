# Round 06 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r05
- File: `proposals/GEO-P3_geometry_confidence/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已冻结 90% frame coverage，把 selected-branch regret risk 设为唯一 primary，并加入 unseen family/severity、episode cluster 功效和同时超过 generic/regret-only 的规则。R5 endpoint 攻击面已收缩。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 几何错误选择性路由有部署价值。 |
| D2 失败模式清晰度 | 4.5 | task-relevant relation bad-event 明确。 |
| D3 创新性/最近邻 | 4.0 | selective routing 既有，增量在 relation-specific target。 |
| D4 机制因果闭环 | 4.5 | repair target→calibrator→三分支 route 闭合。 |
| D5 技术正确性 | 4.5 | coverage/risk/repair validity 已统一。 |
| D6 可观测性/泄漏 | 4.5 | GT repair 严格 target-only。 |
| D7 数据可得性 | 4.0 | corrupt exact-reset 可行。 |
| D8 算力/工程 | 4.0 | 三分支全算成本高但已计。 |
| D9 可证伪性 | 4.5 | 单终点、双 comparator 和降级规则明确。 |
| D10 基线强度 | 4.0 | generic/regret-only 齐，但监督预算不等。 |
| D11 消融充分性 | 4.0 | repair placebo 强，geometry label 与 router capacity 未正交。 |
| D12 OOD/真机 | 4.0 | unseen corruption 合理，真机较薄。 |
| D13 复现性 | 4.5 | calibration split、阈值与成本可复现。 |
| D14 CVPR契合度 | 4.0 | calibration 与视觉机器人交叉契合。 |
| D15 风险/负结果 | 4.5 | relation target无效即删除，结论可降级。 |

平均分：**4.23/5.00**。D3/D10/D11 未达门槛；round<10，不通过。

## Top 问题与证据缺口

1. **regret-only router 少拿 `B_ij` 监督。** 本法使用昂贵 oracle repair 产生 relation bad-event；若 comparator 只看最终 regret 标签，primary 改善可能来自额外 target，而非 geometry-aware factorization。
2. **generic router 的“同输入”未定义到标签与容量。** 应有一个参数匹配 generic auxiliary head，拿完全相同的 per-relation `B_ij` 但打乱/删除 relation identity，检验结构索引而不是多任务监督。
3. **三分支全算掩盖路由工程价值。** 作为 reliability study 可接受，但 baseline 也必须用同 full/coarse/RGB actions、disagreement features 和总成本；不能让 proposed router 独享三分支证据。

## 具体修改动作

1. 预注册 `supervision {final-regret only, same repair-derived B}` × `structure {generic pooled head, relation-indexed head}` 2×2，四格同 encoder、参数±5%、label-seconds、三分支与 calibration split。
2. baseline-native 与 label-equal 分开：SelectiveNet/Learning-to-Defer 原生目标一表；同 `B`/三分支/coverage 的重实现一表，primary 对 label-equal validation winner。
3. 增加 B-target 质量曲线：valid repair acceptance、editor density strata、label flip/noise、same-label shuffled relation ID；否则无法区分 target 噪声与机制失败。
4. 明示所有 comparator 共享 frozen `(ε,λ)`选择程序而非共享数值；每个方法只能在同 validation 预算独立拟合，test coverage再用插值匹配会泄漏。

## Round 07 验收条件

需补 label-equal 2×2、三分支证据共享、每方法 calibration 冻结流程与 repair-label pilot 质量/成本；否则即使 primary 提升也只能归因于额外监督。
