# JEP-P2：接触拓扑操作驱动的动态 Slot-JEPA

- Proposal-ID: JEP-P2
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: 增加0/±1/±2 frame matching tolerance、原始sensor-to-event timestamp误差与transaction regret联表，防宽容匹配掩盖时序错误。

## 问题与假设

OA-WAM、POT-VLA、3D-ALP 已覆盖对象 slot/anchor 的持久身份；ContactWorld/ViTacWorld 已预测接触/触觉。固定 slot 仍隐含“对象集合和归属不变”，但 manipulation 中 grasp 会把 gripper-object 临时组成复合体，handover 改变 ownership，开盖/拆装产生 attachment 的建立/解除。若拓扑不更新，遮挡期间运动预测与规划会把被抓物体当独立自由体。

H1：**给定候选 action chunk**预测带时间戳/偏序、typed、满足合法性约束的 graph-edit event sequence，再在事件执行后的动态图 latent 中预测 future，能比 fixed persistent slots 与 action-conditioned graph dynamics 更好地排序拓扑变化动作。`merge/split/transfer` 不再作为互斥分类；compound 是可逆 derived view，transfer 是多条 edge edit 的原子事务。图网络、对象 slot、JEPA predictor 本身均不是新意。

## 最近邻差异

- OA-WAM/POT-VLA：保持身份地址/3D token；本方案允许关系拓扑改变，并以操作准确率/反事实图编辑为主中介。
- 身份 belief 邻近方向研究 association 的概率校准；本方案研究正确 identity 已知时接触拓扑如何改变动力学表示。
- ContactWorld/ViTacWorld：预测 contact/tactile signal；本方案预测 contact 导致的对象图结构操作并用于 JEPA planning。
- StageWAM：预测 next semantic stage；本方案是局部物理 attachment graph，不做阶段语义。

| 最近邻 | graph/object 状态 | action conditioning | 预测字段 | 本方案差异 |
|---|---|---:|---|---|
| OA-WAM / POT-VLA | persistent address/token | causal world/action | slot content/address | 显式 attachment/ownership edit algebra，而非新增持久 token |
| ContactWorld v1 | action-conditioned latent contact-world prediction | 是 | 未来 contact/visual latent；正文未给 body/attachment/ownership typed graph | 同 candidate ranking 检验显式 event transaction 的独立增益；代码状态按项目页 promised/未在本地核验 |
| ViTacWorld v1 | action-conditioned visual-tactile world model | 是 | future visual+tactile representation；无 typed ownership/attachment graph | tactile rollout 是强基线；官方代码链接状态需冻结 manifest |
| TouchWorld v1 | future visual-tactile subgoal/tactile residual | 是 | subgoal/residual；无逐 candidate typed graph edit sequence | 不把 tactile prediction 当缺口，差异只在 event topology |
| Interaction Networks / NRI | object relations/dynamics graph | 可含 action/control | learned edge/dynamics | 直接图动力学强基线；JEPA/机器人应用本身不是创新 |
| C-SWM 1911.12247 / graph world model | object-centric contrastive structured dynamics | 可含 action | object/relational next-state latent | structured predictor 不是新意；必须共享 typed event labels 公平比较 |
| 本方案 | current causal identity graph+typed edge events | **每个 candidate action 显式输入** | timestamped/partially ordered Add/Del transaction + future latent | 仅主张遮挡 transient event 不被 endpoint cancellation 丢弃、合法事务可诊断 |

版本/代码状态截至 cutoff：ContactWorld=2606.13877v1，正文承诺公开 benchmark/data/model/code、未本地验证发布；ViTacWorld=2607.22530v1，项目页存在、代码/权重未本地验证；TouchWorld=2607.07287v2，项目页存在、代码/权重未本地验证。不可得时按正文重实现并单列 reproduction gap，不能把实现不可得计为本方法胜利。

## 方法

**闭合 DAG。** action proposer 先从 `(o_{≤t},l,s_{≤t})` 产生固定 N 候选 `a^{1:N}`；current graph `G_t` 只由 current/past causal detector/association 得到。operator 对每个候选输出 `p_θ(ΔG^{(i)}|G_t,a^{(i)})`；typed executor 得 `G_{t+H}^{(i)}=Exec(G_t,ΔG^{(i)})`，JEPA predictor 输出 future node latent，candidate scorer 最后排序。所有基线共享候选，operator 不反向生成 candidate，因而无 action—operation 循环。

**Typed ontology/edit-event algebra。** nodes 是 robot-link、rigid object、articulated part；持久 node identity 不因 compound view 消失。edge types：瞬时 `contact(i,j,normal-bin)`、持久 `rigid-attach(i,j)`, `kinematic-joint(i,j,type)`, `ownership(robot,obj)`。primitive event 为 `e_k=(τ_k,Add/Del,typed-edge,confidence)`，`τ_k∈{1…H}`；同一时间 bin 的并发事件构成 antichain，不同 bin 由偏序 `≺` 约束。derived compound 是 rigid-attach 连通分量。transfer 事务为同一 commit group 内 `Del ownership(r1,o)+Del attach(r1,o)+Add attach(r2,o)+Add ownership(r2,o)`，要么全提交要么全拒绝。合法性：每对象至多一个 ownership；rigid-attach 不得形成跨独立 robot 的非法 cycle；Del 必须对应当时已存在 edge；同 edge 的 Add→Del 可在不同时间合法存在，因而 attach 后 detach 不会被 endpoint cancellation 抹掉。

