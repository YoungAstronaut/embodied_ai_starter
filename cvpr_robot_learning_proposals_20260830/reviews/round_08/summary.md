# Round 08 Summary — OOD、真机与风险边界

- Review date: 2026-08-30
- Input revisions: 12/12 r07，`Responds-To-Review: round_07`
- Refinement logs: 12/12 含 `## round_07 / r07`，各自7个distinct rounds
- Individual reviews: 12/12，均含十五维评分与R9验收条件
- Policy: round<10，全部 **FAIL / REVISE**
- Score range: 4.23–4.47

## 汇总

| ID | 平均分 | Fatal | R8首要缺口 |
|---|---:|---|---|
| GEO-P1 | 4.27 | 否 | 四OOD轴/预训练边界、candidate support、真机near-pair |
| GEO-P2 | 4.37 | 否 | sim-engine-real接触语义、fallback与force安全 |
| GEO-P3 | 4.27 | 否 | LOFO family、achieved coverage公平、stop dominance、真机规模 |
| WAM-P1 | 4.37 | 否 | “provably”应降ε-symmetric；4+实例与tag/安全 |
| WAM-P2 | 4.33 | 否 | 真机仅校准无独立test；task/model/device OOD混叠 |
| WAM-P3 | 4.40 | 否 | physics×appearance、真机block drift与force guard |
| STR-P1 | 4.37 | 否 | 只有task OOD；RMRT缺collision/jerk硬约束 |
| STR-P2 | 4.47 | 否 | held-out device、fallback dominance、在线prefix guard |
| STR-P3 | 4.23 | 否 | synthetic→AliasBench不验机制；真机near-match未定义 |
| JEP-P1 | 4.30 | 否 | adapter regime与跨embodiment OOD边界 |
| JEP-P2 | 4.33 | 否 | closed/open ontology、sim-real event GT与在线guard |
| JEP-P3 | 4.33 | 否 | combinatorial vs extrapolative OOD、q失校和真机安全 |

## Fatal复核

r07已修正R7全部资源P0：GEO-P1两成员/存储、GEO-P3 relation repair、WAM-P2 S16、WAM-P3 candidate/sample、STR-P3总cap、JEP-P3 K总账均未复发。本轮未发现新方法公式级fatal。

## R8跨Proposal结论

1. **OOD必须分轴。** 未见asset、renderer、task、physics、event family、action×e cell、device trace不是同一种shift；各自给train/calibration/test支持，不能只报一个macro OOD。
2. **组合留出不等于外推。** JEP-P3 held-out action×e cells是combinatorial generalization，只有超出`μ_train(e)`的speed/phase才是extrapolative shift；JEP-P1若在target embodiment训练adapter也不是zero-shot。
3. **真机外测不能证明sim target。** WAM-P2真机拿不到continuation target、STR-P3/AliasBench拿不到pair-Q；只能验证closed-loop transfer，必须拆claim。
4. **fallback/stop会伪造安全收益。** GEO-P2/GEO-P3/WAM-P2/STR-P2/JEP-P2/JEP-P3须报告route/K/abstain/fallback比例、fallback-only及conditional success；高fallback触发claim降级。
5. **安全约束应成为可行条件。** collision、force、workspace、jerk、deadline、illegal transaction、prefix/timestamp检查需在线commit前执行，并由所有方法共享。
6. **GT与marker只在独立logger/evaluator。** AprilTag、external marker、belt encoder、force/physics/e label不能进入model RGB或metadata；需报告裁除、反射、同步和annotation误差。
7. **真实配对以root为单位。** 方法顺序在root template/trajectory/physics/trace block内随机；reset漂移、磨损、温度和硬件负载纳入block，不能把重复trial当独立。

## Round 09统一验收 — 论文叙事与审稿攻击面

1. 每份写一句唯一主命题、一句明确“不声称什么”、一个primary、一条自动claim ladder；摘要/标题/贡献不得超过实验合同。
2. Related Work先承认被最近邻覆盖的部分：VGA/MECo、ContactGuard、JPDA、VOC、BOCPD、Action-Bisim、NRI、functional ANOVA等；只突出剩余可证伪差异。
3. 把最危险近同构baseline放在主表第一行，不藏appendix；native与label/input-equal并列。
4. 主图只画部署可见信息流，GT/oracle/repair/Q/e/physics走虚线target shard；真机logger单独画，不与student混线。
5. 预写三条审稿攻击及正文回应：额外oracle supervision、synthetic self-consistency、fallback dominance/real transfer。
6. 标题和摘要准备claim降级版本：method→benchmark/diagnostic/representation/runtime；若关键secondary未过，替换而非继续保留强标题。

## R9优先级

- **P0**：STR-P3、WAM-P2、GEO-P1/GEO-P3（外部效度与主claim错位最明显）。
- **P1**：GEO-P2、WAM-P1/WAM-P3、STR-P1、JEP-P1/P2/P3（需限制OOD/安全并准备claim ladder）。
- **P2**：STR-P2（协议最接近合格，重点压缩叙事并显式held-out device/fallback边界）。
