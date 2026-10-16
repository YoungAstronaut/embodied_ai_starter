# WAM-P1：长遮挡下的校准对象身份 Belief-WAM

- Proposal-ID: WAM-P1
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: 主表加入orbit构造/support size/certification failure与null/uniform proper-score rows；摘要固定simulator-certified，避免现实对称证明误读。

## 问题与可观察失败

OA-WAM 已有固定 identity address，POT-VLA/3D-ALP 已有 persistent 3D tokens/anchors；“再加对象记忆”已无新意。真正未解决的是完全遮挡、手内转移、相似实例交叉后，系统不知道哪个 identity hypothesis 正确，却仍以单一 slot 自信行动。可观察失败：两只外观相同物体在遮挡区交换或仅一只被操作，重现后 slot identity switch；语言仍指向原对象，但动作抓错实例。

H1：显式维持 `p(referent=physical-object, pose, contact-owner | history)` 的多假设 belief，并用预测—观测证据更新，比固定地址/最近邻 tracker 更能在**可辨识**遮挡中降低错误重关联；在部分/完全不可辨识条件中价值是给出 calibrated ambiguity 与边缘化动作，而不是猜中 ID。belief estimation gain 与 uncertainty-aware control gain 分开报告，不声称二者已构成可识别中介。

## 最近邻差异

- OA-WAM：地址在 t=0 固定、content 每帧更新，条件于 SAM tracking 正确；本方案允许关联不确定、假设分裂/合并和重现后后验更新。
- POT-VLA/3D-ALP：强调 persistent token/world anchor；本方案的主变量是身份分布及其 calibration，不以持久 token 存在为贡献。
- WAM4D：承认遮挡 identity inconsistency；本方案部署时保留低维 belief，而非训练期 depth register。

| 最近邻 | identity 状态 | 遮挡 association | 不确定性 | 部署控制 |
|---|---|---|---|---|
| OA-WAM v1 | t=0由language label+initial DINO计算32d address并逐层reset；content/pose逐帧SAM3+DINO更新 | SAM3 concept tracking；正确上游slot为条件，不维护association posterior | address本身固定，无多假设校准 | 同forward预测next slot+16-step action；有slot-swap test，未报告长遮挡posterior |
| POT-VLA v1 | role-indexed RGB-D 3D records，chunk后refresh，含visibility/confidence/relations | 角色slot在遮挡时保留，低置信触发re-observation | 记录confidence但非多实例referent posterior | tokens进GR00T action head，predicate verifier复用；无learned dynamics |
| 3D-ALP v1 | persistent camera SE(3) anchor+MCTS subtree/reference latent | FK更新anchor，保存last-known tree value | 非对象identity posterior | test-time world-model MCTS；主要解决离开视野的spatial memory |
| JPDA/多目标 Bayesian tracking | track posterior/联合关联 | 显式 likelihood+motion prior | proper posterior | 通常不学 action-conditioned visual WAM |
| JRDB/RALO tracking | long-occlusion/ID-switch 视觉 tracking | 视觉/激光遮挡恢复 | tracking metrics | 提供非机器人操控的强视觉参照；本方案必须额外证明语言 referent、contact-owner 与 control gain |
| MHT | association-hypothesis tree | measurement+motion likelihood | 多假设/剪枝 | 无language/contact-conditioned manipulation objective |
| SCALOR/SAVi等probabilistic slots | sequential object slots | learned visual dynamics/occlusion | latent slot uncertainty依实现 | 非referent-grounded control主终点 |
| ReferFormer等language video tracking | language-grounded mask/track | video-language association | 通常point estimate | 不用robot action/contact likelihood，不边缘化到control |
| 本方案 | **语言 referent 对物理对象的 posterior** | action/contact-conditioned causal update | calibrated multi-hypothesis+unknown mass | passive policy 对 posterior 边缘化；active sensing 另文/扩展 |

