# GEO-P2：接触转移场驱动的几何策略

- Proposal-ID: GEO-P2
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: 主验收表固定双标κ、event support/censor率与0/±1/±2 timestamp tolerance敏感性，防ontology annotation选择决定结论。

## 问题与假设

深度、点图和轨迹可以很准，但在插入、刮取、推拉中仍会因接触时刻、法向和支撑关系错误而失败。失败可观察为：几何重建误差相近的两条候选轨迹，一条在接触前后出现穿透/滑脱/错误支撑，动作 success 分叉。H1：**给定候选动作**预测局部“接触转移”（何处、何时、何种接触状态建立/切换/解除），能比同预算 dense geometry 更好地区分候选动作。本文只主张定向 contact-field 干预会按预测方向改变选择与成功率，不把它直接称为已识别中介。

## 路线与最近邻差异

- GeoPredict 预测未来机械臂关键点与 3D Gaussian；MECo-WAM 预测 action-aware 时序几何关系；VGA 使用原生 3D backbone。这些工作没有把接触建立/解除的离散拓扑变化作为主要目标。
- VT-WM/ViTacWorld 用触觉改善 world rollout；本方案部署不要求触觉，训练时仿真接触/可选真机触觉只做标签与 oracle。
- “Where to Touch”层级 RL-MPC 明确 contact intention，但依赖结构化 MPC；本方案检验视觉策略 latent 是否需要 contact-transition supervision。

若 MECo-WAM 的关系目标已经在相同数据上等价编码 contact mode，且显式 contact target 无独立增益，则主张失效。

| 工作 | 输入传感器 | 预测对象/字段 | 动作条件 | policy 使用 | 与本方案的边界 |
|---|---|---|---|---|---|
| ContactGuard v1 | 3-view RGB(+proprio variant)+planned single chunk | action-conditioned autoregressive post-contact latent+binary failure probe | planned chunk显式输入 | gripper-close前0.5s anchor、30步rollout、单chunk abort；不搜索候选 | 本方案不能再以pre-contact/action-conditioned预测为新；须证明显式field对多候选方向诊断增益 |
| ContactWorld v1 | wrist/front RGB或point cloud+state，可选TacRGB/TacDepth/TacFF | action-conditioned autoregressive fused latent | CEM candidate sequences显式输入 | latent goal-distance CEM-MPC、执行首动作 | 已覆盖接触任务多模态latent planning；未监督event time/mode/normal topology field |
| TouchWorld v2 | multi-view RGB+语言+proprio+部署触觉 | high-level future visual-tactile subgoal；nominal flow chunk；tactile residual | world subgoal由current obs/subtask生成，不读candidate chunk；residual读nominal lookahead | goal-conditioned chunk+高频触觉纠偏 | 触觉预测/反应强基线；无触觉显式candidate event field不同 |
| ViTacWorld v1 | visual+tactile+action chunks | temporally aligned future visual/tactile rollout | action chunk显式输入 | rollout生成/策略评估，不是在线field scorer | 检验显式event ontology是否超过完整多模态rollout |
| Where to Touch v1 | object surface keypoints/goal flow/clearance | contact location+post-contact object subgoal；低层ComFree-MPC建模mode | high-level选intention，低层MPC优化action | 层级RL-MPC、单contact n=1实验 | 已覆盖where/how contact；本方案只保留learned multi-event field的候选ranking诊断 |
| GeoPredict | RGB/状态 | 未来关键点/3D Gaussian | action-related rollout | 表征注入策略 | 在相同 candidate set 下用 contact transition 对照未来几何 |
| 本方案 | 当前 2–4 帧/语言/本体+候选 action chunk | event time、pair、mode、normal/impulse sign | **是** | 逐候选预测→风险/任务 scorer→选一个执行 | 无动作—field 循环；只比较同候选/同算力的 contact 信息增益 |

版本/代码状态截至 2026-08-30：ContactGuard=2608.13438v1（arXiv正文可核；论文未以代码可用作为复现前提）；ContactWorld=2606.13877v1（正文称将公开 benchmark/data/model/code，当前按“承诺、未本地验证”）；TouchWorld=2607.07287v2（项目页存在，代码/权重未本地验证）；ViTacWorld=2607.22530v1（项目页存在，代码/权重未本地验证）；Where-to-Touch=2601.10930v1（项目页存在）。不可获得实现时按正文重实现，并把复现差距单列，不能把失败当本方案胜利。

## 方法

