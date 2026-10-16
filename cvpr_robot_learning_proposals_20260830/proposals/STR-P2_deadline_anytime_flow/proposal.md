# STR-P2：截止时间条件的 Multi-Exit Chunk Flow 控制

- Proposal-ID: STR-P2
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: 新增cutoff state跨进程serialization/replay单测，禁止依赖later solver state；主表加入host-sync worst latency。

## 问题与假设

RTC 已解决异步 prefix inpainting，REMAC 已修复 intra-chunk mismatch，PACE/DEHP 已选择执行 horizon，CheckVLA 还加入 latency-aware hard prefix。仍未回答：推理耗时随机、观测逐渐变旧时，生成模型在任意 cutoff 被打断能否给出质量可预测、完整可执行的 chunk，而不是 deadline 到时丢弃未完成采样或执行旧动作。

H1：对**标准 conditional chunk flow/diffusion**，多个 NFE cutoff 通常不保证都输出校准的完整 action chunk。对 1/2/4/8 NFE 用同一 teacher/shared noise 蒸馏，并把 observation age 对 scheduler 与 action content 正交建模，可在 burst jitter 下形成优于 RTC+固定 NFE 与一步模型的质量—deadline Pareto。这里不把 SFP 的 physical-time intermediate 当作完整 chunk；若普通 multi-exit/consistency distillation 在同预算持平，本方案只保留 wall-clock benchmark，不宣称新 flow primitive。

## 精确差异

- RTC/CheckVLA：处理 chunk 间并发与硬前缀；本方案保留 RTC 的 frozen-prefix contract，研究标准 chunk 生成内部的 multi-exit validity。
- PACE/DEHP：选择执行多少动作，未改变生成在何时停止；本方案固定 action execution protocol，只分配 NFE/cutoff。
- DMPO/HybridFlow：固定一步/两步；本方案同一模型支持 1…K 步并随 deadline/观测龄平滑退化。
- SFP：其 ODE 时间就是物理 action-trajectory time，Algorithm 2 每积分步立即执行当前动作，输出对象不是“同一完整 chunk 的多 NFE exits”。因此只作 physical-streaming 参照，不作为本模型 checkpoint/teacher，也不用完整 chunk 指标攻击它。

**匹配所选语义的最小 deadline 反例。** 标准 chunk-flow pipeline 的控制周期 80ms，完整 chunk exits 在 20/40/80ms（1/2/4 NFE）完成；Trace-A/B 都有 mean=40ms、p95=80ms，但 A 的 80ms 负载独立，B 将其组成连续 5-cycle burst。动态障碍每 40ms 横移：RTC+固定4-NFE在 B 中连续复用旧 chunk，age 变为 80/160/240ms；固定1-NFE总能按时，却在 A 的常态周期精度较低。本模型在每个固定 observation/version 上提交最近完成的完整 chunk，并在 burst 首周期选择 age-conditioned 1-NFE exit，恢复后回到4-NFE。SFP 作为另一 pipeline 报 next-action availability/success/compute，不要求它产生同一完整 chunk exits，也不被包含在此反例的“丢弃未完成 chunk”指控里。

## 方法

底座选定为标准 conditional chunk flow。对每k与预注册Mondrian group(device family×queue bin)用exchangeable calibration traces估 latency upper quantile `q̂_{1-α/4,k}(x features)`；部署选最大满足 `q̂_k≤remaining deadline` 的k。union bound给同group内、marginal over calibration/test exchangeability的simultaneous miss≤α，不声称任意x conditional guarantee；新device/shift只报empirical miss并触发fallback。另在第二calibration replay直接检验selected-policy miss≤5%，test不调阈值。

**两条不混合的时间轴。** (1) 生成 solver-time `τ∈[0,1]`：固定 `(o_n,l,q_n,ξ,version=v)`，按 k=1,2,4,8 次 vector-field evaluation 得到四个完整 tensor `A_v^(k)[B,H,D_a]`；exit 只有全部 H 个动作完成且通过约束检查才可 commit，commit unit 是整个 `versioned chunk`。(2) 物理 control-time `n,n+1,…`：控制器持有 `A_v[H,D_a]`，每 tick 仅执行一行 `A_v[h_elapsed,:]`；若推理与执行并发，RTC 冻结 `A_old[0:h_elapsed,:]`，新 version 只能替换未执行 suffix。SFP 的积分步/物理动作推进属于第二种范式，本方法不复用其 t。

