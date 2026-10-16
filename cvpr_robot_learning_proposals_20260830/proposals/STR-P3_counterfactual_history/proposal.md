# STR-P3：严格配对的反事实历史辨识训练

- Proposal-ID: STR-P3
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: 增加第二checkpoint/reward evaluator一致性门槛、分歧率与rejected-pair manifest，进一步破除generator-evaluator共偏自洽。

## 问题与假设

IntentVLA 已证明短历史有用，Remember Smarter 已做记忆压缩；“再加历史 encoder/contrastive loss”无新意。现有自然数据里，历史往往与纹理、episode、任务 ID 同时变化，策略可能凭静态线索区分。H1：只有两条**合法历史 rollout** 到达匹配的当前可见观测/语言/本体，却因物理 hidden state 不同而具有交叉不兼容的高价值 action sets，才直接监督 history-dependent action。示范者的任意 commitment/style 不进入主 claim，单独作为多模态 imitation 诊断。

| 最近邻 | history 构造 | action target | 是否验证交叉价值 | 本方案差异 |
|---|---|---|---:|---|
| IntentVLA / AliasBench | 自然短历史+VGGT | demonstration action | 按原协议 | 复现后检查是否存在严格 same-current paired reachability |
| Remember Smarter | learned memory compression | demonstration action | 否/按原协议 | 同窗口/参数下作为 learned forgetting 强基线 |
| Diffusion Policy / BeT | 多模态 behavior distribution | set/mode-like action | 不要求 hidden-state pair | 排除“两个示范动作都有效”的替代解释 |
| 本方案 | 两条合法 rollout 到 same-current tolerance | simulator value 验证的 set-valued actions | **是：A-action 在 B 低值且反之** | history swap 只在物理可辨识 pair 上要求方向变化 |

本方案不主张新 history encoder。贡献优先级固定为：(1) Counterfactual-Alias 配对生成器/benchmark；(2) 由交叉 value incompatibility 提供的 paired supervision；(3) 该 supervision 在两类既有 history backbone 上是否都有增益。若只在定制 encoder 上有效，只能视为架构技巧。

**IntentVLA AliasBench 官方代码 overlap 审计。** 已实际克隆官方仓库 commit `6d513c8118e8041fcb1db218cce2201a27a9b58c` 并运行 `literature/audit_aliasbench.py`；报告见 `literature/aliasbench_schema_audit.md`。静态AST结果为12 task files、46 trace calls，字段仅 `intent,destination,ambiguous,control`；未发布 pair index/current-frame tolerance/reachability hash/candidate-Q。README同时说明当前只发布task code、full model待发布，故结论限定该commit。

| 审计项 | AliasBench v2 当前可核验状态 | Counterfactual-Alias 必须额外满足 | 重合时处理 |
|---|---|---|---|
| 当前帧匹配 | 该commit无pair index/LPIPS/depth/proprio tolerance | 四阈值同时通过 | 公开代码未覆盖strict合同 |
| history control | trace有intent/ambiguous/control，但无双rollout hash | 两条合法rollout+hash | 部分覆盖自然context，不覆盖reachability |
| value incompatibility | 无candidate-Q/value-set字段 | S=8双向cross regret | 未覆盖 |
| 字段泄漏 | trace调用无state/future/seed/episode ID | student继续schema拒绝 | 仅静态API结论，运行数据仍审计 |

相邻的 causal representation / counterfactual sequence 工作说明“用反事实配对学不变表示”本身并不新；本方案只主张机器人 POMDP 中**双可达历史、同当前观测、交叉 value-set 不兼容**这一数据合同及其控制终点。

## 配对生成过程

主数据只用物理 hidden-state pairs。生成器从同一任务/asset 分别执行两条合法 causal action histories `h_A,h_B`，不允许在末端直接编辑 hidden state；二者到达时要求当前 RGB LPIPS≤ε_img、visible depth MAE≤ε_d、语言完全同义、proprio L∞≤ε_q、可见对象 pose≤ε_p。保存 rollout action/state hashes 证明从 reset 到当前帧的可达性。直接 state edit 只作 `diagnostic-edit` split，永不混入主表。

从 snapshot A/B 对同一候选 action library 用 S=8 matched seeds 估计 `Q_A(a),Q_B(a)`，定义高价值集合 `A_A={a:Q_A(a)≥max Q_A−ε_Q}` 与 `A_B`。relevant pair 必须满足 `max_{a∈A_A}Q_B(a)≤max Q_B−δ_Q` 且反向亦然；因此“两个示范动作距离大但都成功”会被拒绝。irrelevant-history pairs 则要求两集合 Jaccard≥0.8。示范 commitment pairs 另存，仅研究 multimodal behavior，不要求 history swap 跟随某个任意 style。

## 方法

