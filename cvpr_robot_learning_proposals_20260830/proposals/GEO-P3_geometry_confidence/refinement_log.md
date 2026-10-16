# GEO-P3 Refinement Log

## r00 / pre-review

- 评审要点：尚未进入独立评审。
- 决策：明确只校准几何证据，不重复通用 VLA confidence。
- 具体改动：加入 selective-risk、等 FLOPs ensemble 对照、跨域 calibration 失效与非安全声明。
- 改后分数：待 round_01。
- 未决项：coverage 与真机 trial 功效待评审。

## round_01 / r01

- 评审要点：原 router 在部署中使用未知 `L_act`，RGB fallback 与 geometry branch 不在统一事件空间；relation/frame/episode coverage 混用；target 可能退化为通用 depth error；在线输入含混。
- 决策：全部接受。主终点锁定 frame-level routing，不再跨粒度计算 AURC。
- 具体改动：用 exact-reset 三分支 short-horizon outcome 训练可部署 branch-regret risk/quantile，推理只读 `z_t`；统一三支风险定义；relation bad-event 改成“oracle 修复是否降低动作 regret”；加入大几何错但动作不变/小错却动作翻转 hard pairs；明确 4 当前帧增强、层分歧、两帧 motion 及无多视角约束；新增同标签预算最近邻表。
- 改后分数：自评 D5 3.0→4.0、D6 4.0→4.5、D9 4.0→4.5；待 round_02。
- 未决项：三分支 exact-reset 标签成本、regret horizon `H_c` 与 τ_r 的敏感性、90% frame coverage 的真实基线分布待审。

## round_02 / r02

- 评审要点：三分支风险可能只是 generic mixture-of-experts/defer；缺 selective prediction 邻域；三分支标签交互成本远高于 Platt/entropy；`B_ij` oracle repair 路径需target-only审计。
- 决策：全部接受；geometry claim仅在relation target相对generic/regret-only有独立增益时成立。
- 具体改动：加入 SelectiveNet/Learning-to-Defer、generic shared-feature router、regret-only router；逐字段写 `GT relation→offline repair→repaired action→regret→B_ij target` 且schema拒绝GT进入feature；2k/10k换算384k/1.92M env steps并给等episode/等environment-step两套公平协议；新增relation-delete≤2pp即收缩claim。
- 改后分数：自评 D3/D5由4.0→4.5、D6/D9维持4.5；待 round_03。
- 未决项：三分支short-horizon标签偏差、oracle repair定位误差和真实sim step/s/label-seconds待机制轮核算。

## round_03 / r03

- 评审要点：GT relation repair 可能 off-manifold；action disagreement 要先算三分支；branch×frame label 与 frame coverage 聚合不唯一。
- 决策：全部接受；方法定位为全分支 reliability selector并完整记账。
- 具体改动：独立 editor/decoder+reconstruction/detector gate，加入 random/valid-wrong/full-oracle placebo；给三分支→router→single action 顺序/FLOPs/p95；定义 selected-branch frame risk/coverage 与危险分支最小例；failure-type metadata 仅 evaluator。
- 改后分数：自评 D4/D5/D13→4.5；待 round_04。
- 未决项：relation editor 是否真正独立、三分支并行内存峰值与 detector-shift calibration 待审。

## round_04 / r04

- 评审要点：90% coverage不可在test调λ；q/v排序可能冲突；on-manifold需density/policy检验且placebo为主门槛。
- 决策：全部接受。
- 具体改动：独立calibration拟合冻结ε/λ；单一regret CDF导出q/v并q优先；repair加editor density/decoder/policy-latent三门槛；coverage-risk-cost同步报告。
- 改后分数：自评 D5/D13→4.5；待 round_05。
- 未决项：CDF tail calibration与coverage shift时的无重校准性能待审。

## round_05 / r05

- 评审要点：唯一 primary 应为 calibration-frozen 90% coverage selected-branch risk；需 unseen family/severity、单终点比较与 episode-cluster 功效。
- 决策：全部接受。
- 具体改动：锁 regret-only router 为最强比较器；加入 unseen corruption family/severity、50-shot独立外测、episode/task/family分层 bootstrap、25%功效；geometry-aware 必须在同一 risk 终点同时超过 generic/regret-only，success<3pp降级。
- 改后分数：自评 D8/D9/D10/D13→4.5；待 round_06。
- 未决项：90% coverage shift 下的有效样本量与 family-wise 功效待审。

## round_06 / r06

- 评审要点：regret-only少拿repair B；需structure×supervision与每法独立校准。
- 决策：全部接受。
- 具体改动：native/label-equal双表；final-regret/B×pooled/relation 2×2；同budget独立validation校准；补repair acceptance/noise曲线与资源manifest，0 pilot前不确认。
- 改后分数：自评D10/D11/D12→4.5；待round_07。
- 未决项：repair acceptance/precision需实测。

## round_07 / r07
- 评审要点：三branch账漏per-relation repair rollout，B语义可能不成立。
- 决策：保留真实regret B并全额计rollout。
- 具体改动：公式改`[3+Nvalid repairs]×S×H`；validity与router split分离；corruption cell/group split；100 snapshot repair smoke；不可负担则删除B而非换定义。
- 改后分数：自评D5/D11/D12→4.5；待round_08。
- 未决项：Nvalid relation分布未知。

## round_08 / r08
- 评审要点：LOFO/achieved coverage/stop dominance与真机规模。
- 决策：接受。
- 具体改动：LOFO与severity分表；coverage CI[.85,.95]可行条件；route/fallback conditional表；3task root blocks与共享stop，降级可靠性atlas。
- 改后分数：自评D9/D14/D15→4.5；待round_09。
- 未决项：zero-shot family calibration无保证。

## round_09 / r09
- 评审要点：D3=4，需Atlas不可删除对象。
- 决策：接受。
- 具体改动：LOFO/coverage/route/fallback Reliability Atlas；same-B pooled首行；cost/oracle/stop三攻击与B/control/OOD三段降级。
- 改后分数：自评D3/D14→4.5；待round_10。
- 未决项：R10验证非措辞升分。

## round_10 / r10
- 评审要点：conditional route均值可能掩盖repair attempts。
- 决策：接受。
- 具体改动：attempted/accepted/selected三分母、branch fallback、pipeline p95/p99/energy固定主表；root utility不升则B判负。
- 改后分数：内容PASS；待R11。
- 未决项：repair分母待pilot。
