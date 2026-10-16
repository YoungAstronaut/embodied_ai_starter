# STR-P1：基于预测创新的事件触发意图重置

- Proposal-ID: STR-P1
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: 加target-shard独立性断言、future字段schema test与视觉闪烁/低速真事件盲评confusion，防ΔQ target暗带事件标签。

## 问题与假设

IntentVLA 通过历史 intent 减少跨 chunk 冲突，但持久 intent 会在目标移动、抓取失败、接触突变后形成错误惯性。PACE 的速度谷只是运动 phase，REMAC 修的是异步 chunk 不一致，Remember Smarter 压缩历史；它们都没有检验“何种当前证据足以推翻旧 intent”。

H1：预测创新只提供环境/执行 change-point 证据；只有当同一当前观测下“继续旧 intent”的反事实价值比重新规划的最佳替代 intent 低超过 δ 时，才是 reset-worthy change。将这两步分开，能在 novelty 但无需改 intent 时保持模式，也能在视觉变化很小但控制/接触证据要求改 intent 时重置。

三个标签严格分开：`N_t`=观测/动力学分布发生变化，`F_t`=已执行动作未达到预测局部效果，`C_t`=reset-worthy intent change。仿真 oracle 在 snapshot t 上用相同外生 seeds 分别执行旧 intent 与 K 个重新规划 intent，若 `max_j Q_t(z_j)-Q_t(z_old)>δ_v` 且 CI 不跨 0 则 `C_t=1`；干预时刻只生成 `N/F` 候选标签，不能直接等同 `C`。oracle value/未来 rollout 仅作训练 target，student 不可见。

## 最近邻边界

| 工作 | 更新/遗忘信号 | 是否区分 novelty 与 reset value | 时间/控制对象 |
|---|---|---:|---|
| IntentVLA | 固定 causal history intent | 否 | 低频 intent→高频 action |
| PACE | speed-profile phase valley | 否 | execution horizon |
| Remember Smarter | learned history compression/forgetting | 未显式以 paired reset value 为 target | memory token |
| BOCPD/change-point detector | predictive likelihood/run length | 只检测 change，不决定 policy intent 是否应变 | observation process |
| 本方案 | innovation CUSUM **且** alternative-intent value posterior | 是 | observation at t→reset→action at t |

更严格地说，CUSUM、BOCPD、event-triggered control 和“检测到变化后重规划”都不是新意；本方案唯一待验证的增量是：用同一 snapshot、同一外生 seed 的成对 rollout，把 change evidence 与 intervention utility 联合成 `C_t` target，并检验该 target 是否优于纯 likelihood/risk/change gate。

| 邻居 | 在线检测量 | 干预动作 | 候选如何生成 | 最短延迟 | 本方案不重复之处 |
|---|---|---|---|---|---|
| Online Replanning in Belief Space | belief/规划失配 | belief-space replan | 原规划器 | replanning cycle | 已覆盖 belief 触发重规划；未以 paired alternative-intent value 监督 gate |
| Dynamic Planning Horizons | 计划价值/计算预算 | 改 planning horizon | 同一 MPC/planner | planning cycle | 已覆盖触发与 horizon；不区分 novelty 和 reset utility |
| IntentVLA | causal history intent | 固定节奏更新 intent | 自身 intent head | 固定 chunk 周期 | 无 value-paired reset target |
| When-to-Trust | predicted/real future executability discrepancy | 调整剩余 chunk/介入 | 原 action policy | rolling check | 风险/可执行性触发，不是 alternative-intent utility |
| CheckVLA | rolling world discrepancy + conformal risk | suffix repair/functional intervention | 原 VLA suffix | rolling window | 已覆盖“何时介入”；不训练旧/新 intent 的 common-seed ΔQ gate |
| REMAC | asynchronous chunk inconsistency | chunk repair | 原生成器 | chunk boundary/runtime | 修 chunk 一致性，不判 intent 是否应被推翻 |
| 本方案 | innovation + paired `ΔQ_reset` posterior | 保留旧 intent 或重置到 K 个候选之一 | **固定同一 proposer** | one observation/control cycle | 只主张 paired reset-value supervision 的附加价值 |

