# 一周学习与定方向计划

这一周的产出不应只是“大家都读了一些论文”，而应是一页可证伪的研究假设、一张方法草图和一个最小实验。建议每天安排 2-3 小时共同阅读，另留 1-2 小时做代码或数据检查。

## Day 1：统一术语与评判标准

阅读本资料包总览和四个方向的 `README.md`，明确以下区别：

- 3D input、geometry feature alignment、geometry prediction 三者不是一回事；
- world model 的作用可能来自训练期 predictive representation learning，也可能来自推理期 rollout；
- action chunk 的多模态性、observation aliasing 和扩散采样延迟是三个不同问题；
- JEPA 预测 target representation，不等于预测 RGB，也不天然等于可规划的 world state。

当天产出：每位合作者给四个方向分别打 1-5 分，评价新意、资源适配度、实验周期和个人兴趣。

## Day 2：方向一和方向二

必读：按 VGGT→VGGT-Ω 的顺序对照阅读，再读 Spatial Forcing、Geometric Action Model、GeoSem-WAM 和 WAM4D。快速浏览 GEM-4D 和 X-WAM 的方法图。

当天讨论：

1. 几何基础模型应该作为 teacher、backbone 还是 inference module？
2. 完整深度是否是机器人动作真正需要的监督？
3. 如何证明提升来自 action-relevant geometry，而不是额外参数或额外数据？

当天产出：画出至少两个候选模型的数据流，并明确训练期与推理期保留的模块。

## Day 3：方向三和方向四

必读：Streaming Flow Policy、IntentVLA、V-JEPA 2、V-JEPA 2.1。基础不熟时先快速阅读 Diffusion Policy 和 V-JEPA。

当天讨论：

1. streaming action 的快响应与 intent persistence 是否存在矛盾？
2. 哪一种 latent distance 真能反映机器人任务进度？
3. action-conditioned future feature prediction 是否比直接行为克隆提供额外信息？

当天产出：一个时间轴图，标出 observation、history、intent、flow integration、action execution 和 replanning 的时序。

## Day 4：代码与数据可行性审计

对排名前两位的方向检查：

- 是否已有可运行的官方代码与 checkpoint；
- 当前 GPU 能否加载 backbone；
- LIBERO、RoboTwin、DROID 或自有数据是否已就绪；
- 最强基线是否可复现；
- 训练、推理和评估预计需要多少天；
- 没有真实机器人时，结论是否仍足够完整。

当天产出：两张工程清单，每项标注“已有、两天内可得、未知、阻塞”。

## Day 5：最小原型

只实现能验证核心机制的一刀：

- 几何 VLA：冻结策略和几何 teacher，训练一个 task-conditioned feature adapter，并做 depth/contact probe；
- 4D WAM：在同一 backbone 上比较 RGB、depth、feature 三种 training-only future supervision；
- Streaming + Intent：在 action chunk 数据上加入 history intent，并测 inter-chunk discontinuity；
- JEPA：冻结 V-JEPA/VGGT 特征，训练轻量 action-conditioned predictor，测未来特征预测和 action retrieval。

当天产出：至少一条 loss 曲线、一张定性图或一个小表。即使结果为负，也要记录失败原因。

## Day 6：形成 CVPR 论证闭环

为两个候选方向分别写四句话：

1. 现有方法在什么可观察条件下失败？
2. 我们认为缺失的状态、监督或时序机制是什么？
3. 我们的模块怎样只补上这个缺口？
4. 哪个实验可能推翻我们的假设？

当天产出：每个方向一页 proposal，禁止只写“首次结合 A 和 B”。

## Day 7：决策

按以下权重决策：问题重要性 25%，与最新工作的差异 25%，两个月内可形成结果的概率 25%，数据与算力匹配 15%，团队兴趣 10%。最终只保留一个主方向和一个低成本备选方向。

最终产出：研究假设、方法框图、最小实验、三条主要 baseline、三个关键 ablation，以及未来两周的执行人和时间表。
