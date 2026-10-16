# JEP-P1：局部动作—后果伪度量 JEPA

- Proposal-ID: JEP-P1
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: duplicate/missing/corrupted detector的abstention、assignment coverage与regret联表；GT UUID严格只出oracle列，攻击stable-order shortcut。

## 问题与操作定义

V-JEPA 2-AC、VLA-JEPA 与 JEPA-WM 已能做 action-conditioned latent prediction；What Matters for Latent Actions 又警告 proxy 与控制不一致。r00 用距离阈值定义 `a~a'`，但它不传递，不能形成 equivalence class；该种子被废弃。

新对象是局部 action-effect pseudometric。对同状态 s，令 `Y=(canonical object SE(3),contact graph,collision)`，先定义有单位归一的 ground cost：
每任务预注册最大 `role-instance` slots：language referent优先为target#1，其余由部署detector category后按初始GFM 3D `(x,y,z)`量化字典序编号并由tracker保持；无检测为null。几何完全相同且排序差低于ε的同类实例形成可交换orbit，主预测对orbit边缘化而非借GT拆分。GT UUID只oracle/evaluator，主metric包含deploy assignment error/coverage。

对固定node slots定义 `c_node=Σ_s min(||Δp_s-Δp'_s||/.1m+d_SO3/π,2C)`含null extension；全局edge/contact adjacency distribution只计算一次 `c_edge=λ_g TV(G,G')`，全局collision一次`c_col=λ_c|b-b'|`，总 `c=c_node+c_edge+c_col` 为product metric，避免每node重复contact edge。
`d_s^phys(a,a')=W_1^c(P(Y|s,a),P(Y|s,a'))`。
它对 action 可为 pseudometric：两个不同命令只要诱导相同物理 outcome distribution 就距离0；由 Wasserstein/TV 的性质满足非负、对称和三角不等式，不需要阈值关系传递。任务/语言价值另定义 `d_{s,l}^val(a,a')=|E[U_l(Y_a)]-E[U_l(Y_{a'})]|`，不写入物理距离；同物理效果在任务阶段变化时 physical metric 应稳定、value compatibility 可变化。

H1：用 triplet/ranking 把 JEPA prediction distance 对齐 `d^phys`，并让 planner 单独读取 task value，可减少对无效动作微差的过敏，同时保持真正改变物理后果的梯度；终点是 metric distortion 和 action ranking regret，不是“类内 retrieval”。

## 最近邻差异

- VLA-JEPA：leakage-free future latent target，但不以同状态 alternative-action outcome pseudometric 为监督/评价。
- V-JEPA 2-AC/JEPA-WM study：比较 predictor/planner 设计；本方案改变 latent 的局部动作拓扑。
- CoCo：约束 action controllability，强调不同动作产生不同未来；本方案允许不同命令具有零/小物理效果距离，并保持连续 graded geometry。
- Action-Bisimulation：已提出多步 controllability pseudometric，是直接理论基线；本方案不能把 pseudometric 本身当新意，差异必须落在视觉 JEPA 的 same-state matched-seed contact-rich监督、physical/value 分离和跨 embodiment canonical outcome。
- Invariant JEPA-WM：bisimulation 去 slow features；本方案度量 action-induced outcome distribution，而非 state slow-feature invariance。

| 最近邻 | 对齐对象 | 多步/随机 outcome | task value 是否混入 | 本方案的可核验增量 |
|---|---|---|---|---|
| VLA-JEPA / V-JEPA2-AC | future latent prediction | action-conditioned future | 可由 planner 使用 | 加同状态多动作的 distribution metric supervision |
| CoCo | counterfactual controllability/consistency | same-state multi-action | 非 pseudometric 主对象 | 对小/零物理效果动作不过度分开；比较 graded distortion |
| Action-Bisimulation 2403.16369 | 多步 controllability pseudometric | 是 | 按其定义 | 移植不是贡献；必须在视觉接触操作、matched stochastic seeds 和跨 embodiment 显著胜过其直接实现 |
| 本方案 | canonical object/contact outcome distribution | S matched seeds + uncertain abstain | **分开报告** | JEPA latent metric→candidate ranking 的机制干预 |

