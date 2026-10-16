# GEO-P3：置信度校准的选择性几何路由

- Proposal-ID: GEO-P3
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: 主表固定attempted/accepted/selected三分母、各branch fallback与端到端总pipeline latency，杜绝conditional均值掩盖repair/stop成本。

## 问题与假设

几何 teacher/backbone 在遮挡、反光、透明体、运动目标和大视角变化下会自信地给错深度/对应；强制融合使策略比 RGB-only 更差。UAOR 用 action entropy 触发 observation reinjection，VLA calibration 估计总体成功概率，但二者不回答“当前几何证据是否会让动作比 RGB fallback 更差”。H1：校准**任务相关关系坏事件引起的分支 action regret**并在每个控制 frame 路由，可在不牺牲 ID success 的前提下降低 geometry-corruption OOD 风险；收益来自拒绝会伤害动作的几何，而不是增加 ensemble 容量。

## 最近邻差异

相对 VGA/Spatial Forcing：保持 backbone/teacher，新增的是几何证据的可拒绝接口。相对 UAOR：门控目标是 geometry-vs-RGB 的配对 action regret，不是 action entropy，且允许退回 RGB/低阶几何。相对 Confidence Calibration in VLA：相同校准标签预算下预测三个分支的配对 regret，而非只对最终策略成功做 Platt calibration。若简单 action entropy 在全部 corruptions 上等效，则本机制失效。

| 最近邻 | 校准目标 | 推理信号 | 决策粒度 | 标签预算/算力对照 |
|---|---|---|---|---|
| VLA Calibration v2 | action-wise/总体成功 calibration | prompt ensemble/action score | action/episode | 与本法使用同数量 calibration episodes、同三次 branch forward 上限 |
| UAOR v2 | action uncertainty 触发 observation reinjection | action entropy/不确定性 | control step | 共享 policy、观测历史、控制频率和 p95 latency |
| VGA/GAM | 原生/多层几何表征 | 几何特征 | always-on | 冻结同 backbone；只替换 router；GAM 强预训练作为反证压力 |
| SelectiveNet/selective classification | risk-coverage/abstention | classifier confidence/shared features | sample reject | 通用 selective-risk 参照；不含 geometry relation repair |
| Learning-to-Defer | 分支/专家的期望代价 | shared representation+expert outcome | sample routing | 直接攻击“三分支风险就是通用 defer”解释 |
| 本方案 | exact-reset 下 branch action regret + task-relevant relation bad-event | 当前帧增强、层分歧、两帧 motion/visibility | **每个 control frame 一次三路选择** | 与上面同时匹配 calibration labels、FLOPs、参数与 latency |

## 方法

同一个冻结 policy 提供三个可执行分支 `k∈{full geometry,coarse relation,RGB}`。从 VGA/GAM 的层 6/12/18 特征、当前帧 4 个固定可逆增强的一致性、t−1:t 的 forward/backward motion residual、visibility 与 action disagreement 得到 `z_t`；**没有多相机时不使用跨视图信号**，也不把 single-view photometric residual 写成 3D 真值。训练集在同 snapshot/外生 seed 上执行三分支 short horizon，定义部署统一的 target `R_k=1[H_c内失败]+λ_d·deadline_miss+λ_j·jerk`，以及 `Regret_k=R_k-min_jR_j`。risk head 输出 `q_k(z_t)=P(Regret_k>τ_r|z_t)` 与分位数 `v_k`；部署规则只用可见量：`k*=argmin_k [v_k+λCost_k]`，若 `min q_k>ε` 则强制 RGB/stop 预注册 fallback。未知 `L_act` 和 GT geometry 均不在公式内。

关系级辅助 target 不是通用 depth error，而是 `B_ij=1[关系 ij 的 oracle 修复使 full-geometry action 与低风险 branch 的距离下降>δ_a]`。target-only 生成路径逐字段为：simulator GT relation `g*_{ij}`→只在离线 copy 中替换 full branch 对应 predicted relation→冻结 action head 得 repaired action→与 unmodified full/RGB/coarse actions 在同 short-horizon seed 上算 regret 差→产生 `B_ij`。GT relation、repaired action、branch outcomes 全部停梯度且只写 target shard；router feature shard 只含 current predicted relation/residual/层分歧，schema validator 拒绝 `g*`/future/outcome 字段。

on-manifold repair 用独立 relation editor/decoder 将替换后的 token 重构回 detector/GFM observable relation；只有重构误差≤ID 95%分位且 detector consistency≥0.8 的 repair 可产生 B。四档为 GT valid repair、随机 relation、语义合法但错误 relation、full oracle geometry；若 valid repair 与两个 placebo 的 action shift无显著差异，B 判 artifact。failure-type/GT relation 只在 evaluator shard，禁止选择 calibration model。

