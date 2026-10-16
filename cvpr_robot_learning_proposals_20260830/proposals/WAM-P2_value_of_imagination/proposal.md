# WAM-P2：固定实时预算下的世界想象价值学习

- Proposal-ID: WAM-P2
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: 资源主表拆target-build compute、teacher quality与deploy decision compute，明确离线oracle rollout不计部署但全额计research cost。

## 问题与假设

When-to-Trust 已用 predicted-vs-real consistency 调执行长度，HarmoWAM 已 gate predictive/reactive experts，CheckVLA 已用 conformal risk 验证/重写动作，DELE 又证明可直接预测未来状态。剩余问题不是“是否按需想象”，而是在固定 wall-clock/NFE 下，多做一单位 world rollout 是否能带来超过延迟代价的决策改进。

在一个 decision epoch，固定初态、候选/WAM随机源与外生 seed e。第 k 次扩展后选择 `a_k` 并得到环境效用 `Y_k=progress-2collision-0.1jerk-λ_d1[deadline miss]`。为允许 `D_k=Y_{k+1}-Y_k` 负后再正，定义有限 `K=4` stopping target：`V_K=Y_K`，`V_k=max(Y_k,E[V_{k+1}|I_k]-c_k)`，continuation advantage `A_k=E[V_{k+1}|I_k]-c_k-Y_k`；部署仅当预测 `A_k>0` 且 chance deadline 可满足时继续。一步 `E[D_k]-c_k` 只作 myopic 强基线。

## 最近邻差异

- When-to-Trust：现实一致性决定执行 horizon；本方案决定想象深度/NFE并显式估计净决策收益。
- HarmoWAM：模式 gate；本方案允许 0…K 序贯计算、任意时刻可停，并对额外计算的反事实收益监督。
- CheckVLA：conformal risk+suffix rewrite；本方案不声称风险保证，主要对象是 computation allocation，CheckVLA 是强基线。
- DELE：never-video compact future；作为 `k=0/compact` 路径，不能被本方案算作弱基线。

| 工作 | gate/停止目标 | 是否直接估计 marginal decision value | world-rollout 统计 | 公平比较 |
|---|---|---:|---|---|
| When-to-Trust | predicted-real consistency / execution | 否；按原文 proxy | rollout consistency | 相同候选/WAM/NFE/clock |
| HarmoWAM v1 | proprio keyframe phase label→predictive/reactive expert gate | 否；BCE interaction-phase target，不是reward delta | current visual gate+fixed future WM | 同模型参数与两路cost |
| CheckVLA v1 | action-conditioned rolling discrepancy+functional conformal first-intervention trigger | 风险/repair，不是额外一次想象的paired reward delta | causal risk/exceedance | 同p95/介入/候选预算 |
| adaptive computation / PonderNet | computation penalty/halting | 通常不是机器人 exact-reset potential outcome | hidden-state halt | compute-only 强基线 |
| rational metareasoning / Selecting Computations | classic expected value of computation | **是，概念先验** | belief/decision statistics | 本方案不能声称发明VOC；只贡献视觉WAM可执行CRN target/data |
| 本方案 | `E[Y_{k+1}-Y_k]−cost` | **是，允许负值和正负交替** | partial visual rollout error/margin/uncertainty | mean/p50/p95/p99/energy/候选/频率均报告 |

When-to-Trust v2 的 verifier target 来自 valid/success segments 与 failed/corrupted segments的 binary executability，并在真实执行中比较 predicted/real future后调整**剩余chunk执行长度**；HarmoWAM v1 按 gripper/EE-height phase label在predictive/reactive experts间路由；CheckVLA v1以 rolling action-consequence discrepancy 和 conformal threshold触发 latency-feasible suffix rewrite。三者都不是 common-state `Y_{k+1}−Y_k` 的边际计算价值监督。这里不宣称 VOC/halting 新，只主张该 paired target 是否比这些 proxy 更能分配视觉 WAM expansion。

## 方法

reactive policy 先产生N个候选。WAM逐次扩展，continuation head从当前 partial rollout预测 `A_k`；从 k=K 向0离线动态规划产生 target。三步最小例 `Y=[0,-1,4]`, costs `[0.2,0.2]`：myopic在0停止，continuation target给 `V_1=3.8,V_0=3.6` 并继续；预注册统计 `D_k<0,D_{k+1}>0` prevalence，低于5%时不声称 continuation必要。primary每个 `(s,k)` 统一用 **S=16** CRN cross-fit；S4/8/32只在nested seed prefix上做bias/variance曲线，不生成另一套primary标签。