上述 OA/POT/3D-ALP 字段来自 2026-08-30 官方正文；OA/POT 代码/权重在本地未验证，任何无法复现项标为“正文重实现”，不把复现差距算胜利。

若 OA/POT 在 identity-swap benchmark 上通过简单多模板匹配达到同等 NLL/success，本 Proposal 失效。

## 方法

每个语言指代对象维护 `M=N_visible+1≤4` 个**referent candidates**（最多 3 个物理实例，加一项 unknown/none），而非枚举三实例的 6 个联合排列：`b_t^m=(w_t^m,anchor_m,μ_t^m,Σ_t^m,c_t^m,z_t^m)`。当对象数>3时报告 top-M+residual mass，并以 M=8 作覆盖消融。

显式建模 referent `R∈Ω` 与全体track-detection assignment `Z`。对 `R=m`：`\tilde p(R=m,Z=z,D)=w_m^- ψ(z) L_ref(D,z|x_m^-,a,c)∏_{r≠m}L_bg(D,z|x_r^-)`，其中ref/background各measurement likelihood只出现一次，`ψ`含one-to-one、miss、false factors；unknown/residual也各有独立prior和likelihood。联合归一 `p(R,Z|D)=\tilde p/Σ_{r,z}\tilde p(r,z,D)`，最终 `w_m^+=Σ_z p(R=m,Z=z|D)`。因此prior只随R乘一次，不是每assignment的常数，且绝不从association row sum定义身份posterior。

非均匀单测：`w^-=(0.8,0.2)`、单证据likelihood `(0.1,0.9)`、相同assignment factor时，posterior=`(0.08,0.18)/0.26=(0.3077,0.6923)`，向可辨识候选2移动；likelihood都0.5时posterior保持0.8/0.2。短时miss给每个R乘各自`p_miss`并保留身份质量；`unknown`是另一个R假设，不能由miss自动替换。exact枚举同时验证联合和为1与上述posterior值。

**置换不变锚定与指标。** 部署 anchor 只由遮挡前 detector+language grounding 初始化；evaluator 另用 GT trajectory Hungarian 冻结映射，GT schema 被 model loader 拒绝。事件空间 `Ω={M candidate identities,unknown/none,residual}`；同物体多个 components 的概率先求和，**miss 只是当前 measurement assignment，不改变 R 的 identity class**；仅确实无已知 referent 时 oracle 才是 unknown/none，top-M 外已知身份质量进入 residual，false detection 不成为 referent class。log score `-log p(y)`、Brier 在 Ω 上计算。partial/symmetric 档对 evaluator 给定的可交换 orbit `O` 用 orbit mass `p(O)=Σ_{m∈O}p(m)` 与 orbit 内 uniform target 计算 permutation-invariant log score；symmetric 档另报 entropy `log|O|` 与 excess NLL。coverage set 按 posterior mass≥0.9 构造。

benchmark 分三档：`identifiable`、`partially identifiable`、`simulator-certified ε-symmetric`。certification字段由 simulator完整state在**评测器离线**按有限rerender与数值容差检查；它不是解析证明。字段写独立 `eval_metadata` shard，只被metric loader读取，禁止进入student/controller。对称档只用NLL/Brier/coverage；任何“猜中”claim判错。

| 变量/token | 训练 student/action 可见 | target/teacher 可见 | 部署 action 可见 | 梯度/代价 |
|---|---:|---:|---:|---|
| 当前/过去 RGB、语言、proprio、已执行动作 | 是 | 是 | 是 | causal cache；10Hz |
| 当前检测/深度估计 | 是 | 是 | 是 | 可部署 detector/GFM |
| 完整轨迹 identity、未来重现关联 | 否 | 是 | 否 | stop-gradient target |
| belief hypotheses/weights/unknown mass | 是 | — | 是 | 单 referent 低维 M≤4；>3实例报告 residual |
| 成功/终止标签 | 否 | 可评估 | 否 | 不进 action query |
| identifiability proof/stratum | 否 | evaluator-only metadata | 否 | 独立shard；train loader schema拒绝 |

