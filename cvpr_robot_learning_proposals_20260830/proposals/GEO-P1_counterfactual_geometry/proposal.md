# GEO-P1：反事实任务相关几何瓶颈

- Proposal-ID: GEO-P1
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: 独立evaluator扩为两类不同checkpoint/reward，冻结hash/version与一致性门槛；分歧超阈值自动降级为ontology-specific benchmark，完成第10次实质refine。

## 问题与可观察失败

通用几何更准并不保证动作更准。VGA 已证明原生 3D backbone 可提升动作，MECo-WAM 已用 action-aware 4D 蒸馏，ST-VLA/GuidedVLA 已选择任务相关区域；尚未回答的是：策略提升究竟由哪一组几何关系因果中介。可复现失败是：在目标—末端相对位姿不变时替换背景/非目标物，full-feature geometry policy 的动作显著漂移；在只改变接触所需相对位姿时，动作却不够敏感。

## 相关路线与缺口因果链

- 第一类（VGA、GAM）：把 GFM 变成 policy backbone，增强整体几何，但无法区分有用几何与容量/正则增益。
- 第二类（Spatial Forcing、MECo-WAM）：蒸馏 dense/关系几何，MECo 已加入 action weighting，但 weighting 仍由观测动作相关性产生，未用反事实干预证明中介。
- 第三类（ST-VLA、GuidedVLA）：显式 mask/head specialization 可定位任务区域，但 mask 正确不等于策略的决策真的依赖这些关系。

缺口链条是：全局几何监督 → 背景与目标关系共同进入 latent → policy 可继续用场景捷径 → 几何 probe 上升但 OOD action 不升。核心假设 H1：若只保留在**环境结构方程决定会改变专家动作分布**的关系 token，则背景干预敏感度下降、任务关系干预敏感度上升。本文只把它称为 intervention-based reliance；不再声称该差分已经识别 OOD success 的因果中介效应。

## 精确差异

相对 VGA：不换 backbone，研究反事实几何充分集。相对 MECo-WAM：不再提出 action-aware 蒸馏，而用配对干预、token swap 和正确动作分布定义“action-relevant”。相对 GuidedVLA/ST-VLA：不以 attention/mask 可视化为终点，而以干预后的动作变化与成功率为判据。若 MECo 的官方实现加入同样配对干预并得到同样结论，本 Proposal 的新意失效。

| 最近邻 | 关系选择信号 | 监督/训练图 | student 可见信息 | 部署图 | 能支持的结论 |
|---|---|---|---|---|---|
| VGA/GAM | 全局原生几何预训练 | 几何 backbone→动作 | 当前图像/语言/本体 | 原生几何 backbone 常开 | 强几何表征是否提升动作 |
| MECo-WAM | 动作加权时间几何 teacher | 训练期 4D expert→因果 student | student 不见未来 4D | student-only | action-aware 几何蒸馏是否有效 |
| ST-VLA | learned task-relevant 3D–4D mask | mask 专家化/策略训练 | 当前观测与 learned mask | mask 分支常开 | 任务区域选择是否有效 |
| CofactVLA 2608.04396 | language-masked counterfactual branch | action/feature 层视觉去混杂 | generic visual features + language mask branch | 原 policy 分支 | 已覆盖 VLA counterfactual deconfounding；本方案不得据此声称新 |
| CAST 2508.13446 | counterfactual labels | 指令遵循/反事实监督 | 视觉语言 feature | VLA policy | 已覆盖 counterfactual labels；不提供结构化几何 relation 映射 |
| 本方案 | 环境 SCM 下成对干预导致的专家动作分布变化 | 反事实标签只进 loss；冻结相同 backbone | 当前/历史可部署 token | K-token gate+原 action head | 被选关系是否具有干预依赖且非背景捷径 |

## 方法与信息流

当前 RGB `o_t` 经冻结 GFM 得到关系集合 `g_t={g_ij}`；语言、proprio 和过去动作生成 query `q_t`。门控 `m_ij=sigmoid(q_t^T W g_ij)` 形成最多 K 个 token 的瓶颈，action head 只读 `m⊙g` 与原 VLA 的语义 token。

