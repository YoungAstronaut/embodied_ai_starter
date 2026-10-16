# WAM-P2 Refinement Log

## r00 / pre-review

- 评审要点：audit-v1 指出 When-to-Trust/HarmoWAM/CheckVLA 已覆盖朴素按需想象。
- 决策：接受，主变量改为 paired counterfactual VOC 与序贯停止。
- 具体改动：加入固定 p95 wall-clock、公平 NFE、oracle VOC、deadline miss 和净收益判负。
- 改后分数：待 round_01。
- 未决项：VOC target 的任务 reward 定义需评审压力测试。

## round_01 / r01

- 评审要点：VOC 无清晰决策单位/common randomness；单调性约束技术错误；视觉命题与纯 scheduler 混合；只匹配 p95 不公平。
- 决策：全部接受；明确允许 harmful imagination，不再正则为单调。
- 具体改动：定义 decision epoch、固定候选、Hc=16 回报和 common-seed `Y_k/Y_{k+1}` potential outcomes；每对用 8 seeds 估方差并拒绝不确定 sign；删除 `L_monotone`；加入 compute-only 与 shuffled visual-stat controls及错误类型分解；公平性扩成 mean/p50/p95/p99/NFE/energy/age Pareto并计 scheduler overhead；补 adaptive-compute/PonderNet 邻域。
- 改后分数：自评 D5 3.0→4.0、D6 维持 4.5、D9 4.0→4.5；待 round_02。
- 未决项：S=8 的 target variance/成本、跨任务 reward 权重和官方近邻是否也有 decision-value proxy 需继续核验。

## round_02 / r02

- 评审要点：VOC/halting是经典概念；三篇WAM近邻target需正文级；20k×k×8规模与4GPU/4天不闭合；head可能记task/step。
- 决策：全部接受；贡献只保留“视觉WAM的CRN paired marginal decision-value dataset/objective”，不再声称发明VOC。
- 具体改动：按官方正文写When-to-Trust binary executability+remaining execution、Harmo phase BCE expert gate、CheckVLA rolling conformal repair；补Selecting Computations/rational metareasoning；闭合5k=5.12M steps/320k records/2.6GB与20k=20.48M/1.28M/10.5GB乘法账和降级矩阵；加40/10 task-blocked、去task/step ID、progress shuffle和cross-task transfer。
- 改后分数：自评 D3/D5由4.0→4.5、D6/D9维持4.5；待 round_03。
- 未决项：5k pilot实测sim/WAM throughput、reward evaluator跨任务归一化与rational-metareasoning直接实现细节待审。

## round_03 / r03

- 评审要点：允许D负后再正却用一步VOC≤0停止；deadline penalty与连续cost可能双计；CRN未锁WAM随机源。
- 决策：接受并改 estimand/decision rule 为 finite-horizon continuation value；myopic VOC降为强基线。
- 具体改动：定义Bellman V_k/A_k与部署伪代码；加入Y=[0,-1,4]三步反例及pattern prevalence≥5%；分离离散deadline后果与ms/J/age连续cost；CRN覆盖环境、候选、WAM、tie-break、evaluator。
- 改后分数：自评 D4/D5/D13→4.5；待 round_04。
- 未决项：continuation target的bootstrapping偏差、有限K敏感性与真实energy计量待审。

## round_04 / r04

- 评审要点：绝对age在Bellman中重复扣；S=8经max有乐观偏差；target schema/文本残留myopic VOC。
- 决策：全部接受。
- 具体改动：cost改Δtime/ΔJ/Δage并给20/40/60手算；S=16两折cross-fit且S4/8/16/32曲线；保存Y0:K和全部增量；表/loss/部署/判负统一continuation。
- 改后分数：自评 D5/D13→4.5；待 round_05。
- 未决项：cross-fit方差、terminal-vs-running cost选择和S32预算待审。

## round_05 / r05

- 评审要点：S16 primary 与 S8 成本矛盾；锁单一资源 operating point、最强 deployable comparator、cluster/power 与统一可见字段。
- 决策：全部接受。
- 具体改动：5k/20k 成本翻倍至10.24M/40.96M steps、640k/2.56M records和5.2/21GB；validation冻结资源/λ；myopic VOC为最强比较器；episode/task bootstrap、5pp功效和机制不转 success 降级。
- 改后分数：自评 D8/D9/D10/D12→4.5；待 round_06。
- 未决项：S16 target 方差与96h full go/no-go可行性待审。

## round_06 / r06

- 评审要点：固定myopic不是winner；paired target×continuation未正交。
- 决策：全部接受。
- 具体改动：winner改五类gate的validation可行集，另closed-test paired-myopic；unpaired/shuffled vs CRN-crossfit×myopic/continuation 2×2；native/adapter双表与逐模块资源账，实际pilot=0不伪造throughput。
- 改后分数：自评D10/D11/D12→4.5；待round_07。
- 未决项：100-epoch吞吐与5k wall-clock待测。

## round_07 / r07
- 评审要点：S8/S16冲突，WAM/model-grid总账和split不足。
- 决策：接受。
- 具体改动：primary统一S16，S4/8/32只nested bias；补Nepoch×K states、4格×3 seeds、validation calls、record bytes/dedup；冻结40/10/10 tasks与100-epoch实测输出。
- 改后分数：自评D5/D11/D12→4.5；待round_08。
- 未决项：actual throughput仍0。

## round_08 / r08
- 评审要点：真机仅calibration无test，task/model/device OOD混叠。
- 决策：接受并拆sim target与real gate transfer两claim。
- 具体改动：三OOD分表；真机cal/eval tasks隔离；K/fallback conditional与zero-shot/recalibration分表；无held-out real test删transfer。
- 改后分数：自评D9/D14/D15→4.5；待round_09。
- 未决项：真机不验证VOC target。

## round_09 / r09
- 评审要点：承认VOC旧、oracle成本与real target攻击。
- 决策：接受。
- 具体改动：paired-myopic/winner首组；VOC/oracle/real三攻击；prevalence/oracle/transfer三种降级摘要与标题。
- 改后分数：自评均分4.5；待round_10。
- 未决项：无新fatal。

## round_10 / r10
- 评审要点：oracle rollout成本可能隐含优势。
- 决策：接受。
- 具体改动：target-build compute/teacher quality/deploy compute三列；oracle不计deploy但全计research cost，双成本视图。
- 改后分数：内容PASS；待R11。
- 未决项：真实GPU-hours待smoke。