故意泄漏阳性对照把未来 association 输入 student，预期 ID 指标异常接近 oracle；正式模型必须回到 causal 结果。另做 history shuffle、identity swap 与只换背景的反向干预。

## 数据、实验与资源

新建 Occlusion-ID：RoboTwin exact-reset 12 tasks，2/3 个同类实例，遮挡 0.5–5s、交叉、手间 transfer、容器进出；50k episode。生成器显式输出 identifiable/partial/symmetric 证明字段与每档占比。训练/测试对象纹理与 episode ID 独立，语言描述平衡。MVP 2×A100、3 天；完整 8×A100、8 天。真机 4 tasks×100 paired trials，外观相同杯/方块，固定轨迹模板保证可重复。

强基线：OA-WAM、POT tokens、3D-ALP、MHT、SCALOR/SAVi slot、ReferFormer-style language tracker、JPDA ladder、SAM tracker、Kalman+Hungarian、单假设WAM、oracle/random；同 backbone/data/slot/action head/NFE、同一离线轨迹与 evaluator。最强 deployable comparator 按下述 L00–L11/adapter validation winner 冻结。**唯一 primary** 为遮挡≥2s 的 identifiable 与 partial strata permutation-invariant log score，预注册 macro 权重 `0.5/0.5`；symmetric excess NLL、switch/ECE/coverage 和 passive success 为 secondary。

消融：M=1/2/4/8、association likelihood vs dynamics prior、无 contact owner、无 pose covariance、无 calibration、filter vs transformer belief、只 persistent token、active-look、身份/背景反向 swap、未来关联泄漏阳性对照。

### R6 JPDA 近同构 ladder、复现与资源合同

| baseline-native | evidence/decision | adapter version |
|---|---|---|
| JPDA-native | visual-motion likelihood + MAP或原生 posterior output | 加同 WAM/language anchor，但保持原 likelihood |
| OA/POT/3D-ALP native | 原论文 persistent token/association | 另加同 posterior-marginal controller；代码不可得时冻结正文公式 |

| label/input-equal ladder | evidence | decision |
|---|---|---|
| L00/L01 | visual-motion | MAP / posterior-marginal |
| L10/L11 | visual+action/contact | MAP / posterior-marginal |

L11 是最危险近同构 comparator；主 2×2 即 evidence `{visual-motion,+action/contact}`×decision `{MAP,posterior-marginal}`。四格共享 M、unknown/residual/pruning、WAM、candidate/controller calls、likelihood family、latent dim与参数±5%；filter/transformer 仅在同 likelihood/capacity 下另比。validation 以 primary macro log score 冻结 L00–L11/OA-adapter winner，native winner另报，test不重选；success上同时估主效应/交互。

资源公式为 `N_episode×T_frame×[1 detector forward + min(H_raw,B=64) assignment hypotheses + 1 WAM forward]`；冻结 max detections=16、tracks=8、referent M=4、beam=64，超限质量进residual，并实测peak RAM/VRAM。symmetric proof：从sim state枚举同类候选置换（上限4!），每个置换用8 rerender seeds比较历史pixel/percept likelihood与action-conditioned transition，容差在train-only数值噪声99%分位冻结；code为 `proof_ok_sym/proof_ok_partial/proof_ok_ident/proof_render_fail/proof_tol_fail/proof_cap`。split按 asset identity+task template+occlusion trajectory+history-policy family group hash；真机model RGB必须裁掉AprilTag，GT视频单独保存，同步误差逐trial记录。**截至r07 actual=0**，strata/proof-computable率未知。

### R8 支持域、logger 与安全边界