每pair由冻结frame-only proposer在lexicographic canonical member上用固定seed生成state-local library并复制给A/B；manifest保存proposer commit/seed/64 action hashes，A/B逐字节相同。Q按任务预注册范围归一为 `Adv_X(a)=(Q_X(a)-max_bQ_X(b))/(Qmax_task-Qmin_task+ε)∈[-1,0]`，cross loss用Adv，避免两任务reward scale 1 vs100时梯度失衡。部署state-local proposer同协议产生library。

不设计专属 encoder：backbone-A 为原 IntentVLA causal history module，backbone-B 为普通 causal Transformer（同 window、action head、参数±5%）；二者分别训练原数据、加入同数量 random pairs、加入 Counterfactual-Alias pairs。由 `Δ_data`（同 backbone 加 pairs）与 `Δ_arch`（同数据换 backbone）分解收益，主 claim 要求两种 backbone 的 `Δ_data` 都显著为正。

**Q-set target 路径。** pair generator 保存 simulator snapshot 到独立 target shard；同一候选 action library 与 `S=8` 外生 common seeds 向前 rollout `H_Q=16`，future reward/success 只在 target worker 计算 `Q_A/Q_B` 与 bootstrap CI。student loader 只允许当前/历史 RGB、proprio、past executed actions、language 及离线生成的 set/rank target，schema validator 禁止 snapshot state、future observation/reward、seed、task/episode ID；target tensor stop-gradient。部署没有 Q rollout、sim state 或未来字段。

| 变量 | student/action 训练 | pair oracle/target | 部署 | 审计 |
|---|---:|---:|---:|---|
| 当前 RGB/语言/proprio | 是 | 是 | 是 | 像素/feature阈值匹配 |
| 过去 RGB/proprio/已执行动作 | 是 | 是 | 是 | causal window |
| hidden simulator state、未来最优动作 | 否 | 是 | 否 | 导出后删除；stop-grad |
| task/episode/random seed ID | 否 | 仅生成器 | 否 | 模型文件不得含字段 |
| future frame/success | 否 | 仅验证 pair | 否 | future-mask/阳性泄漏对照 |

## 数据与实验

成本重算：原20k accepted pairs需要 `20k×2×64×8×16=327.68M` env steps；若acceptance10%，value-stage最坏3.2768B，故不再承诺5天。MVP仅2k total pairs、M=16,S=4：accepted 4.096M steps；记录attempted→reachable→matched→value-accepted漏斗，acceptance<20%或M16 coverage gap>10%即停。完整目标改8k accepted、M64,S8=131.072M accepted steps，attempted hard cap40k（value rollout ceiling655.36M）；CEM512只抽1% accepted，额外10.49M steps。只存1.024M state-action Q summaries约<1GB，不存全部帧；CPU vector sim与GPU policy分工，实测steps/s后wall-clock hard cap7天。

AliasBench 结论继续严格限定公开 commit 的静态 API，不外推私有数据/运行时无泄漏。由于该公开任务代码没有 matched-pair index 或 candidate-Q，**放弃“自然 matched primary”**：唯一 primary 改为生成器中严格 held-out causal physical pairs 的 cross-value regret，pair 的两个历史状态、M=64 candidate library 与 S=8 seeds 视为一个 cluster。官方 AliasBench 只作 external-validity success，不用于证明 cross-value 机制。

强基线：IntentVLA、Remember-Smarter、Diffusion Policy/BeT、causal Transformer、frame-only、普通 contrastive、random pair、oracle hidden state；同 action head/history长度/参数。最强 deployable comparator 按下述三 backbone×data×objective 的 label-equal validation winner 冻结；native 原始数据 history winner 另表。matching propensity 只使用动作前可部署 covariates，在看 Q/outcome 前冻结。

primary cross-value regret 取 task-normalized `Adv` 下的 pair-macro mean；两级 pair/task cluster bootstrap 95% CI，按相对原始数据 history baseline 降15%、α=.05、power=.8 的 pilot ICC 冻结 pairs/task。所有方法在同500-pair audit subset 运行 M16/M64×S4/S8 敏感性；完整 primary 固定 M64/S8。value-set coverage、history-swap、closed-loop success 与官方 AliasBench 均为 secondary。

历史模态严格拆分：only-last-action、only-all-past-actions、only-past-proprio、only-past-video、video+proprio 不含 actions、action-history shuffle；由此把动作平滑/控制状态与视觉历史贡献分开。另消融 physical/commitment、relevant/irrelevant、无 swap、matching tolerance、history 截断/伪历史/反序、字段平衡、diagnostic state-edit、hidden/future 泄漏阳性对照。

### R6 数据×目标正交公平与独立 evaluator

| baseline-native | data/target | label-equal adapter |
|---|---|---|
| IntentVLA、causal Transformer、Remember-Smarter | 原始 history data 与原生 BC/memory loss | 各自接同 strict/control pairs、M64/S8 Q shards 与相同 optimizer steps |