**可逐步模拟的状态机。** `OBS(v,n)→SOLVE(v,k)`；每个 k 完成后生成 `EXIT_READY(v,k,[H,D_a])→CHECK(v,k)`；若 `now≤deadline` 且 version 仍为 v，则 `CAS_COMMIT(v,k)`，否则保留旧 chunk；控制线程只读 committed version 并执行 `EXEC(v,h_elapsed)`；新观测使未提交的旧 version 标记 stale，但不修改已执行 prefix。日志为每次状态转移保存时间戳/version/k/shape。

若所有新exit均miss，old suffix只到age_max=2；之后reactive/hold fallback。**全部baselines共享同fallback权重、参数、训练数据和age_max**，成本计入；另报所有方法no-fallback结果，防fallback贡献冒充scheduler。

**多 cutoff 一致性。** 先冻结 K-step teacher `T(o,l,s,age,ξ)`；对同一条件和同一 base noise `ξ`，所有 cutoff `A_k` 对齐同一个 teacher sample，而不是互相当 teacher：`L_dist=Σ_k w_k||A_k(o,age,ξ)-stopgrad(T(o,age,ξ))||²`。flow consistency 用 probability-flow path 的局部 consistency loss，硬 prefix 坐标在所有 k 完全相同；若 teacher multimodal，则报告 per-cutoff energy distance/MMD、constraint violation、action regret 与 coverage，而不是只报 L2。`L=Σ_k w_k[L_flow^k+αL_dist^k+βL_prefix^k+γL_feasible^k]+ηL_age`。高 NFE 上限若被多出口损伤>2pp则采用共享 trunk+two-head，并把额外参数/FLOPs纳入预算。

| 变量 | student/action 训练 | target | 部署 | 审计 |
|---|---:|---:|---:|---|
| 当前 RGB/语言/proprio、已执行 prefix | 是 | 是 | 是 | RTC-style hard prefix；标准 chunk flow |
| deadline、elapsed time、观测龄、设备负载 | 是 | — | 是 | monotonic clock/queue |
| teacher K-step action | 否 | 是 | 否 | distillation stop-grad |
| future observation/actual latency trace future | 否 | target replay仅采样 | 否 | 不预知未来抖动 |
| 任意 cutoff 完成 chunk `[B,H,D_a]` | 是 | — | 是 | 全 tensor 完成才原子提交/版本号 |

## 数据、系统与实验

使用 π0.5/标准 conditional flow checkpoint（明确排除 SFP action-time checkpoint），在 Kinetix 12 dynamic tasks、RoboTwin 10 tasks 上记录三硬件/网络 trace：p50 20–300ms、长尾/突发负载。trace schema 保存 monotonic `sensor_ts/start_ts/exit_ts(k)/check_ts/commit_ts/controller_ts`、queue depth、device、energy、chunk version、tensor shape；训练/测试按 device 和 burst autocorrelation 隔离，预注册 unseen trace families，并对 family macro 与 worst-family 都报告。MVP 2×A100、3 天；完整 8×A100、7 天；真机 6 tasks×100 trial。

同输出对象强基线：RTC fixed/early-stop、standard multi-exit、DMPO、HybridFlow与oracle cutoff；全部同 checkpoint/data/NFE/output/fallback。open-loop replay 可共享 observations、teacher chunk与latency trace；**closed-loop动作分叉后不再声称共享observations**，只共享 reset、task template、initial environment seed/trace block，统计单元为episode。最强 comparator从validation可行集冻结。唯一primary为冻结budget下success，miss≤5%与jerk≤1.05×RTC是约束。

age 做预注册 2×2：只输入 scheduler、只输入 policy content、两者都输入、两者都不输入；在固定 k 下检验 age-conditioned action regret，隔离“选几步”与“动作内容随陈旧度改变”。其余消融：无 multi-cutoff/teacher/atomic commit、固定 scheduler、cutoff 权重、hard/soft prefix、错误 deadline 反向干预、future-latency oracle 阳性对照。

mode定义只在training teacher actions上用冻结k-means/semantic event clustering，cluster数由train silhouette选定并冻结；test用固定centroid Hungarian匹配，不按结果重聚类。每k用256ξ报MMD/mode coverage/per-mode success；主要mode下降>10%否定。

### R6 exit-objective×scheduler 2×2 与系统复现合同

| baseline-native | native scheduler/wrapper | 同系统 adapter |
|---|---|---|
| RTC fixed/early-stop、standard multi-exit、DMPO/HybridFlow | 各原生 timing/commit | 接统一 CAS atomic-commit、age_max/fallback、deadline/energy logger |