`L=L_rank+αw_k huber(\hat A_k,stopgrad(A_k))+β1[confident]Brier(1[A_k>0])`。环境reward的deadline miss是离散后果；每步cost仅计增量 `c_k=λ_tΔtime_k+λ_EΔjoule_k+λ_age(age_{k+1}-age_k)`。age从20→40→60ms只扣20+20，而非20+40+60；若用terminal age cost则只在stop时扣一次，两定义分表不可混用。

primary用S=16 seeds做2-fold cross-fit：fold A估 `E[V_{k+1}]`，fold B应用max/产生label，再交换A/B平均；另做S=4/8/16/32与nested bootstrap bias曲线。record保存完整 `Y_0:K,Δtime_0:K,Δenergy_0:K,age_0:K,all seeds/candidate hashes`，可离线重算Bellman；CI筛选只作权重，不删除样本。

CRN schema锁定 environment dynamics/sensor seed、candidate proposer seed与candidate hash、WAM expansion noise/dropout、ranking tie-break和evaluator seed；无法共享的随机源显式记录并进入方差分量。部署伪代码：observe→for k=0..K: atomic rank；预测A_k与latency chance；若A_k≤0/不可按时则execute，否则expand。

| 变量 | student/action 训练 | target | 部署 | 审计 |
|---|---:|---:|---:|---|
| 当前/过去观测、语言、proprio、已执行动作 | 是 | 是 | 是 | 时间≤t |
| 部分模型 rollout、排名、elapsed time | 是 | 是 | 是 | 均为模型预测 |
| exact-reset全路径 `Y_0:K`/增量cost | 否 | 是 | 否 | stop-gradient continuation target |
| 未来真实帧/成功标签 | 否 | 可作离线 target | 否 | future-mask/阳性泄漏对照 |
| 设备 deadline/队列状态 | 是 | — | 是 | 实测 monotonic clock |

## 实验

固定 `K=4` 相邻 expansion pairs。primary 的 S=16 cross-fit 使 5k go/no-go 规模为 `5k×4 pairs×2 branches×16 seeds×16 steps=10.24M` env steps、640k branch records；20k 完整规模为 40.96M steps、2.56M records。每 record 预算8KB，分别约5.2GB/21.0GB；图像只存去重引用。必须先实测 aggregate sim steps/s、WAM expansion states/s 与 I/O：若 5k 在 4×A100+CPU simulator 上>96h或>10GB，降级为2k×K=3×S=4 的 variance-only 结果，不伪称 full。

MVP为10 tasks/5k epochs，预算4×A100最多4天；先报告oracle continuation-positive比例，若<10%早停。WAM partial statistics缓存全k路径；真机只校准gate，不生成反事实target。

强基线：always/never/random、fixed K、uncertainty、When-to-Trust、Harmo、CheckVLA、DELE、PonderNet/ACT、one-step myopic VOC、finite-horizon oracle continuation；全部共享候选、partial-rollout fields、fallback、planner、NFE 和 runtime envelope。最强 deployable comparator 按下述 validation 可行集 winner 冻结，且 primary 仍须额外超过 paired-myopic direct baseline；validation 只冻结一个资源 operating point，test 不挑 Pareto 点。

机制分解：`compute-only` 只读 deadline/device/elapsed/ranking step；`visual` 依次加入 rollout uncertainty、object/contact/geometry error、ranking margin；把 visual rollout stats 在相同 elapsed/任务 bin 内 shuffle，若不降则贡献只是 scheduler。另做无时间/无 miss、一次 gate/序贯、regression/classification、reward horizon、target-noise、反向 gate、oracle、jitter、模型错误类型，以及相同平均但不同 tail latency。

### R6 winner、target×stopping 2×2 与资源合同

| baseline-native | 原生 target/gate | adapter |
|---|---|---|
| Ponder/ACT、When-to-Trust、CheckVLA、compute-only | halting/proxy/risk/clock 原目标 | 另给相同 candidate/partial-rollout fields、S16 label count与共享 fallback，但保留各 gate objective |
| myopic VOC | one-step value | paired/unpaired 两版 |

| label-equal 2×2 | myopic stopping | finite-horizon continuation |
|---|---|---|
| ordinary/unpaired或seed-shuffled target | U×M | U×C |
| paired CRN S16 cross-fit target | P×M | P×C（proposed） |