**无循环数据流。** 基础 action proposer `q_φ(a^{1:N}|o_{≤t},l,s_{≤t})` 先产生固定 N 个候选 action chunks。对每个候选，contact predictor `p_θ(E^{(i)}|o_{t-3:t},s_t,a^{(i)})` 单独输出事件分布；scorer `u_ψ(a^{(i)},E^{(i)},z_t)` 只在之后排序，选一条执行。训练时用日志动作加局部扰动构造候选，所有方法共享候选集合；部署时不存在“field 生成 action、action 又生成 field”的循环。

**Event ontology。** `H=16` control steps、`Δt=50 ms`；空间域是 detector 得到的目标实例/末端网格上的有向 body pair `(b_i,b_j,p_i,p_j)`，坐标与法向均在**估计**目标 frame，长度单位 m、时间单位 step。每对实体每步状态 `m_h∈{separate,touching-stick,touching-slide}`，事件 `e_h∈{onset,stick→slide,slide→stick,release,none}`；`approach` 被移除，因为它不是接触拓扑。允许同一步多个 body pair 事件；若 H 内无 onset/release，时间是 right-censored，不回归虚假 `τ`。输出为事件 hazard、conditional time、法向、法向冲量符号及最多 Q=8 个 pair，不把互斥 softmax 错用于多接触。

**标签提取伪代码。** `(1)` 对每个 h 从 simulator contact manifold 读取 body pair、contact point、normal、normal/tangential relative velocity；`(2)` 若 normal force>F_min 连续≥2 帧，则 state=touching；`|v_tan|<v_min` 为 stick，否则 slide；`(3)` 与 h−1 比较发出 onset/switch/release，多 pair 独立；`(4)` 以 first event 定 `τ`，无事件打 censor mask；`(5)` 用前后 2 帧 majority 去弹跳并保存 engine/version/unit。跨引擎分别校准 `F_min,v_min`，不共享隐藏默认值。

对每event slot和仍at-risk pair定义cause-specific discrete hazard `h_{t,c}`, `S_t=1-Σ_c h_{t,c}`。event `(τ,c)` NLL=`-Σ_{t<τ}logS_t-log h_{τ,c}`；no-event through H为`-Σ_{t≤H}logS_t`；truncated@5同样只积到5，不回归虚假τ。多事件发生后更新graph/risk set，再对下一slot重复。若S=.9且h3,c=.1，则event@3 loss=`-2log.9-log.1`；no-event H=3=`-3log.9`；truncated@5=`-5log.9`。

总损失 `L=L_act+αL_survival+λmL_mode+λnL_normal+λeqL_SE3+βL_rank`；删除未定义且可能重复的`L_cons`。typed tensor stop-gradient送scorer。action-ID probe比较同容量/同split下predicted-field probe与**GT-field probe经验accuracy**，前者高出>10pp判shortcut。

训练单元为 `snapshot × N=8 candidates × S=4 exact-reset seeds × H=16`；每个候选都真实执行到 contact/no-contact/horizon censor，负 contact 保存 right-censored survival label，truncated episode 保存 censor time。MVP 2k snapshots=1.024M env steps；manifest 保存 proposer version、candidate hash、support density 与 censor reason。test 候选相对 train codebook 的 nearest distance/coverage 单报，support overlap<90%不做主结论。

| 信息 | 训练 | 推理 | 审计 |
|---|---|---|---|
| 当前/历史 RGB、语言、proprio、过去动作 | 是 | 是 | 全部时间≤t；图像为 t−3:t |
| 候选 action chunks `a^{1:N}` | 是 | 是 | proposer 先生成，逐候选 predictor 后评分 |
| 仿真 contact/法向/模式、未来相对位姿 | 仅 target | 否 | target branch stop-gradient |
| 真机触觉 | 可选标签/oracle | 默认否 | 无触觉主结果单列 |
| 未来 RGB/动作 | loss target | 否 | future-mask 与 action-shuffle 负控 |
| GT object pose/instance mask | 仅标签对齐/oracle | **否** | 部署用 detector+GFM；字段白名单拒绝 GT |

部署 token/时延图：共享 image/GFM encoder 只算一次并缓存 `z_t`；N=8 action chunks 并行 action-embed；batched predictor 输出 `8×H×Q` event logits；scorer batched 输出8分；argmax后只执行1条。profile 覆盖 proposer、encoder、detector/GFM、N-way predictor、scorer、copy 与 safety check，报告 mean/p95/p99/显存；主门槛为**全链路**p95≤100ms、p99≤130ms且相比 ContactGuard latent batch≤1.25×。

