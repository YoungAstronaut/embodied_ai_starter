# 最终推荐：四方向 12 个具身机器人 Proposal

- 文献截止：2026-08-30
- 最终版本：12/12 为 r10
- 独立评审：round_01…round_11；每份 Proposal 完成 round_01…round_10 共 10 次实际 refine
- 认证结果：12/12 PASS；硬门槛为每维≥4.0、均分≥4.30、D3/D5/D6/D9≥4.5、无 fatal

> 重要边界：下列分数认证的是**研究问题、机制、信息可见性和预注册实验合同**，不是实验结果。当前 12 项均未执行正式 pilot；MVP 成本是 proposal 中的预注册 gate/上限，需以第一阶段实测吞吐、acceptance、ICC 和存储重算。认证不代表录用、真机安全保证或 2026-08-30 之后的文献覆盖。

## 方向一：Geometry-Aware VLA

推荐顺序：**GEO-P2 → GEO-P3 → GEO-P1**。

| 顺序 | ID | 一句话定位 | 关键最近邻/最危险比较器 | 最小验证成本 | 最大风险 | 最终分数 |
|---:|---|---|---|---|---|---:|
| 1 | GEO-P2 | 用候选动作条件化的 time/mode/normal 接触转移场，检验显式接触事件是否比同标签 latent failure monitor 更能排序动作。 | ContactGuard-label-equal；ContactWorld、ViTacWorld | 先做 200-snapshot support/吞吐 smoke；通过后 2k snapshots×8×4×16=1.024M env steps，2×A100 级 MVP | hand-engineered ontology 或 sim→real event semantics 主导；fallback 过高会降级为 ontology/router | 4.40 |
| 2 | GEO-P3 | 建立 LOFO Geometry Reliability Atlas，在 achieved coverage 可行条件下选择 full/coarse/RGB/stop 分支。 | same-B generic pooled/regret-only router；UAOR、VLA Calibration | 100-snapshot repair smoke；正式 2k 档基础三分支 384k env steps，另加 `N_valid_repairs×64` steps/snapshot | per-relation repair rollout 昂贵，三分支部署不省算，stop/fallback 可能解释收益 | 4.37 |
| 3 | GEO-P1 | 用双独立 utility evaluator 的 exact-intervention pair protocol，回答 relation tokens 是否超过 generic deconfounding。 | VGA+Cofact/CAST label-equal winner；MECo-WAM、ST-VLA | 1k attempted acceptance smoke；通过后≥2k accepted pairs=16.384M env steps | checker/evaluator 共偏、candidate support 和 foundation pretraining 不可审计 | 4.37 |

## 方向二：4D World–Action Models

推荐顺序：**WAM-P3 → WAM-P1 → WAM-P2**。

| 顺序 | ID | 一句话定位 | 关键最近邻/最危险比较器 | 最小验证成本 | 最大风险 | 最终分数 |
|---:|---|---|---|---|---|---:|
| 1 | WAM-P3 | 从 nominal action-realization residual 更新 functional predictive belief，主测第 2 次被动交互后的 held-out-action regret。 | deploy-equal Robot-Factored+PEARL/RMA、generic recurrent mixture；CoCo | 200-state 64-vs-1024 nested-sample bias/shortcut pilot；2×A100、约4天级 smoke | residual 只编码视觉、controller 或 contact-localization error；t0 泄漏会迫使改称 visually conditioned dynamics | 4.40 |
| 2 | WAM-P1 | 发布 Occlusion-ID：按 identifiable/partial/simulator-certified ε-symmetric strata proper-score referent belief，而非强猜身份。 | L11：action/contact JPDA+posterior-marginal controller；OA-WAM、POT、MHT | 先跑 generator/proof-computable 与 detector/beam memory smoke；原计划 2×A100、约3天级 MVP | 方法可能与 JPDA+WAM 近同构，certificate 不等于现实可识别，4–6实例超出M=4 | 4.40 |
| 3 | WAM-P2 | 在 simulation 构造 CRN paired continuation-value targets，学习非 myopic 的按需世界想象 gate。 | paired-myopic VOC 与 validation winner；When-to-Trust、CheckVLA、PonderNet/ACT | 100-epoch throughput smoke；5k档 S16 约10.24M env steps、640k records，4×A100 上限96h | 离线 target 构建昂贵、continuation-positive 可能稀少，真机无法验证反事实 target | 4.40 |

## 方向三：Streaming Intent / Policy

推荐顺序：**STR-P2 → STR-P1 → STR-P3**。