| 公式字段 | Action-Bisimulation 2403.16369 direct | 本方案 | 新意边界 |
|---|---|---|---|
| domain | state/action controllability representation | 固定视觉历史/状态下的 candidate-action pairs | action metric 域本身不新 |
| recursion/horizon | reward-free multi-step recursive controllability pseudometric/fixed point | 预注册有限 `H=8/16` 的 contact-rich outcome distribution | 不声称 fixed-point 理论；只检验有限时域机器人终点 |
| transition distribution | 环境 transition/controllability distribution | matched-seed empirical canonical SE(3)+contact distribution | 增量候选是接触 schema 与 matched stochastic estimator |
| reward/value | reward-free；按原文 planner/representation 终点 | `d_phys` 明确不含 language utility；`d_val` 单独用于 ranking | physical/value cross-task separation 是实证命题 |
| fixed point | 有递归 operator | 无；state-local empirical W1 | 不是更一般理论，只是更可审计的局部 target |
| visual input | 按 direct 实现的 state observation | RGB/history encoder + canonical outcome target | 必须同视觉输入公平复现 |
| planner | 按原文 controllability/planning protocol | fixed candidate MPC 的 regret/success | 只有 planner regret 改善才保留贡献 |

Deep Bisimulation/goal-conditioned abstraction 把 reward/goal 与 transition similarity共同用于 state representation；本方案刻意将 physical effect metric 与 `U_l` 分开，因而只是一个需要实验支持的 factorization，而不是宣称更正确的 bisimulation 定义。

## 方法

exact-reset simulator 对每 `(s,a)` 生成经验分布；W1是两个经验measure的最优运输，**不把seed pairing当运输对应**。shared seeds仅是common-random-number方差降低：主estimand同时用paired采样与独立采样估计，要求均值差<0.03而paired bootstrap方差降低≥20%，否则不用CRN效率声明。

经验 `W_1^c` 用相同 S 个 outcome 的最优运输估计；按 reset group 做 1,000 次 cluster bootstrap，报告 bias-corrected 95% CI、S=4/8/16 收敛曲线以及相对 S=32 参考的 normalized absolute error。若 S=8 的中位误差>0.10 或 90% CI 宽度>0.15，MVP 不扩展。

encoder `E(o)` 与 predictor `P(E(o_t),a)` 输出 future latent，令 `\hat d_z=||P(E(o),a)-P(E(o),a')||`。损失 `L=L_pred+αL_metric+βL_triplet+γL_rank+ηL_canonical`，其中 `L_metric=|\hat d_z-stopgrad(d^phys)|`，triplet 只要求当 `d^phys(a,b)+m<d^phys(a,c)` 时 latent 同序；`L_rank` 用 `U_l` 单独排序；canonical loss 约束跨 embodiment 的 EE/contact outcome，不强行相同关节命令。target encoder 可看未来但只提供 stop-grad target；student/action query 只看≤t。

完整 2×2 为 metric supervision `{off,on}`× backbone `{non-JEPA action-conditioned encoder,JEPA predictor}`。四格共享 deploy canonicalizer、current/history inputs、candidate set、future target数据、参数±5%、planner与 NFE；`off` 格仅移除 `d_phys/triplet`，保留 action/value rank 监督。由 metric 主效应、JEPA 主效应与交互分解结果；只有 JEPA 主效应/交互独立改善 primary 才称 JEPA contribution。

action-code shortcut 最小例固定同一action code在两个视觉状态产生相反接触后果；若lookup只读action，至少一状态metric误差≥margin。实验交叉为 same-action/different-state、same-state/action permutation、state-conditioned target shuffle：遮掉RGB后action-only probe的triplet accuracy必须≤55%，正确RGB恢复≥15pp；shuffle state targets须使regret恶化≥10pp，否则说明未读视觉。

