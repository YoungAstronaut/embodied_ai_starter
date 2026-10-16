# JEP-P2 Refinement Log

## r00 / pre-review

- 评审要点：普通 object/contact slots 与 OA-WAM/POT/ContactWorld 直接碰撞。
- 决策：接受，主机制改为可逆 contact topology operations。
- 具体改动：区分 identity belief 与 topology，加入 graph edit、反向编辑、无拓扑任务特异性判据。
- 改后分数：待 round_01。
- 未决项：TouchWorld/ContactWorld 正文级代码状态待 round_02。

## round_01 / r01

- 评审要点：未来 graph operation 未条件化 candidate action；attach/detach 与 merge/split/transfer ontology 混乱；full-trajectory ID teacher 可能隐式解难；缺 action/edit 正交干预。
- 决策：全部接受；将 r00 operator 图判为 fatal 并替换，弃用互斥 `attach/detach/transfer/merge/split` CE。
- 具体改动：数据流改为 proposer→`G_t+a_i`→concurrent edit distribution→executor→JEPA/scorer；primitive 仅 typed edge Add/Del，compound 为 derived view，transfer 为原子多 edit transaction；新增 legality 和 extractor 伪代码；主 teacher 限 current/past association，full trajectory 只 oracle；加入 action×edit 2×2 和 NRI/Interaction Networks 基线。
- 改后分数：自评 D5 2.5→4.5、D6 4.0→4.5、D9 4.0→4.5；待 round_02。
- 未决项：ContactWorld/ViTacWorld 是否已有 attachment graph、并发 edit set decoder 的 event imbalance 与 causal teacher ID noise 待审。

## round_02 / r02

- 评审要点：graph dynamics+JEPA 组合风险高；endpoint `G0/GH` 会把 attach→detach transient 静默抵消；ContactWorld/ViTac/TouchWorld 正文字段与代码状态不足；缺 NRI+同标签对照。
- 决策：全部接受；图 predictor/JEPA 不列创新，主对象改为遮挡下 timestamped/partially ordered typed event transaction。
- 具体改动：加入 C-SWM/graph-world-model 邻域；primitive 升级为 `(τ,Add/Del,typed-edge,confidence)`，同 bin antichain+跨 bin partial order，标签按全过程抽取不再 endpoint diff；补三篇 contact/tactile WM 的正文字段/版本/代码状态；增加 action-conditioned NRI 与 non-JEPA C-SWM+完全同 event labels/loss；用 transient recall/timestamp MAE 和 JEPA tie 判负。
- 改后分数：自评 D3 3.5→4.5、D5 4.0→4.5、D6 维持4.5、D9 维持4.5；待 round_03。
- 未决项：偏序 event matching 的评价算法、长 transaction 暴露偏差和 causal association 对事件时间戳的偏置需深审。

## round_03 / r03

- 评审要点：每候选event target支持未闭合；联合梯度可编码action；partial-order matching无唯一算法。
- 决策：全部接受；主模型stop-gradient typed tensor且全候选exact-reset。
- 具体改动：snapshot×8×4×16/1.024M steps manifest；action-ID shortcut probe；±1-frame+typed-edge Hungarian、null FP/FN、transaction exact、abstain coverage与四类单测；NRI/C-SWM共享全部target/executor/scorer。
- 改后分数：自评 D4/D5/D13→4.5；待 round_04。
- 未决项：event quantization、autoregressive exposure bias与真实association timestamp噪声待审。

## round_04 / r04

- 评审要点：transaction ID任意置换；Bayes probe不可知；abstain抬高F1；fixed-action success混写。
- 决策：全部接受。
- 具体改动：pairwise co-membership transaction loss；predicted-vs-GT event经验probe；calibration-only 90% coverage/AURC/fixed-graph fallback；score vs selection/success分层。
- 改后分数：自评 D5/D13→4.5；待 round_05。
- 未决项：co-membership传递性约束、fallback成本与AURC样本量待审。

## round_05 / r05

- 评审要点：event F1 primary 不能证明 planning H1；需改为同候选 selection regret 相对 NRI+same-label，锁阈值/cluster/power并共享fallback。
- 决策：全部接受。
- 具体改动：唯一 primary 改 validation-frozen 90% coverage selection regret，NRI+same-label 为最强比较器；F1降机制门槛，success为key secondary；snapshot/task cluster 20%功效，NRI/C-SWM共享confidence/fallback/runtime；success<3pp降级。
- 改后分数：自评 D3/D8/D9/D10→4.5；待 round_06。
- 未决项：90% event coverage 与 snapshot selection coverage 的映射待审。

## round_06 / r06

- 评审要点：action×edit只是干预；representation×executor训练2×2缺失。
- 决策：全部接受。
- 具体改动：NRI/JEPA×flat/typed 2×2，endpoint/ordered同成本target；native/adapter、validation winner与JEPA/executor/benchmark claim ladder；资源/event pilot gate。
- 改后分数：自评D3/D10/D11→4.5；待round_07。
- 未决项：200 snapshots coverage/null/probe待测。

## round_07 / r07
- 评审要点：full/power、target来源、ontology family split不足。
- 决策：接受。
- 具体改动：200 smoke后ICC定N/100M cap；字段来源表与future拒绝单测；topo_event_v1 canonical schema；task+asset+contact-program group split与4格训练账。
- 改后分数：自评D5/D11/D12→4.5；待round_08。
- 未决项：actual event distribution未知。

## round_08 / r08
- 评审要点：closed/open ontology、sim-real GT与online guard。
- 决策：接受。
- 具体改动：closed-program primary/open-event atlas；marker隔离双标confusion；coverage/fallback conditional；shared force/collision/transaction guard与claim ladder。
- 改后分数：自评D3/D9/D14→4.5；待round_09。
- 未决项：open ontology只unknown能力。

## round_09 / r09
- 评审要点：NRI+labels、closed ontology、branding攻击。
- 决策：接受。
- 具体改动：TopoManip ordered transactions标题；NRI×typed首行；JEPA/executor/control/external四级删claim。
- 改后分数：自评均分4.5；待round_10。
- 未决项：无新fatal。

## round_10 / r10
- 评审要点：±1 frame容忍可能掩盖错误顺序。
- 决策：接受。
- 具体改动：0/±1/±2 tolerance与raw timestamp error、transaction regret联表；只在±2成立则降coarse endpoint。
- 改后分数：内容PASS；待R11。
- 未决项：raw timing误差待测。
