# GEO-P1 Refinement Log

## r00 / pre-review

- 评审要点：尚未进入独立评审。
- 决策：先按 rubric v1.0 写入可见性表、最近邻失效条件与判负阈值。
- 具体改动：建立反事实配对、token-swap 中介、等预算基线和资源降级路径。
- 改后分数：待 round_01。
- 未决项：配对生成器字段与样本量功效需评审确认。

## round_01 / r01

- 评审要点：必要关系标签有循环定义；原 `L_sens` 允许错误方向变化，`L_inv` 只约束 mask；差分指标不能冒充中介效应；缺变量级 pair 生成协议与最近邻训练图。
- 决策：全部接受。拒绝继续使用“中介效应”强表述，改为无识别主张的 intervention-based reliance。
- 具体改动：新增 `S=(G_task,G_nui,A_exo)` SCM、3 类 nuisance/3 类 causal/3 类 hard-negative 与拒绝情形；oracle 改为任务 checker 的有效动作集合且不进入 student；以专家分布 KL 和最终动作 JS 替换无方向 margin；新增 acceptance rate、标签噪声、oracle-label ablation、DROID 边界及 VGA/GAM/MECo/ST-VLA 五字段表。
- 改后分数：自评 D5 由 3.0→4.0、D6 维持 4.0、D9 维持 4.5；以 round_02 独立评分为准。
- 未决项：checker 动作码本离散化误差、pair acceptance 的实际统计与功效分析仍需下一轮审计。

## round_02 / r02

- 评审要点：CofactVLA/CAST 已覆盖一般 counterfactual deconfounding；pair `Y*` 没有直接给 relation-token GT，gate 可能只学 objectness；旧 loss 消融名未同步；动作码本近似未审计。
- 决策：全部接受；明确 counterfactual/去偏本身不是创新，唯一 claim 收缩到 SCM entity relation 与部署 GFM token 的结构映射和方向性动作依赖。
- 具体改动：最近邻/强基线加入 CofactVLA、CAST；定义 detector-mask→GFM token pool→typed relation adapter 与 unmappable 分层；增加 geometry relation vs objectness-matched generic feature × generic deconfounding vs SCM objective 2×2、token semantic permutation；消融改成现有 `L_dir/L_nui/L_swap`；加入16–128动作码本 coverage-regret 判负。
- 改后分数：自评 D3 3.5→4.5、D5 3.5→4.5、D6/D9维持4.5；待 round_03。
- 未决项：CofactVLA/CAST 代码可复现状态、GFM token correspondence 的 unmappable 比例与码本 coverage 实测仍需核验。

## round_03 / r03

- 评审要点：fatal——checker relation type 可能经 `type_embedding` 进入 action；oracle pair 筛选有 collider shortcut；`L_swap` 同时称训练项/诊断。
- 决策：全部接受；checker type/id 从 student schema 彻底删除，type 改为部署 soft prediction；swap 固定为纯评测。
- 具体改动：新增 target-worker→schema-validator→soft-type predictor→adapter 的字段 DAG；no/predicted/oracle type 三档与泄漏阳性；accepted/rejected 五字段匹配及 acceptance AUROC≤0.65；删除 `λ4L_swap`，selector 只读部署预测并 stop-gradient。
- 改后分数：fatal 已解除；自评 D6 3.0→4.5、D4/D5→4.5；待 round_04。
- 未决项：soft-type label 噪声、matched rejected 可获得率和 predictor OOD calibration 待审。

## round_04 / r04

- 评审要点：π* categorical与continuous policy无法直接KL；nuisance token index不对齐；type CE不等于action效应。
- 决策：全部接受；主action endpoint改为共享M=64库的set-mass ranking。
- 具体改动：定义可手算`-log sum_S p`与64→128同步support；部署Hungarian+null token matching/unmatched mass；checker ID仅oracle；type CE辅助，primary selection regret降20%。
- 改后分数：自评 D5/D8/D13→4.5；待 round_05。
- 未决项：frozen proposer coverage、Hungarian track断裂与M=128成本待审。

## round_05 / r05

- 评审要点：必须锁定一个 primary、最强部署比较器、regret 定义、层级统计与功效；机制指标未转控制收益时需降级。
- 决策：全部接受；不再把 OOD episode success 写成主要终点。
- 具体改动：定义 M64 exact-reset `Reg=maxY-Y(selected)` 与 task/pair macro；最强比较器锁定 VGA+generic deconfounding；加入 pair/task 两级 bootstrap、20% 功效、validation 冻结与 success<3pp 降级。
- 改后分数：自评 D8/D9/D10/D13→4.5；待 round_06。
- 未决项：pilot ICC、accepted-pair task balance 与自然 DROID 外部效度待审。

## round_06 / r06

- 评审要点：Y*/SCM额外监督不公平，matching与representation混叠；需native/label-equal、winner与2×2。
- 决策：全部接受。
- 具体改动：建两张监督合同；winner扩为四类adapter按validation regret/p95冻结；relation/generic×generic/SCM正交2×2且共享Hungarian；补label-seconds、资源/manifest及actual pilot=0降级gate。
- 改后分数：自评D10/D11/D12→4.5；待round_07。
- 未决项：需真实1k attempted漏斗后才能确认power。

## round_07 / r07

- 评审要点：64KB×20k错千倍，pair第二member漏×2；需三阶段gate与lineage。
- 决策：全部接受。
- 具体改动：修为8192 steps/pair、20k=163.84M、1.28GB/1.19GiB；smoke→2k MVP→ICC power；补pair/member/reject/checker/hash/license/group split与target共享/model-grid分账。
- 改后分数：自评D11/D12→4.5；待round_08。
- 未决项：actual仍0，去重率/吞吐待测。

## round_08 / r08
- 评审要点：OOD/预训练/candidate support与真机near-pair错位。
- 决策：接受，主claim收窄sim exact-intervention ranking。
- 具体改动：冻结四轴OOD、逐域support/fallback/conditional指标；真机3task×30 roots随机、GT隔离与安全guard；无power仅secondary。
- 改后分数：自评D9/D14/D15→4.5；待round_09。
- 未决项：foundation pretraining不可审计。

## round_09 / r09
- 评审要点：D3=4，需不可删除科学对象、三攻击与降级稿。
- 决策：接受。
- 具体改动：固化independent-evaluator pair protocol与relation/generic×objective 2×2；label-equal首行；checker/组合/oracle攻击；method→control→external自动删claim。
- 改后分数：自评D3/D14→4.5；待round_10。
- 未决项：R10独立重评分。

## round_10 / r10
- 评审要点：独立evaluator仍可能与ontology共偏。
- 决策：接受，增加第二checkpoint/reward而非只改措辞。
- 具体改动：冻结A/B evaluator hashes；方向一致且效应差≤10pp门槛；分歧自动降ontology-specific benchmark并主表报告。
- 改后分数：R10内容门槛已过；待R11 lifecycle/diff核验。
- 未决项：实际evaluator分歧率需实验。
