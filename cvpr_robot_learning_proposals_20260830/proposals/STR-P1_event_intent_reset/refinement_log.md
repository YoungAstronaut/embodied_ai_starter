# STR-P1 Refinement Log

## r00 / pre-review

- 评审要点：audit-v1 要求 reset 事件在线可观测并优于固定窗口/forget gate。
- 决策：接受，以预测创新似然比和 CUSUM 定义事件。
- 具体改动：加入假闪烁/低速真事件反向干预、误/漏 reset 指标与 oracle 上界。
- 改后分数：待 round_01。
- 未决项：contact proxy 的跨平台阈值需校准。

## round_01 / r01

- 评审要点：外部 event 不等于 intent change；预测下一帧的 residual 时间索引错位；alternative intent support 未定义；false/miss 未按 prevalence/severity 分层。
- 决策：全部接受；干预时刻只定义 novelty/control-failure 候选，不再直接监督 reset。
- 具体改动：用 same-snapshot common-seed 旧 intent 与 K=4 替代 intents 的 ΔQ 定义 reset-worthy C；重写 `prediction at t−1→residual at t→reset→action t` 并计一周期延迟；形式化 CUSUM+posterior margin；加入 3 类 novelty-no-reset 和 3 类 low-visual-reset hard pairs；指标按 prevalence/severity 分层；补 BOCPD/Remember 最近邻。
- 改后分数：自评 D5 3.0→4.0、D6 4.0→4.5、D9 4.0→4.5；待 round_02。
- 未决项：alternative value oracle 成本、density estimator 稳定性与跨平台 contact residual 标准化待审。

## round_02 / r02

- 评审要点：缺 event-triggered replanning 与 CheckVLA/When-to-Trust/REMAC intervention 邻域；K 候选 proposer 可能混淆 trigger 增益；C oracle 的 future/seed/horizon 路径不足。
- 决策：全部接受；明确 CUSUM/change detection 不新，唯一增量为 change evidence 与 common-seed intervention utility 的 paired reset-value supervision。
- 具体改动：新增六路线 trigger-object 表；所有 gate 固定同一 K=4 proposer 和预算，并加入 oracle-K/current/random-K 分层；形式化 S=8、H_Q=16 的 C-target 生成、target-only future reward 与字段删除；把判负对象升级为同 proposer 的 event-triggered/CheckVLA/When-to-Trust 强基线。
- 改后分数：自评 D3 4.0→4.5、D5 4.0→4.5、D6 维持4.5、D9 维持4.5；待 round_03。
- 未决项：paired oracle 的 30k×5×8×16 rollout 成本与跨任务 density-ratio 校准仍需精算。

## round_03 / r03

- 评审要点：训练paired ΔQ却部署比较intent log-prob；AND CUSUM会漏low-visual reset；s_t易误解为sim state。
- 决策：全部接受；部署决策量改为student ΔQ/CI，视觉与control failure取OR。
- 具体改动：给ΔQ-cost score、OR evidence与low-visual绕行；统一阈值成本/coverage/latency伪代码；所有s改为q_prop/contact部署字段；加入value-head删除和log-prob gate判负。
- 改后分数：自评 D4/D5/D13→4.5；待 round_04。
- 未决项：ΔQ head跨事件校准、CI tail coverage与总rollout成本待审。

## round_04 / r04

- 评审要点：winner CI无同时覆盖；student CI来源未定义；deploy coverage疑似oracle；gate逻辑冗余。
- 决策：全部接受。
- 具体改动：5-head+independent split-conformal residual，Bonferroni α/4 simultaneous LCB后选择；target CI仅权重；oracle coverage仅evaluator；V/F/U八格表与唯一reset逻辑。
- 改后分数：自评 D5/D6/D13→4.5；待 round_05。
- 未决项：event-family exchangeability、Bonferroni保守性与OOD经验coverage待审。

## round_05 / r05

- 评审要点：恢复未操作化；需右删失 restricted mean、event-family macro primary、FWER coverage 下界与功效。
- 决策：全部接受。
- 具体改动：定义回到 pre-event progress/trajectory tube 并连续L=3无失败；H=64右删失；锁 family-macro restricted mean recovery time、最强同proposer gate、event/task cluster 30%功效及 interval coverage lower bound≥.93。
- 改后分数：自评 D5/D8/D9/D10→4.5；待 round_06。
- 未决项：trajectory tube 对不同 task 的可比性与 censor horizon 敏感性待审。

## round_06 / r06

- 评审要点：innovation与ΔQ reset-worthiness未正交。
- 决策：全部接受。
- 具体改动：change×value 2×2+generic concat；native/label-equal双表、validation RMRT winner、equal-rate thresholds；补event target/censor漏斗、资源manifest与0-pilot gate。
- 改后分数：自评D10/D11/D12→4.5；待round_07。
- 未决项：每族50-event smoke尚未运行。

## round_07 / r07
- 评审要点：每event至少640 target steps且history/recovery未计。
- 决策：接受。
- 具体改动：分账history、5×S8×H16=640 target、每方法Hrec64；root_snapshot配对lineage；10/3/3 task split、smoke与root ICC power分离。
- 改后分数：自评D11/D12→4.5；待round_08。
- 未决项：每族acceptance/censor未知。

## round_08 / r08
- 评审要点：仅task OOD且RMRT缺安全约束。
- 决策：接受，claim限seen-family cross-task。
- 具体改动：compositional仅stress；真机root event blocks；collision/jerk/false-reset可行约束、matched-rate/fallback Pareto与detector降级。
- 改后分数：自评D9/D14/D15→4.5；待round_09。
- 未决项：held-out family不作coverage claim。

## round_09 / r09
- 评审要点：BOCPD旧、oracleΔQ、tube手调攻击。
- 决策：接受。
- 具体改动：标题去intent；label-equal gate首行；三攻击与ΔQ/control/OOD降级稿。
- 改后分数：自评均分4.5；待round_10。
- 未决项：tube sensitivity主表。

## round_10 / r10
- 评审要点：ΔQ target可能暗带未来event label。
- 决策：接受。
- 具体改动：opaque shard join/future-field schema rejection/泄漏阳性；flicker vs low-visual event盲评confusion与>60% metadata泄漏门槛。
- 改后分数：内容PASS；待R11。
- 未决项：盲评待运行。
