# GEO-P2 Refinement Log

## r00 / pre-review

- 评审要点：尚未进入独立评审。
- 决策：把泛化的 contact-aware 表述收缩为接触转移场。
- 具体改动：增加 mode/time/normal 目标、可见性审计、dense-depth 与触觉 oracle 对照、判负阈值。
- 改后分数：待 round_01。
- 未决项：真机 contact proxy 噪声模型待验证。

## round_01 / r01

- 评审要点：r00 的未来 contact field 未条件化候选动作，action head 再读取 field 构成未定义循环；ontology、部署 frame 和定向机制干预不足。
- 决策：全部接受；将 r00 技术图判作 fatal 并替换，不保留无动作条件的措辞。
- 具体改动：改为 proposer 先给 N 个候选、action-conditioned contact predictor 逐条预测、scorer 后排序的 DAG；定义 H/Δt/body-pair/mode/event/多接触/censoring 与二元可实现 extractor；主部署禁用 GT pose，加入 detector/GFM、noise、failure fallback；新增五最近邻字段表与只错 time/normal/mode 的方向干预。
- 改后分数：自评 D5 2.5→4.0、D6 4.0→4.5、D9 4.0→4.5；以 round_02 为准。
- 未决项：ContactWorld/TouchWorld 字段需继续正文级核对；多接触 Q=8 覆盖率和跨引擎阈值敏感性待实测。

## round_02 / r02

- 评审要点：ContactGuard 已覆盖 planned-action-conditioned pre-contact latent rollout/真机 abort；邻居表“按原实现”不可审计；显式 field 可能只是标签工程；缺 N×field predictor token/延迟图。
- 决策：全部接受；pre-contact/action conditioning 不再作为新意，唯一方法 claim 锁定 explicit multi-event field 的方向可诊断多候选排序。
- 具体改动：按官方正文填 ContactGuard/ContactWorld/TouchWorld/ViTacWorld/Where-to-Touch 输入、动作条件、target、policy作用与版本/代码状态；加入同N/同标签预算 ContactGuard latent probe；预注册 latent-only/field-only/combined/oracle-field；增加 encoder缓存→N=8 batched predictor→scorer 的逐模块 p50/p95 和≤100ms门槛；ContactGuard持平时放弃方法claim。
- 改后分数：自评 D3 3.5→4.5、D5 4.0→4.5、D6/D9维持4.5；待 round_03。
- 未决项：ContactGuard/邻居代码权重可得性、N=8实测吞吐、Q=8多接触覆盖与字段label budget等价性待审。

## round_03 / r03

- 评审要点：联合训练允许 field 编码 action；候选 target 支持域未闭合；100ms 未含完整链路。
- 决策：全部接受；主设置 typed bottleneck+stop-gradient，所有候选 exact-reset 监督。
- 具体改动：明确 snapshot×8×4×16 数据单元/1.024M MVP steps/censor manifest/support≥90%；加入 action-ID probe、end-to-end 消融、固定动作 wrong-field 阈值；profile 纳入 proposer到safety并设p95/p99合同。
- 改后分数：自评 D4/D5/D13→4.5；待 round_04。
- 未决项：typed discretization 分辨率与真实 contact field 的 censor calibration 待审。

## round_04 / r04

- 评审要点：censor likelihood、多事件risk set、fixed-action success、Bayes probe和L_cons不唯一。
- 决策：全部接受；采用cause-specific discrete hazard，删除L_cons。
- 具体改动：event/no-event/truncated三手算；事件后更新risk set；score intervention与selection success分层；probe改GT-field经验上界。
- 改后分数：自评 D5/D13→4.5；待 round_05。
- 未决项：competing-event slot ordering与hazard calibration待审。

## round_05 / r05

- 评审要点：锁唯一 selection-regret primary、ContactGuard 最强比较器、snapshot cluster 功效；区分 MVP/full 标签漏斗与真机 confirmatory 能力。
- 决策：全部接受。
- 具体改动：写出1.024M attempted-step MVP漏斗/support≥90%；固定 ContactGuard-style latent comparator 与共享字段/labels/planner/runtime；selection regret唯一主终点、task/snapshot bootstrap、20%功效及 success<3pp降级；真机 paired-reset 不足功效则仅外部效度。
- 改后分数：自评 D8/D9/D10/D13→4.5；待 round_06。
- 未决项：真机 event label 审计误差与 snapshot ICC 待审。

## round_06 / r06

- 评审要点：ContactGuard native/typed-label公平与ontology×executor未正交。
- 决策：全部接受。
- 具体改动：拆native/label-equal；generic/typed target×flat/typed executor 2×2、等维null消融、validation winner；补资源manifest与0-pilot诚实gate。
- 改后分数：自评D10/D11/D12→4.5；待round_07。
- 未决项：200-snapshot实际support/吞吐待测。

## round_07 / r07
- 评审要点：full公式、有效censor漏斗、ontology版本缺失。
- 决策：接受。
- 具体改动：闭合task×snapshot×N×S×H与target bytes；互斥7类漏斗；contact_transition_v1 schema/extractor；smoke与task ICC power分离、100M cap。
- 改后分数：自评D11/D12→4.5；待round_08。
- 未决项：实际class balance未知。

## round_08 / r08
- 评审要点：sim-engine-real语义、fallback与force安全边界。
- 决策：接受。
- 具体改动：冻结单位/摩擦材质bins、跨域阈值；真机root双标κ/同步；共享abort，fallback>30%降ontology/router。
- 改后分数：自评D9/D14/D15→4.5；待round_09。
- 未决项：跨域event confusion待实测。

## round_09 / r09
- 评审要点：锁标题/primary/危险基线/攻击/降级。
- 决策：接受。
- 具体改动：ContactGuard-equal首行；ontology/nearest/sim-transfer攻击；typed→diagnostic→external删claim与降级标题。
- 改后分数：自评均分4.5；待round_10。
- 未决项：无新fatal。

## round_10 / r10
- 评审要点：annotation ontology可能决定结果。
- 决策：接受。
- 具体改动：主表加event/root support、censor、κ/timestamp MAE、0/±1/±2 tolerance；support/κ门槛触发降级。
- 改后分数：内容PASS；待R11。
- 未决项：annotation实测未运行。