**Pair SCM。** 对同一 simulator snapshot 与随机种子，结构变量写为 `S=(G_task,G_nui,A_exo)`：`G_task` 是接触/避障可行性图实际读取的目标—末端、目标—容器或障碍—轨迹关系；`G_nui` 是纹理、背景、非交互物和保持投影误差阈值内的相机变量；`A_exo` 是固定的控制/物理随机量。oracle 不是当前 policy，也不把完整状态喂给 student：它只用任务定义的 collision/contact checker 枚举一个小动作码本，返回有效动作集合 `Y*(S)`。只有 `Y*` 在 nuisance pair 上 Jaccard≥0.95、在 causal pair 上 Jaccard≤0.5，且 renderer/可见度/动力学检查通过时才接受。

| Pair 类型 | do 变量 | 必须保持 | 标签/接受规则 | 例子 |
|---|---|---|---|---|
| positive nuisance（3类） | 背景纹理；非目标实例位姿；小相机扰动 | `G_task,A_exo,Y*` | `Jaccard(Y*,Y*')≥0.95` | 换桌布、移开无关杯、视角小变但任务关系不变 |
| positive causal（3类） | 目标—夹爪相对位姿；目标—容器间隙；障碍—候选轨迹交叉 | `G_nui,A_exo` | `Jaccard(Y*,Y*')≤0.5` 且有效动作改变方向可判定 | 左移目标、缩小插入间隙、把障碍移入路径 |
| hard negative（3类） | 相机扰动造成遮挡；移动“背景”但其成为障碍；改目标位姿但动作码本仍等价 | 其余变量 | 分别拒绝为 nuisance、改标 causal、拒绝 causal | 防止用干预名称代替结构检查 |
| 不可生成 | 布料/液体无稳定关系图；完全不可见目标；多个变量无法独立重置 | — | 从主结论排除并报告拒绝率 | 不把不可控编辑伪称 exact-reset |

每个snapshot由冻结continuous proposer用固定seed产生同一 `M=64` candidate chunks，SCM checker只在该库上标有效集 `S*`；student auxiliary energy head对同64个chunks输出 `p_i=softmax(score_i)`，主方向损失 `L_dir=-logΣ_{i∈S*}p_i`，部署也从同库选/执行，不对continuous flow density与categorical π*做KL。两动作例：S*={a1}, scores(ln3,0)给p=(.75,.25), `L_dir=-ln.75=.288`；翻转score得1.386。库由64→128时loss/support同步扩，continuous CEM oracle coverage regret>3pp即暂停。

nuisance token consistency不按index相减：只用部署detector track embedding、mask IoU、semantic soft type与GFM pose构造Hungarian cost，匹配后算token L1；unmatched token进入null并以unmatched mass单报，不零填。checker ID仅oracle alignment。action consistency仍在同candidate library算JS。type CE只是辅助表征指标，action主结论只看no-type vs predicted-type的success/selection regret。

**`G_task→token` 映射契约与字段 DAG。** checker 仅在 target worker 输出 `(checker_entity_ids,checker_relation_type)` 用于 pair 接受和 `CE(p_type,type*)`；student loader 严格只读 `RGB,language,detector_masks/confidence,GFM_tokens,proprio,past_actions`。部署 relation-type predictor 用当前语言 token、两端 detector-pooled GFM feature 与 `Δpose_GFM` 输出 soft distribution `p_type(r|x_≤t)`，adapter 构造 `r_ij=[pool_i,pool_j,Δpose_GFM,p_type]`；checker type/id、GT mask/pose 均被 schema validator 拒绝。主结果只含 `predicted-type` 与删除最后一项的 `no-type`；`oracle-type` 仅上界。故意把 checker type 喂给 student 是泄漏阳性，若异常跃升必须标红且不得入主表。若任一端 detector confidence<0.5、遮挡后无 token 支持或 GFM 不提供 correspondence，则标 `unmappable` 并分层。

**选择偏差与 swap selector。** 对每个 accepted causal/nuisance pair，从 rejected pool 按 RGB LPIPS、objectness、mask 面积、detector confidence、动作码本 coverage 1:1 最近邻匹配；只用 accepted 训练，但另训 acceptance probe。matched control 上 AUROC>0.65 即说明可观察 collider shortcut，主 claim 暂停。swap 仅离线评测，selector 只读部署预测 `p_type/mask/confidence` 且 stop-gradient；checker-selected swap 仅 oracle 上界，不产生训练梯度。

| 信息 | 训练可见 | 推理可见 | 防泄漏 |
|---|---|---|---|
| 当前 RGB/语言/proprio/已执行动作 | 是，时间≤t | 是 | 日志核对时间戳 |
| GFM 当前帧 token | 是 | 是（可缓存） | 不输入未来帧 |
| 反事实配对、SCM 关系标签、`Y*` | 仅 pair 筛选/loss | 否 | 字段白名单、stop-gradient、action-shuffle 负控 |
| 未来动作/成功标签 | 仅 `L_act` 监督 | 否 | 故意泄漏阳性对照必须异常高后再移除 |

