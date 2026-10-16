# 方向一：几何感知的 VLA 与机器人策略

这个方向的核心并不是“给 VLA 增加深度”，而是识别哪一种空间信息真正决定动作。机器人需要的不只是场景重建，而是目标物体、末端执行器、接触区域、可达空间、遮挡后的物体状态及其相对运动。当前研究正在从显式 3D 输入，转向几何基础模型蒸馏、几何 backbone 和 action-relevant feature specialization。

## 先建立五个概念

1. **几何输出**：depth、point map、camera、track 是可解释的 3D 量，VGGT 属于这一层。
2. **场景级几何 token**：VGGT-Ω 用 register attention 将每帧 registers 训练成 scene tokens，并验证冻结 token 可以直接增强 VLA。
3. **几何表征对齐**：中间 token 可能编码空间结构，但未必能直接解释；Spatial Forcing 通过 feature alignment 将这类表征注入 VLA。
4. **几何策略基模**：不再把 GFM 当辅助 teacher，而是直接把它改造成时序和动作 backbone；GAM 属于这一层。
5. **动作相关几何**：只强化对当前任务有用的 object、contact、motion patch；GuidedVLA 给出了 attention specialization 的一种入口。

## 分层阅读路线

### 第一层：必读，建立主线

1. **VGGT**：先看 Figure 1、Section 3 和任务定义，理解 camera、depth、point map、track 的区别。实验只需看多视图重建和 feature backbone 部分。
2. **VGGT-Ω**：重点看 register attention、单 dense head + 多任务 loss、动态视频数据引擎，以及 scene tokens 接入 OpenVLA-OFT 的实验。它代表“重建预训练产生可复用空间 token”。
3. **Spatial Forcing**：重点看中间层对齐的位置、teacher 表征、alignment loss 与 depth probing。它代表“训练期 teacher，推理期无显式 3D”。
4. **Geometric Action Model**：重点看 GFM 如何在中间层被拆分，future predictor 如何接入，以及 geometry/action 如何共享 backbone。它代表“直接以 GFM 为基模”。
5. **GuidedVLA**：重点看 object grounding、spatial geometry、temporal skill logic 三类 attention head 的监督来源，以及 specialized factor quality 与 action success 的关系。

### 第二层：理解扩展问题

5. **GEAR-VLA**：重点看 coarse-to-fine action、semantic-aligned 3D integration 和 embodiment canonicalization。不要被系统规模遮住，应逐一分清每个模块回答哪一种泛化失败。
6. **Vision Transformers Need Registers**：只作为 token 机制背景。原始 register 用来承接 ViT 内部全局计算、消除高范数背景伪影；它不是空间监督，也不是 3D token。

## 读完应能回答

- feature alignment 与显式 depth supervision 的信息差是什么？
- VGGT-Ω 的 scene tokens 已经能提升 VLA，后续工作怎样证明 token 是 task-relevant，而非仅仅增加容量或正则化？
- teacher feature 更强是否必然意味着 action-relevant？
- 单目、少视图与多视图几何在机器人数据中分别有哪些可用条件？
- 任务语言如何决定应该选择哪些几何 token？
- 精确 depth、3D correspondence、contact relation 三者中，哪个与 manipulation success 更直接？
- 去掉几何 teacher 后，推理期为什么仍能保留空间能力？

## 适合快速入门的实践

先运行 VGGT 与 VGGT-Ω 官方 demo，对同一机器人片段比较 depth、camera、VGGT 中间特征和 VGGT-Ω scene tokens；再冻结一个现有 VLA 的视觉编码器，训练轻量投影头。不要立即做完整控制训练，先做三个 probe：深度、末端-目标相对位姿、接触区域分类。若 scene token 只提升 depth probe，而动作相关 probe 不提升，说明“通用场景几何”仍不等于“动作相关几何”。

## 退出标准

当你能画出五条不同管线——3D input VLA、frozen scene-token injection、GFM teacher alignment、GFM backbone policy、task-conditioned geometry selection——并能说明它们训练期和推理期的成本差异，就已经具备进入选题讨论的基础。