最小三动作反例：一维末端后果均值分别为 `Y_a=0,Y_b=0.6,Y_c=1.2`，ε=0.7 时 r00 得 `a~b,b~c,a!~c`；connected-components 会把 a/c 错合并，CoCo 式“所有动作不同”又会忽略 a/b 的小差异。pseudometric 直接保留 0.6/0.6/1.2，triplet 只约束有置信 margin 的相对距离。

| 变量 | student/action 训练 | target/teacher | 部署 planner | 防泄漏 |
|---|---:|---:|---:|---|
| 当前/历史 RGB、proprio、语言 | 是 | 是 | 是 | causal mask |
| candidate action/canonical action | 是 | 是 | 是 | 部署可采样 |
| 同状态 matched-seed outcome/contact | 否 | `d^phys`/confidence target | 否 | S seeds、stop-grad |
| future target latent | 否 | 是 | 否 | 独立 target encoder/cache |
| simulator state/embodiment ID | 不输入（仅 canonical adapter 可见 robot spec） | pair generator | adapter 可见 robot spec | 字段审计 |

canonical adapter部署只读robot spec+language+detector/GFM/tracker；target adapter的sim UUID只产oracle assignment。对抗单测：两个同类obstacles A/B、一个missing null、三outcomes X/Y/Z，固定slot/orbit下验证identity或对称边缘化且triangle成立；错误deploy assignment计入noise，不用UUID修正。

信息流固定为：`future outcome/contact + matched seeds → target-only d_phys/CI`；`future frame → stop-grad target encoder`；`current/history RGB + candidate a → student predictor → latent distance/value head`；部署 planner 只读 candidate latent/value，绝不读取 target encoder cache、outcome/contact GT、future frame 或 seed。physical metric target 与 language utility target 分成两个 shard/head，互换/删除作反向干预。

强制攻击：action label shuffle、future target 送入 student 的阳性泄漏、等价/非等价标签反转、action-preserving 与 action-changing latent intervention。

## 数据、实验与资源

ActMetric-3D：ManiSkill/RoboTwin 10 tasks，先做 2k states×16 actions×8 seeds 的 variance MVP，完整上限 20k states×32 actions；按 CI/算力 go-no-go 扩展。train/test 物体/相机/embodiment 拆分。MVP 冻结 V-JEPA2 encoder、2×A100、3 天；完整 8×A100、8 天。真机只做 3 tasks×6 安全微扰×80 reset groups，使用重复 reset 估 outcome variance，不声称覆盖全 metric。

强基线：V-JEPA2-AC、VLA-JEPA、JEPA-WM、CoCo、Action-Bisimulation native/adapter、bisimulation-style encoder、non-JEPA+same metric、plain contrastive与oracle outcome；同 candidates/planner/NFE。最强 comparator 按下述 validation winner 冻结。**唯一 primary** 是 deploy canonicalizer 下单平台 held-out action ranking regret；GT UUID 只给 assignment-noise oracle。state/reset group cluster、task分层，按20%下降冻结power；跨 embodiment、distortion/triplet/MPC success均secondary。

消融：S/CI abstention、horizon、outcome 字段、contact mode、canonical adapter、metric/triplet/rank、predictor MSE、跨 embodiment、标签噪声、task/phase swap、反向 intervention。

### R6 Action-Bisim 复现、公平 target 与资源合同

| baseline-native | objective/input | same-data adapter |
|---|---|---|
| Action-Bisim-native | paper-faithful recursive objective与原输入 | 同 RGB/history/candidates/deploy canonicalizer、local ground outcome |
| non-JEPA/JEPA baselines | 原生 predictive/contrastive objective | 同 metric/local target、future data与planner |

validation winner 在 `max{Action-Bisim-native,Action-Bisim-adapter,non-JEPA+same metric,JEPA without metric}` 中按单平台 primary regret 且 assignment coverage 可行冻结；test 不重选。已有 backbone×metric 2×2 外，在同一 non-JEPA backbone 增 target `{Action-Bisim recursive,local matched-outcome}` 对照，确认增益不只是 target 替换。所有格共享 deploy canonicalizer，并按 assignment `{correct,error,abstain}` 分层；UUID oracle只量上界。

