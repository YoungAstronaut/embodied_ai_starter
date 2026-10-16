# WAM-P3：动作实现分解下的 Hidden-Dynamics Predictive Belief-WAM

- Proposal-ID: WAM-P3
- Revision: r10
- Last-Modified: 2026-08-30
- Source-Cutoff: 2026-08-30
- Responds-To-Review: round_10
- Change-Summary: 新增innovation-shuffle、wrong-controller、held-out-action联合负控行；任一shortcut probe成功即删除functional-belief claim。

## 问题与可观察失败

CoCo 已约束动作反事实响应，Robot-Factored WM 已把命令经控制器/运动学变为 nominal robot trajectory，DELE/LaWAM/LiLa-WAM 已做 compact future latent。仍缺的可观察失败是：视觉几乎相同、命令相同，但物体质量、摩擦或顺应性不同，导致接触后转移与正确后续动作不同；单一确定性 WAM 把多模态结果平均化，连续重复错误力度。

H1：先分解可部署的 action realization，再从过去“名义机器人运动—实际物体响应”残差更新 **predictive-equivalence belief**，能在物性 OOD 下改善未来 outcome-set calibration 和动作。首次作用前相同视觉/历史的不同物性不可辨识，此时所有方法必须共享 prior；主张只覆盖作用后的被动更新，主动 probe 是带成本的扩展。latent 不被解释成真实质量/摩擦坐标。

## 最近邻差异

- Robot-Factored WM 解决动作命令到可视机器人几何接口；本方案新增跨交互更新的functional predictive belief，不称物理参数后验。
- DELE/LaWAM/LiLa-WAM 直接未来 latent/action，本方案不以 compact latent 为新意，而以同观测不同 hidden dynamics 的多假设 belief 为对象。
- VT-WM/ViTacWorld 依赖触觉建模接触；本方案主结果只用 RGB+proprio，触觉作为 oracle 上界。
- CoCo 保证动作 counterfactual sensitivity，但不识别为何同动作产生不同物理响应。

| 邻域 | context input | privileged training/监督 | posterior与校准 | visual prediction | planner/control |
|---|---|---|---|---|---|
| Robot-Factored WM | RGB/robot trajectory/action realization | robot/object factorized target | 非context posterior主项 | 显式对象future | action-conditioned rollout |
| PEARL | transition/reward context set | off-policy meta-RL任务分布，无需部署GTθ | probabilistic latent context，非视觉outcome-set校准 | 非主项 | policy条件化z |
| RMA | recent proprio/action history | base policy用privileged extrinsics，adaptation module模仿privileged latent | point/rapid context，非Bayesian set coverage | 非视觉WAM | adaptive policy |
| Robot-Factored+PEARL/RMA（强组合） | nominal realization+与本法相同RGB/proprio/history | PEARL posterior或RMA teacher按最公平可用信息 | 同latent dim/更新次数 | 同WAM decoder | 同CVaR objective |
| DELE/LaWAM/LiLa-WAM | history→compact future/action | future/action supervision | generic recurrent latent | latent/direct future | direct policy |
| 本方案 | nominal residual + controller log + detector covariance/contact confidence | 不用GT dynamics；GT参数仅评测/监督oracle | predictive-equivalence mixture+outcome-set calibration | 对象future distribution | posterior samples+CVaR |

因此 generic context adaptation、Bayes update、action realization factor均不作为创新；唯一可判重增量是**在视觉WAM中把可观测controller/vision/contact误差从persistent hidden-dynamics context中分开，并验证这一步改善calibrated future-set planning**。

## 方法

控制器/URDF 把命令 `a_t` 展开为部署可得 nominal trajectory `r^nom_{t:t+H}`；scene encoder 分离机器人/对象区域。观测 residual 的生成模型显式写为
`e_t = h_θ(z_{t-1},r^nom_t,c_t) + Bε_ctrl_t + Cε_obs_t + Dε_loc_t + ε_dyn_t`，
字段合同：controller deploy input=`command,measured joint,error,latency`，train target=日志error，evaluator GT同日志；camera deploy input=`RGB,detector covariance`，target=训练augmentation ID/known perturbation，eval GT=相机日志；contact deploy input=`predicted point/confidence,proprio residual`，train target=sim/marker localization error，eval GT=sim/marker，**GT error不进q更新**。g由deploy input预测nuisance embedding，target只监督其head并stop-gradient。

