# 讨论问题与最小原型：Streaming + Intent

## 组会问题

1. 当前任务中的不稳定是控制噪声、采样多模态，还是 task phase 判断错误？
2. intent 应每帧更新、固定若干步，还是由不确定性/事件触发？
3. 如何区分“有益的动作连续性”和“错误动作惯性”？
4. streaming flow 中每个中间状态都物理可执行吗？训练目标如何保证？
5. 如果环境突然移动目标或加入障碍，模型多快放弃旧 intent？
6. 怎样公平比较 chunk policy 与 streaming policy 的 wall-clock latency 和感知频率？

## 三个可落地选题

### A. Event-triggered intent streaming

用 change-point/uncertainty 模块决定何时更新 intent；正常执行保持慢变量，发生遮挡、目标移动或接触事件时快速刷新。

### B. Intent-conditioned flow field factorization

将 flow field 分为由 intent 控制的低频轨迹模式和由当前观测控制的高频 residual，使稳定性与反应性在结构上分离。

### C. Counterfactual intent consistency

对 aliased observation 构造具有不同历史的配对样本，要求相同当前帧在不同 intent 下产生不同动作，而同一历史的小视觉扰动保持同一 intent。

## 两天最小原型

1. 在现有 action chunk 数据上找到相似当前观测但下一 chunk 不同的样本对。
2. 训练 frame-only 与 short-history 两个小策略。
3. 测 overlap horizon 上的 chunk disagreement、jerk、成功率和扰动恢复时间。
4. 加一个最简单的 intent persistence 门控：固定 K 步或余弦变化阈值。
5. 如果稳定性提高但动态扰动恢复显著变慢，下一步必须做 event-triggered reset，而不是继续增加平滑 loss。

