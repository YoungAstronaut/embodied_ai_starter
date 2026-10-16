# JEP-P3：可控—外生动力学分解的随机 JEPA

- Proposal-ID: JEP-P3
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: learned-q primary/true-e oracle/q-corrupt stress固定同一主表；预注册q ECE/coverage触发conservative fallback，任何true-e进入deploy即fatal。

## 问题与假设

JEPA-WM study 明确指出 deterministic MSE predictor 会学习多模态未来的条件均值；Invariant JEPA-WM 去除 slow/background distractors，VLA-JEPA 抵抗 nuisance motion，CoCo 提升 action controllability。动态 manipulation 中还有一类不同问题：传送带、他人手臂、自由滚动物体是任务相关但不完全可控的外生动态，不能被简单丢弃；若与 robot-caused change 混在一个 latent，action effect 被外生方差淹没，planner 可能把偶然变化归因于动作。

H1：把 future **predictive function** 分解为 action main effect、exogenous main effect、action×exogenous interaction 与 stochastic innovation，并在部署时对部分可观测外生状态的 posterior 混合，可在外生速度/相位 OOD 下改善 action ranking。我们不要求“改 e 时整个 controllable outcome 不变”，也不声称 latent 坐标本身可因果识别；贡献不是通用风险阈值或 conformal safety。

functional ANOVA、controllable/uncontrollable 两 latent、stochastic world model 都是既有工具，不列为贡献。唯一论文级命题是：**balanced factorial manipulation benchmark + interaction-aware predictive objective 是否通过 calibrated exogenous posterior 的 mixture planning 降低 held-out action×e ranking regret**；若普通 stochastic object WM 用同目标持平，JEPA 名称从贡献中删除。

## 最近邻差异

- Invariant JEPA-WM：去 task-irrelevant slow features，当前主要简单导航；本方案保留任务相关外生动态并建模其分布。
- VLA-JEPA：leakage-free latent transition，但未用 same-state action×exogenous factorial interventions 解耦因果来源。
- CoCo：保证 action response并含 action/observation counterfactual consistency；本方案不重复 controllability，核心是 balanced factorial 下显式估计 action×exogenous interaction 及部署 mixture regret。
- CheckVLA/JEPA Safety：校准风险并干预动作；本方案不输出安全概率、不做 suffix rewrite，比较它们只是防止把 planning gain 误写成 risk gain。

| 最近邻 | 分解对象 | 是否显式 action×exo interaction | 实验范围 | 本方案必须超过的边界 |
|---|---|---:|---|---|
| Sawada 2018, 1804.06955 | controllable/uncontrollable latent | 否/强调分离 | toy、独立障碍 | 不能把“两 latent”当新意；须证明 strong interaction 与 calibrated planning 增益 |
| CoCo | action/observation counterfactual consistency | 部分 factorial consistency | 机器人 WAM | 同 4×4 groups 下比较 main/interaction recovery 与 ranking regret |
| JEPA-WM study | deterministic/stochastic predictor/planner | 非主分解 | 多设计系统研究 | 复现其 strongest stochastic/rollout setting，不只打 deterministic 弱基线 |
| causal representation/functional ANOVA | factors/functions | 可建交互 | 通用 | 只声称相对预注册 intervention distribution 的 functional decomposition |
| 本方案 | `f_a+f_e+f_ae+ε` 的 outcome predictor | **是** | conveyor/rolling/dual-arm contact | interaction ablation 必须伤害 mixture ranking；低 probe 不是因果证据 |

| CoCo v1 逐对象比较 | CoCo 2608.04653 | 本方案 | 公平判定 |
|---|---|---|---|
| 干预/公式 | inverse/zero action、镜像动作与空间反事实一致性；same-state multi-action controllability | 同 state 的 `a_i×e_j×ξ_r` factorial cells，显式 `f_ae` 与 posterior mixture | counterfactual/consistency 本身不新 |
| 外生变量 | observation/spatial counterfactual，不以可重复 phase/speed/other-arm policy 建 4×4 e levels | e 为预注册 task-relevant external dynamics | 若 CoCo 官方实现能隐式恢复同 interaction，不保留 objective 新意 |
| 数据单元 | same-state multi-action/counterfactual pair | 每组 4 actions×4 e×K seeds，held-out cells | 在**完全相同的 factorial groups**运行 CoCo loss |
| 指标 | controllability/consistency 与机器人终点 | `f_ae` held-out error、q calibration、mixture ranking regret/OOD success | CoCo 同预算持平即否定新增机制 |