冻结`H=16`；S32 outcome bank为 `2k×16×32×16=16.384M` env steps，S8是每state/action的前8个nested seeds，不另生成。pairwise target records=`2k×C(16,2)=240k`（不是outcome数）；若每record存2 action hashes(32B)+distance/CI(12B)+state id(8B)+flags(4B)≈56B，则约13.44MB，另计outcome cache。OT用exact network-simplex/CPU于S≤32，记录O(S^3) wall-time；必要时Sinkhorn仅诊断。2k MVP只决定S/CI/assignment；20k由state-cluster power与8-day cap共同决定。manifest增state-family/task-template/asset/role-instance hash并family group split。**截至r07 actual=0**。

### R8 adapter/OOD 与主张边界

- **唯一主命题：** pseudometric本身不新；只检验视觉JEPA matched-outcome supervision与deploy canonicalization是否降单平台regret。**不声称**全局equivalence或target-trained adapter的zero-shot。
- target-free/train-only morphology/few-shot adapter分表；asset/camera/morphology OOD分轴，coverage<90%严格判负，报assignment/fallback-only/conditional regret。
- 真机root state内随机方法/扰动；GT只logger，共享force/workspace stop。JEPA持平删JEPA，local target与Action-Bisim持平删metric增量；降级标题 **ActMetric-3D Benchmark**。

### R9 论文合同与审稿攻击

- 标题：**ActMetric-3D: Matched-Outcome Action Pseudometrics for Visual Planning**。primary=single-platform regret；not-claim=pseudometric理论/等价类不新。最危险基线Action-Bisim native+same-data adapter首组。
- 不可删除对象是local contact-rich matched physical outcome schema、canonical role/noise strata与same-backbone recursive-vs-local target protocol；Action-Bisim不提供此3D contact outcome benchmark。
- 攻击：Action-Bisim已做→target对照；abandoned equivalence→只pseudometric；canonicalizer做功→全基线共享/strata。持平→删JEPA/method留ActMetric；control<3pp→representation benchmark；cross-embodiment失败→删secondary。降级标题 **ActMetric-3D Benchmark**。

### R10 detector-order shortcut 主表

主表按 detector condition `{clean,duplicate,missing,corrupted-order}` 联合报告 abstention、assignment coverage/error 与 action regret；所有非oracle列只用deploy detector/canonicalizer，**GT UUID仅出现在明确标注的oracle列**。若corrupted-order使coverage不降但assignment/regret恶化>10pp，说明stable ordering shortcut，主claim判负。

## 判负

primary 相对 Action-Bisim direct 的 held-out action ranking regret 降≥20%且 state-cluster 95% CI 不跨0；deploy role assignment coverage≥90%、error≤10%。若 distortion/triplet 改善但 MPC success 增益<3pp，降级为 action metric representation，不声称控制收益。重复 role/missing adversarial 单测必须0 triangle violations；Action-Bisim 持平否定 metric 增量。cross-embodiment 只作 secondary，不能替代单平台 primary。

## 风险与里程碑

pseudometric 随 state/horizon/outcome schema 变化，明确报告 `(s,H,Y)`，不声称全局同余；真机微扰受安全约束。两周完成三动作反例、matched-seed generator 和 variance audit；两月完成 planner、Action-Bisimulation direct baseline、跨 embodiment 与真机。负结果产出 latent proxy 与 action ranking 脱钩的诊断数据。

## 证据

[VLA-JEPA 2602.10098](https://arxiv.org/abs/2602.10098)、[V-JEPA 2 2506.09985](https://arxiv.org/abs/2506.09985)、[JEPA-WM study 2512.24497](https://arxiv.org/abs/2512.24497)、[CoCo 2608.04653](https://arxiv.org/abs/2608.04653)、[Action-Bisimulation 2403.16369](https://arxiv.org/abs/2403.16369)、[Deep Bisimulation for Control 2006.10742](https://arxiv.org/abs/2006.10742)、[Invariant JEPA-WM 2602.18639](https://arxiv.org/abs/2602.18639)、[What Matters for Latent Actions 2608.19613](https://arxiv.org/abs/2608.19613)。