## 方法

一致时间图为：在 `t−1`，预测器用 `(z_{t-1},RGB_{≤t-1},q^{prop}_{≤t-1},a^{exec}_{t-1})` 预测 t 的 feature/proprio/contact；当前 `RGB_t,q_t^{prop},contact_t` 到达后分别计算 visual innovation `g_t^v` 与 control/contact failure `g_t^f`。同一K=4 proposer产生替代 intents，student value head直接输出 `\widehat{ΔQ}_j=\widehat Q(z_j)-\widehat Q(z_old)` 和 calibrated `P(C)`；部署 score 是 `S_t=max_j \widehat{ΔQ}_j-c_reset`，不是 intent log-probability。evidence gate 为 `(g_v>τ_v OR g_f>τ_f OR S_t>κ_direct) AND S_t>κ_Q`，因此 low-visual contact failure 可绕过纯视觉门槛。

student用5-head ensemble输出每候选ΔQ分布；独立calibration split对absolute residual做split-conformal，K=4使用Bonferroni `α/K` quantile得到simultaneous lower bounds `LCB_j`，再选 `j*=argmax LCB_j`，family-wise marginal coverage目标95%。target bootstrap CI只作label-noise weight，不冒充部署CI；exchangeability只在同event-family/Mondrian stratum声称，unseen event只报经验coverage。

部署伪代码：`residual→(g_v,g_f)→same K→ensemble ΔQ/LCB→if (g_v OR g_f) AND max_j LCB_j>c_reset then reset(argmax LCB) else keep→a_t`。删除任何oracle coverage check；oracle-K/current/random coverage仅evaluator。deploy proposer confidence仅日志，不控制主gate。阈值真值表对 `(V=gv>τv,F=gf>τf,U=maxLCB>cost)` 八格：仅`U=1`且`V∨F=1`的三格reset，其余keep；因此visual novelty但U=0不reset，low-visual的`V=0,F=1,U=1`会reset，无冗余direct-S分支。

`L=L_action+αCE(N,F)+βBrier(C)+γL_value-rank+ηL_delay+ζL_false-reset`。density ratio 用 normalizing-flow/mixture-density 两版并以 held-out NLL 选择，不假定手工高斯。reverse controls：novelty-but-no-reset 三类为照明闪烁、无关区域障碍、目标在动作容差内小抖动；low-visual-novelty-but-reset 三类为遮挡后的抓取滑落（proprio/contact）、抽屉 jam（tracking error）、容器内目标滚动但当前 RGB 遮挡（history residual）。每类都由 paired value oracle 判 `C`，不是人工把名称当标签。

**C-target 信息路径。** 生成器在 snapshot `x_t` 固定语言、历史与 `K=4` 候选 proposer；对 `z_old,z_1…z_K` 各用同一组 `S=8` 外生 seeds，向前执行 `H_Q=16` 控制步，target 端读取未来 reward/success/contact cost 得到 `Q_t(z)` 与 bootstrap CI。导出 student shard 时只保留当前可部署输入和 `C_t/ΔQ` target，删除 snapshot simulator state、未来帧、未来 reward、seed、task/episode ID；target encoder/value head stop-gradient。部署只运行 current proposer 和 student posterior，不运行 oracle rollout。

| 变量 | student/action 训练 | target | 部署 | 审计 |
|---|---:|---:|---:|---|
| `RGB_{≤t},q^{prop}_{≤t},contact_{≤t},l,a^{exec}_{≤t-1}` | 是 | 是 | 是 | 全部部署传感；无 simulator state |
| `t−1` 预测与 t residual/CUSUM | 是 | 是 | 是 | 明确一周期物理检测延迟 |
| 干预时刻、N/F/C、paired intent values | 否 | loss target | 否 | 干预≠intent-change；stop-gradient |
| 未来帧/下一动作真值 | 否 | prediction target | 否 | future-mask；阳性泄漏对照 |
| task/episode ID | 否 | 否 | 否 | 数据导出前移除 |