| label/input-equal 2×2 | best fixed/ordinary scheduler | same conformal chance scheduler |
|---|---|---|
| standard consistency/multi-exit objective | S×F | S×C |
| shared-noise multi-cutoff objective | P×F | P×C（proposed） |

四格共享 teacher/data/NFE/output chunk、scheduler features、calibration traces、age scheduler/content 2×2、parameters±5%、CAS/fallback与 runtime profiler；wrapper-off 仅诊断。validation winner 只在 success 最大且 miss/jerk 满足约束的可行集中冻结；若无 baseline 可行，报告 constraint frontier，不把 infeasible 当0分。

trace block固定60s、1kHz CUDA/monotonic timestamps与10Hz power samples；丢前5s warm-up，以 latency ACF降至<0.1后的首个lag或10s（取大者）切block，ESS=`n/(1+2Σρ_l)`，power用ESS而非raw blocks。训练总账列 demonstrations、teacher calls、4 cutoffs losses、4格×3 seeds GPU-hours、calibration/test episodes。CUDA event与host monotonic做每run同步，能耗减idle baseline并梯形积分，queue/CAS wait/retry全计。manifest锁device/driver/CUDA/clock/power Hz/trace schema。**截至r07 actual replay=0**。

### R8 device OOD、fallback 与在线 guard

- **唯一主命题：** standard chunk flow 的完整multi-NFE exits在冻结budget改善held-out trace success；SFP仅secondary。**不声称**held-out device conformal guarantee。
- device split固定train=A100、cal=独立A100负载、test=另一GPU family；recalibration另表。真机root×trace block随机方法，shared collision/force/hold controller。
- commit前检查shape/version/prefix/timestamp/constraint，失败原子回退旧suffix/hold并计deadline。报fallback/CAS/stale、fallback-only与conditional success；fallback>30%或解释>50%增益则降级 **Atomic Multi-Exit Runtime**。

### R9 论文合同与审稿攻击

- 标题：**Deadline-Valid Complete-Chunk Exits for Conditional Flow Policies**。primary=constraint-feasible success；not-claim=SFP同输出或新device guarantee。最危险基线standard multi-exit+same scheduler首行。
- 攻击：consistency已有→同scheduler下objective 2×2；只是systems→complete-chunk/age/deadline联合命题；SFP更强→cross-paradigm secondary。
- P×C与S×C持平→删training innovation；control<3pp→runtime；device/real失败→atomic benchmark。降级标题 **Atomic Multi-Exit Runtime Benchmark**。

### R10 cutoff serialization/replay 单测

对每k保存 `obs/version/base-noise/scheduler-state/cutoff-state/checksum`，终止原solver进程并在**无later solver state/cache**的新进程反序列化，重建chunk须bitwise identical（浮点非确定路径容差1e-6且hash一致）。故意删除字段必须失败closed。主表报告serialization bytes/time、host→device同步与clock alignment的worst/p99延迟，并计入deadline。

## 判负

在至少三种 unseen jitter traces、冻结预算且 mean/p95 compute ±5% 下，primary success 相对最强 deployable comparator 提升≥5pp，deadline miss 降≥50%且 jerk≤1.05×RTC。与 best fixed 和 multi-exit 的两项主比较用预注册 closed-testing，未全部通过不得选 test 上较容易者。若 MMD/mode 指标改善但 success<3pp，降级为生成一致性结果。SFP 仅独立报告跨范式结果。若通用 consistency/multi-exit 同预算差≤2pp、one-step DMPO 更好，或 age 只进 scheduler 与两处都进差≤2pp，则分别否定新增机制。任何 exit prefix violation>0.5% 即暂停真机。

## 风险与里程碑

多-cutoff loss 可能损害高 NFE 上限，报告 Pareto 并允许 two-head；设备 trace 过拟合用 unseen GPU/network。两周完成原子 runtime+trace replay；两月完成真机与三硬件。负结果产出 VLA wall-clock benchmark 与 cutoff validity 测试套件。

## 证据

[RTC 2506.07339](https://arxiv.org/abs/2506.07339)、[Streaming Flow Policy 2505.21851](https://arxiv.org/abs/2505.21851)、[REMAC 2601.20130](https://arxiv.org/abs/2601.20130)、[PACE 2606.00537](https://arxiv.org/abs/2606.00537)、[DEHP 2606.11408](https://arxiv.org/abs/2606.11408)、[CheckVLA 2607.26789](https://arxiv.org/abs/2607.26789)、[DMPO 2601.20701](https://arxiv.org/abs/2601.20701)。
