# 讨论问题与最小原型：几何感知 VLA

## 组会问题

1. 当前策略失败是因为不知道绝对深度，还是因为不知道目标与末端的相对关系？
2. 如果把背景区域的 depth 预测得更准，动作是否会更好？如果不会，应该怎样定义 task-relevant geometry？
3. VGGT 的 camera、point map、depth、track、中间 feature，与 VGGT-Ω 的 scene tokens，哪一种最适合做 teacher 或策略输入？
4. 语言条件应该进入 teacher selection、student attention，还是只进入 action expert？
5. 监督 attention head 是否真的改变因果决策，还是只让可视化更漂亮？
6. 如何构造 controlled benchmark，分别改变纹理、相机、物体姿态、遮挡和 embodiment？

## 三个可落地选题

### A. Task-conditioned geometric token selection

语言和 action query 从 GFM dense token 中选出目标、末端和潜在接触区域，只蒸馏这些 token。与 full feature alignment 比较动作成功率、probe 和计算量。

### B. Contact-centric geometric forcing

用未来 contact/near-contact region、relative pose 或 3D track 监督中间表征，不追求完整深度。关键实验是：相同 teacher 和训练量下，contact supervision 是否优于 dense depth。

### C. Geometry layer routing

比较 GFM 不同层对语义、深度、track 和 action 的贡献，用任务条件动态组合浅层局部几何与深层全局结构。贡献应是机制与分析，而不是简单 layer fusion。

## 两天最小原型

1. 选 200-1000 条机器人短片，离线提取 VGGT 中间 token、depth、track，以及 VGGT-Ω scene tokens。
2. 冻结现有视觉 encoder，训练 linear/MLP adapter。
3. 评估 depth probe、目标-末端相对位置、接触二分类和下一动作 retrieval。
4. 比较 all-patch alignment、object-mask alignment 和随机 patch alignment。
5. 如果 object/contact 选择没有明显优于全局对齐，暂缓把它升格为主方向。