## 数据与实验

EventAlias-16：RoboTwin 16 tasks，每个初态 paired 四类基础干预并扩成上述 3+3 hard pairs；干预时间均匀，另含无事件长段。每个 event 记录 novelty type、value severity bin（`ΔQ`: 0–δ/δ–2δ/>2δ）、是否 control failure、是否 reset-worthy；30k episode。真机 4 tasks×100 trial，机械滑落/目标移位可重复。MVP 1×A100、2 天；完整 4×A100、6 天。

强基线：IntentVLA、Remember-Smarter-style memory、固定 K reset、learned GRU forget gate、BOCPD、event-triggered replanning、When-to-Trust、CheckVLA、PACE velocity valley、action entropy、REMAC、oracle `C_t`、oracle novelty、never/always/random matched-rate；同 history、action head、控制频率和参数。**最强 deployable comparator 固定为同 proposer 的 CheckVLA/BOCPD/learned-gate 中 validation 较强者**；所有非 oracle gate 共享完全相同的 K=4 proposer、候选 tensor、fallback 与重规划预算。oracle-K coverage 只由 evaluator 报告，不进入部署 gate。

恢复时间操作化如下：事件时刻为 `t_e`；从 `t_e` 起首次回到由 pre-event task progress ±δ_p、预事件 nominal trajectory tube 距离 ±δ_x 定义的集合，并连续 `L=3` 控制步无 collision/failure，记 `T_rec`；到固定 horizon `H_rec=64` 未恢复则右删失。`δ_p,δ_x,H_rec` 只在 validation 冻结。**唯一 primary** 为 event-family（shift/slip/obstruction/false-visual）等权 macro 的 restricted mean recovery time `E[min(T_rec,H_rec)]`；detection latency、precision/recall、false reset、success 与 jerk 为 secondary。event/reset group 为 cluster、task 分层，paired bootstrap 和 censored survival estimator 交叉核验；按30% RMRT 下降、α=.05、power=.8 的 pilot ICC 冻结 events/family。

消融：innovation 模态、CUSUM vs one-step、intent posterior、无 flow factor、阈值、history 长度、视觉闪烁/低速真事件反向干预、event label shuffle、故意看下一帧阳性对照。

### R6 原生/同监督 gate、正交 2×2 与资源合同

| baseline-native | 原生 evidence/target | 用途 |
|---|---|---|
| IntentVLA/BOCPD/CheckVLA/PACE/REMAC | 各自 intent/change/risk/phase target | 外部可用系统表，忠实公式/commit冻结 |

| label-equal adapter | shared target pool | shared deploy system |
|---|---|---|
| pure innovation、pure ΔQ、generic concat、proposed factorized | 相同 K4×S8×H16 rollouts、事件数、reset-worthiness labels/label-seconds | 同 proposer、fallback、reset budget、history、latency envelope |

主 2×2 为 change evidence `{off,on}`×reset-value evidence `{off,on}`：off/off 是 matched-rate gate，on/off 纯 innovation，off/on 纯 ΔQ，on/on 为 proposed；另有同参数 generic concat MLP。visual/proprio 各单模态用 validation 选择 equal-rate threshold，使触发率与双模态格一致。label-equal winner 按 validation RMRT 冻结，native winner另报；所有 threshold 只调一次，test不重选。

