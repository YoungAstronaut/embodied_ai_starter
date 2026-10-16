# JEP-P1 Refinement Log

## r00 / pre-review

- 评审要点：VLA-JEPA/V-JEPA2 已覆盖普通 action-conditioned future latent。
- 决策：接受，显式定义局部动作等价关系。
- 具体改动：加入 same-state action interventions、类内/类间指标、跨 embodiment 边界与 label-reversal 反向实验。
- 改后分数：待 round_01。
- 未决项：真机安全微扰半径需平台预实验。

## round_01 / r01

- 评审要点：距离阈值关系不传递，不能称 equivalence class；随机 outcome 单 rollout 不足；物理效果与 task value 混合；缺三动作反例与 action abstraction 最近邻。
- 决策：全部接受；将 r00 定义判为 fatal 并废弃，标题/数据/指标全部改为 pseudometric。
- 具体改动：定义 Wasserstein+TV action-effect pseudometric 和独立 task-value distance；用 S=8 matched seeds、bootstrap CI 与 uncertain abstain 估 distribution；改为 metric regression+triplet+value rank；加入 0/0.6/1.2 三动作反例；新增 Action-Bisimulation 2403.16369 直接基线、CoCo/action smoothing 边界与 physical/value swap 判负。
- 改后分数：自评 D5 2.5→4.5、D6 维持 4.5、D9 4.0→4.5；待 round_02。
- 未决项：pseudometric outcome schema 的权重、S=8 估计误差、跨 embodiment canonical adapter 与 Action-Bisimulation 复现需继续审计。

## round_02 / r02

- 评审要点：Action-Bisimulation 已覆盖 multi-step controllability pseudometric；JEPA 必要性、physical/value 相对 bisimulation 边界、SE(3)+contact 单位/triangle/估计误差不足。
- 决策：全部接受；pseudometric 不再列为贡献，新意仅锁定 matched-seed contact-rich target、physical/value cross-task test 及 JEPA structure 是否有独立增益。
- 具体改动：新增 Action-Bisimulation 七字段逐公式表和 Deep Bisimulation 边界；定义 0.10m/π/contact/collision 归一 ground metric 与 W1；加入 S=32 reference、cluster bootstrap 误差 go/no-go；新增 non-JEPA action predictor+同 metric loss；补 target/teacher/student/planner 完整路径和 JEPA tie 判负。
- 改后分数：自评 D3 3.5→4.5、D5 4.0→4.5、D6 维持4.5、D9 维持4.5；待 round_03。
- 未决项：dustbin cost 与多对象 assignment 是否保持身份置换不变、Action-Bisim direct 的视觉输入对齐仍需实现核验。

## round_03 / r03

- 评审要点：可变对象/dustbin未证明metric；shared seed与W1角色混淆；predictor可能只编码action code。
- 决策：全部接受；固定global role index并构造截断null extension metric。
- 具体改动：定义c0截断2C、null cost C与固定role sum；10万三元组triangle单测；CRN只作variance reduction并与独立采样对照；same-action/different-state、state-target shuffle与action-only≤55% probe；adapter train/deploy字段闭合。
- 改后分数：自评 D4/D5/D13→4.5；待 round_04。
- 未决项：semantic role跨任务定义、C敏感性与unshared role coverage待审。

## round_04 / r04

- 评审要点：semantic role非唯一实例；deploy role来源不足；contact edge在node cost可能重复；随机triangle不是证明。
- 决策：全部接受。
- 具体改动：最大role-instance slots，language+detector+initial3D排序+tracker；ε内同类建symmetry orbit；node/edge/contact/collision product metric；GT UUID仅oracle；duplicate/missing三状态对抗例。
- 改后分数：自评 D5/D8/D13→4.5；待 round_05。
- 未决项：3D排序跨camera稳定性、orbit ε与role coverage待审。

## round_05 / r05

- 评审要点：需要 metric supervision×JEPA 完整2×2、Action-Bisim direct同输入主比较、deploy canonicalizer 主结果与 state/task/embodiment功效。
- 决策：全部接受。
- 具体改动：写出2×2四格及共享项；锁单平台 deploy-canonicalizer action regret primary、Action-Bisim comparator、state/task 20%功效；GT UUID仅assignment-noise oracle，跨embodiment降为secondary，success<3pp降级。
- 改后分数：自评 D3/D8/D9/D10→4.5；待 round_06。
- 未决项：2×2 参数匹配与 canonicalizer error strata 样本量待审。

## round_06 / r06

- 评审要点：Action-Bisim native/adapter边界、winner与target替换对照缺失。
- 决策：全部接受。
- 具体改动：两版Action-Bisim合同；四模型validation winner；同non-JEPA recursive/local target危险对照；assignment strata；S32=1.024M outcomes、triangle/runtime manifest与0-pilot gate。
- 改后分数：自评D3/D10/D11→4.5；待round_07。
- 未决项：variance/triangle smoke未运行。

## round_07 / r07
- 评审要点：H、pairwise OT/storage与seed nesting缺失。
- 决策：接受。
- 具体改动：H16；S32 bank=16.384M env steps、S8 prefix；240k OT records约13.44MB；exact OT/cache；power×8-day gate与family hashes。
- 改后分数：自评D5/D11/D12→4.5；待round_08。
- 未决项：OT实测wall-time未知。

## round_08 / r08
- 评审要点：adapter regime与cross-embodiment OOD边界。
- 决策：接受。
- 具体改动：zero/train/few-shot分表；asset/camera/morphology分轴；真机root/GT/guard；明确pseudometric不新与JEPA/metric删claim ladder。
- 改后分数：自评D3/D9/D15→4.5；待round_09。
- 未决项：主adapter regime需在validation前锁定。

## round_09 / r09
- 评审要点：D3=4，Action-Bisim已覆盖理论核心。
- 决策：接受，科学对象改ActMetric protocol。
- 具体改动：local 3D contact outcome/canonical strata/recursive-vs-local target不可删除对象；Action-Bisim首行；三攻击与pure-benchmark降级。
- 改后分数：自评D3/D14→4.5；待round_10。
- 未决项：R10检验是否实质差异。

## round_10 / r10
- 评审要点：stable detector order shortcut。
- 决策：接受。
- 具体改动：clean/duplicate/missing/corrupted-order的abstain/coverage/error/regret联表；GT UUID仅oracle；>10pp shortcut判负。
- 改后分数：内容PASS；待R11。
- 未决项：detector corruption pilot未运行。