belief shift不在latent空间计算：固定held-out actions A_eval与noise seeds，比较干预前后posterior predictive distributions的MMD/W1、90% set change和action regret；component permutation/可逆latent transform后应数值不变。四格confusion matrix填predictive MMD/decision regret，physics-only必须比nuisance-only≥2×。

每候选16×4=64 utilities，升序`u_(i)`时 fractional-tail `CVaR_.2=[Σ_{i=1}^{12}u_(i)+0.8u_(13)]/12.8`；所有基线同64 calls。离线以1024 samples为reference，画64/128/256/1024 bias/CI，64相对1024 bias>5%则改128主预算。residual whiteness用Ljung-Box在lag4、按有效N算p值（p<.05拒绝i.i.d.），不固定任意ACF .1。

三阶段协议：(0) `prior`：首次接触前比较所有方法的 prior predictive NLL/coverage，不允许声称识别；(1) `passive update`：执行相同任务动作后逐周期更新 q，报告第 1/2/4 次交互；(2) `active probe`：可选候选含 probe，单独扣除时间/失败风险并与 oracle information gain 比较。适应收益与 probe 收益不合并。

| 变量 | student 训练 | teacher/target | 部署 | 防泄漏 |
|---|---:|---:|---:|---|
| 当前/过去 RGB、proprio、已执行命令 | 是 | 是 | 是 | causal prefix |
| nominal trajectory（控制器/URDF） | 是 | 是 | 是 | 部署前可计算，不用真实未来状态 |
| 执行后的对象响应 | 下一时刻才进入 history | target | 下一周期可见 | 禁止同一步回填 |
| GT mass/friction/compliance/contact force | 否 | 仅分层评测/监督 oracle | 否 | 不计算主 latent 的 θ-NLL |
| future RGB/pose/success | 否 | loss target | 否 | future mask + 阳性泄漏对照 |

## 数据、实验与资源

HiddenPhysics-12：ManiSkill/RoboTwin 12 tasks，物性拉丁超立方采样，训练/测试区间错开；相同初始视觉 exact-reset、相同 nominal action。50k episode。真机用可换配重盒、不同桌面摩擦和软硬海绵，4 tasks×120 paired trials；质量/摩擦标签只评测。MVP 2×A100、4 天；完整 8×A100、10 天。

强基线：Robot-Factored WM、Robot-Factored+PEARL/RMA、generic recurrent mixture、DELE、RSSM、CoCo、system-ID/tactile oracle。最强 deployable comparator 按下述 deploy-equal validation winner 冻结；各法共享部署 fields/history、64 samples、candidate set、CVaR planner、fallback与NFE。**唯一 primary** 是恰好第2次被动交互后 held-out actions 的 task-normalized regret；第1/4次、MMD/NLL/coverage/success均为 secondary。

消融：belief vs point context、history、无 realization factor/residual、prior/passive/probe、expectation/CVaR/minimax、i.i.d./AR(1)/state-dependent innovation、latent dimension、真实 θ supervision oracle、触觉、同一步 future-state 泄漏阳性对照。做 `physics×controller error×observation noise×contact localization` 2×2×2×2 factorial，并输出四类 belief-shift confusion matrix，不用latent probe解释物性。

### R6 信息公平、正交 2×2 与资源合同

| baseline-native | training privileged fields | deploy fields |
|---|---|---|
| PEARL-native | reward/transition context，按原文 posterior | 原生 context |
| RMA-native | privileged teacher 可见 dynamics，student history | 原生 student fields |

| deploy-equal adapter | training target | deploy contract |
|---|---|---|
| PEARL/RMA/Robot-Factored/generic mixture | 同 outcome/contact labels、context horizon、64 posterior/outcome samples | 同 RGB+proprio+executed history、candidates、CVaR planner、fallback、NFE |

主 2×2 是 dynamics representation `{raw recurrent,nominal-realization residual}`×adaptation `{point context,calibrated distributional belief}`；四格 encoder/decoder、latent dim、loss数、samples与参数±5%。i.i.d./AR1/state-dependent innovation decoder 对四格与强基线均开放，由 validation 统一选一次，不能由本法独享。winner 仅按 validation t=2 normalized regret 在 deploy-equal adapters 中冻结；native winner另表，test不按 NLL/success重选。