- **唯一主命题：** Occlusion-ID benchmark 上 calibrated referent posterior 的 proper score 优于近同构 JPDA；control只secondary。**不声称**pseudoposterior识别不可观察的真实identity或严格证明现实对称。
- 全文 `provably symmetric` 改称 `simulator-certified ε-symmetric`；扫train-frozen ε的0.5×/1×/2×并发布proof failure atlas。instance OOD为train 2/3、test 4–6；M=4外质量必须进入residual，报residual calibration、support/fallback与conditional success。
- 真机以root trajectory×object set为block随机顺序；tag/overhead GT不进model camera，报detector recall strata与同步误差。所有方法共享workspace/collision/force guard与wrong-object abort；fallback-only/oracle detection单列。安全层或fallback解释>50%增益则删除control claim，标题降为 **Occlusion-ID: Calibrated Referent Tracking Benchmark**。

### R9 论文合同与审稿攻击

- 标题：**Occlusion-ID: Calibrated Referent Beliefs under Long Occlusion**。primary为proper score；not-claim为不猜不可观察identity。最危险基线L11=action/contact JPDA+posterior marginal，主表第一行。
- 不可删除对象是identifiable/partial/simulator-certified ε-symmetric三strata、orbit-mass proper score、proof-failure与2/3→4–6 support协议；JRDB/JPDA无语言referent/contact-owner和对称正确评分合同。
- 攻击：只是JPDA+WAM→承认且用L11判方法；identity不可见→proper scoring即对象；sim自证→ε/rerender atlas+真实tracking分开。L11持平→删novel update留benchmark；control<3pp→删control；real失败→sim benchmark。降级标题同上但摘要纯benchmark。

### R10 certification 与proper-score主表

主表每stratum列 orbit构造规则、orbit support `|O|`、certification attempted/success/failure codes、null predictor与uniform-on-orbit predictor的NLL/Brier、各方法excess score。摘要固定使用 **simulator-certified ε-symmetric**；证书失败样本不得重标identifiable，单列failure atlas。

## 判负

primary 相对 `JPDA+same WAM+language anchor` 的 macro log score 改善≥10%且 task-stratified episode-cluster bootstrap 95% CI 不跨0；pilot 按 10% NLL 改善、α=.05、power=.8 冻结每 task episodes。identifiable switch 降≥30%、ECE≤0.08、passive success 提升≥6pp，symmetric excess NLL≤0.1 为 secondary。若 score 达标但 passive success 增益<3pp，结论降级为 belief calibration，不声称控制收益；若 learned action/contact likelihood删除后差≤2%，则降级为经典 tracker+WAM。belief 置乱须损失≥5pp；只 probe 提升或 oracle 上界<3pp 判负；active-look 才有效则降级主动感知。

## 风险与里程碑

检测漏检可能主导结果，按 detector recall 分层并报告 oracle detection。完全对称不是算法错误而是可辨识性边界。多假设计算用 referent-only M≤4+unknown mass；真机身份 GT 用 AprilTag 仅评测不输入。两周完成三档 benchmark、冻结匹配 evaluator 与 filter；两月完成 WAM、真机、passive/active 分解与 calibration。负结果仍产出 identity-swap benchmark 和 persistent token 的失效边界。

## 证据

[OA-WAM 2605.06481](https://arxiv.org/abs/2605.06481)、[POT-VLA 2607.18016](https://arxiv.org/abs/2607.18016)、[3D-ALP 2604.11302](https://arxiv.org/abs/2604.11302)、[WAM4D 2606.14048](https://arxiv.org/abs/2606.14048)、[JPDA DOI](https://doi.org/10.1109/TAC.1983.1103234)、[MHT DOI](https://doi.org/10.1109/TAC.1979.1102177)、[JRDB 1910.11792](https://arxiv.org/abs/1910.11792)、[SCALOR 1910.02384](https://arxiv.org/abs/1910.02384)、[ReferFormer 2201.00487](https://arxiv.org/abs/2201.00487)。