**标签提取伪代码。** `(1)` 在 h=0:H 从 simulator causal body IDs 读取 contact manifold、joint constraints、gripper closure/force；`(2)` 连续≥2 frames 的 stable grasp 且相对 transform 方差<τ_pose，在首个满足 bin 发 `Add rigid-attach/ownership`；`(3)` force/closure解除≥2 frames，在解除确认 bin 发 `Del`；`(4)` 对每个时间 bin 顺序执行 events 并跑 legality checker，保存 partial-order DAG 与 commit-group，不再只比较 `G_0/G_H`；`(5)` ambiguous/tie 或 association confidence<0.8 标 abstain。主 teacher 的 ID matching 只能用 t 及过去 frames；full-trajectory association 只作 oracle gap，禁止进入主 target。

event decoder预测typed sequence。主scorer只读离散 `(time-bin,Add/Del,edge-type,node-role,co-membership)` tensor的 **stop-gradient**；operator/proposer不接收scorer梯度，end-to-end仅消融。action-ID probe从event tensor解码candidate index，并与同split GT-event tensor probe经验accuracy比较，前者高出>10pp即判串谋。

数据单位 `snapshot×N=8 candidates×S=4 exact-reset seeds×H=16`，全部候选都执行并提取event/no-event/censor target；2k snapshot MVP=1.024M env steps。manifest含proposer/version/action hash/seed/horizon/abstain/censor，train/test candidate support overlap须≥90%。

唯一匹配算法：预测/GT按±1 frame+typed-edge Hungarian匹配event。transaction不预测任意ID，而对匹配后事件对预测co-membership矩阵 `C_kl=1[same atomic group]`，BCE/loss与exact partition metric对group label置换不变；canonical显示顺序只按最早τ/edge tuple。null计FP/FN，四事件handover只有co-membership和偏序全对才exact。

ambiguous event可abstain训练，但评测全部进入risk-coverage：主固定90% event coverage阈值只在calibration split拟合；abstain样本closed-loop使用fixed-graph fallback并计成本/success，报AURC，不能静默删除难handover。action-ID probe用同模型/同split分别读predicted-event与GT-event tensor，前者超过后者经验accuracy+10pp判shortcut。

| 变量 | student/action 训练 | target/teacher | 部署 | 审计 |
|---|---:|---:|---:|---|
| 当前/过去 RGB、proprio、已执行动作、语言 | 是 | 是 | 是 | causal |
| 当前检测/对象 slots/contact proxy | 是 | 是 | 是 | 可部署视觉/proprio |
| candidate action chunks | 是 | 是 | 是 | proposer 先产生；逐候选 operator |
| current/past-only association teacher | 否（仅 target 构造） | 是 | 否 | causal 主监督；记录置信/abstain |
| full-trajectory mask/association/graph | 否 | oracle only | 否 | 不进入主结果，单列 gap |
| 未来 operation label | 否 | loss target | 否 | action发生后才可进入下一周期 |
| 触觉 | 默认否 | 可选 oracle | 默认否 | 单列结果 |

## 数据、实验与资源

TopoManip-10：RoboTwin/ManiSkill 10 tasks（抓持复合、handover、开盖、插拔、工具挂接），每种 primitive edit≥5k；严格遮挡与同类物体，并分 detector/contact/association noise 轴。MVP 2×A100、3 天；完整 8×A100、8 天；真机 4 tasks×80 trials，外部 marker 仅评 graph GT。

强基线：OA-WAM、POT、NRI/C-SWM、object-centric JEPA、ContactWorld、tactile oracle、fixed/oracle/random events；同 detector/slots/NFE/candidates。最强 deployable comparator 按下述 native/adapter 2×2 validation winner 冻结。**唯一 primary** 是 frozen 90% event coverage 的同候选 selection regret；event F1/timestamp/legality是机制指标，planning success secondary。snapshot cluster、task分层，按20%下降冻结power。

公平合同进一步固定：NRI/C-SWM/object-JEPA共享同candidate manifest、event targets、matching、typed executor与scorer，只替换representation/predictor；任何基线不得少拿label或换executor。

2×2 机制干预保持 current graph/RGB 固定：right action+right edit、right action+wrong edit、wrong action+right edit、wrong action+wrong edit，分别进入 predictor/scorer；只有 edit correctness 在固定 action 内仍改变 ranking/success 才支持 graph-update 机制，而不是动作标签捷径。其余消融：无 operator、只 contact binary、无 cycle/legality、fixed slots、tracker、触觉、label shuffle、future graph 泄漏阳性对照。

