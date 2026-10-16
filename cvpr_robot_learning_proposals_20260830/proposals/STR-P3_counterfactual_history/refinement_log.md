# STR-P3 Refinement Log

## r00 / pre-review

- 评审要点：audit-v1 要求严格同当前观测、不同历史、不同最优动作，并排除静态元数据。
- 决策：接受。
- 具体改动：定义 relevant/irrelevant pair、字段删除、history swap 因果终点和 MDP 边界。
- 改后分数：待 round_01。
- 未决项：真机 exact visual matching 的容差需预注册。

## round_01 / r01

- 评审要点：不同示范动作不等于不同正确动作；直接 state edit 可能生成不可达 pair；收益或仅来自 last-action continuation。
- 决策：全部接受；主 claim 删除 demonstrator commitment，只保留 simulator-value 可验证的 physical pairs。
- 具体改动：pair 必须由两条 reset 起合法 rollout 到达并保存 hash；用 S=8 matched seeds 定义高价值 action sets 和双向交叉低值，不再用动作距离；直接 state edit/commitment 单列诊断；加入 only-last-action/all-actions/proprio/video/video+proprio/action-shuffle controls；补 BeT/多模态 BC 强基线和真机 near-match 边界。
- 改后分数：自评 D5 3.5→4.5、D6 维持 4.5、D9 4.0→4.5；待 round_02。
- 未决项：合法 history 到 same-current 的 acceptance rate、Q-set Monte Carlo 方差与真机容差功效仍需审计。

## round_02 / r02

- 评审要点：pair generator 可能才是贡献，loss/encoder 常规；IntentVLA AliasBench 重合未量化；缺 causal/counterfactual data 邻域、跨 backbone 验证与 Q-set oracle 字段路径。
- 决策：全部接受；不再声称新 encoder，把 benchmark/generator 与 paired supervision 置于贡献首位。
- 具体改动：新增 AliasBench 当前帧/history/value/泄漏四字段 overlap 表和 schema 审计脚本计划；加入 causal representation 邻域；在 IntentVLA 与普通 causal Transformer 两 backbone 做原始/random/strict pair 3格分解；形式化 S=8、H_Q=16 target worker 与 student field whitelist；把 only-video ≥3pp 设为视觉历史必要门槛。
- 改后分数：自评 D3 4.0→4.5、D5 4.0→4.5、D6 维持4.5、D9 维持4.5；待 round_03。
- 未决项：AliasBench 发布 schema 可能尚不含逐 pair hash；若无法审计，只能把重合状态标为未知并缩窄 novelty claim。

## round_03 / r03

- 评审要点：连续policy sample没有离散Q support；AliasBench audit仍是将来时；oracle筛选的合成域迁移不足。
- 决策：全部接受；主action head改为M=64离散检索，实际审计官方代码。
- 具体改动：对全部64 actions×8 seeds精确Q并重写可计算L_cross；用512-eval CEM oracle设coverage gap阈值；克隆官方commit并运行AST脚本，产出`literature/aliasbench_schema_audit.md`；自然/合成按五类可观察难度匹配，transfer≥3pp。
- 改后分数：自评 D3/D5/D13→4.5；待 round_04。
- 未决项：公开release仅task code、离散库1.024B级标签总成本和CEM oracle方差待审。

## round_04 / r04

- 评审要点：20k×2×64×8×16=327.68M未记账；library共享不明；Q跨任务尺度不一；audit不可外推。
- 决策：全部接受并缩小full数据目标。
- 具体改动：pair-local canonical proposer+seed/hash逐字节共享；Adv归一[-1,0]；MVP2k/M16/S4=4.096M，full8k=131.072M accepted、40k attempted ceiling655.36M、CEM1%=10.49M；7天cap；audit边界保留。
- 改后分数：自评 D8/D13→4.5；待 round_05。
- 未决项：实测sim throughput、M16到M64 coverage曲线与1% CEM置信度待审。

## round_05 / r05

- 评审要点：官方 AliasBench 无 pair/Q，natural matched primary 不可执行；需合成 strict primary、明确 transfer comparator、pre-action matching 与 M/S 敏感性。
- 决策：全部接受；明确 abandoned natural seed → synthetic strict replacement。
- 具体改动：唯一 primary 改 held-out generated causal pairs cross-value regret；原始数据 history baseline 为最强比较器，官方任务仅 external validity；matching propensity 仅 pre-action deploy covariates；500 pairs 做 M16/M64×S4/S8，pair/task功效15%。
- 改后分数：自评 D5/D8/D9/D10/D13→4.5；待 round_06。
- 未决项：合成到自然域 transfer 只作为 secondary 的论文定位待审。

## round_06 / r06

- 评审要点：本法多拿pair/Q；data×loss未正交，原始history非公平winner。
- 决策：全部接受。
- 具体改动：control/strict data×ordinary/cross-value 2×2且四格均计M64/S8 Q；三backbone native/adapter与validation winner；hard Jaccard control；独立seeds/H32/reward/checkpoint evaluator；资源/0-pilot gate。
- 改后分数：自评D10/D11/D13→4.5；待round_07。
- 未决项：2k attempted实际acceptance/steps/s待测。

## round_07 / r07
- 评审要点：history search与H32/checkpoint evaluator未计，MVP/primary边界不清。
- 决策：接受。
- 具体改动：total cap含history+value+evaluator≤1B；M16只工程smoke、M64 primary；给new-seed/H32/reward/checkpoint evaluator复用与最坏公式；lineage/near-duplicate及3backbone×4格×3seed账。
- 改后分数：自评D11/D12→4.5；待round_08。
- 未决项：full cap可能迫使缩小clusters。

## round_08 / r08
- 评审要点：synthetic→AliasBench/真机不验机制。
- 决策：接受并收窄为benchmark/supervision。
- 具体改动：sim-A生成、sim-B zero-shot；AliasBench标无pair-Q；真机near-match容差/80 roots或删除；group去重与shared guard。
- 改后分数：自评D3/D9/D15→4.5；待round_09。
- 未决项：自然迁移不作为机制证据。

## round_09 / r09
- 评审要点：synthetic自洽、1B成本、观测非identical攻击。
- 决策：接受。
- 具体改动：标题tolerance-matched reachable pairs；三backbone winner首行；独立evaluator/cost/hard-control回应与pure-benchmark降级。
- 改后分数：自评均分4.5；待round_10。
- 未决项：acceptance仍P0工程风险。

## round_10 / r10
- 评审要点：generator与Q evaluator可能共偏。
- 决策：接受。
- 具体改动：第二checkpoint/reward/H32 evaluator、一致性/分歧率门槛；rejected-pair保存双Q hashes/version/reject reason。
- 改后分数：内容PASS；待R11。
- 未决项：分歧>20%将只发布atlas。
