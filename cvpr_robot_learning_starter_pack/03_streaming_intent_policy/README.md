# 方向三：流式动作生成与短期意图建模

这个方向处理的是策略的时间结构。传统 diffusion/flow policy 先生成整个 action chunk 再执行，采样有延迟；每次重新规划又可能在多个合理动作模式之间切换，产生 inter-chunk conflict。Streaming Flow Policy 解决“何时能开始执行”，IntentVLA 解决“相邻重规划是否保持同一短期意图”。

## 三个容易混淆的问题

1. **动作多模态**：同一任务可能有绕左/绕右、不同抓取姿态等多个合理轨迹。
2. **观测混叠**：相似当前画面可能处于不同任务阶段，需要历史才能区分。
3. **采样延迟**：扩散/flow 要完成多步积分后才能输出完整 chunk，降低闭环频率。

## 分层阅读路线

### 第一层：生成式策略基础

1. **Diffusion Policy**：理解 action sequence 作为联合分布、receding-horizon control、多模态动作和迭代去噪。重点看问题设定和 action chunk 执行方式，不必先钻网络细节。
2. **Streaming Flow Policy**：重点理解“trajectory of trajectories”批评、从上一动作附近初始化、边积分边执行，以及 demonstration-stabilizing flow。
3. **IntentVLA**：重点理解 observation aliasing、history encoder、compact intent conditioning 和 AliasBench 的控制变量设计。

## 联合后的关键张力

- intent 越稳定，跨 chunk 越连续，但动态环境变化后可能反应迟缓；
- streaming 越依赖上一动作，运动越平滑，但错误动作也可能被持续放大；
- history 越长，阶段判断更准，但计算和 stale information 增加；
- 每步重估 intent 响应快，却可能重新引入 intent flicker。

## 读完应能回答

- SFP 的 flow time 与物理执行时间是什么关系？
- 从上一动作附近初始化为何仍能表达多模态行为？
- action chunk conflict 如何量化，而不仅仅看任务成功率？
- IntentVLA 的 intent 表示的是目标、技能阶段还是局部轨迹模式？
- 环境突变时，什么信号应该触发 intent reset？
- streaming policy 如何与 perception/control latency 对齐？

## 入门实践

先不要训练大 VLA。选一个 action chunk imitation baseline，记录相邻 chunk 在重叠 horizon 上的差异；加入短历史 encoder 预测 intent，观察 discontinuity 和 success；再把 chunk decoder 替换为或近似成从上一动作初始化的 flow decoder。最先验证的是时间一致性，不是大规模语义泛化。

## 退出标准

能够在一张时间轴上标清 observation、history window、intent update、flow integration、action emission、environment feedback 和 replanning，并提出至少两个动态扰动测试，就具备进入该方向的基础。

