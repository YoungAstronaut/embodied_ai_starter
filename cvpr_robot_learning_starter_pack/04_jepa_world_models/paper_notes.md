# 核心论文导读：JEPA 潜空间世界模型

## V-JEPA：只预测特征能否学好视频表示

V-JEPA 研究 feature prediction 能否作为独立的无监督视频学习目标，不依赖预训练图像 encoder、文本、负样本或像素重建。它从可见 context 预测被 mask 区域的 target encoder representation，迫使模型利用空间和时间上下文。

- 第一类 pixel reconstruction 需要建模纹理等不可预测细节，未必形成抽象语义。
- 第二类 contrastive 方法依赖负样本、augmentation 与 instance discrimination 设计。
- 第三类借助 image/text teacher 的视频模型难分辨性能来自视频预测还是外部监督。

V-JEPA 用 context encoder、EMA target encoder 和 predictor 构成非生成式预测学习闭环。它证明 frozen feature 对 motion 和 appearance task 都有效，但机器人读者必须注意：通用视频分类好，不等于 latent 对 action 可控或适合规划。

## V-JEPA 2：互联网视频表征如何变成可规划 world model

V-JEPA 2 将 action-free 预训练扩展到大规模互联网视频，再使用少量无标注机器人轨迹 post-train action-conditioned model。其机器人部分不是直接输出 policy，而是对 candidate action sequence 预测未来 latent，并使预测状态接近 image goal。

- 第一类只用机器人数据训练 world model，规模有限，视觉和常识覆盖不足。
- 第二类互联网视频表征擅长理解，却没有 action-conditioned controllable dynamics。
- 第三类像素级规划容易被背景、光照和无关细节主导 cost。

V-JEPA 2 的关键结构是“大规模 action-free representation + 小规模 action alignment”。阅读时要仔细看规划 action horizon、candidate optimization、goal cost 和 zero-shot deployment 条件。它展示了方向可行性，但低维 goal matching 是否足以处理接触与遮挡仍是开放问题。

## V-JEPA 2.1：让 JEPA 同时具备全局与 dense feature

V-JEPA 2.1 针对早期 JEPA 的 dense spatial grounding 不足，引入 dense predictive loss，使 visible 和 masked token 都接受训练信号；同时在多个 intermediate layer 施加 deep self-supervision，并统一图像/视频 tokenizer 与扩大规模。

- 第一类只监督 masked target 的方法对所有局部 token 的训练信号不均衡。
- 第二类只在最终层施加目标，可能让中间层的局部空间结构不足。
- 第三类全局视频表征适合理解，却未必适合 depth、tracking、grasping 等 dense task。

这篇对机器人方向的重要性在于，它把 JEPA 与 dense geometry/action interface 拉近。后续工作仍需验证：dense feature 是否稳定追踪同一物体，是否编码相对深度和接触，以及其提升是否在严格几何 OOD 下成立。

## LeJEPA：用 embedding distribution 重新解释防塌缩

LeJEPA 认为 JEPA 研究过度依赖 stop-gradient、EMA teacher、scheduler 等经验性机制，却缺少对“好的 embedding distribution”统一解释。它论证 isotropic Gaussian 对一类 downstream prediction risk 是理想分布，并提出 Sketched Isotropic Gaussian Regularization，以随机投影统计检验约束 embedding。

- 第一类 teacher-student JEPA 用 stop-gradient 和 EMA 防止 collapse，但结构和超参数较多。
- 第二类 variance/covariance 类正则分别修补维度退化，理论目标不统一。
- 第三类只追求 alignment 容易出现 constant 或低秩表示。

LeJEPA 将 predictive alignment 与 SIGReg 组合，强调线性复杂度、跨架构稳定和简化训练。对机器人研究，它更适合作为 action-conditioned JEPA 的稳定性工具或 ablation，而不是单独的应用贡献；还要验证 isotropic distribution 是否保留物理状态的局部度量结构。

## 联合方向：Geometry-Aware Action-Conditioned JEPA

自然的研究接口是：V-JEPA 2.1 提供时序与 dense feature，VGGT/GFM 提供明确几何，action-conditioned predictor 只预测目标、末端、接触等 task-relevant future token。LeJEPA 类正则负责稳定 embedding。真正的贡献必须落在 latent 的 controllability、geometry sufficiency 或 planning metric 上，而不能只是把两个预训练模型的 loss 相加。