| 主 2×2 | ordinary history BC/ranking | cross-value swap objective |
|---|---|---|
| covariate-matched irrelevant/control pairs | C×B | C×X |
| strict Q-set pairs | Q×B | Q×X（proposed） |

四格获得相同数量 extra pairs、全部 M64/S8 Q（即使 ordinary loss 不使用也计成本）、backbone/action head/parameters±5%、steps与 runtime；random pair只sanity。hard control 要求同样外观/动作历史接近且合法可达，但 Q-set Jaccard≥0.8；strict 则 Jaccard≤0.2。label-equal validation winner 从三 backbone×C/Q×B/X 冻结；native winner另报，primary 对 winner closed compare。

history search/reachability/matching 与 value stage 分账：每attempt记录 `history_steps_A/B`、render/match steps与互斥reject code；total hard cap=`history_search_steps + value_rollout_steps + evaluator_steps ≤ 1.0B`，不再只限value。MVP M16/S4只测acceptance/coverage/throughput，不能出primary；primary固定M64/S8且power达标才启动。evaluator矩阵以base H16为参照：new seeds/H32需 `N_pair×2×64×8×32` new steps；reward-only可复用H32 trajectories重打分；independent checkpoint须重新生成candidate library并再跑同H32，为最坏额外一倍，报告共享后与最坏总量。manifest加checkpoint/asset/task/pair lineage与perceptual+state hash近重复拒绝；三backbone×四格×3 seeds训练另计GPU-hours。**截至r07 actual=0**。

### R8 synthetic-to-external 边界

- **唯一主命题：** sim-A reachable history-alias benchmark与cross-value supervision改善held-out pair regret；**不声称**AliasBench/真机验证cross-value，也不声称自然域普适memory。
- sim-A仅train/generation/threshold；sim-B换renderer+asset+history-policy作zero-shot且不fit matching/Q，recalibration另表。AliasBench只报native success/history ablation并标“无pair-Q”。
- 真机只保留2–3 near-match tasks、每task≥80 root blocks；RGB/pose/proprio容差在sim-A validation冻结，独立GT logger。达不到acceptance/power则删除真机措辞。共享collision/workspace guard；降级标题 **Counterfactual-Alias Benchmark**。

### R9 论文合同与审稿攻击

- 标题：**Counterfactual-Alias: Reachable History Pairs with Conflicting Action Values**。primary=pair regret；not-claim=不称identical state/natural memory。最危险基线三backbone label-equal winner。
- 攻击：synthetic self-consistency→H32/reward/checkpoint/sim-B；1B steps→M16 gate/同Q成本；观测不相同→tolerance-matched+hard controls。
- acceptance不足→generator feasibility report；cross-value持平→pure benchmark；control<3pp或external失败→删除memory method。降级标题 **Counterfactual-Alias Benchmark**。

### R10 双 evaluator 与rejected-pair审计

generator后用 evaluator-A（base checkpoint/reward）与 evaluator-B（独立checkpoint+reward weights+H32）复算Q-set。accepted strict pair要求两者cross-value冲突方向一致、Jaccard阈值均过；分歧率>20%或method regret effect差>10pp则只发布generator disagreement atlas。manifest对每个rejected pair保存root lineage、match metrics、A/B Q hashes、reject code与两evaluator版本，禁止静默筛掉分歧。

## 判负

primary 相对各自原始数据 history baseline 的 regret 降≥15%且两 backbone 的 CI 均不跨0；causal physical pairs 上交叉 ranking≥75%。history swap 后至少70%选择对应高价值集合、irrelevant swap 的 action JS≤0.1；闭环 alias success 提升≥5pp为 secondary。若 primary 达标但 closed-loop success<3pp，降级为离线 alias ranking benchmark。若 strict pairs 只在一个 backbone 提升，architecture-agnostic claim失败；only-last-action 与 full history差≤2pp则不宣称长期历史；only-past-video 相对 frame-only不提升≥3pp则降级为控制状态记忆。oracle hidden state 上界<5pp、random-pair 与 strict-pair 差≤2pp，或 AliasBench 后续已有同合同，均否定对应主张。

## 风险与里程碑

严格同当前可见观测但 value set 不同正是 POMDP 边界；主 claim 只在合法 rollout 可达的物理 hidden state 上成立。两周完成 reachability/hash/value-set validator 与 acceptance audit；两月完成两模拟器、模态分解与真机 near-match。负结果仍给出 AliasBench 静态捷径审计与 pair construction 工具。

## 证据

[IntentVLA 2605.14712v2](https://arxiv.org/abs/2605.14712)、[Remember Smarter 2608.15269](https://arxiv.org/abs/2608.15269)、[Diffusion Policy 2303.04137](https://arxiv.org/abs/2303.04137)、[Behavior Transformer 2206.11251](https://arxiv.org/abs/2206.11251)、[Towards Causal Representation Learning 2102.11107](https://arxiv.org/abs/2102.11107)。
