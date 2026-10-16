# 讨论问题与最小原型：JEPA

## 组会问题

1. JEPA 忽略不可预测细节的能力会不会同时丢掉精细抓取所需的小位姿差异？
2. action-free 视频预训练获得的运动 prior，如何与机器人动作空间对齐？
3. latent distance 是否满足 goal planning 所需的局部单调性？
4. dense predictive loss 改善的是语义定位、深度，还是 correspondence？
5. LeJEPA 的 isotropic Gaussian 是否与物理状态流形冲突？
6. 如何证明 predicted future feature 是因 action 改变，而不是只按视觉惯性外推？

## 三个可落地选题

### A. Action-sensitive dense JEPA

增加对比式 controllability 约束：同一状态下不同动作的 future token 必须在受影响区域可分，而不受影响背景保持一致。

### B. Geometry-grounded JEPA planning metric

将 V-JEPA dense feature 与 VGGT point/track 对齐，学习对相对位姿与接触敏感、对纹理和背景不敏感的 goal distance。

### C. Object-centric latent world model

从 dense token 聚合 persistent object/contact slots，预测其 action-conditioned future，专门处理遮挡和长 horizon identity。

## 两天最小原型

1. 用公开 V-JEPA 2/2.1 checkpoint 提取一个小型 robot dataset 的连续帧 feature。
2. 训练 `z_t, a_t -> z_{t+1}` 的两层 predictor。
3. 做 action retrieval：给定 `z_t, z_{t+1}` 选择真实 action 与负 action。
4. 做 goal ranking：正确动作 rollout 是否比随机动作更接近目标帧 latent。
5. 比较 global token、dense token、object-masked dense token 和 VGGT feature。
6. 若预测 loss 很好但 action retrieval/goal ranking 很差，说明表征主要学到视觉惯性，不能直接支撑选题主张。

