# 独立文献与创新边界审计（Reviewer Audit）

> 审计角色：独立 Proposal 评审，不参与主 Proposal 写作。  
> 检索截止：2026-08-30（Asia/Shanghai）。  
> 版本：audit-v1，后续至少在 round_02 与 round_10 刷新。  
> 结论用途：确定最近邻、冲突边界、强基线与证伪条件；本文不构成任何 Proposal 的 PASS。

## 1. 审计方法与证据等级

本审计先逐篇核对 starter pack 的本地 PDF 正文与版本，再以 arXiv 摘要/HTML、作者项目页和作者明确链接的代码仓库补检 2026 年新工作。检索刻意围绕“机制”而非只围绕任务名称展开，例如：训练期几何蒸馏是否在部署期移除、跨遮挡对象身份是否有持久地址、想象是否由风险或现实一致性触发、流策略是否支持异步前缀冻结、JEPA 潜变量是否只表达动作可辨识的等价类等。

证据等级：

- **A：正文级直接证据**。已读方法、信息路径、实验/消融或附录，且版本可定位。
- **B：官方摘要/项目页级证据**。可确认核心 claim，但未把所有实现细节或附录逐项复核；评审时不得把摘要 claim 当作已复现结论。
- **C：待核查信号**。标题/摘要高度相关，但代码、数据、协议或关键定义尚未独立确认，只能作为风险提示，不能单独判 Proposal 重复。

审计原则：

1. `future target at training` 不自动等于泄漏；关键是任何未来真值、目标编码、离线重建结果是否进入部署时的动作查询路径。
2. “加入几何/记忆/置信度/JEPA”不是创新点；必须说明变量、干预、失败模式与可证伪预测。
3. 与最近邻的差异必须在相同数据、参数、动作头、chunk、NFE/延迟预算下成立，不能靠更大预训练或额外传感器掩盖。
4. LIBERO 等饱和均值不能单独支撑机制 claim；必须包含机制定向压力测试、分轴 OOD 和真实机器人置信区间。
5. 代码仓库“存在”不等于可复现；仍需核查训练脚本、数据准备、权重、评测协议与许可证。

## 2. Starter pack 正文版本清单

以下 18 篇为本地 PDF 正文核对的锚点。版本号按 PDF 首页或 arXiv 标识记录；没有必要把所有锚点都当作 Proposal 的最近邻，实际最近邻以机制为准。

| 方向 | 论文 | 本地核对版本 | 证据 | 对评审的主要用途 |
|---|---|---:|---:|---|
| geometry-aware VLA | GEAR-VLA | arXiv:2606.08530v2, 2026-06-10 | A | 语义对齐 3D、embodiment canonicalization、粗到细注入 |
| geometry-aware VLA | Geometric Action Model (GAM) | arXiv:2606.17046v2, 2026-06-22 | A | GFM 主干、未来 feature/depth 目标、动作联合训练及算力规模 |
| geometry-aware VLA | GuidedVLA | arXiv:2605.12369v2, 2026-06-01 | A | object/spatial/temporal 因子化动作注意力 |
| geometry-aware VLA | Spatial Forcing | arXiv:2510.12276v2, 2025-10-17 | A | 3D 空间监督进入 VLA 的直接基线 |
| geometry-aware VLA | VGGT | arXiv:2503.11651v1 | A | 通用几何基础模型与 camera/register token |
| geometry-aware VLA | VGGT-Ω | arXiv:2605.15195v1 | A | 几何主干扩展与机器人相关能力边界 |
| geometry-aware VLA | Vision Transformers Need Registers | arXiv:2309.16588v2 | A | register token 的表示与伪影诊断 |
| 4D WAM | GEM-4D | arXiv:2605.22882v4, 2026-08-03 | A | 显式 4D rollout + inverse dynamics |
| 4D WAM | GeoSem-WAM | arXiv:2606.03188v1 | A | 训练期几何/语义辅助；部署期动作生成 |
| 4D WAM | WAM4D | arXiv:2606.14048v3, 2026-07-07 | A | spatial register、未来深度读出、训练期分支移除 |
| 4D WAM | X-WAM | arXiv:2604.26694v2 | A | 共享世界/动作联合生成，而非单纯辅助正则 |
| streaming | Diffusion Policy | arXiv:2303.04137v5 | A | chunking diffusion 基础基线 |
| streaming | IntentVLA | arXiv:2605.14712v2, 2026-07-11 | A | VGGT 历史 token、门控 cross-attention、AliasBench |
| streaming | Streaming Flow Policy | arXiv:2505.21851v2 | A | 以上一动作附近初始化、边去噪边执行 |
| JEPA | LeJEPA | arXiv:2511.08544v3 | A | JEPA 表示目标与坍塌/正则边界 |
| JEPA | V-JEPA | arXiv:2404.08471v1 | A | 视频潜变量预测基础 |
| JEPA | V-JEPA 2 | arXiv:2506.09985v1 | A | 1M 小时无动作视频预训、62 小时 DROID 动作条件预测、CEM 真机规划 |
| JEPA | V-JEPA 2.1 | arXiv:2603.14482v3 | A | dense prediction、deep self-supervision、多模态 tokenizer 与抓取提升 |

