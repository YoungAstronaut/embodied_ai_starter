# 四个方向的选题比较

| 方向 | 核心问题 | 最小方法单元 | 主要实验 | 资源成本 | 最大风险 | 适合的论文叙事 |
|---|---|---|---|---|---|---|
| 几何感知 VLA | 策略真正需要哪种几何 | task/action-conditioned 几何选择或对齐 | OOD 物体、背景、相机、遮挡与精确操作 | 中 | 容易退化为“再加一个几何 loss” | action-relevant geometry，而非通用深度 |
| 4D WAM | 几何应在训练期还是推理期存在 | future geometry/feature readout | 动作成功、几何一致性、推理延迟 | 高 | 视频模型训练重，基线更新快 | structured predictive supervision 或显式 imagination 的必要性 |
| Streaming + Intent | 如何兼顾快响应与跨 chunk 稳定性 | history intent + streaming flow | aliasing、动态扰动、平滑度、延迟 | 中低 | 容易只得到工程性平滑提升 | 部分可观测下的实时生成式控制 |
| JEPA 世界模型 | 什么 latent 可预测且可用于规划 | action-conditioned dense latent predictor | 未来预测、规划、probe、控制成功 | 中高 | latent metric 与控制效果未必相关 | non-generative predictive world representation |

## 建议优先级

如果团队已有 VLA 训练框架和几何模型 checkpoint，优先做“task-relevant geometric latent for VLA”。它最贴近 CVPR 的视觉表示问题，又能用机器人任务验证价值。

如果团队希望一到两周看到闭环结果，优先做“intent-consistent streaming policy”。它不依赖大规模视频生成预训练，失败模式和评估指标都比较明确。

如果已有视频 DiT/WAM 代码与较强算力，可以做“training-only action-centric 4D supervision”，但必须避开 GeoSem-WAM 和 WAM4D 已经覆盖的通用 depth/semantic readout。

JEPA 方向适合有自监督视频或规划积累的团队。它的上限很高，但需要先证明 latent 中保留了接触、遮挡和可控动态，而不是只获得更好的通用视觉特征。

## 共同的评审追问

- 增益是否来自额外数据、teacher 或参数，而不是所声称的机制？
- 表征 probe 更好，是否真的导致 action success 更高？
- 是否在严格 OOD 设置下验证，而不是训练分布附近的平均分提升？
- 推理期延迟、显存和控制频率是否公平报告？
- 方法是否只在某一个 VLA/WAM backbone 上有效？
- 对遮挡、相机变化、任务阶段混淆和动态扰动的失败分析是否足够具体？

