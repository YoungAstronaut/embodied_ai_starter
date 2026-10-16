# WAM-P3 Refinement Log

## r00 / pre-review

- 评审要点：CoCo 已覆盖通用反事实 controllability；Robot-Factored/DELE 压缩 future latent 空间。
- 决策：接受，完全更换核心假设为 hidden-physics belief。
- 具体改动：加入 nominal action-realization 分解、物性 exact-reset、触觉 oracle 与跨周期信息时序。
- 改后分数：待 round_01。
- 未决项：真机摩擦配对重置误差需预实验。

## round_01 / r01

- 评审要点：未对齐 latent 却报告 θ-NLL/ECE 自相矛盾；首次作用前不可识别；nominal residual 混有 controller/vision/contact localization；稳健 action 未定义。
- 决策：全部接受；选择 predictive-equivalence belief，不用 GTθ 对齐主 latent。
- 具体改动：评价改为 held-out future NLL、outcome-set coverage/width 与 action regret；分 prior/passive/probe 三阶段并禁止 t=0 识别 claim；写出含 controller/observation/contact-location/dynamics 的 residual 生成式和 2×2×2×2 干预；action objective 固定 CVaR0.2；补 PEARL/RMA/Bayes-adaptive 邻域。
- 改后分数：自评 D5 3.0→4.0、D6 维持 4.5、D9 4.0→4.5；待 round_02。
- 未决项：outcome set 的 conformal/calibration split、真机 confounder 可独立操控程度与 PEARL/RMA 同信息复现需进一步审核。

## round_02 / r02

- 评审要点：RMA/PEARL已覆盖context adaptation；关键组合baseline应为Robot-Factored+PEARL/RMA；“physics”标题过强；需generic recurrent mixture和z/innovation梯度边界。
- 决策：全部接受；标题与正文统一为hidden-dynamics predictive belief，GT物理量只分层/监督oracle。
- 具体改动：新增逐字段RMA/PEARL/Robot-Factored表、两种组合baseline与同参数generic recurrent mixture；唯一增量锁定visual residual confounder attribution+future-set calibration；明确u_t nuisance encoder stop-gradient、q_t仅影响t+1、persistent z跨action共享、ε_dyn为decoder i.i.d. innovation；组合baseline持平即判负。
- 改后分数：自评 D3/D5由4.0→4.5、D6/D9维持4.5；待 round_03。
- 未决项：近期visual system-ID补充、组合baseline privileged信息公平性、outcome-set calibration实现与真机独立confounder操控待审。

## round_03 / r03

- 评审要点：stop-gradient不能证明nuisance分离；i.i.d. innovation过强；CVaR采样/偏差预算未定义。
- 决策：全部接受；分离结论只靠factorial intervention/predictive check。
- 具体改动：为controller/camera/contact nuisance给可观察target；四类belief-shift confusion；i.i.d./AR(1)/state-dependent三族；每候选16×4=64 samples、L-statistic CVaR、128 reference bias<5%、PIT/coverage/ACF检查。
- 改后分数：自评 D4/D5/D13→4.5；待 round_04。
- 未决项：AR/state-dependent family选择、64-sample tail方差与真机nuisance-only干预纯度待审。

## round_04 / r04

- 评审要点：latent belief-shift非表示不变；contact localization residual不是部署GT；128不足tail reference；残留物理参数后验措辞。
- 决策：全部接受。
- 具体改动：shift改held-out action predictive MMD/W1/regret且做latent permutation invariance；三列nuisance字段合同；64 fractional CVaR公式、1024 reference收敛；Ljung-Box whiteness；清理物理参数posterior措辞。
- 改后分数：自评 D4/D5/D13→4.5；待 round_05。
- 未决项：MMD kernel、1024离线成本与真机marker target偏差待审。

## round_05 / r05

- 评审要点：锁恰好两次交互的 normalized action regret primary；标准化 predictive MMD、state/task cluster 功效及组合最强基线公平性。
- 决策：全部接受。
- 具体改动：固定 t=2 primary，t=1/4降为曲线；最强 comparator 为 Robot-Factored+PEARL/RMA 与 generic mixture 的 validation winner；所有方法共享 deploy fields/history/64 samples/CVaR planner；加入MMD标准化、20%功效与 success<3pp降级。
- 改后分数：自评 D8/D9/D10/D13→4.5；待 round_06。
- 未决项：pooled MMD scale 稳定性与 state/task ICC 待审。

## round_06 / r06

- 评审要点：PEARL/RMA信息不等；factorization×belief未正交。
- 决策：全部接受。
- 具体改动：native/deploy-equal字段表；raw/residual representation×point/distributional belief 2×2；统一innovation decoder；仅按validation t2 regret选winner；补64/1024资源/pilot gate。
- 改后分数：自评D10/D11/D12→4.5；待round_07。
- 未决项：200-state采样bias/runtime待测。

## round_07 / r07
- 评审要点：candidate/sample/horizon/1024 subset缺失。
- 决策：接受。
- 具体改动：冻结N16 candidates×16 belief×4 noise×H16；50k cell与asset+physics split；200-state nested K1024；完整2×2×seed/innovation/baseline calls账。
- 改后分数：自评D8/D11/D12→4.5；待round_08。
- 未决项：64 bias未实测。

## round_08 / r08
- 评审要点：physics×appearance、真机block drift与force guard。
- 决策：接受。
- 具体改动：全交叉与t0 stratum leak；root physics block记录温磨漂；logger隔离、passive/probe分表、shared guard/fallback降级。
- 改后分数：自评D6/D9/D14→4.5；待round_09。
- 未决项：appearance泄漏可能迫使改visually-conditioned。

## round_09 / r09
- 评审要点：PEARL/RMA、可见physics、latent解释攻击。
- 决策：接受。
- 具体改动：Functional Predictive标题/not-claim；deploy-equal winner首行；t0/generic/control自动降级。
- 改后分数：自评均分4.5；待round_10。
- 未决项：t0是硬门槛。

## round_10 / r10
- 评审要点：residual可能只编码视觉/controller误差。
- 决策：接受。
- 具体改动：innovation-shuffle/wrong-controller/held-out-action联合行；任一shortcut成功删除functional-belief claim。
- 改后分数：内容PASS；待R11。
- 未决项：负控效应待测。