### R6 representation×event-use 训练 2×2 与 claim ladder

| baseline-native | native target/executor | same-label adapter |
|---|---|---|
| NRI/C-SWM/OA/POT | 原生 endpoint/dynamics/token objective | 同 ordered event labels、matching、confidence与candidate future loss |

| 主 2×2 | flat same-label tensor scorer | typed transaction executor |
|---|---|---|
| NRI/C-SWM dynamics | N×F | N×T |
| JEPA predictor | J×F | J×T（proposed） |

四格共享 event targets、Hungarian/null/abstain、confidence、future loss、parameters±5%、candidate/planner calls、fallback与 runtime。另用同 event sequence 确定性压缩 endpoint-edge target，与 ordered-event target 在同表示、同 label-generation cost 下比较。validation winner 在四格/adapter 中按 primary regret冻结，native winner另表。

claim ladder：N×T 与 J×T 持平→删 JEPA；J×F 与 J×T 持平→删 typed executor；两者都持平→仅benchmark。200-snapshot smoke后以snapshot/task ICC求confirmatory N，full hard cap=100M env steps；四格×3 seeds GPU-hours另计。`topo_event_v1.yaml`版本化nodes/edge/event/null/abstain/censor、co-membership与partial-order canonical serialization。字段来源表：sim body ID/contact/force仅target；teacher只读current/past detection/association confidence；full-track/future字段被loader单测拒绝，oracle gap独立shard。split按task-template+asset+contact-program family group hash；candidate support overlap只检候选空间。**截至r07 actual=0**。

### R8 ontology OOD、真机与在线 guard

- **唯一主命题：** transient ordered events避免endpoint cancellation并改善closed-ontology新program ranking；**不声称**open-ontology新edge/event零样本预测，后者只unknown/atlas。
- 真机marker独立视角/裁除，双标event time/type/transaction并报confusion/κ/同步CI。coverage不在frozen `[.85,.95]`则不可确认。
- 所有方法共享force/workspace/collision与illegal-transaction pre-commit guard，计latency。N×T持平删JEPA、flat持平删executor、都持平降级 **TopoManip Event Benchmark**。

### R9 论文合同与审稿攻击

- 标题：**TopoManip: Ordered Contact Transactions beyond Endpoint Graph Prediction**。primary=coverage-feasible regret；not-claim=slots/graphs/JEPA新。最危险基线NRI×typed executor首行。
- 攻击：NRI+rich labels→2×2决定；closed engineered→主动限定；branding→标题无JEPA。
- N×T持平→删JEPA；J×F持平→删executor；两者持平或control<3pp→纯event benchmark；real失败→sim-only。降级标题 **TopoManip Ordered-Event Benchmark**。

### R10 timestamp tolerance 与transaction regret联表

同一raw sensor/event timestamps下，以exact `0`、`±1`、`±2` frame三种匹配容差重算event F1/order/transaction exact与selection regret；另报sensor→logger→event timestamp error distribution。若order/transaction贡献仅在±2成立或raw timing error大于预测改进，typed sequence claim降级为coarse endpoint benchmark。

## 判负

primary 是90% coverage 下 selection regret 相对 NRI+same-label 降≥20%且 snapshot-cluster 95% CI 不跨0；event-sequence F1≥.80、wrong-event 使 fixed-candidate score accuracy 降≥10pp为机制门槛。closed-loop 层固定 candidate set 后 wrong events 改变 argmax，再要求 success 降≥5pp；若 primary/F1 达标但本法 success 相对 NRI 增益<3pp，则降级为 event-topology diagnostic，不声称 planning H1。阈值、coverage 与 fallback 只在 calibration/validation 冻结。NRI 同标签持平则删除 JEPA 贡献。

## 风险与里程碑

完整轨迹 association 可能成为部署不可达 oracle，因此主监督只用 current/past teacher并对低置信事件 abstain。compound view 始终可逆且不删除 node identity。两周完成 typed ontology/extractor/legality 单测和 candidate-conditioned operator；两月完成 causal-teacher gap、JEPA planning/真机。负结果产出 contact topology benchmark 与固定 slot 边界。

## 证据

[OA-WAM 2605.06481](https://arxiv.org/abs/2605.06481)、[POT-VLA 2607.18016](https://arxiv.org/abs/2607.18016)、[ContactWorld 2606.13877](https://arxiv.org/abs/2606.13877)、[ViTacWorld 2607.22530](https://arxiv.org/abs/2607.22530)、[TouchWorld 2607.07287](https://arxiv.org/abs/2607.07287)、[StageWAM 2608.10780](https://arxiv.org/abs/2608.10780)、[Interaction Networks 1612.00222](https://arxiv.org/abs/1612.00222)、[Neural Relational Inference 1802.04687](https://arxiv.org/abs/1802.04687)、[C-SWM 1911.12247](https://arxiv.org/abs/1911.12247)。
