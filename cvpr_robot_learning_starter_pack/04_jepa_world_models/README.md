# 方向四：JEPA 潜空间世界模型与机器人规划

JEPA 的出发点是：对未来像素逐项重建会浪费容量拟合不可预测细节，而世界模型真正需要预测的是抽象、稳定且能服务下游任务的 representation。机器人方向因此关心一个更严格的问题：什么 latent 既能被动作条件预测，又保留接触、遮挡、对象运动和任务进度，并能用于规划或动作解码？

## 演进主线

1. **V-JEPA**：证明仅做 masked latent feature prediction，也能学习视频中的运动与外观表征。
2. **V-JEPA 2**：扩大到互联网规模视频，并以少量机器人视频训练 action-conditioned latent world model，用 image-goal latent planning 做机器人操作。
3. **V-JEPA 2.1**：通过 dense predictive loss、deep self-supervision 等设计改善局部空间结构与 dense feature。
4. **LeJEPA**：从 embedding distribution 和 anti-collapse 角度提出更简化、理论化的 JEPA objective；它是预训练目标，不直接等于机器人 world model。

## 分层阅读路线

### 第一层：理解 JEPA 与生成模型的差异

1. **V-JEPA**：重点看 context encoder、target encoder、predictor、masking strategy 与 stop-gradient/EMA；理解预测的是 target feature 而非 pixel。
2. **V-JEPA 2**：重点看互联网视频预训练与 robot post-training 的分工，以及 V-JEPA 2-AC 如何以 candidate action 预测 goal latent 并进行 planning。
3. **V-JEPA 2.1**：重点看 dense predictive loss 为什么让 visible 与 masked token 都接受信号，deep self-supervision 如何改善 intermediate feature，以及机器人 grasping 提升。
4. **LeJEPA**：先读动机、SIGReg 直觉和主 ablation，理解 collapse、dimension collapse 与 isotropic Gaussian；数学证明可放在第二遍。

## 需要掌握的判别标准

- **可预测性**：future latent 是否比 pixel 更容易预测，是否忽略不可控背景噪声。
- **充分性**：latent 是否保留完成动作所需的信息，而非只保留语义类别。
- **可控性**：不同 candidate action 是否导致可区分的 predicted latent。
- **度量性**：latent distance 是否与 task progress、goal achievement 和 collision 风险一致。
- **密集性**：局部 object/contact token 是否稳定，而不只是全局 video embedding 好。
- **防塌缩**：表示是否保持足够维度和可分性，正则与 teacher 机制是否必要。

## 读完应能回答

- JEPA 与 masked autoencoder、contrastive learning、video diffusion 的训练目标分别是什么？
- target encoder 为什么需要 stop-gradient/EMA，LeJEPA 试图替代哪些 heuristic？
- V-JEPA 2 的 action-conditioned planning 优化什么 latent cost？
- dense feature 变好为何可能改善抓取？这是否等同于几何理解？
- latent distance 何时会忽略对控制关键的小位姿差异？
- 如何把 VGGT 几何 token 与 V-JEPA temporal token 对齐，而不牺牲语义或动态？

## 入门实践

先用公开 checkpoint 离线提取连续机器人帧的 V-JEPA 2/2.1 feature。冻结 encoder，只训练一个小 predictor，根据当前 feature 和 action 预测未来 feature。做三项检验：action retrieval、goal ranking 和 object/contact linear probe。如果 feature prediction loss 很低但 action retrieval 接近随机，说明 latent 对动作不敏感，暂时不适合直接用作 world state。

## 退出标准

能从信息内容、训练稳定性和规划用途三个层面解释 V-JEPA、V-JEPA 2、V-JEPA 2.1、LeJEPA 的差别，并能设计一个验证 latent controllability 的实验，就达到入门标准。

