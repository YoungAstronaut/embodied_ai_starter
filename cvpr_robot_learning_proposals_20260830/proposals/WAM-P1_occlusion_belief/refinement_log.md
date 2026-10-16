# WAM-P1 Refinement Log

## r00 / pre-review

- 评审要点：审计已指出 persistent slot 与 OA-WAM/POT-VLA 直接碰撞。
- 决策：接受，改为多假设 identity belief 与 calibration。
- 具体改动：加入 identity-swap benchmark、causal association、oracle/错误关联反向干预和明确判负。
- 改后分数：待 round_01。
- 未决项：OA/POT 官方实现可复现程度需 round_02 刷新。

## round_01 / r01

- 评审要点：完全对称场景身份不可辨识；NLL/ECE/switch 受 label permutation 影响；belief estimation 与 active-control 收益混合；更新方程和 M=4 覆盖不清。
- 决策：全部接受；删除对称档“正确重关联”要求，主结果固定 passive policy。
- 具体改动：把数据分 identifiable/partial/provably-symmetric，后者以 proper scoring 对均匀 posterior 评估；定义遮挡前一次 Hungarian 锚定、遮挡后冻结映射和 permutation-invariant NLL/ECE/switch；写出 prediction/association/Sinkhorn/update/pruning；M=4 明确为单 referent 的三实例+unknown，而非联合排列；active look 改为 2×2 扩展并补 JPDA、JRDB/RALO 长遮挡跟踪邻域。
- 改后分数：自评 D5 3.0→4.0、D6 维持 4.5、D9 4.0→4.5；待 round_02。
- 未决项：三档自动证明器、OA/POT 官方 association protocol 与 detector recall 分层的实际分布待核。

## round_02 / r02

- 评审要点：创新可能只是 JPDA/MHT+language anchor+WAM；OA/POT描述需正文级；identifiability字段可能事后泄入训练；缺probabilistic slot/language tracking。
- 决策：全部接受；多假设tracking本身不再作为新意，唯一机制定位为action/contact-conditioned association likelihood及posterior-marginal control。
- 具体改动：加入 MHT、SCALOR/SAVi、ReferFormer与 `JPDA+same WAM+same language anchor`；按官方正文补OA t0 address/reset/SAM3跟踪/slot-swap、POT role records/confidence/refresh、3D-ALP anchor；将proof stratum置独立evaluator-only shard且train schema拒绝；判负要求显著超过组合基线且删除action/contact likelihood必须有损。
- 改后分数：自评 D3/D5由4.0→4.5、D6/D9维持4.5；待 round_03。
- 未决项：probabilistic-slot基线选择、OA/POT代码可得性、symmetry evaluator数值容差与end-to-end吞吐待审。

## round_03 / r03

- 评审要点：`A_mj·ell_mj` 可能平方似然；proper score未含unknown/residual/miss/false；deploy anchor与GT Hungarian易混。
- 决策：全部接受；改用一次性 generative assignment posterior。
- 具体改动：定义assignment联合因子/归一/边缘，显式禁止二乘likelihood；加2×2枚举单测；定义完整Ω、symmetric orbit entropy/excess NLL/coverage；分离detector-language anchor与evaluator GT schema并加sharpness/ECE审计。
- 改后分数：自评 D4/D5/D13→4.5；待 round_04。
- 未决项：top-M residual 的更新、large-M Sinkhorn误差和p_FA校准待审。

## round_04 / r04

- 评审要点：fatal——association row sum恒1，且每Z乘完整prior乘积会归一抵消，无法更新referent belief。
- 决策：完全接受；显式引入R与Z联合后验，废弃row-sum identity update。
- 具体改动：定义`p(R,Z,D)`，prior仅随R一次，ref/bg/miss/false likelihood一次；`w+=sum_Z p(R,Z|D)`；0.8/0.2 prior与0.1/0.9 likelihood手算得0.3077/0.6923；symmetric evidence保持prior；miss、unknown、residual分离。
- 改后分数：fatal已解除；自评 D4/D5/D13→4.5；待 round_05。
- 未决项：ψ(z)近似、background track likelihood与top-M residual联合归一待审。

## round_05 / r05

- 评审要点：正文仍将 miss 映射 unknown；需锁 ≥2s identifiable+partial proper-score primary、固定宏观层权重、同轨迹比较与功效。
- 决策：全部接受；miss 仅是测量事件，绝不改 referent identity。
- 具体改动：修正完整 Ω 指标与 orbit-mass score；锁 identifiable/partial 各0.5 macro log score、JPDA+same WAM comparator、同轨迹 task-stratified episode bootstrap、10%功效和 success<3pp降级。
- 改后分数：自评 D5/D8/D9/D10→4.5；待 round_06。
- 未决项：partial orbit evaluator 稳定性与 residual proper-score 细节待审。

## round_06 / r06

- 评审要点：完整JPDA posterior+marginal control近同构基线缺失。
- 决策：全部接受。
- 具体改动：建evidence×MAP/marginal L00-L11 ladder与native/adapter；L11危险比较；统一likelihood/capacity；validation winner、stratum漏斗、内存/时延manifest与0-pilot gate。
- 改后分数：自评D3/D10/D11→4.5；待round_07。
- 未决项：三stratum实际比例未知。

## round_07 / r07
- 评审要点：50k无frame/assignment上限，symmetric proof未操作化。
- 决策：接受。
- 具体改动：冻结T-frame公式、detections16/tracks8/M4/beam64；定义4! permutation×8 rerender proof/tolerance/codes；family split与真机tag裁除/同步审计。
- 改后分数：自评D5/D11/D12→4.5；待round_08。
- 未决项：proof-computable率未知。

## round_08 / r08
- 评审要点：“provably”过强、4+实例与tag/安全边界。
- 决策：接受并改ε-symmetric。
- 具体改动：2/3→4–6 support OOD、residual/fallback；ε sweep/failure atlas；真机root/tag裁除/logger/guard，control可删。
- 改后分数：自评D3/D9/D14→4.5；待round_09。
- 未决项：M4 residual校准待测。

## round_09 / r09
- 评审要点：D3=4，需benchmark独特性与L11攻击。
- 决策：接受。
- 具体改动：三strata proper-scoring/support protocol对JRDB/JPDA差异；L11首行；JPDA/不可见/sim自证攻击与pure-benchmark降级。
- 改后分数：自评D3→4.5；待round_10。
- 未决项：方法贡献可被删除。

## round_10 / r10
- 评审要点：ε-symmetric仍可能被误读现实证明。
- 决策：接受。
- 具体改动：orbit/support/certification failure/null-uniform proper score主表；摘要固定simulator-certified，failure不重标。
- 改后分数：内容PASS；待R11。
- 未决项：certification failure率待测。