冻结每state `N_candidate=16`；每候选由 `N_belief=16` posterior particles×`N_noise=4` innovations=64 outcomes，rollout `H=16`，故规划账为 `N_state×16×16×4×16` WAM steps。50k episodes manifest含 simulator/task/asset/physics-bin/nuisance-bin/interaction-index/episode，并按 asset + held-out physics interval group split；外观纹理在physics bins间平衡。1024 reference只在固定200-state train/calibration subset，64 seeds是1024 nested prefix；cache belief-conditioned trunk并报告复用。model grid 至少4个2×2格×3 seeds，加各格统一innovation validation选择与baseline adapters；分别列train GPU-hours、planner calls、storage与latency。**截至r07 actual 200-state pilot=0**；bias>5%则改128并重算power/预算。

### R8 hidden 边界、真机 block 与安全合同

- **唯一主命题：** 两次被动交互后 functional predictive belief 降低 held-out-action regret；**不声称**识别质量/摩擦等物理参数，内部latent只在predictive equivalence意义下解释。
- dataset按 physics-bin×appearance-family全交叉，train/test physics interval与asset都group split；t0按appearance stratum检验，若t0已超过3pp可预测physics层，则改称 visually conditioned dynamics，不称hidden。
- 真机root object×trajectory×physics block内随机方法顺序，记录温度、磨损、表面漂移；marker/force/θ只进独立logger，passive/probe分表。共享force/workspace/collision guard，报unsafe candidate rejects、fallback与conditional regret。安全层/fallback解释>50%增益则降为 system-ID diagnostic，标题改 **Functional Predictive Adaptation under Dynamics Shift**。

### R9 论文合同与审稿攻击

- 标题：**Functional Predictive Beliefs from Action-Realization Residuals**。primary=t2 regret；not-claim=不识别物理参数。最危险基线deploy-equal generic mixture/PEARL-RMA winner。
- 攻击：PEARL/RMA已做→差异为nominal-realization residual+t2；physics可见→appearance cross+t0 gate；latent不可解释→只predictive equivalence。
- t0泄漏→改visually-conditioned；generic持平→删factorization；control<3pp或real失败→system-ID diagnostic。降级标题 **Predictive Adaptation under Dynamics Shift**。

### R10 shortcut 联合负控

主表同一行报告：(a) innovation在task/elapsed bin内shuffle；(b)换wrong-controller residual但保持视觉；(c)只在held-out actions算predictive regret。要求(a)/(b)使本法相对优势至少下降50%，且(c)仍相对最强baseline降≥20%；若action-only/appearance probe成功、wrong-controller不伤或held-out-action优势消失，立即删除functional-belief claim，只留generic predictive adaptation。

## 判负

被动交互第2次后，primary action regret 相对最强 deployable comparator 降≥20%，state 为 cluster、task 分层的 paired bootstrap 95% CI 不跨0；按20%相对下降、α=.05、power=.8 的 pilot ICC 冻结 states/task。success 提升≥6pp、future NLL降≥10%、90% set coverage∈[.87,.93]且 width 降≥15%为 secondary；若 MMD/NLL 改善但 success 增益<3pp，降级为 predictive belief，不声称控制收益。t=0若显著“识别”即泄漏。去显式 nuisance factor而参数匹配的 recurrent mixture若差≤2%，说明收益来自容量。仅 controller/vision/location noise 造成的标准化 predictive shift 与 GT-dynamics shift 比值>0.5即否定归因。tactile oracle巨大而 RGB+proprio oracle上界<3pp则降级传感不可辨识。

## 风险与里程碑

隐变量只声明 functional predictive equivalence，不解释成质量/摩擦；GT dynamics只用于分层。两周完成 residual schema、组合基线接口、t=0 leak与two-update smoke；两月完成两模拟器、CVaR/probe与真机hidden-dynamics OOD。负结果形成视觉WAM对hidden dynamics的可辨识边界。

## 证据

[Robot-Factored WM 2607.22535](https://arxiv.org/abs/2607.22535)、[DELE-w0.5 2608.22067](https://arxiv.org/abs/2608.22067)、[CoCo 2608.04653](https://arxiv.org/abs/2608.04653)、[VT-WM 2602.06001](https://arxiv.org/abs/2602.06001)、[ViTacWorld 2607.22530](https://arxiv.org/abs/2607.22530)、[PEARL 1903.08254](https://arxiv.org/abs/1903.08254)、[Rapid Motor Adaptation 2107.04034](https://arxiv.org/abs/2107.04034)、[VariBAD 1910.08348](https://arxiv.org/abs/1910.08348)。
