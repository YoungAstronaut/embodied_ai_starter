# 核心论文导读：Streaming + Intent

## Diffusion Policy：action chunk 生成的基础范式

Diffusion Policy 将 visuomotor policy 表述为条件去噪过程，在动作序列空间中建模多峰分布，并以 receding horizon 重复规划和执行。它解决的是行为克隆中回归均值和复杂动作分布的问题，但迭代采样会增加控制延迟，完整 chunk 的生成也与执行时间分离。

- 第一类确定性回归策略容易在多种合理动作之间取平均，产生不可执行轨迹。
- 第二类逐步自回归策略可能累积误差，也难并行表达整段动作的协调结构。
- 第三类生成整段 action chunk 的扩散策略表达力强，但必须等待若干去噪步骤。

这篇论文应作为术语与 baseline 学习，而不是当前选题贡献。需要重点理解 observation horizon、prediction horizon、action horizon 三者的区别。

## Streaming Flow Policy：把动作轨迹本身当成 flow trajectory

SFP 的核心批评是普通 diffusion/flow policy 实际上生成“动作轨迹的采样轨迹”：每个去噪中间状态都是一整条候选 action trajectory，绝大多数被丢弃，机器人只能等待最终样本。SFP 从上一动作附近的窄高斯开始积分，将连续 flow state 直接解释为依次执行的动作。

- 第一类 chunk-based diffusion 表达多模态，但 sampling 完成前不能执行。
- 第二类只减少 denoising steps 的加速方法仍保持 chunk 生成结构，控制与采样没有真正统一。
- 第三类从 arbitrary noise 开始的 flow 与真实动作流形距离远，早期中间状态不可执行。

SFP 通过近 last action 初始化和稳定到 demonstration trajectory 的 flow training，让中间积分结果可执行并适配 receding horizon。阅读时应检查控制频率、integration step 与 action step 的对应，以及 perturbation 后从上一动作启动是否会形成错误惯性。

## IntentVLA：历史用于消除短期观测混叠

IntentVLA 观察到机器人示范中，相似的当前视觉语言观测可能对应不同 task phase、recent context 或短期意图。frame-conditioned VLA 每次独立采样 action chunk，因而会在相邻规划周期选择不同模式，造成冲突和抖动。

- 第一类 frame-conditioned chunk policy 忽略 recent history，在部分可观测环境下无法识别阶段。
- 第二类只在输入端堆叠更多帧可能计算昂贵，也未形成紧凑、可持续的 intent state。
- 第三类单次 chunk 内部虽然平滑，却没有跨 chunk 的模式一致性约束。

方法用近期视觉历史编码 compact short-horizon intent，再条件化 action chunk generation；AliasBench 通过匹配训练数据和环境，专门隔离 observation aliasing。其最值得复用的不只是模块，而是问题与 benchmark 设计：应明确哪些 observation 是 aliased、正确动作如何依赖历史，以及稳定性如何量化。

## 自然结合点：Intent-Consistent Streaming Policy

两篇最新工作的结合不应只是把 intent vector 拼到 SFP 输入。更完整的研究问题是：在持续输出动作的同时，怎样以事件驱动方式维护和更新短期意图。候选机制包括 intent posterior、change-point detector、uncertainty-triggered reset，以及对 flow field 的慢变量/快变量分解。核心实验必须同时展示稳定性和反应性，不能只展示轨迹更平滑。