干预拆两层：(1) fixed candidate/action，只换right vs matched-wrong field，验candidate score变化≥10pp，不谈物理success；(2) 固定candidate set后给各候选换field，经argmax改变最终selection，再评closed-loop success降≥5pp。只有第二层动作随selection变化，语义不再写“fixed action success”。

部署 frame 由当前图像的 open-vocabulary detector/segmentation+GFM pose head 估计，时间戳为 t；若实例置信<0.4 或 pose covariance 超阈值，则退回 camera-frame dense baseline，不生成伪精确 canonical field。四档必须分开：GT-pose oracle、部署 detector/GFM、注入 pose noise、detector failure fallback；主结果只用后两者。

## 数据与实验

标签漏斗分开记账：MVP 为 2k snapshots×8 candidates×4 matched seeds×16 steps=1.024M attempted env steps，经 legality/reset/checker 后逐项报告 accepted、censored、rejected；只有 support≥90% 才扩到 6 类任务各 5k episodes 的 full stage。训练/验证/测试按 object/task 隔离。完整再加 RoboCasa/LIBERO contact proxy；3 个 Franka 任务（peg insertion、drawer、spatula）各 100 paired-reset trials 只作外部效度。真机标签用力矩阈值+视觉接触，抽样 500 帧人工审计误差。MVP 2×A100、3 天，完整 8×A100、7 天；材质/摩擦 OOD 单独分轴。

强基线：RGB-only、dense depth、future keypoint/GeoPredict、MECo-style relation、ContactWorld、Where-to-Touch compatible scorer、ContactGuard action-conditioned latent+failure probe、ViTacWorld latent rollout、VT-WM/TouchWorld（有触觉 oracle）、contact binary-only、同参数 random auxiliary。最强 deployable comparator 按下述 R6 native/label-equal validation-winner 合同冻结；各法使用同 N=8 candidates、accepted labels、scorer/planner/fallback 与 runtime envelope。candidate proposer/checkpoint/N/执行 horizon 只在 validation 冻结。

主分解为 latent-only、field-only、latent+field、oracle-field（共享 proposer/candidate/scorer、相同 label budget）。**唯一 primary** 为固定候选集的 selection regret `max_a \bar Y(a)-\bar Y(\hat a)`；time/mode/normal MAE/F1 是机制指标，closed-loop success 为 key secondary。每个 snapshot 的 candidates 与 matched seeds 构成一个 cluster，task 为分层；两级 bootstrap 95% CI，按相对 ContactGuard 20% regret 下降、α=.05、power=.8 用 pilot ICC 冻结 snapshots/task。定向干预保持 RGB/action 不变，仅把 onset±2 steps、normal 旋转30°、stick↔slide，检测 score/selection 是否按 checker 方向变化。

### R6 监督公平、正交 2×2 与资源合同

| baseline-native | target | deploy interface |
|---|---|---|
| ContactGuard-native | 原论文 latent/binary failure probe | current RGB+candidate chunk→latent risk |
| ContactWorld/ViTacWorld-native | 原生 future latent/触觉目标 | 按正文忠实重实现并冻结版本/公式 |

| label-equal adapter | target | shared interface |
|---|---|---|
| ContactGuard-label-equal / generic-hazard | 同 rollout 的 time/mode/normal labels，编码为等长 generic tensor；label-seconds相同 | 同 detector/frame/N8/scorer/planner/fallback/CAS/p95 |
| typed-transition proposed | 同一 labels，仅 typed slots/algebra 不同 | 同上，oracle field 仅上界 |

训练主 2×2 为 target `{generic/binary tensor,typed transition}`× execution `{flat MLP scorer,typed executor}`，四格参数±5%、相同 accepted target shard、optimizer steps、candidate calls 与 runtime envelope。删除 mode/time/normal 时以 null channel 或 train-shuffled label 保持维数。label-equal winner 在 validation 以 selection regret 最低且 p95/p99 合同可行，从 `max{ContactGuard-label-equal,generic-hazard,typed+flat}` 冻结；native winner另报，test不重选。

full 资源公式冻结为 `N_task×N_snapshot/task×N8×S4×H16` env steps；target bytes=`N_snapshot×8×4×(bytes_event+bytes_censor+bytes_hash)`，以实测schema序列化大小替代猜测。2×2四格共享同一target shard，训练成本为4×seeds×GPU-hours另计。漏斗code互斥为 `accepted_event / accepted_no_event / valid_censored / rejected_reset / rejected_legality / rejected_association / unsupported`；按event type/body-pair/mode报cluster与imbalance。发布 `contact_transition_v1.yaml`（m、step、normal-bin、Q=8、legality/censor）、extractor commit/hash与单测。200-snapshot smoke只估support/steps/s；随后以≥6 tasks的task/snapshot ICC定power，full受100M env-step hard cap约束。**截至r07 actual=0**。