## 方法

exact-reset simulator交叉采样 `a_i,e_j,ξ_r`。ANOVA不再只作用条件均值，而作用于完整预测分布 `P_{a,e}` 的 characteristic-RBF kernel mean embedding `m(P)=E_Y[k(Y,·)]`：`m(P_ae)=μ+f_a+f_e+f_ae`，在RKHS中做center约束；characteristic kernel下embedding相等蕴含分布相等。decoder仍以mixture density NLL/energy score训练，`L_interact=||m_hat(P_ae)-μ-f_a-f_e-f_ae||²_H`，因此mode weight/scale交互也可见。
为在**预注册均匀 4×4 intervention measure** 下识别函数分量，约束 `Σ_i f_a=0, Σ_j f_e=0, Σ_i f_ae(i,j)=0, Σ_j f_ae(i,j)=0`；相同 decoder/空间 object masks 用于所有 cells，且 train/test action/e levels 留出组合。该约束只识别 outcome functions（及其预测），不识别可任意旋转的内部 latent axes。

离散实验的 centering measure 是训练期均匀 `μ_a×μ_e`；连续 speed/phase 时使用预注册训练 intervention density `μ_train(e)`，满足 `∫f_e(e)dμ_train(e)=0`、`∫f_ae(a,e)dμ_train(e)=0` 与 `∫f_ae(a,e)dμ_a(a)=0`，用 quadrature/Monte Carlo penalty 实现。测试 `μ_shift(e)` 只评估，不允许用 test e 重新 centering；结果同时报告相对固定 `μ_train` 的 function error 和 planner regret，避免换 measure 后重定义成功。

conditional predictor `p_θ(Y|a,e)` 与 RKHS ANOVA **只用匹配 true-e 的 factorial cells**；任何q-sampled/corrupt e都不得进入其conditional NLL。q-head用可部署history预测e并由true-e label监督。另在冻结/stop-gradient predictor后，用正确边缘目标 `L_marg=-log∫p_θ(Y|a,e)q_ω(e|h)de` 更新q，或蒸馏oracle-e mixture planner的candidate utility；q temperature/corruption只用于该边缘/planner robustness，不把错误e冒充条件真值。报告oracle-e/oracle-q/learned-q三角，regret gap>10pp即不称部署闭环。

三条梯度路径固定：`true-e,Y→conditional predictor+ANOVA`；`history,true-e→q calibration`；`history,Y→∫stopgrad(p_θ)q_ω de / planner distillation`。无标签真实序列只走第三条，不进入factorial cell估计。

mixed outcome kernel固定为 `k=k_pos·k_rot·k_contact·k_collision`：translation RBF、SO(3) heat kernel、contact-simplex RBF、binary collision delta kernel；各 bandwidth 只用 train median heuristic 后冻结。全量 15k factorial groups 固定 `K=4`；另在预注册 500-group calibration subset 上做 K=4/8/16/32 收敛，MMD 与 interaction norm 相对 K=32 误差>10%则不扩 full experiment，绝不把全量 K32 成本藏入 K4 预算。

局部action measure固定为每state由冻结proposer+固定seed生成4候选后等权 `μ_a=1/4`；train/test都不按成功重权。`μ_e`为预注册intervention density；held-out cell只留组合不改measure，test shift绝不重新center。分量仅在同一state/measure内比较，跨state只比较分布预测与planner regret。

信息路径为：`intervention controller→target-only e label`；`past/current RGB+proprio→student q_ω(e|h)`；训练时 `e label` 监督 q 且条件化 target predictor，target stop-gradient；部署时没有 e label，planner 从 q 抽样/积分，经 `p_θ(Y|h,a,e)` 得每个候选的 mixture utility。对 q 输入 e label 是泄漏阳性对照，任何主结果禁止。