部署明确是**三分支 reliability selector，不声称省算**：先并行计算 full/coarse/RGB actions，再以三者 disagreement 和 current features 选 branch。主表计三分支+router的总 FLOPs、mean/p95 latency/energy；另做不读 disagreement 的 cheap-router 作为可选变体。

每branch只训练一个regret distribution/CDF `F_k(r|z)`，由它同时导出 `q_k=1-F_k(τ)` 与tail quantile `v_k=F_k^{-1}(.9)`，不再独立head。decision先排除`q_k>ε`，余下最小化`v_k+λCost_k`；全被排除则RGB/stop。三branch冲突例若full的v低但q高，先被q门槛排除。

独立calibration split拟合 `(ε,λ)` 使geometry coverage `P(k∈{full,coarse})≈.90` 且风险最小，随后冻结；test不回调，只报coverage偏差CI、完整risk-coverage curve及三分支总cost。repair validity同时要求editor log-density≥ID 5%分位、decoder consistency≥.8、policy latent distance≤ID95%；valid repair相对random/valid-wrong placebo的primary action effect<3pp即禁用B target。

损失 `L=Σ_k pinball(Regret_k,v_k)+αBrier(1[Regret_k>τ_r],q_k)+βBCE(B_ij,c_ij)+γL_capacity`。generic router 只读 shared RGB/action features和branch logits；regret-only router读 `z_t` 但去掉 relation head/`B_ij`；geometry-aware再加入 relation bad-event aggregation。三者同参数/FLOPs，能测 geometry term 是否超越通用 defer。

| 信息 | 训练 | 推理 | 防泄漏 |
|---|---|---|---|
| 当前 RGB/语言/proprio | 是 | 是 | t 时刻；motion 仅 t−1:t |
| 几何预测、4 个当前帧增强/层分歧、两帧 motion/visibility | 是 | 是 | 无未来、无隐含多视角 |
| GT depth/pose、未来 track | 仅校准 target | 否 | stop-gradient、future-mask |
| 三分支 short-horizon outcome/regret | 仅 calibration target | 否 | exact-reset 离线生成、字段白名单 |
| action entropy | 可作 baseline/input ablation | 可部署 | 主模型是否使用单独消融，不混入 GT |

## 数据、实验与算力

构造 GeometryCorrupt：RoboTwin/LIBERO exact-reset 上透明/高光、遮挡比例、运动速度、视角四轴，每轴5级，并加入(A)几何误差大但动作不变、(B)全局误差小但关键关系翻转 hard pairs。校准 split 按物体/场景隔离；test 同时含完全未见的 corruption family 与已见 family 的未见 severity，另设 50-shot recalibration 结果且绝不并入 zero-shot primary。每 snapshot 三分支×S=4 seeds×Hc=16，因此2k档=384k env steps、10k档=1.92M env steps（另报 sim wall-clock/存储）。两套公平性：(i)等标签 episode 预算；(ii)等 environment-step/label-seconds 预算。真实 Franka 三任务只外测。MVP 预计算 GFM 1×A100/24h；完整4×A100/5天。

强基线：RGB-only、always geometry、VLA Calibration v2、UAOR、SelectiveNet、Learning-to-Defer、generic shared-feature router、regret-only router、action-entropy、MC-dropout、deep ensemble、oracle regret gate、random route、同FLOPs layer-disagreement。**唯一 primary** 是 validation-frozen 90% frame geometry coverage 下 selected-branch binary regret risk `mean 1[Regret_selected>τ_r]`；最强 comparator 按下述 R6 label-equal winner 规则冻结。AURC、ECE 和 episode success 均为 secondary。episode 为 cluster、task/corruption family 分层，paired cluster bootstrap 95% CI；pilot 按 25% 相对 risk 下降、α=.05、power=.8 冻结 episodes/family，family-wise contrasts做 Holm 校正。

### R6 监督公平、校准与 repair 审计

| baseline-native | supervision/branches | calibration |
|---|---|---|
| SelectiveNet/Learning-to-Defer/UAOR/VLA-Cal | 各自原生 reject/entropy/success target与原生分支 | 正文忠实版本，单列 native 结果 |

| label-equal adapter | supervision/branches | shared system |
|---|---|---|
| generic pooled / relation-indexed router | 同 final-regret 与 repair-derived `B` shards、同三分支 evidence、label-seconds | 同 encoder、参数±5%、branch calls、fallback、calibration size、runtime |

正交 2×2 为 supervision `{final-regret only,+same B}`× structure `{generic pooled,relation-indexed}`；relation ID shuffle 但 label 不变为负控。primary 只对 label-equal validation winner；每个方法在相同 validation 预算内独立拟合并冻结自己的 `(ε,λ)`，共享**程序与预算**而非数值，test 不插值回90%。native winner另表。

