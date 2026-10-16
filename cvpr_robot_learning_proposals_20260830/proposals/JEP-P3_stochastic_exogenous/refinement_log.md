# JEP-P3 Refinement Log

## r00 / pre-review

- 评审要点：原风险校准种子被 CheckVLA/JEPA Safety 覆盖。
- 决策：接受并更换科学问题。
- 具体改动：建立 action×exogenous factorial generator、随机 latent factorization、probe+干预判据和非安全声明。
- 改后分数：待 round_01。
- 未决项：interaction residual 的技术形式需 round_04 深审。

## round_01 / r01

- 评审要点：外生变化会改变 action-caused outcome，原 independence/factorization 与 conveyor/双臂任务矛盾；latent 不可识别；planner 需要联合 mixture；缺数值最小反例和 Sawada 邻居。
- 决策：全部接受；将 r00 独立性约束判为 fatal 并删除，不保留“换 e 时 zc 不变”表述。
- 具体改动：改为 `μ+f_a+f_e+f_ae+ε` functional ANOVA，并以行/列零和约束仅识别预注册 intervention measure 下的 outcome functions；planner 明确积分 `p(Y|a,e)q(e|history)`；给 `Y=a·e`、q(e)=0.8 的 conveyor 2×2 反例；加入 held-out action×e cells、main-only ablation、JEPA-WM strongest stochastic/CoCo/Sawada 1804.06955 基线；probe 降为诊断。
- 改后分数：自评 D4 3.0→4.5、D5 2.5→4.5、D6 维持4.5、D9维持4.5；待 round_02。
- 未决项：ANOVA function 在连续 e 下的推广、partial-e posterior calibration、真机 factorial synchronization 和 Sawada 复现仍需审计。

## round_02 / r02

- 评审要点：ANOVA/两 latent 不是创新；CoCo overlap 需公式/数据 cell/指标级比较；JEPA 必要性未证；连续 e 的 centering measure 与 q(e|h) 校准不足。
- 决策：全部接受；唯一命题收窄为 factorial benchmark+interaction-aware objective+calibrated mixture-planning consequence。
- 具体改动：新增 CoCo inverse/zero/mirror/spatial consistency 对本方案 a×e×ξ cells 的逐项表并要求同 4×4 groups 运行；加入 non-JEPA stochastic object WM+同 ANOVA/q-cal/mixture loss；连续 e 固定 μ_train centering、test μ_shift 不重心化；补 q 的 NLL/ECE/CRPS/coverage 与 `e target→student q→mixture planner` 隔离路径；加入 JEPA tie/q-calibration 失败判负。
- 改后分数：自评 D3 4.0→4.5、D5 4.0→4.5、D6 维持4.5、D9 维持4.5；待 round_03。
- 未决项：continuous e quadrature 误差、真实 conveyor e 的同步标签噪声和 learned-q 下 CVaR Monte Carlo 方差待审。

## round_03 / r03

- 评审要点：mean ANOVA与distribution NLL对象不一致；teacher-e到learned-q shift；μa随proposer/state可能漂移。
- 决策：全部接受；ANOVA改为characteristic-kernel distribution embedding。
- 具体改动：RKHS distributional interaction+mixture NLL/energy；均值/纯方差/同均值方差双峰mode三最小例；true-e/q-sampled/q-corrupted 1:1:1训练与oracle/learned q gap≤10pp；冻结proposer/seed、局部等权μa和不重心化test shift。
- 改后分数：自评 D4/D5/D13→4.5；待 round_04。
- 未决项：kernel bandwidth、有限K对embedding估计误差和q corruption幅度待审。

## round_04 / r04

- 评审要点：fatal——q-sampled/corrupt e与true-e outcome做conditional NLL会把P(Y|a,e)主动混合，抹平f_e/f_ae。
- 决策：完全接受；条件predictor只读true-e cell，q robustness移到正确边缘化/规划层。
- 具体改动：分离conditional predictor、q supervised、stopgrad predictor marginal/planner三路径；无标签序列只走边缘目标；定义SE3/contact/collision product characteristic kernel和K=4/8/16/32对K32误差≤10%。
- 改后分数：fatal已解除；自评 D4/D5/D13→4.5；待 round_05。
- 未决项：离散/连续e积分器、SO(3) heat kernel近似与planner distillation偏差待审。

## round_05 / r05

- 评审要点：K32 收敛要求与 K4 预算矛盾；需锁 learned-q held-out action×e regret primary、2×2、最强比较器与 factorial-cluster 功效。
- 决策：全部接受。
- 具体改动：full 15k groups固定K4，500-group subset另做K4/8/16/32并计448k outcomes；唯一 primary 为 learned-q normalized ranking regret；加入 additive/interaction×oracle/learned-q 2×2、CoCo/Sawada/JEPA-WM winner comparator、20%功效和 success<3pp降级。
- 改后分数：自评 D8/D9/D10/D12→4.5；待 round_06。
- 未决项：K4 full estimator 方差及 learned-q group-wise有效样本量待审。

## round_06 / r06

- 评审要点：winner漏non-JEPA同目标；oracle-e/true-q混入deploy 2×2。
- 决策：全部接受并废弃混写种子。
- 具体改动：winner纳入non-JEPA/MDN-RSSM；deploy 2×2改additive/interaction×learned/generic-q，oracle三角独立；observational/factorial×generic/ANOVA MVP 2×2；claim ladder与K-pilot资源gate。
- 改后分数：自评D3/D10/D11→4.5；待round_07。
- 未决项：500-group K pilot尚未运行。

## round_07 / r07
- 评审要点：448k措辞矛盾，H/history/model-grid未计。
- 决策：接受。
- 具体改动：full K4=960k、额外448k、unique1.408M outcomes×H16；q history8、K prefix；MVP/deploy grid×3 seeds及baseline账；task/scenario group split，K subset不触test。
- 改后分数：自评D5/D11/D12→4.5；待round_08。
- 未决项：K误差/throughput/power仍待pilot。

## round_08 / r08
- 评审要点：combinatorial/extrapolative混写、q失校与真机安全。
- 决策：接受。
- 具体改动：ID/combinatorial/μshift三层；q阈值触发conservative baseline；3 real tasks/logger/guard；balanced→ANOVA→JEPA层级。
- 改后分数：自评D3/D9/D14→4.5；待round_09。
- 未决项：μshift q calibration未知。

## round_09 / r09
- 评审要点：ANOVA旧、CoCo覆盖、JEPA branding攻击。
- 决策：接受。
- 具体改动：ExoManip标题无JEPA；non-JEPA/CoCo首行；三攻击与dataset→objective→JEPA/transfer降级。
- 改后分数：自评均分4.5；待round_10。
- 未决项：无新fatal。

## round_10 / r10
- 评审要点：deploy若偷用true-e为fatal。
- 决策：接受。
- 具体改动：learned-q/true-e oracle/q-corrupt同表；schema拒绝true_e；ECE/coverage阈值自动切conservative并删mixture claim。
- 改后分数：内容PASS；待R11。
- 未决项：q shift calibration待测。
