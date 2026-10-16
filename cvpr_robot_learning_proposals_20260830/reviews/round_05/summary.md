# Round 05 Summary — 实验与可证伪性

- Review date: 2026-08-30
- Input revisions: 12/12 r04，`Responds-To-Review: round_04`
- Refinement logs: 12/12 含 `## round_04 / r04`
- Individual reviews: 12/12，均含十五维评分
- Policy: round<10，全部 **FAIL / REVISE**
- Score range: 4.20–4.33

## 汇总

| ID | 平均分 | Fatal | R5首要缺口 |
|---|---:|---|---|
| GEO-P1 | 4.20 | 否（旧fatal解除） | selection regret定义/功效；与OOD success层级 |
| GEO-P2 | 4.30 | 否 | 多primary；snapshot cluster与真机功效 |
| GEO-P3 | 4.30 | 否 | 90%coverage risk唯一化；unseen corruption协议 |
| WAM-P1 | 4.27 | 否（R4 fatal解除） | miss/unknown矛盾；proper score primary与stratum权重 |
| WAM-P2 | 4.23 | 否 | S16但成本仍按S8；冻结资源预算/λ |
| WAM-P3 | 4.33 | 否 | primary时点/指标；baseline同deploy fields |
| STR-P1 | 4.33 | 否 | recovery操作定义、censor和family-macro统计 |
| STR-P2 | 4.33 | 否 | 唯一resource-constrained primary；trace-block CI |
| STR-P3 | 4.27 | 否 | official natural split无pair/Q，当前primary不可直接计算 |
| JEP-P1 | 4.20 | 否 | metric/JEPA 2×2；role assignment train/eval公平性 |
| JEP-P2 | 4.27 | 否 | event F1 primary不能证明planning H1 |
| JEP-P3 | 4.30 | 否（R4 fatal解除） | K4/K32预算；interaction×q 2×2与唯一regret primary |

## Fatal复核

WAM-P1 与 JEP-P3 的R4 fatal均已通过公式重写和最小例解除：前者现在显式边缘化`p(R,Z|D)`，prior不再抵消；后者conditional predictor只用true-e cells，learned-q只走监督/正确边缘化/规划蒸馏。GEO-P1旧relation-type泄漏也持续解除。本轮未发现新的公式级fatal。

## R5跨Proposal结论

1. **“有很多指标”不等于可证伪。** GEO-P2/GEO-P3/WAM-P1/WAM-P3/STR-P2/JEP-P3仍把多个endpoint并列；必须指定一个primary及固定比较者。
2. **统计单元普遍过细。** candidate、seed、event、frame、action pair不是独立样本；至少以snapshot/episode/factorial group为cluster，task为更高层。
3. **修复支持域后要同步预算。** WAM-P2从S8升S16却没翻倍成本；JEP-P3加入K32收敛却仍按K4报资源。
4. **primary必须能在数据上实际计算。** STR-P3自己证明官方AliasBench release无pair/Q，却把natural matched cross-value regret写primary；需改合成primary或明确重建naturalistic数据。
5. **机制endpoint与控制endpoint要层级化。** JEP-P2的event F1、GEO-P1的selection regret、JEP-P1的metric distortion不能单独证明closed-loop H1；控制收益至少是key secondary和claim降级门槛。
6. **operating point必须在validation冻结。** compute/coverage/λ/threshold不能在test后匹配或挑最好曲线点。

## Round 06统一验收 — 基线与消融

1. 每份锁定唯一primary、唯一最强deployable comparator、effect size、cluster unit、CI和功效。
2. 所有强基线共享同candidate manifest、deploy fields、label budget、fallback、planner calls与runtime budget。
3. 对核心机制做正交2×2，不能只做单项删除：representation/supervision、interaction/q、event/scorer、geometry/deconfounding等。
4. baseline代码不可得时冻结正文级重实现差异，不把复现失败计为胜利。
5. key secondary控制终点不达预注册门槛时，自动降级为benchmark/representation claim。

## R6优先级

- **P0**：STR-P3（primary数据不可得）、WAM-P2/JEP-P3（资源合同不一致）、JEP-P2（primary不支持H1）。
- **P1**：GEO-P1/GEO-P2/GEO-P3/WAM-P1/WAM-P3/STR-P2（endpoint/cluster/power）。
- **P2**：STR-P1/JEP-P1（实验合同较接近合格，补定义和正交baseline）。

