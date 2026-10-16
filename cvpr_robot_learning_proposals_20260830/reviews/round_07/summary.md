# Round 07 Summary — 数据、算力与复现压力测试

- Review date: 2026-08-30
- Input revisions: 12/12 r06，`Responds-To-Review: round_06`
- Refinement logs: 12/12 含 `## round_06 / r06`
- Individual reviews: 12/12，均含十五维评分与R8验收条件
- Policy: round<10，全部 **FAIL / REVISE**
- Score range: 4.13–4.40
- Actual pilots reported in proposals: 12/12为0；均明确标注为预注册而非已验证结果

## 汇总

| ID | 平均分 | Fatal | R7首要缺口 |
|---|---:|---|---|
| GEO-P1 | 4.13 | 否；资源P0 | 64KB×20k存储错约1000倍；pair第二成员疑漏×2 |
| GEO-P2 | 4.33 | 否 | full公式、有效censor漏斗、ontology版本 |
| GEO-P3 | 4.20 | 否；资源P0 | 三分支账遗漏per-relation repair rollout |
| WAM-P1 | 4.27 | 否 | 50k无frame/assignment上限；symmetric proof未操作化 |
| WAM-P2 | 4.23 | 否 | S8/S16冲突；WAM/model-grid总账缺失 |
| WAM-P3 | 4.27 | 否；资源P0 | candidate数、episode horizon、1024 subset缺失 |
| STR-P1 | 4.33 | 否 | 每event至少640 target steps且生成/recovery未计 |
| STR-P2 | 4.40 | 否 | trace block/ESS、open/closed路径与训练总账 |
| STR-P3 | 4.20 | 否；可行性P0 | history search与H32/checkpoint evaluator未计全 |
| JEP-P1 | 4.20 | 否 | horizon、9.92M pairwise OT/storage与seed nesting |
| JEP-P2 | 4.30 | 否 | full/power、target来源与ontology family split |
| JEP-P3 | 4.27 | 否 | 448k措辞矛盾；H/history/model-grid未计 |

## Fatal与算术复核

本轮未发现新的方法公式级fatal，但发现三项必须在r07修正的资源算术/定义问题：

1. GEO-P1：若target shard真是64KB/pair，20k仅约1.28GB而非1.3TB；若两名pair成员均执行M64×S4×H16，则是8192而非4096 env steps/pair。
2. GEO-P3：384k/1.92M只含三原始branch；`B_ij`若以repaired-action short-horizon regret定义，必须再乘有效relation repairs。若不执行，则B不能称regret差。
3. JEP-P3：额外K8/16/32为448k正确；若称K4/8/16/32总和则应480k，K4必须说明复用full subset。

另有两项复现矛盾：WAM-P2同时写S8估值与S16 primary；STR-P2 paired trace只能共享外生latency，closed-loop动作分叉后不能继续共享observations。

## R7跨Proposal结论

1. **“A100×天”不是资源账。** 至少要有`cluster/state×candidate×member/branch×seed×horizon`公式，再列target生成、model-grid训练、validation和独立evaluator。
2. **数据漏斗必须互斥且按cluster。** accepted/censored/rejected、proof-computable、support-valid、abstain等要有稳定code；candidate/seed不是独立样本。
3. **smoke与power pilot不能混用。** 100–200 snapshot可测吞吐/acceptance，不能证明task-level power；先工程gate，再用cluster ICC决定confirmatory规模。
4. **共享target不等于共享训练成本。** 2×2四格可复用rollout shard，但model×seed GPU-hours、validation episodes和planner calls仍需相加。
5. **manifest要能实际重放。** 除commit/schema/seed外，还需generator lineage、task/asset/family split、target字段来源、版本/许可证、hardware/driver/clock及去重断言。
6. **actual pilot=0可以接受为Proposal阶段事实，但不能写已可行。** 当前12份都正确降级为预注册；r07应修算术和gate，不得补造吞吐/acceptance数字。

## Round 08统一验收 — OOD、真机与风险

1. 明确每个OOD轴的train/calibration/test支持：新asset、renderer、task、dynamics、event family、hardware分别改变什么，避免把未见seed称OOD。
2. 真机只作外部效度时必须限制claim；给paired/reset/block随机化、独立trial单位、功效、同步/标注误差与安全停止。
3. simulator GT/AprilTag/force/physics/e标签仅评测或target，验证像素/metadata/threshold不会流入部署。
4. 对sim-to-real detector failure、support shift、latency drift、q/belief miscalibration和fallback dominance做预注册分层。
5. key secondary控制收益未达门槛时，严格执行diagnostic/benchmark/representation降级，不用另一个OOD指标救主claim。
6. 给负结果仍有价值的最小交付：数据生成器、schema、evaluator、failure atlas或runtime benchmark，并明确哪些方法claim删除。

## R8优先级

- **P0**：GEO-P1、GEO-P3、WAM-P3、STR-P3（资源定义直接决定可执行性）。
- **P1**：WAM-P2、STR-P1、JEP-P1、JEP-P3（公式/总账与split需修）。
- **P2**：GEO-P2、WAM-P1、STR-P2、JEP-P2（资源框架较完整，主要补操作化与OOD边界）。