### 2.1 已从正文确认的三条关键边界

- **GAM 不是小规模几何辅助头**：其训练包含动作、未来 feature 与未来 depth 目标，主干来自几何基础模型；正文给出的预训练规模约 784K trajectories、64 GH200 约 96 小时，后训练 16 GH200 约 48 小时。因而任何“几何主干提升动作”的 Proposal 必须做同数据/同算力或明确的 scaling 分离。更重要的是，已预训练主干下去除 future-depth/future-feature 的某些消融变化很小，这使“辅助未来几何是因果来源”的 claim 必须用更尖锐干预验证。官方 [arXiv](https://arxiv.org/abs/2606.17046)、[项目页](https://cvlab-kaist.github.io/GAM/) 与 [代码仓库](https://github.com/cvlab-kaist/Geometric-Action-Model) 可交叉核查；审计日仓库仍把部分预训练数据代码列为待发布。
- **WAM 家族存在不同数据流，不可混称**：GeoSem-WAM/WAM4D 的 4D/几何分支主要作为训练期监督并可在部署移除；GEM-4D 是显式世界 rollout 后 inverse dynamics；X-WAM 是共享主干的世界/动作联合生成。Proposal 必须明确自己改的是训练表示、部署 rollout，还是动作生成耦合。
- **IntentVLA/V-JEPA 2 已覆盖很强的历史与潜变量基线**：IntentVLA 已用近期视觉历史与 VGGT token 处理视觉 alias；V-JEPA 2 已把冻结视频编码器、动作条件 latent predictor 与 CEM 真机规划连成闭环。仅替换 memory encoder 或把 JEPA 接到 planner 上不构成充分新意。

## 3. 2026-08-30 前新增最近邻与冲突性工作

### 3.1 几何感知 VLA

1. **VGA: Robotic Manipulation is Vision-to-Geometry Mapping**，arXiv:2604.12908v2（2026-08-12 更新），是几何主干 VLA 的直接冲突：以预训练 3D world model/VGGT 类主干、Progressive Volumetric Modulation 和动作/3D 联合预测形成 VLA。任何“把几何 backbone 注入 VLA”的朴素版本均不再新。审计证据：[arXiv](https://arxiv.org/abs/2604.12908)、[作者项目页](https://hcplab-sysu.github.io/VisionGeometryActionModel/)、[作者仓库](https://github.com/HCPLab-SYSU/VisionGeometryActionModel)。审计日仓库主要可见文档与 README，完整训练实现是否已经释放仍不确定，标为 **B/代码不确定**。
2. **See Like a Robot: Robot-Centric Pointmaps**，arXiv:2607.11498v1，以机器人坐标系 XYZ pointmap 加额外 encoder/fusion 提升相机变化泛化，直接压缩“robot-centric geometry”创新空间。证据：[arXiv](https://arxiv.org/abs/2607.11498)、[作者项目页](https://davian-robotics.github.io/pointmap/)，**B**。
3. **GEAR-VLA / GAM / Spatial Forcing / GuidedVLA** 已分别覆盖语义对齐 3D、几何基础模型主干、空间监督和动作因子化。新的任务相关几何必须回答：为何不是 attention 重加权、为何不是 teacher scaling、在哪类干扰几何上产生相反预测。
4. 接触相关直接相邻工作包括 **ViTacWorld**（arXiv:2607.22530）、**TouchWorld**（2607.07287）、**ContactWorld**（2606.13877）和 **Where to Touch, How to Contact**（2601.10930）。它们已覆盖视觉-触觉 rollout、层次触觉预测、接触基准/力场表示、接触意图接口。证据均为官方 arXiv，当前为 **B**： [ViTacWorld](https://arxiv.org/abs/2607.22530)、[TouchWorld](https://arxiv.org/abs/2607.07287)、[ContactWorld](https://arxiv.org/abs/2606.13877)、[Where to Touch, How to Contact](https://arxiv.org/abs/2601.10930)。因此 GEO-P2 不能只把接触/力作为额外预测头。
5. 尚未发现完全等价于“任务条件、失效类型可校准、可拒绝的几何置信度路由器”的明确直接邻居，但这是暂时性检索结论而非新颖性证明。GEO-P3 必须与 teacher confidence、深度/位姿 ensemble、reprojection residual、OOD detector 和 oracle router 比较。
6. 补检后确认 **ST-VLA**，arXiv:2603.13788v1，已经用 task-relevant 3D-4D spatial masks 作为语义推理到连续控制的接口；它使“语言/任务选择相关几何区域”本身不再足够。证据：[arXiv](https://arxiv.org/abs/2603.13788)，**B**。
7. **Confidence Calibration in Vision-Language-Action Models**，arXiv:2507.17383v2，已经建立 VLA 成功置信度、prompt ensembles 和 action-wise Platt scaling；**UAOR**，2602.18020v2，已经用 action entropy 触发 observation reinjection。证据：[VLA calibration](https://arxiv.org/abs/2507.17383)、[UAOR](https://arxiv.org/abs/2602.18020)，**B**。GEO-P3 只有把置信度限定到“几何证据的错误类型与动作后果”、并显示总体 VLA confidence/action entropy 不能替代，才可能保留创新性。
8. **CofactVLA**，arXiv:2608.04396v1，已将 VLA 的视觉捷径形式化为 counterfactual deconfounding，并同时在 action velocity field 与 feature covariance 层干预；它虽针对 language-vs-vision confounding、不是几何关系选择，但已使“反事实干预去视觉捷径”不再新。证据：[arXiv](https://arxiv.org/abs/2608.04396)，**A/B**。GEO-P1 必须把差异落在 geometry-SCM 下的 relation-level intervention 与动作充分集，而不能把 counterfactual/deconfounding 作为贡献本身。
9. **ContactGuard**，arXiv:2608.13438v1，已在 planned action chunk 条件下预测短时 post-contact latent 并做 pre-contact abort，且报告真实机器人部署。证据：[arXiv](https://arxiv.org/abs/2608.13438)，**B**。GEO-P2 的 candidate-action-conditioned contact predictor 因而不是独占新意；必须证明显式 event time/mode/normal topology field 相对 latent failure probe 的新增因果诊断与 candidate ranking 收益。

### 3.2 4D World-Action Model

1. **MECo-WAM: Learning 4D Geometric Priors for Inference-Efficient WAMs**，arXiv:2607.05468v1，几乎正面覆盖“训练期 4D 几何、部署期移除”：video/action/4D experts，冻结 VGGT 关系目标，非对称可见性与衰减 4D read mask，4D 组件部署时移除。所有仅主张“用训练期 4D 几何提升 WAM 且不加推理开销”的方案都应视为直接重复风险。证据：[arXiv](https://arxiv.org/abs/2607.05468)，**B**；审计日未独立定位到完整官方实现，代码状态不确定。
2. **OA-WAM**，arXiv:2605.06481v1，以对象/机器人 slots、持久地址和动态内容、block-causal 未来 slot/action 建模覆盖了遮挡身份记忆的核心设计空间，并包含 slot-swap 类因果测试。证据：[arXiv](https://arxiv.org/abs/2605.06481)，**B**。WAM-P1 若只是 persistent object slots，应判 fatal novelty flaw。
3. **POT-VLA: Persistent 3D Object Tokens**，arXiv:2607.18016，以及 **3D-ALP**，arXiv:2604.11302，进一步覆盖跨遮挡/接触的 3D 对象持续性和世界坐标锚点。证据：[POT-VLA](https://arxiv.org/abs/2607.18016)、[3D-ALP](https://arxiv.org/abs/2604.11302)，**B**。
4. **When to Trust Imagination**，arXiv:2605.06222v2，以 predicted-vs-real consistency 自适应选择执行长度并报告减少 WAM forward passes；**HarmoWAM**，2605.10942v1，以 predictive/reactive experts 和过程自适应 gating 分配模式。二者直接压缩“按需想象/自适应算力”的空间。证据：[When to Trust Imagination](https://arxiv.org/abs/2605.06222)、[HarmoWAM](https://arxiv.org/abs/2605.10942)，**B**。
5. **CheckVLA**，arXiv:2607.26789v1，以冻结 action-conditioned world model、conformal 风险、suffix rewrite 和 latency-aware hard prefix 组合验证/修正动作，是 WAM-P2、STR-P2、JEP-P3 的跨方向直接碰撞。证据：[arXiv](https://arxiv.org/abs/2607.26789)，**B**。
6. **Robot-Factored World Models**，arXiv:2607.22535v1，把动作经控制器/运动学展开为部署可得 nominal trajectory，显式区分部署可观测信息与未来真值，对 WAM-P3 的“动作可辨识状态”尤为关键。证据：[arXiv](https://arxiv.org/abs/2607.22535)，**B**。
7. **τ0-WM**，arXiv:2606.01027v2，覆盖大规模 shared video/action backbone、action-conditioned simulator、候选动作重排序/修复；**World Action Planner**，2607.27599v1，覆盖以 world model 搜索/优化动作。它们要求任何 deployment-time rollout Proposal 不能只与纯 reactive VLA 比。证据：[τ0-WM](https://arxiv.org/abs/2606.01027)、[World Action Planner](https://arxiv.org/abs/2607.27599)，**B**。
8. 潜状态桥接的近期工作 **LaWAM**（2606.15768）、**LiLa-WAM**（2608.03701v1）、**DELE-w0.5: Inferring Action from Future Latent State**（2608.22067v3）已覆盖 compact future latent/action bridge，后者还报告真实机器人试验。证据：[LaWAM](https://arxiv.org/abs/2606.15768)、[LiLa-WAM](https://arxiv.org/abs/2608.03701)、[DELE-w0.5](https://arxiv.org/abs/2608.22067)，**B**。WAM-P3 不得仅提出“用 future latent 帮助 action”。
9. **CoCo: Overcoming Statistical Bias in Action-Controllable World Models**，arXiv:2608.04653v1，已对 inverse-action、zero-action、镜像场景/变换动作施加反事实一致性，并提出 action controllability 指标与 same-state multi-action 评测。证据：[arXiv](https://arxiv.org/abs/2608.04653)，**B**。若 WAM-P3 仍以“反事实动作响应/动作可辨识 future state”为核心，将存在 fatal novelty collision；可以转向部署可观测 residual 下的隐式物性 belief，但必须控制 action realization。
10. 机器人 WAM 之外还有两个不能忽略的机制基线：**JRDB**（arXiv:1910.11792）明确把长遮挡与 ID switch 联系，并给出 long-occlusion re-identification baseline；**PonderNet**（2107.05407）已把 adaptive computation/learned halting 作为一般机制。证据：[JRDB](https://arxiv.org/abs/1910.11792)、[PonderNet](https://arxiv.org/abs/2107.05407)，**B**。WAM-P1 的新意不能只来自“比 tracker 多一个 belief”，WAM-P2 也不能只来自 learned stopping；差异分别要落在 manipulation identity uncertainty 的决策后果和 paired decision-value target。

### 3.3 流式策略与意图

1. **RTC: Real-Time Execution of Action Chunking Flow Policies**，arXiv:2506.07339v2（NeurIPS 2025），以异步生成下一 chunk、冻结必然执行前缀并 inpaint 其余部分处理真实延迟。证据：[arXiv](https://arxiv.org/abs/2506.07339)，本地相邻材料之外的 **B**。所有 deadline/anytime 控制必须把 RTC 当强直接基线。
2. **REMAC**，arXiv:2601.20130v1（ICLR 2026），以 masked action-chunk correction 和 prefix-preserved sampling 修复 chunk 内不一致且不增加额外延迟。证据：[arXiv](https://arxiv.org/abs/2601.20130)，**B**。
3. **PACE**，arXiv:2606.00537v2，以速度曲线 phase transition 无训练地选择执行 horizon；**DEHP**，2606.11408v2，以冻结 chunk policy 外的 RL horizon 分支学习动态执行长度。证据：[PACE](https://arxiv.org/abs/2606.00537)、[DEHP](https://arxiv.org/abs/2606.11408)，**B**。STR-P2 必须超越动态 horizon 本身。
4. **Remember Smarter**，arXiv:2608.15269v1，以时空压缩与 experience memory 注入 VLA，是“更强历史编码器”的直接相邻。证据：[arXiv](https://arxiv.org/abs/2608.15269)，**B**。
5. IntentVLA 已定义视觉 alias 与历史融合。STR-P1 若只是 event token/门控 reset，需证明 reset 事件是可观测、低延迟、对错误历史产生方向性因果作用；STR-P3 若只是历史对比学习，需升级为**当前帧相同、历史不同、最优动作不同**的配对反事实协议，并排除 language/task-ID 泄漏。

### 3.4 JEPA / 潜变量世界模型

1. **VLA-JEPA**，arXiv:2602.10098v2，已强调 leakage-free state prediction：target 可看未来，student/action query 只看当前，且考察 nuisance/camera 鲁棒性。证据：[arXiv](https://arxiv.org/abs/2602.10098)，**B**。JEP-P1 必须精确画出信息路径并证明 action equivalence，而非再做普通 future latent prediction。
2. **FF-JEPA**，arXiv:2606.09311v1，把 action-conditioned forward model 与 action-free latent planner 组合，当前证据仍偏初步。证据：[arXiv](https://arxiv.org/abs/2606.09311)，**B**。
3. **StageWAM**，arXiv:2608.10780v3，把 WAM 与冻结 V-JEPA 2 的 current-state/next-stage latent 连接，直接压缩“JEPA 表示 + WAM”的空间。证据：[arXiv](https://arxiv.org/abs/2608.10780)，**B**。
4. **What Matters for Latent Actions?**，arXiv:2608.19613v1，系统比较大量 latent-action 设计选择并指出 proxy 指标与下游控制可能不一致，应作为 JEP-P1 的诊断性基线/设计审计。证据：[arXiv](https://arxiv.org/abs/2608.19613)，**B**。
5. JEP-P2 与 OA-WAM、POT-VLA、ViTacWorld/ContactWorld 重叠；JEP-P3 与 CheckVLA 的 conformal 风险干预重叠。分别需要在“接触导致的对象身份/拓扑变化”与“潜 rollout 误差的校准风险如何改变动作选择”上形成更窄、更可证伪的机制。
6. **What Drives Success in Physical Planning with Joint-Embedding Predictive World Models?**，arXiv:2512.24497v3/TMLR，已系统比较 JEPA-WM 的模型架构、目标与 planner，并公开代码、数据和 checkpoint；它应作为 JEPA planner 设计的最低系统基线，而不是只引用 V-JEPA 2。证据：[arXiv](https://arxiv.org/abs/2512.24497)、[官方仓库](https://github.com/facebookresearch/jepa-wms)，**B**。
7. **Calibrated Predictive Safety for Heterogeneous Robots**，arXiv:2608.17496v1，已明确提出 action-conditioned JEPA 候选 rollout、risk/progress heads、校准不确定性、候选排序、deterministic embodiment shield 与 fallback ladder。其 arXiv 页面同时诚实披露当前仅有 LIBERO-Long 仿真、无真机和部分显著性检验未执行。证据：[arXiv](https://arxiv.org/abs/2608.17496)，**B**。因此原始的“JEPA 风险校准规划”种子应视为**直接重复并否决**；除非 JEP-P3 改写为该工作没有解决的可证伪问题，例如外生动态导致的多模态未来及其 planner regret，而不能继续把 risk head、calibration 或 shield 当贡献。
8. **Learning Action-based Representations Using Invariance**（Action-Bisimulation），arXiv:2403.16369，已经以 bisimulation-inspired pseudometric 表达多步 controllability；它是 JEP-P1 的直接理论邻域。证据：[arXiv](https://arxiv.org/abs/2403.16369)，**B**。若 JEP-P1 采用阈值邻接，不得把通常不传递的关系称作 equivalence class；应说明相对于 action-bisimulation metric 新增的是同状态 action-effect geometry、局部 planner regret，还是合法 quotient 构造。
9. **Disentangling Controllable and Uncontrollable Factors of Variation by Interacting with the World**，arXiv:1804.06955，早已训练 controllable/uncontrollable 两套表示；其证据限于简单模拟并依赖近似独立对象。证据：[arXiv](https://arxiv.org/abs/1804.06955)，**A/B**。这既是 JEP-P3 的同名先驱，也是关键反例：在 manipulation 中 action 与 exogenous dynamics 通常交互，新的贡献必须显式建模 action main effect、exogenous main effect 与 interaction，不能只复刻两个 latent 的独立约束。

## 4. 十二个 Proposal 的碰撞矩阵与最低差异化条件

| ID | 当前最危险最近邻 | 不能接受的朴素版本 | round_01 起最低差异化证据 |
|---|---|---|---|
| GEO-P1 | VGA、GAM、GEAR-VLA、Spatial Forcing、ST-VLA | 几何 backbone/aux loss/attention 权重，或语言生成 task-relevant 3D mask 后直接接动作头 | 明确定义“任务相关几何”的干预变量；构造动作无关几何干扰与动作相关几何干扰；在冻结规模下显示只对后者敏感，并有错误几何反向/置换试验 |
| GEO-P2 | ContactWorld、ViTacWorld、TouchWorld、Where-to-Touch | 预测接触点/力/触觉再输入 policy | 以**接触前后可控转移**为对象：预注册可失败的 transition consistency；区分 free-space、pre-contact、stick/slip、post-contact；必须有无触觉版本和 oracle contact 上界 |
| GEO-P3 | VLA confidence calibration、UAOR、GAM/VGA + 通用 uncertainty/OOD | 用总体 action entropy、深度置信度或 ensemble 选择是否启用几何 | 置信度须按几何失效类型校准且改变动作决策；证明总体 VLA confidence/UAOR 不能替代；报告 ECE/coverage-risk、selective success 与介入代价；含错误高置信几何、反光/遮挡/动态体和 oracle router |
| WAM-P1 | OA-WAM、POT-VLA、3D-ALP | persistent object slots/memory bank | 明确超过持久 slot：长遮挡后 belief update/re-identification、接触交换与身份切换；成对 identity-swap benchmark；报告 identity calibration 而非只看 success |
| WAM-P2 | When-to-Trust、HarmoWAM、CheckVLA、τ0-WM | 不确定时多 rollout、简单 gating/阈值 | 在固定 wall-clock/NFE 下学习“想象的价值”；区分何时想象、想象多少、何时停止；与 always/never/random/uncertainty/consistency gating 比；计算介入净收益与失败恢复 |
| WAM-P3 | CoCo、Robot-Factored WM、DELE、LaWAM、LiLa-WAM、X-WAM | future latent/action joint prediction，或一般 counterfactual action consistency | 若保留 action-identifiability 主题须超越 CoCo 的 same-state multi-action/zero/inverse action；更可信的转向是用部署可得 residual 识别隐式物性 belief，并控制 action realization、用触觉作 oracle 上界；始终排除 future-state leakage |
| STR-P1 | IntentVLA、Remember Smarter、REMAC | 事件触发清空 KV/memory | 事件必须能在线观测且优于固定窗口/学习遗忘门；明确 reset 对应的因果断点；评测 false reset、missed reset、恢复时间和相同视觉不同意图 |
| STR-P2 | RTC、PACE、DEHP、REMAC、CheckVLA | 动态 horizon、异步 chunk 或 deadline early-exit | 定义 deadline-conditioned objective 和 anytime validity；在真实感延迟抖动/控制频率下与 RTC/PACE/DEHP 公平比较；任何截止时刻输出都须安全可执行，报告 deadline miss 与控制抖动 |
| STR-P3 | IntentVLA、Remember Smarter | 历史 contrastive loss / 更长记忆 | 创建当前观测严格匹配、历史不同、最优动作不同的 counterfactual pairs；语言/task-ID 平衡；对历史交换/截断/伪历史做因果试验，证明不是静态场景线索 |
| JEP-P1 | VLA-JEPA、V-JEPA 2、DELE、latent-action study | 用 JEPA latent 预测 action | 以局部动作等价类为显式对象：定义局部扰动半径、同效动作判据与跨 embodiment 边界；证明 latent 内类不敏感、类间可分且下游控制收益一致 |
| JEP-P2 | OA-WAM、POT-VLA、ContactWorld、ViTacWorld | object slots + contact token + JEPA loss | 接触事件驱动 slot 的出生/合并/分裂/归属更新；跨遮挡持久性与接触拓扑变化同时测试；与无 contact、无 persistence、普通 tracker 和 oracle association 比 |
| JEP-P3 | JEPA Safety、CheckVLA、JEPA-WM study、V-JEPA 2/2.1 | JEPA candidate rollout + risk/progress head + calibration/shield，或普通 rollout ensemble | 原“风险校准规划”种子已被 JEPA Safety 直接覆盖，必须换核心问题；若转向外生动态的多模态未来，应以 action ranking regret/模式覆盖为对象，与 deterministic mean、ensemble、JEPA Safety 式 risk head 和 oracle modes 比，并明确不声称安全保证 |

## 5. 强制信息路径与泄漏审计

每份 Proposal 必须包含一张按阶段分开的 token/变量表；缺失时 D6 不得高于 3.0，出现部署时未来真值则为 fatal：

| 变量 | 训练 student/action query 可见？ | 训练 target/teacher 可见？ | 部署动作 query 可见？ | 梯度路径/stop-grad | 获得代价 |
|---|---:|---:|---:|---|---|
| 当前 RGB/深度/触觉/本体状态 | 必填 | 必填 | 必填 | 必填 | 传感器与频率 |
| 历史窗口/持久状态 | 必填 | 必填 | 必填 | 必填 | 内存与更新延迟 |
| 动作前缀/nominal trajectory | 必填 | 必填 | 必填 | 必填 | 必须证明部署可得 |
| 未来图像/深度/位姿/接触 | 必填 | 可作 target | 必须为否，除非由模型预测 | 必填 | 离线标注/重建 |
| 离线 SLAM/全轨迹重建/未来关联 ID | 必填 | 可作 teacher，但要说明 | 通常必须为否 | 必填 | 额外工具与失败率 |
| 任务 ID/语言/终止信号 | 必填 | 必填 | 必填 | 必填 | 防止标签捷径 |

强制攻击：

- 目标编码器权重共享时，检查 attention mask、缓存和 normalization 是否间接混入未来 token。
- 历史成对数据必须平衡语言、初始位姿、对象纹理和 episode ID，防止“反事实历史”被静态元数据识别。
- 几何 teacher 的离线重建若利用完整轨迹，必须与只用当前/过去帧的 teacher 做隔离比较。
- 接触/成功/终止标签若在动作发生后才可得，不得在同一步部署 action query 中出现。
- 真实机器人 nominal trajectory 必须来自实际可部署的控制器/运动学，不得用执行后的真实状态回填。

## 6. 最低基线、消融与证伪协议

所有 Proposal 共用以下底线，具体 round 会继续加严：

1. **同预算 base**：相同数据、预训练权重、参数/可训练参数、动作头、action chunk、优化步数；若无法完全相同，必须做 scaling curve 或明确限定 claim。
2. **简单控制**：参数量匹配 MLP/Transformer、随机 gate、固定窗口/固定 horizon、普通 ensemble/残差、通用 tracker 等，以排除容量收益。
3. **最近邻复现/强替代**：优先运行官方代码；若代码缺失，需实现最接近的机制替代并把差异写清，不能只引用论文数字。
4. **oracle 上界与反向干预**：oracle geometry/contact/identity/trigger/risk 与故意错误、置换、延迟的对应反向干预必须成对出现。
5. **分轴 OOD**：至少按相机、几何、对象、动力学/接触、语言或历史 alias 中与 claim 对应的轴拆分；不得只报告混合 OOD 均值。
6. **真实机器人**：给出每任务 trial 数、随机化/重置协议、失败定义、paired seed 或合理分层，以及置信区间；演示视频不是统计证据。
7. **算力/延迟**：训练 GPU 型号与时长、部署参数/FLOPs、NFE、峰值显存、传感到动作延迟、控制频率、WAM 介入率必须报告。
8. **统计与预注册式预测**：明确核心指标、最小有意义效应、置信区间/重复次数以及“若 X 不成立则机制 claim 被否定”的条件。

推荐统一报告的 mechanism metrics：

- 几何：task-relevant vs irrelevant perturbation sensitivity、相机/位姿误差曲线、selective risk。
- 4D WAM：rollout/calibration error 随 horizon、介入净收益、身份切换率、未来信息剥离差值。
- streaming：deadline miss、闭环延迟、jerk、prefix inconsistency、意图切换恢复步数。
- JEPA：类内/类间 latent 距离、action ranking regret、risk-coverage、planner failure detection AUROC 及其任务代价。

## 7. 代码、数据与版本不确定性

- **GAM**：官方仓库可见训练/配置/脚本/测试与 checkpoint 线索，但审计日部分预训练数据代码仍为 TODO；不能把“仓库已开源”写成“完整可复现”。
- **VGA**：官方仓库在审计日主要可见项目文档/README；完整训练代码状态需在后续轮次重查。
- **MECo-WAM 与多篇 2026-07/08 新稿**：没有在本轮独立确认完整官方实现、权重和数据协议；均按 B 级处理。其摘要足以构成新颖性风险，但实验数字不作为已复现事实。
- **版本波动**：2607/2608 系列在 CVPR 截稿前高度可能新增版本、代码或改名。round_02 与 round_10 必须重新核对 arXiv version、项目页与仓库；若 Proposal 使用这些工作作对比，还需在实验冻结前再检查一次。
- **数据可得性**：若依赖大规模私有轨迹、离线未来几何/触觉标注或 64-GPU 级预训练，D7/D8 不会因为“理论上可训练”而通过；必须给出可在目标预算内验证核心机制的缩小版垂直切片。

## 8. 初始审计结论

当前最严重的创新碰撞是：

- 训练期 4D 几何且部署移除：WAM4D、GeoSem-WAM、**MECo-WAM** 已形成密集直接邻域。
- 几何 foundation backbone 到 VLA：GAM、GEAR-VLA、**VGA** 已覆盖朴素主线。
- 持久对象/遮挡身份：OA-WAM、POT-VLA、3D-ALP 已覆盖持久 slot/anchor。
- 按需想象/动态执行：When-to-Trust、HarmoWAM、CheckVLA、RTC、PACE、DEHP 已覆盖多种 gating/horizon/prefix 机制。
- JEPA latent 到 action/planning：VLA-JEPA、V-JEPA 2/2.1、StageWAM、DELE、FF-JEPA 已形成高密度邻域。
- JEPA 风险头/校准/候选排序/安全 shield：JEPA Safety 已覆盖原始 JEP-P3 种子，需直接换题；动作反事实一致性：CoCo 已覆盖原始 WAM-P3 的朴素版本。

因此，12 个 Proposal 都必须从“组件组合”收缩到**可观测失败模式 + 独特因果机制 + 明确反事实干预 + 同预算强基线**。round_01 不会根据标题或叙事给创新分；只有在 proposal 正文给出变量定义、信息路径、最近邻逐项差异和会推翻自己的实验时，D3/D6/D9 才可能达到硬门槛。

## 9. Round 10 版本刷新（2026-08-30）

本轮按官方 arXiv 页面、作者/官方仓库重新核对最容易改变最终创新边界的工作；没有只沿用主笔的 related-work 表。结果如下：

1. **VGA** `2604.12908` 已为 **v2（2026-08-12）**，并标注 ACM MM 2026；geometry-foundation backbone 直接接 VLA 的碰撞仍成立。官方 `HCPLab-SYSU/VisionGeometryActionModel` 仓库审计时仍主要可见 README/文档，未见与论文声称相称的完整训练源码树，因此“可按官方代码完整复现”仍不能确认。
2. **MECo-WAM** `2607.05468` 仍为 **v1（2026-07-06）**；训练期 4D expert、部署移除的直接碰撞未变化，完整官方实现仍未独立确认。
3. **CofactVLA** `2608.04396` 仍为 **v1（2026-08-05）**；counterfactual deconfounding 本身不能再作为 GEO-P1 的创新，最终边界必须落在独立 utility evaluator 下的 geometry-relation protocol。
4. **ContactGuard** `2608.13438` 仍为 **v1（2026-08-13）**；action-conditioned pre-contact latent/abort 与真机证据继续构成 GEO-P2 的最危险基线，typed event-time/mode/normal field 只能作为可证伪的新增对象。
5. **CoCo** `2608.04653` 仍为 **v1（2026-08-05）**；inverse/zero/mirror intervention 已覆盖一般 action controllability，WAM-P3/JEP-P3 不能退回一般反事实动作响应。
6. **Calibrated Predictive Safety for Heterogeneous Robots / JEPA Safety** `2608.17496` 仍为 **v1（2026-08-18）**；其 action-conditioned JEPA risk/progress、candidate ranking、shield/fallback 继续否决原始 JEP-P3 风险校准种子。官方页面仍披露证据限于 LIBERO-Long 仿真、无真机，因此也不能把它当真实机器人安全结论。
7. **Action-Bisimulation** `2403.16369` 当前为 **v3（2024-06-24）**；recursive multi-step controllability metric 的理论邻域未变化。JEP-P1 最终可保留的边界是 local 3D contact matched-outcome schema、canonical assignment strata 与 same-backbone recursive-vs-local target protocol，而不是 pseudometric 概念本身。
8. **GAM 官方仓库状态有实质改善**：当前可见 `configs/scripts/src/tests/checkpoints/eval` 等代码结构；但 README 的 To Do 仍保留 pretraining dataset code release，故从“partial release”更新为“主要代码可见、预训练数据流程仍不完整”，不能写成端到端完全复现。
9. **JEPA-WM study** 的官方 `facebookresearch/jepa-wms` 代码、数据/权重入口仍可见，继续作为 JEP 系列的最低系统基线。

本次刷新没有发现与 r09 四个窄协议（Geometry Counterfactual Ranking、LOFO Geometry Reliability Atlas、Occlusion-ID 分层 proper-score protocol、ActMetric-3D matched-outcome protocol）完全同构的新工作，因此它们的 D3 可以在严格限定 claim 后从 4.0 提至 4.5。该结论不是形式化新颖性证明：2026-07/08 新稿仍可能在截稿前增补版本、代码或实验，最终实验冻结时必须再次记录 arXiv version/commit；截止日后的工作属于未覆盖风险。