## 数据、算力与工程

RoboTwin 2.0 exact-reset renderer 先跑1k attempted smoke；acceptance≥35%后才生成≥2k accepted MVP，最终规模由pair/task ICC功效与163.84M-step硬上限共同决定，不再预承诺20k。四类干预为纹理/背景、相机、目标位姿、末端位姿；LIBERO-Plus作外部OOD。SCM标签做0/5/10/20%翻转/阈值噪声曲线。10k DROID只作自然对照。每任务30真机配对仅外部效度。基础模型OpenVLA-OFT/π0 adapter；冻结VGGT/VGA。

## 实验与统计

**唯一 primary** 是预注册 held-out causal/nuisance pairs 上的 selection regret：对 pair `p` 的共享候选库 `A_p`，以 exact-reset、`S=4` seeds 的效用均值 `\bar Y_p(a)` 定义 `Reg_p=max_{a∈A_p}\bar Y_p(a)-\bar Y_p(\hat a)`，再以任务内 causal/nuisance pair 等权、任务间等权作 macro mean。最强 deployable comparator 按下述 R6 label-equal validation-winner 规则冻结；各方法共享 M=64 proposer、accepted labels、backbone、训练步、planner、fallback 和 p95 runtime。几何 OOD episode success 是 key secondary，`Intervention Reliance = ΔJS_causal-ΔJS_nuisance` 仅为诊断且不解释为 mediation effect。

关键 2×2 是 replacement unit `{structured geometry relation token, objectness-matched generic visual feature}` × counterfactual objective `{Cofact/CAST-style generic deconfounding, 本 SCM directional objective}`；只有 structured+SCM 额外有效才支持 geometry-specific claim。训练消融去 `L_dir/L_nui`；纯评测另做 no/predicted/oracle type、token permutation、选中/背景 swap；再扫K、GFM层、动作码本coverage与future-token泄漏阳性。

### R6 监督公平、复现与资源合同

| baseline-native | 原生输入/目标 | 冻结版本 |
|---|---|---|
| VGA / full-token GFM | RGB/geometry，原 action loss，无 `Y*`/SCM pair | arXiv版本、backbone commit 与正文公式写 manifest |
| Cofact/CAST/MECo-style | 各自原生 masked/counterfactual/distill target | 不可得代码时冻结重实现公式；复现失败不算本法胜利 |

| label-equal adapter | 额外监督 | 共享系统 |
|---|---|---|
| VGA+generic、full-token、objectness-token、MECo/CAST | 完全相同 accepted pairs、`Y*`、soft type 与 SCM label-seconds；不用 relation structure 的格也收到等维 shuffled/generic tensor | M64 hashes、Hungarian+null matching、backbone、steps、planner calls、fallback、p95 |

主正交格为 representation `{generic objectness,relation-indexed}`× objective `{generic deconfounding,SCM directional}`；两种 representation 具有同 cardinality、同 shared-Hungarian matching 代码、参数±5%。oracle/no-matching 只诊断。primary comparator 是 validation 上 `max{VGA+generic,full-token+SCM,objectness+SCM,MECo/CAST adapter}`，以 regret 最低且满足 p95 为 winner，冻结一次；native winner另表，test 不重选，主比较做 proposed-vs-label-equal winner closed test。

每 accepted pair 两个 members 都执行，故 `2×M64×S4×H16=8192` env steps；2k accepted MVP=16.384M、20k仅为上界163.84M。若 target shard 为64KB/pair，则20k为1.28GB（十进制）/1.19GiB，不是TB；另报frame引用去重前后bytes与dedup ratio。三阶段 gate：(1) 1k attempted smoke只估acceptance/throughput；(2) 达35%后生成≥2k accepted MVP；(3) 用pair/task ICC反推confirmatory clusters，20k不是固定承诺。target shard四个2×2格共享不乘4；student training/model×seed GPU-hours逐格相加。manifest增 `pair_id/member_id/intervention/reject_code/checker_commit/renderer_seed/candidate_hash`、schema/version/license，并按task+asset+snapshot-family group split，断言任一pair/member/hash不跨split。**截至r07 actual=0**，不得写已可行。

### R8 唯一主命题、OOD 与真机边界

