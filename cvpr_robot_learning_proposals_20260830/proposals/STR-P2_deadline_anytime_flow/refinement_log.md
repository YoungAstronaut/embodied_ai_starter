# STR-P2 Refinement Log

## r00 / pre-review

- 评审要点：RTC/PACE/DEHP/REMAC/CheckVLA 已覆盖异步、horizon 和 prefix。
- 决策：接受，将对象改为生成内部多 cutoff validity 与真实 deadline。
- 具体改动：加入 observation age、atomic commit、同 p95 compute、每 cutoff 约束率与 future-latency 泄漏对照。
- 改后分数：待 round_01。
- 未决项：SFP 中间状态与多-cutoff teacher 的最小实现差异需代码验证。

## round_01 / r01

- 评审要点：核心可能退化为 multi-exit+scheduler；只匹配 p95 不公平；age 对 scheduler 与 action content 混合；multi-cutoff teacher 一致性不清。
- 决策：全部接受；对 SFP 重合设 go/no-go，新意只保留可核验的 conditional-distribution calibration。
- 具体改动：给 mean/p95 相同但 burst 自相关不同的 80ms 最小 trace 和动态障碍后果；所有 cutoff 用同 teacher/shared noise 并以 energy distance/MMD/constraint/regret 校准；公平性扩为 mean/p50/p95/p99/energy/age 且计 runtime overhead；加入 age-scheduler×age-policy 2×2；补官方 SFP 2505.21851 强基线和重合失效条件。
- 改后分数：自评 D3 3.5→4.0、D5 3.5→4.0、D6 维持 4.5、D9 4.0→4.5；待 round_02。
- 未决项：官方 SFP multi-time loss/中间态 calibration 的正文与代码级差异仍是 R2 首要审计；Trace-A/B 的 mean/p95 精确构造需单元测试。

## round_02 / r02

- 评审要点：fatal——SFP 的 ODE t 是 physical action time 且每步立即执行动作，不能同时把其 intermediate 解释为同一完整 chunk 的 1/2/4/8 NFE exits 与 atomic commit。
- 决策：完全接受并选择范式 A：标准 conditional chunk flow 的完整 chunk multi-NFE exits；SFP 降为不同输出对象/时间语义的外部参照。
- 具体改动：标题与假设改为 Multi-Exit Chunk Flow；明确不用 SFP checkpoint；绘出 solver-time `τ,k` 与 physical control-time `n,h` 双轴及 `[B,H,D_a]` tensor/whole-chunk commit；新增可逐步模拟的 versioned state machine；burst 反例只攻击固定-NFE chunk pipeline；基线分为同对象严格比较与 SFP 跨范式 closed-loop 参照。
- 改后分数：fatal 已解除；自评 D3 3.5→4.5、D5 3.0→4.5、D6 维持4.5、D9 4.0→4.5；待 round_03。
- 未决项：multi-exit consistency 的同参数预算、完整 chunk 高 NFE 上限退化和 CAS runtime 尾延迟待 R3 深审。

## round_03 / r03

- 评审要点：scheduler不能预知可完成NFE；单ξ对齐不足以证明分布；old suffix过龄与CAS故障合同缺失。
- 决策：全部接受；部署用条件延迟分布的chance constraint。
- 具体改动：定义conformal latency `P(Tk≤d)≥.95`、mean/oracle对照；256 ξ的MMD/mode coverage；age_max=2 cycles后reactive/hold fallback；stale/CAS/prefix/timestamp故障注入单测。
- 改后分数：自评 D5/D13→4.5；待 round_04。
- 未决项：latency quantile在新硬件的coverage、fallback安全性与mode标注待审。

## round_04 / r04

- 评审要点：split conformal不保证任意x条件概率；max-k破单独coverage；fallback不公平；mode可test重定义。
- 决策：全部接受并收窄保证。
- 具体改动：per-k/Mondrian α/4 quantile+union bound及selected-policy calibration replay；声明仅exchangeable marginal；所有baseline共享fallback并报no-fallback；teacher-train clustering冻结。
- 改后分数：自评 D5/D13→4.5；待 round_05。
- 未决项：Mondrian小样本、union-bound保守性与device shift fallback触发待审。

## round_05 / r05

- 评审要点：validation冻结一个 budget/operating point；primary success、miss/jerk安全约束、paired trace replay、trace-block cluster 和 closed testing。
- 决策：全部接受。
- 具体改动：锁定单一deadline/energy点与最强RTC-fixed/multi-exit比较器；共享obs/环境随机/fallback；episode success唯一主终点，miss/jerk硬约束；unseen trace macro/worst、trace-block×episode功效与双比较closed-testing。
- 改后分数：自评 D8/D9/D10/D12→4.5；待 round_06。
- 未决项：unseen trace family 数与 worst-family 功效待审。

## round_06 / r06

- 评审要点：standard multi-exit未共享chance scheduler/wrapper。
- 决策：全部接受。
- 具体改动：standard/proposed exit×fixed/chance scheduler 2×2；统一age/CAS/fallback/calibration；winner只在validation安全可行集；补driver/clock trace manifest、逐格时延能耗与0-replay gate。
- 改后分数：自评D10/D11/D12→4.5；待round_07。
- 未决项：每硬件100 trace blocks待采。

## round_07 / r07
- 评审要点：trace/ESS、open/closed共享语义、训练/能耗总账不足。
- 决策：接受。
- 具体改动：60s block/ACF/ESS；open共享obs、closed仅reset/task/seed；补demo/teacher/4格×3seed账；CUDA-host同步、10Hz power、idle-subtracted integration和CAS wait。
- 改后分数：自评D5/D11/D12→4.5；待round_08。
- 未决项：actual traces仍0。

## round_08 / r08
- 评审要点：held-out device、fallback dominance、online prefix guard。
- 决策：接受。
- 具体改动：A100 train/cal与new-GPU test；commit前shape/version/prefix/time guard；fallback/CAS/stale conditional表，>30%降runtime。
- 改后分数：自评D5/D9/D14→4.5；待round_09。
- 未决项：new-device只empirical miss。

## round_09 / r09
- 评审要点：consistency旧/系统工程/SFP攻击。
- 决策：接受。
- 具体改动：主线complete-chunk exits；standard+same scheduler首行；三攻击与training/control/device降级runtime稿。
- 改后分数：自评4.5全维；待round_10。
- 未决项：无新fatal。

## round_10 / r10
- 评审要点：cutoff可能依赖later solver/cache。
- 决策：接受。
- 具体改动：跨进程无later-state serialization/replay、hash/1e-6合同、missing-field fail-closed；host-sync worst/p99计deadline。
- 改后分数：内容PASS；待R11。
- 未决项：bitwise GPU确定性待smoke。