`B_ij` 继续定义为真实 short-horizon regret 差，因此必须执行 repair rollout：每 snapshot 资源为 `[3+N_valid_relation_repairs]×S4×H16` env steps；原384k/1.92M只覆盖三原始branches，repair另加 `N_snapshot×N_valid_relation×64` steps。editor/decoder/policy validity 用 train-only split 拟合阈值并冻结，router calibration用独立calibration split，二者不复用 outcomes。corruption manifest列 family×severity×task×asset×episode cell、renderer/asset seed group隔离与最低cluster。100-snapshot smoke实测每snapshot relations、各gate acceptance、B重标一致性、CPU/GPU/I/O后才能定2k/10k。若无法负担repair rollout，则必须删除B-regret措辞与该监督，不得改称无执行oracle action-distance。**截至r07 actual=0**。

### R8 LOFO、coverage 与 fallback 合同

- **唯一主命题：** 本法是 reliability selector（不是省算系统），在每法 validation-frozen 且 test achieved geometry coverage CI⊆`[.85,.95]` 时降低 selected-branch regret risk；**不声称**对未见 corruption family 有分布无关coverage保证。
- LOFO每轮完整hold透明高光/遮挡/运动/视角一family；seen-family unseen severity另表。asset family与hard A/B root group不跨split；RoboTwin-alt renderer与真实透明物仅secondary。
- 主表同时给full/coarse/RGB/stop比例、各route conditional risk/success、fallback-only与progress-adjusted utility。coverage CI不落`[.85,.95]`即该方法primary失败，不能后验匹配coverage；stop/fallback>20%或其单独解释>50%增益时只保留abstention诊断。
- 真机3 tasks×≥30 root blocks，corruption与50-shot recalibration roots不重合；方法顺序随机，force/workspace/emergency stop共享。trial不足power只外测。降级标题 **When Geometry Should Be Rejected: A Reliability Atlas**。

### R9 论文合同与审稿攻击

- 标题：**When Should Geometry Be Rejected? Relation-Aware Reliability for VLA Branches**。primary为coverage-feasible risk；not-claim为非省算、非distribution-free guarantee。最危险基线：same-B generic pooled/regret-only winner。
- 不可删除对象是LOFO Geometry Reliability Atlas：三分支matched outcomes、repair-validity/noise、achieved-coverage/route/fallback同表；现有calibration/UAOR不提供relation-indexed错误atlas与coverage失败合同。
- 攻击：三branch不实用→全成本主表；oracle B→same-B与noise curve；stop获益→route/conditional/progress utility。B无效→删relation method留Atlas；control<3pp→reliability-only；OOD失败→family failure atlas。降级标题 **Geometry Reliability Atlas**。

### R10 三分母与端到端成本主表

每个corruption cell固定报告 `(N_attempted repairs,N_valid/accepted,N_selected)`，risk分别以attempted-root和selected为分母；同时列full/coarse/RGB/stop各route与fallback率、从三branch forward到router/safety/commit的mean/p95/p99总latency与energy。禁止只在accepted/selected子集报均值；若attempted-root utility不改善，relation-B claim判负。

## 判负

在≥3 corruption 轴，fixed 90% coverage 的 regret risk 相对最强 regret-only router 降≥25%且 CI 不跨0，ID success 降≤1pp、**含三分支**p95≤1.25×、ECE≤0.05。geometry-aware 必须在同一 primary 上同时超过 generic 与 regret-only，而非以 success/AURC 的 OR 过关；若 primary 达标但 episode success 增益<3pp，则降级为 calibration/diagnostic claim。on-manifold repair 与 placebo 差<3pp、删除 relation calibrator 差≤2pp、或 failure-type metadata 泄入校准均否定 geometry-specific claim。所有阈值、50-shot 选项和 fallback 在 validation 冻结。

## 风险与里程碑

ensemble 成本可能抵消收益，默认单模型 layer disagreement；calibration 会随域漂移，单独报告跨域失效并测试 50-shot recalibration。两周完成 corruption generator/calibration curve；两月完成两 backbone、真机与延迟 Pareto。负结果产出 GFM error atlas 与“何时 RGB 优于几何”的部署准则。

## 证据

[UAOR 2602.18020](https://arxiv.org/abs/2602.18020)、[Confidence Calibration in VLA 2507.17383](https://arxiv.org/abs/2507.17383)、[SelectiveNet 1901.09192](https://arxiv.org/abs/1901.09192)、[Learning to Defer 2006.01862](https://arxiv.org/abs/2006.01862)、[VGA 2604.12908](https://arxiv.org/abs/2604.12908)、[VGGT 2503.11651](https://arxiv.org/abs/2503.11651)。