- **唯一主命题：** 在 RoboTwin exact-intervention、candidate-support-valid 的 held-out task/asset pairs 上，relation-indexed SCM supervision 降低 M64 selection regret。
- **不声称：** 不声称识别现实因果效应、基础模型未见过 test assets、LIBERO/真机验证了 simulator `Y*`，也不声称省算。
- OOD矩阵固定四轴：asset按family 70/10/20% train/cal/test；task template 8/2/2；renderer仅RoboTwin-default参与train/cal，RoboTwin-alt与LIBERO只secondary；intervention severity train中3档、cal1档、test外推1档。foundation pretraining组成不可审计，明确列为威胁而不写zero-shot novelty。
- 每域报告 candidate coverage/unmappable/fallback、conditional-on-support regret 与 episode success；coverage<80%则该域只作failure atlas。真机3 tasks×30 root templates，root内方法顺序随机，reset pose drift入block covariate；marker/GT用独立logger且model RGB裁除。所有方法共享collision/force/workspace checker与emergency stop。无root-cluster power或success<3pp时，真机/LIBERO只外部效度，论文标题降级为 **Geometry Counterfactual Ranking Benchmark**。

### R9 论文合同与审稿攻击

- 建议标题：**Geometry Counterfactual Ranking: Do Relation Tokens Beat Generic Deconfounding?**
- 唯一主命题/primary沿用R8与M64 regret；最危险基线为label-equal validation winner。不可删除科学对象是：同一pair/candidate/utility下 relation-vs-generic×SCM-vs-generic 的四格协议与独立reward/checkpoint evaluator；VGA/Cofact/MECo均未提供这一可反驳测量对象。
- 攻击→回应：checker自洽→primary不用checker score且换reward/checkpoint；VGA+Cofact组合→不称因果理论，只称pair protocol/2×2；oracle监督→label-equal首组。strong baseline持平→删method只留protocol；success<3pp→删control；OOD/真机失败→删external transfer。降级标题 **Geometry Counterfactual Ranking Benchmark**。

### R10 独立 evaluator 一致性门槛

primary同时由 evaluator-A（训练checkpoint+原reward schema）与 evaluator-B（独立policy checkpoint+预注册替代reward：success/collision/jerk权重改变）重算；冻结 `evaluator_id/checkpoint_sha/reward_schema_sha/code_commit`。两者方法效应方向必须一致且相对regret reduction差≤10pp；否则不称geometry-general ranking，只降级为 **ontology-specific pair benchmark**，并把分歧率/任务层分布列主表。

## 可证伪判据

primary endpoint 为同 M=64 库的 held-out selection regret；推断以 pair 为 cluster、task 为上层的两级 bootstrap（10k resamples），并用 mixed model `regret~method+pair_type+(1|task/pair)` 作一致性核验。按基线平均 regret 的 20% 相对下降、两侧 α=.05、power=.8，在 pilot 估 intracluster correlation 后冻结每任务 pair 数；不足则只报探索性 CI。四 OOD 轴只用于 secondary，并做 Holm 校正。若 primary 达标但 geometry-OOD success 增益 <3pp 或方向不一致，结论降级为“候选排序诊断”，不得声称控制改进。predicted-type 相对 no-type selection regret 差≤5%则删除 type；checker/oracle type 不进主结论。unmatched mass>20%、acceptance AUROC>.65 或 coverage regret>3pp 均判机制不可用。所有 operating point（acceptance checker、K、type threshold）只在 validation 冻结。

## 失败、负结果与里程碑

门控可能塌缩到语言/objectness；用容量匹配、熵监测与 oracle 上界诊断。GFM 在反光/动态物体上的置信失效属于另一独立方向，不在本 Proposal 偷换。两周：实现 SCM/checker、验收 acceptance 与 3+3 pair、gate smoke test；两月：两 backbone、四 OOD 轴、真机配对与完整干预依赖分析。即使负结果也产出“几何 probe 与动作干预依赖脱钩”的 benchmark。

## 证据

[VGA 2604.12908](https://arxiv.org/abs/2604.12908)、[MECo-WAM 2607.05468](https://arxiv.org/abs/2607.05468)、[ST-VLA 2603.13788](https://arxiv.org/abs/2603.13788)、[CofactVLA 2608.04396](https://arxiv.org/abs/2608.04396)、[CAST 2508.13446](https://arxiv.org/abs/2508.13446)、[Spatial Forcing 2510.12276](https://arxiv.org/abs/2510.12276)、[GuidedVLA 2605.12369](https://arxiv.org/abs/2605.12369)。