| 顺序 | ID | 一句话定位 | 关键最近邻/最危险比较器 | 最小验证成本 | 最大风险 | 最终分数 |
|---:|---|---|---|---|---|---:|
| 1 | STR-P2 | 为 standard conditional chunk flow 训练 deadline-valid complete-chunk 1/2/4/8-NFE exits，并以 age-aware scheduler 原子提交。 | standard multi-exit+same chance scheduler；RTC、DMPO；SFP仅跨范式 | 先完成跨进程 cutoff replay 与每硬件≥100 trace blocks；2×A100、约3天级系统 MVP | 可能退化为 consistency distillation+runtime engineering；host-sync与fallback可能主导 | 4.50 |
| 2 | STR-P1 | 把 change evidence 与 paired intervention value 分开，判断事件后“是否值得 reset”，而不是再做一个 change detector。 | label-equal pure-ΔQ/change/generic gate；BOCPD、CheckVLA、PACE、REMAC | 每event 5×S8×H16=640 target steps；先每family 50 events，1×A100、约2天级 smoke | 稀有事件功效不足，ΔQ shard 可能暗带event标签，RMRT tube敏感 | 4.40 |
| 3 | STR-P3 | 构造 tolerance-matched、双可达但 action-value 冲突的 history-alias pairs，并用双 evaluator 审计跨历史监督。 | IntentVLA、Remember Smarter、causal Transformer 的 label-equal winner | 2k attempted、M16/S4 feasibility；若2k均accepted，上限4.096M value steps；primary必须M64/S8 | acceptance低、总hard cap 1B steps，synthetic-to-natural transfer有限 | 4.40 |

## 方向四：JEPA World Models

推荐顺序：**JEP-P2 → JEP-P3 → JEP-P1**。

| 顺序 | ID | 一句话定位 | 关键最近邻/最危险比较器 | 最小验证成本 | 最大风险 | 最终分数 |
|---:|---|---|---|---|---|---:|
| 1 | JEP-P2 | 用 transient ordered typed contact transactions 避免 endpoint cancellation；JEPA 和 typed executor 均可被独立删除。 | NRI×typed executor；C-SWM、OA/POT、ContactWorld | 200-snapshot event/timestamp smoke；2k档 1.024M env steps，2×A100、约3天级 MVP | rich labels而非representation带来收益，closed ontology与timestamp误差限制外推 | 4.40 |
| 2 | JEP-P3 | 建 ExoManip balanced action×exogenous factorial benchmark，并以 learned-q 检验 distributional interaction objective。 | non-JEPA same-objective、CoCo、Sawada、MDN/RSSM | 500-group K4/8/16/32 convergence pilot=480k outcomes、H16即7.68M env steps | factorial到自然 `μ_shift` 不一致，q失校会触发保守fallback，JEPA可能只是branding | 4.40 |
| 3 | JEP-P1 | 建 ActMetric-3D local contact-rich matched-outcome pseudometric/assignment benchmark，对照 Action-Bisim recursive target。 | Action-Bisim native+same-data adapter；non-JEPA+same metric | 2k states×16 actions×S32×H16=16.384M env steps，240k pairwise OT records | 理论核心已被 Action-Bisim 覆盖，canonicalizer shortcut与跨embodiment role coverage可能主导 | 4.37 |

## 跨方向 MVP 启动顺序

按“最快得到决策性证据、复用基础设施、避免先投入最昂贵target”为原则：

1. **STR-P2**：先做纯runtime/serialization/trace vertical slice，最少依赖新标签，评分最高。
2. **GEO-P2**：200-snapshot contact extractor+label-equal ContactGuard smoke，能快速判ontology是否有信息增益。
3. **STR-P1**：每family 50-event盲评与target-shard审计，先排泄漏和稀有event问题。
4. **JEP-P2**：复用GEO-P2的contact ontology、timestamp与safety guard，测试ordered transaction是否超endpoint。
5. **WAM-P3**：200-state nested-sample与三shortcut联合负控，先判断residual是否真的携带dynamics信息。
6. **GEO-P3**：100-snapshot repair smoke，先测valid repair acceptance和三分支成本。
7. **WAM-P1**：先交Occlusion-ID generator/proper-score/proof-failure，不立即训练完整WAM。
8. **WAM-P2**：100-epoch吞吐与continuation-positive prevalence，未过gate不生成5k target。
9. **GEO-P1**：1k attempted pair acceptance与双evaluator分歧率，未过35%不扩。
10. **JEP-P3**：500-group K convergence和learned-q calibration，再决定full factorial grid。
11. **JEP-P1**：S32/OT成本高，先在前述contact schema稳定后启动。
12. **STR-P3**：最后启动高成本history search/Q evaluator；先复用成熟的root lineage、hash与independent evaluator工具。

## 最终执行建议

如果只选择一个主攻题，优先 **STR-P2**：设计成熟度最高（4.50），最小验证不依赖大规模oracle target，负结果仍能形成可复用runtime benchmark。如果希望更偏视觉/机制论文，优先 **GEO-P2**；如果希望更偏world-model adaptation，优先 **WAM-P3**；如果希望以数据集/benchmark切入JEPA，优先 **JEP-P2**。

每个MVP必须先填正文预注册的actual-pilot字段，再根据acceptance、ICC、吞吐和安全约束决定是否进入confirmatory阶段。任何关键secondary未过门槛，应使用各Proposal已写好的降级标题并删除method/control/transfer claim，不能以另一个OOD指标替代primary。