每event资源分三段：(a) history-to-event/reachability steps按实际长度记；(b) `z_old+K4=5` candidates×S8×H_Q16=`640` target env steps；(c) 每方法closed-loop recovery最多H_rec64，不能混入target。2×2共享(b) shard不乘4，gate model×3 seeds GPU-hours另加。manifest根键为 `root_snapshot_id`，paired variants含 event_variant/family/severity/time/task/asset，所有variants按root cluster同split；16 tasks冻结train10/calibration3/test3，每family最低cluster与不足时合并规则仅validation预定。50-event/family smoke只估acceptance/censor；另以root-cluster ICC定power。**截至r07 actual=0**。

### R8 主命题、OOD 与安全边界

- **唯一主命题：** seen-family cross-task 中，change+ΔQ 证据降低RMRT；**不声称**发明change-point detector或保证held-out family coverage。compositional unseen event仅stress。
- 真机按root trajectory/event block随机方法，覆盖visual false event与physical slip/shift；GT logger只评测。primary可行条件：collision不高于best+1pp、jerk≤1.05×、false-reset≤5%；所有方法共享force/workspace stop。
- 主表报告reset/fallback率、conditional RMRT和matched-rate safety Pareto。安全失败或fallback解释>50%增益则只保留reset-worthiness detector，降级标题为 **EventAlias Reset-Worthiness Benchmark**。

### R9 论文合同与审稿攻击

- 标题：**Reset-Worthiness from Change and Intervention Value for Long-Horizon VLA**。primary=安全可行RMRT；not-claim=不发明change detection。最危险基线label-equal pure-ΔQ/change/generic winner。
- 攻击：BOCPD旧→贡献是should-reset value；oracle ΔQ→四格同target；tube手调→validation冻结+敏感性+success/jerk。
- ΔQ无增益→删policy留EventAlias；success<3pp→detector；OOD/real失败→seen-family only。降级标题 **EventAlias Reset-Worthiness Benchmark**。

### R10 target-shard 独立性与盲评

导出时断言 student shard 与 target shard 的 `root_snapshot_id`仅通过opaque join key连接，student schema禁止future frame/reward/success/event time/seed/task ID；CI运行future-field rejection与故意泄漏阳性测试。另对visual flicker与low-visual true slip/shift做盲评confusion matrix（V/F/U八格、按root cluster CI）；若ΔQ head能从非因果metadata预测event family>60%，判泄漏并重建shard。

## 判负

primary 相对同 proposer 最强 gate 的 macro restricted mean recovery time 降≥30%且 event-cluster 95% CI 不跨0；四 event-family simultaneous interval 的 empirical FWER coverage 下界≥.93（cluster/binomial CI），否则校准主张失败。若 value/coverage 指标改善但 RMRT 降幅<10%或 success 增益<3pp，降级为 event detector，不声称恢复控制收益。offline candidate coverage<80%只判 proposer stratum，不进入部署。删除 ΔQ head伤害<3pp或 log-prob gate持平则否定机制。

## 风险与里程碑

创新残差会受感知噪声误触发，用假闪烁负控和跨模态一致性；真机 event GT 用外部日志仅评测。两周完成 EventAlias+oracle；两月完成 flow integration/真机。负结果产出 intent persistence 的 stability-reactivity Pareto 与事件诊断基准。

## 证据

[IntentVLA 2605.14712](https://arxiv.org/abs/2605.14712)、[PACE 2606.00537](https://arxiv.org/abs/2606.00537)、[REMAC 2601.20130](https://arxiv.org/abs/2601.20130)、[Remember Smarter 2608.15269](https://arxiv.org/abs/2608.15269)、[Bayesian Online Changepoint Detection 0710.3742](https://arxiv.org/abs/0710.3742)、[Online Replanning in Belief Space 1911.04577](https://arxiv.org/abs/1911.04577)、[Dynamic Planning Horizons 2208.02312](https://arxiv.org/abs/2208.02312)、[When-to-Trust 2604.14480](https://arxiv.org/abs/2604.14480)、[CheckVLA 2607.26789](https://arxiv.org/abs/2607.26789)。
