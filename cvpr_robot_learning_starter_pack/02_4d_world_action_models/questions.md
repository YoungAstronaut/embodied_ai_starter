# 讨论问题与最小原型：4D WAM

## 组会问题

1. 推理期 rollout 对动作成功是否有被控制变量实验独立证明？
2. RGB、depth、semantic、correspondence 和 GFM feature 中，哪个监督最接近 manipulation 的充分状态？
3. 如果 auxiliary branch 在部署时删除，怎样证明 backbone 真的使用了几何，而不是把它隔离在 readout token 中？
4. future action token 是否看到了真实 future video/geometry，造成 teacher-forcing shortcut？
5. 世界生成质量指标与真实机器人 success 的相关性是多少？
6. 严重遮挡后，模型如何维持 object identity、任务阶段和接触历史？

## 三个可落地选题

### A. Action-centric 4D registers

register 不覆盖完整图像网格，而是由 language/action query 初始化为 object、end-effector、contact 与 support tokens；监督它们的未来 3D 状态和 relation。

### B. Persistent object memory for lightweight WAM

在 training-only geometry readout 基础上加入跨 rollout 的 persistent object slots，专门解决遮挡后的 identity inconsistency。评估应构造长遮挡和 reappearance。

### C. Adaptive world-model computation

动作持续高频输出，latent geometry 低频更新；只有在不确定性或接触事件发生时才做更完整 future prediction。比 X-WAM 更强调事件驱动而非固定异步 schedule。

## 两天最小原型

1. 从 robot video 提取 RGB latent、depth 和冻结 GFM feature。
2. 用相同小型 transformer 预测下一时刻三类 target，参数量与 horizon 对齐。
3. 冻结 predictor，比较 linear action probe、future contact probe 和 OOD object pose probe。
4. 加入 object mask，只预测任务相关区域，观察是否以更低 loss/计算获得更高 action probe。
5. 若 geometry target 只改善重建指标而不改善 action/contact 指标，应重新审视完整 4D WAM 的必要性。