四格共享输入、K、head width、candidate manifest、label count、optimizer steps、planner calls与 runtime；seed-shuffled 仍用相同 rollout records，只破坏 pairing。deployable winner 在 validation 的冻结资源点与 safety 可行集中按 primary success 从 `max{myopic,Ponder/ACT,When-to-Trust,CheckVLA,compute-only}` 选一次；primary closed testing 必须同时超过该 winner 与 P×M direct myopic。finite-horizon oracle 不参选；native winner另表。

总账除10.24M/40.96M env steps外，另记 `N_epoch×K4` WAM expansion states、4个2×2格×3 train seeds的model-grid GPU-hours、各deployable gate validation env steps和planner calls；8KB record逐字段列bytes并报告image-reference dedup/cache hit。task列表固定train40/validation10/test10（模板不交叠），step blocks按root episode分组；`λ`只在validation拟合。100-epoch smoke必须实际输出sim steps/s、WAM states/s、I/O MB/s、cache hit、peak VRAM与projected wall-clock；**截至r07仍为0，未测前不进入full**。

### R8 双 claim、OOD 与真机 held-out 合同

- **Claim A（主）：** simulation 中 paired CRN continuation target 改善冻结预算 success；**Claim B（secondary）：** 不读反事实target的实时gate可迁移到真机。**不声称**真机验证了VOC/continuation label。
- OOD分开：held-out task template、held-out WAM checkpoint/error family、held-out device trace各独立表；不取macro掩盖。device zero-shot保持`λ`/threshold冻结，50-shot recalibration另表。
- 真机calibration tasks与held-out evaluation tasks不重叠；每task root trials内方法顺序随机，只报success-latency-energy Pareto。K=0…4选择率、fallback-only、conditional success、deadline/energy/age strata必报。fallback>K0执行的30%或解释>50%增益时，Claim A不受影响但Claim B降为compute scheduler/runtime诊断。若没有held-out real evaluation，删除真机transfer措辞与强标题。

### R9 论文合同与审稿攻击

- 标题：**Paired Continuation-Value Targets for Budgeted World-Model Imagination**。唯一primary为sim budgeted success；not-claim为不发明VOC、不声称真机验证target。最危险基线paired-myopic与validation winner并列首组。
- 攻击：VOC旧→差异仅CRN potential-outcome target/non-myopic prevalence；oracle rollouts买增益→target×stopping与成本主表；real无target→只gate Pareto。
- continuation-positive<5%→删non-myopic、留variance dataset；oracle上界<4pp→终止method；real transfer失败→删Claim B。降级标题 **Paired Imagination-Value Dataset and Scheduler Diagnostic**。

### R10 三列compute/quality分账

主表将 `(1) target-build compute`（env steps、teacher/WAM calls、CPU/GPU-hours、I/O）、`(2) teacher quality`（S16 CI宽、cross-fit/naive差、oracle upper bound）、`(3) deploy decision compute`（gate/WAM calls、mean/p95/p99、J/decision）分列。离线oracle rollouts**不计部署时延**但全额计research/data-generation cost，任何方法比较同时给training-cost与deploy-cost视图。

## 判负

**唯一 primary** 是冻结资源 operating point 下的 episode success，相对 one-step myopic VOC 提升≥5pp；episode 为 cluster、task 分层，paired bootstrap 95% CI，并按5pp、α=.05、power=.8 的 pilot 方差冻结 episodes/task。continuation sign AUROC≥.75/ECE≤.08 为机制指标；若它达标但 success 增益<3pp，降级为 computation-value prediction，不声称控制收益。cross-fit 与 naive max label 差>10%则必须用 cross-fit；compute-only 差≤2pp或 oracle 上界<4pp 否定 paired continuation 主张。

## 风险与里程碑

仿真回报与真机不一致，只校准gate；两周完成full-path schema、cross-fit continuation稳定性；两月完成多硬件/真机Pareto。

## 证据

[When to Trust Imagination 2605.06222](https://arxiv.org/abs/2605.06222)、[HarmoWAM 2605.10942](https://arxiv.org/abs/2605.10942)、[CheckVLA 2607.26789](https://arxiv.org/abs/2607.26789)、[DELE-w0.5 2608.22067](https://arxiv.org/abs/2608.22067)、[EVA 2603.17808](https://arxiv.org/abs/2603.17808)、[Selecting Computations 1207.5872](https://arxiv.org/abs/1207.5872)、[PonderNet 2107.05407](https://arxiv.org/abs/2107.05407)、[Adaptive Computation Time 1603.08983](https://arxiv.org/abs/1603.08983)。