### R8 语义迁移、真机与安全合同

- **唯一主命题：** 在无触觉部署输入下，candidate-conditioned typed contact transition 相对 label-equal latent monitor 改善 sim contact-rich ranking；**不声称**跨引擎/真机 event GT 同构或触觉不需要。
- sim1/sim2/real均映射到`contact_transition_v1`：time统一50ms bins、normal单位向量、force/impulse统一N/N·s；各域阈值只由该域train/cal标签拟合，test不回调。摩擦μ train `[.2,.5]`、cal`(.5,.7]`、test`(.7,1.0]`；材质family按asset group隔离，跨引擎与detector-failure分别报。
- 真机按task×root template配对随机方法顺序；500 audit frames按event type分层双标，报Cohen κ、time MAE/CI、force-video同步误差。marker与force只进logger/target，model默认RGB+proprio。
- 所有方法共享force/torque/velocity/workspace abort；route/fallback率、fallback-only与conditional success主表报告。fallback>30%或安全层贡献>总success增益一半时，自动删“field planning”主张，只保留 ontology/safety-router；降级标题 **Contact Transition Diagnostic Benchmark**。

### R9 论文合同与审稿攻击

- 标题：**Action-Conditioned Contact Transition Fields for Candidate Ranking**。唯一primary是sim selection regret；not-claim为不把跨引擎/真机当同标签复现。最危险基线：ContactGuard-label-equal，主表第一行。
- 攻击：engineered ontology→typed/generic×executor 2×2+wrong-field；ContactGuard已覆盖→逐字段chunk/latent/abort差异；sim labels不迁移→真机只semantic audit。
- typed持平→删field method、留ontology benchmark；success<3pp→diagnostic；real/OOD失败→删transfer。降级标题 **Contact Transition Ontology and Diagnostic Benchmark**。

### R10 annotation 稳健性主验收行

主表固定四列：每event type/body-pair的独立root support、valid-censor rate、双标者 Cohen κ（type/mode）与 timestamp MAE、matching tolerance `0/±1/±2` steps 下的 selection regret。任一关键event support<30 roots、κ<.7或结论只在±2成立时，该event不进入confirmatory macro并触发ontology-noise降级。

## 判负阈值

primary 相对 ContactGuard-style latent 的 selection regret 降≥20%且 CI 不跨0；contact-rich success 提升≥6pp、timing MAE 降≥20%为 secondary。field-only 对 latent-only ranking 提升≥5pp、latent+field 再提升≥2pp，wrong field 按方向使正确率降≥10pp。若机制指标达标而 success 增益<3pp，则只保留 ontology/diagnostic claim；若 ContactGuard-style latent 持平（regret 相对差≤2%且 success 差≤2pp），放弃 explicit field 方法贡献。真机以 reset/template block 配对分析；若 paired power 达不到 80%，不把 6pp 当 confirmatory。若仅触觉部署有效则降为多模态 policy；dense depth 持平则放弃“field更充分”。

## 风险、里程碑与负结果

仿真接触标签可能过于理想；用噪声注入、真机 label audit 和跨引擎验证。canonical frame 的 detector failure 显式回退，不把 GT pose 藏进部署。两周完成 ontology/extractor 单元测试、action-conditioned field 与 N=8 小规模 ranking；两月完成两仿真引擎、detector/noise/fallback 和真机。负结果仍可发表接触标签误差/视觉可辨识性与 dense geometry 的边界分析。

## 证据

[GeoPredict 2512.16811](https://arxiv.org/abs/2512.16811)、[MECo-WAM 2607.05468](https://arxiv.org/abs/2607.05468)、[ContactGuard 2608.13438](https://arxiv.org/abs/2608.13438)、[VT-WM 2602.06001](https://arxiv.org/abs/2602.06001)、[ViTacWorld 2607.22530](https://arxiv.org/abs/2607.22530)、[ContactWorld 2606.13877](https://arxiv.org/abs/2606.13877)、[TouchWorld 2607.07287](https://arxiv.org/abs/2607.07287)、[Where to Touch 2601.10930](https://arxiv.org/abs/2601.10930)。