**最小 conveyor 反例。** action `a∈{-1,+1}` 表示从左/右接近，hidden belt phase `e∈{-1,+1}`，接触 outcome `Y=a·e`，目标 `Y=+1`，当前 history 给 `P(e=+1)=0.8`。deterministic MSE 若对未建交互的多模态 future 取均值，会把两个 action 拉向不具物理意义的中间；naive additive `μ+f_a+f_e` 无法表示 XOR 式符号翻转，排序接近 tie；interaction model 得 `P(success|a=+1)=0.8`、`P(success|a=-1)=0.2`。MVP 必须先在此 2×2 数值例和 rendered conveyor 上复现，再扩双臂。

纯方差反例：两action均值都0，但 `Var(Y|a=+,e=+)=0.01, Var(Y|a=+,e=-)=1` 且a=-反转；mean-ANOVA恒零，risk ranking随e改变，distributional RKHS interaction必须恢复。另构造相同mean/variance但mode weights反转的双峰例；分别报告mean error、variance error、mode-weight CE与CVaR ranking。

| 变量 | student/action 训练 | target/teacher | 部署 planner | 审计 |
|---|---:|---:|---:|---|
| 当前/历史 RGB、proprio、语言 | 是 | 是 | 是 | causal |
| candidate action | 是 | 是 | 是 | 部署可采样 |
| exogenous intervention/seed label | student 不输入；posterior只读 history | pair generator/target | 否 | 导出移除、未知时做 mixture |
| future target latent/frame | 否 | 是 | 否 | stop-grad |
| sampled ξ/预测未来 | 是（模型） | — | 是（模型） | 无真实未来 |
| success/collision/conformal score | 否 | 只评测 | 否 | 不复制 CheckVLA |

故意未来帧泄漏、action/exogenous label swap、只换背景、固定 a/改 e 与固定 e/改 a 均为强制攻击。

## 数据、实验与资源

ExoManip-12 full K4=`15k groups×4 actions×4 e×4 seeds=960k` outcomes；固定`H=16`即15.36M env steps。500-group train/calibration subset复用full K4作为K32 nested prefix，再额外K8/16/32的56 seeds=`500×16×56=448k` outcomes；unique total=1.408M outcomes/22.528M env steps。q history固定8 frames，其history-to-state生成steps单列，不藏入outcome账。K subset不取test shift。

强基线：JEPA-WM/VLA-JEPA/Invariant JEPA、CoCo、Sawada、single stochastic latent、ensemble、RSSM、non-JEPA+same objective与oracle e；同 data/samples/planner/fallback。最强 deployable comparator 按下述扩展 validation winner 冻结。**唯一 primary** 是 learned-q、held-out action×e cells 的 task-normalized ranking regret；factorial group cluster、task分层，按20%下降冻结power。ANOVA error、q calibration、future NLL与success均secondary。

原先把 oracle-e/true-q 混入 deploy 2×2 的种子已放弃；R6 改为下述四格均可部署的 outcome×posterior 设计，oracle 只作独立三角上界。

### R6 deploy 2×2、数据×目标 2×2 与复现合同

| baseline-native | native objective/input | same-data adapter |
|---|---|---|
| CoCo/Sawada/JEPA-WM/RSSM/MDN | 各原生 counterfactual/two-latent/stochastic target | 同 balanced 4×4×K、同 calibrated q、planner/fallback |
| non-JEPA object WM | generic stochastic native | 同 RKHS-ANOVA/q/mixture objective，参数匹配 |

最强 deployable winner 必须在 validation 从 `max{CoCo,Sawada,JEPA-WM stochastic,non-JEPA+same objective,conditional MDN/RSSM}` 按 learned-q primary regret冻结。deploy 主 2×2 改为 outcome `{additive,interaction}`×posterior `{learned q,calibrated generic q}`；四格都可部署。`oracle-e / oracle-q / learned-q` 作为独立三角上界，绝不塞进2×2或winner。

MVP data×objective 2×2跑4 models×3 seeds；deploy outcome×posterior再4格×3 seeds，重复架构/目标相同者复用checkpoint并在ledger标注，full winner baselines各3 seeds。逐格列forward calls/GPU-hours/VRAM/storage/latency。cell manifest为 task×scenario×action-level×e-level×group，按task/scenario group split train/calibration/test；K subset只来自train/calibration。进入full前同时过K误差<10%、throughput cap与cluster power。**截至r07 actual K-pilot=0**。

消融：只 main effects/加入 interaction、无 stochastic、single latent、factor capacity、ξ samples、centering/region masks、action/exo swap、mean vs mixture/CVaR planning、posterior q vs oracle e。反向干预固定 e 改 a、固定 a 改 e、同时改 a/e，逐格检查预测差分；probe 不用作因果证明。

### R8 三层 OOD、q fallback 与 claim hierarchy

- **唯一主命题：** balanced factorial benchmark 上 distributional action×exogenous objective降低learned-q regret；JEPA可删除。**不声称**ANOVA新理论或held-out cell等于外推。
- 分ID、combinatorial held-out cells、超`μ_train(e)` speed/phase extrapolation三层。shift上ECE>0.10或80% coverage不在[.75,.85]即切validation-frozen conservative baseline；oracle-q仅上界。
- 真机≥3 tasks root blocks，e独立logger；共享speed/workspace/collision/emergency guard，报fallback/conditional success。层级balanced data→interaction→JEPA；non-JEPA持平删JEPA，generic持平降级 **ExoManip Factorial Benchmark**。

### R9 论文合同与审稿攻击

- 标题：**ExoManip: Balanced Action–Exogenous Interventions for Interaction-Aware World Models**。primary=learned-q regret；not-claim=ANOVA/JEPA理论新。最危险基线non-JEPA same-objective/CoCo winner首行。
- 攻击：ANOVA旧→贡献是balanced robot benchmark+deploy q；CoCo覆盖→同4×4主表；JEPA branding→可删且不进标题。
- non-JEPA持平→删JEPA；generic objective持平→纯factorial benchmark；control<3pp或real失败→删planning/transfer。降级标题 **ExoManip Factorial Benchmark**。

### R10 learned-q/true-e/q-corrupt 同表与fatal guard

主表固定三列：learned-q deployment primary、true-e oracle upper bound、q-corrupt stress（temperature/label permutation）；三列共享candidates/samples/planner。部署schema断言拒绝`true_e/e_label/intervention_seed`；任一进入student/planner为fatal。若learned-q ECE>0.10或80% coverage不在[.75,.85]，自动切validation-frozen conservative stochastic baseline并删除mixture-planning claim。

## 判负

primary 相对最强 deployable comparator 降≥20%且 factorial-group cluster 95% CI 不跨0；外生 OOD success 提升≥6pp、interaction NLL降≥10%、rendered conveyor ranking提升≥10pp、q 的80% interval coverage 75–85%为 secondary。若 interaction/NLL 指标达标但 OOD success<3pp，降级为 distributional decomposition，不声称控制收益。若 single stochastic latent、Sawada 或 CoCo 同数据差≤2%，否定 interaction objective；non-JEPA 同目标与 JEPA差≤2%则删除 JEPA contribution；q calibration失效或 oracle-q/learned-q regret gap>10pp则不能声称部署 mixture planning。deterministic mean 在最小例不失效则放弃主张。

## 风险与里程碑

functional components 只相对均匀 intervention measure 定义，换 measure 会变；因此不解释 latent 语义。两周完成 2×2 XOR/conveyor、4×4 generator、centering/held-out-cell 单测；两月完成 strongest stochastic baselines、mixture planner/真机。负结果产出 JEPA 在强 action×external interaction 上的 deterministic/additive 失效边界。

## 证据

[JEPA-WM study 2512.24497](https://arxiv.org/abs/2512.24497)、[Invariant JEPA-WM 2602.18639](https://arxiv.org/abs/2602.18639)、[VLA-JEPA 2602.10098](https://arxiv.org/abs/2602.10098)、[CoCo 2608.04653](https://arxiv.org/abs/2608.04653)、[Sawada et al. 1804.06955](https://arxiv.org/abs/1804.06955)、[Causal Representation Learning survey 2102.11107](https://arxiv.org/abs/2102.11107)、[CheckVLA 2607.26789](https://arxiv.org/abs/2607.26789)。
