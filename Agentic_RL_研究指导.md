# 长程 Agentic RL 的两类训练偏差

## 异步轨迹一致性与跨阶段能力合并

> 以 GLM-5/GLM-5.2 配套工作与 DeepSeek-V4 技术报告为起点的研究指导
>
> 版本：2026-07-20

## 执行摘要

长程 Agentic RL 的核心难点，不是简单地把 PPO 或 GRPO 搬到更长的序列，而是同时解决两类分布漂移：

1. **轨迹层面的分布漂移**：交互经验在进入 learner 时，是否仍然来自可识别的行为策略，是否保留了正确的环境状态，是否混入了不可学习的环境失败，以及中断恢复是否改变了样本分布。[1-11]
2. **能力层面的分布漂移**：Reasoning、Coding、Agent 和 General Alignment 等阶段分别优化后，最终策略能否吸收新能力而不覆盖旧能力。[1-2,13-17]

本文据此把后续研究压缩为两个问题：

- **RQ1：异步生成、环境故障和中断恢复共同存在时，一条长轨迹何时仍然是合法且有效的学习样本？**
- **RQ2：多个训练阶段或专家策略形成后，如何通过 on-policy distillation（OPD）等方法合并能力而不退化？**

这两个问题应分别研究，但共享同一评价原则：不能只报告最终 benchmark 分数，还必须报告轨迹新鲜度、有效样本利用率、训练稳定性、旧能力保留率和单位计算成本。[5-9,13-17]

---

## 1. 文档定位与证据规则

### 1.1 研究边界

本文不再把“轨迹长度、环境噪声、off-policy、SFT/RL 协调、熵下降”等现象并列成多个松散方向，而是把它们纳入两个因果问题：

- 一条轨迹何时仍然可学；
- 多个阶段形成的能力如何合并。

上下文压缩、reward shaping、课程学习和环境扩展只有在能够解释上述两个问题时才进入研究范围。[3-4,10-12]

### 1.2 来源表述说明

GLM-5.2 模型卡引用的是 GLM-5 技术报告；SAO 与 CompactionRL 两篇配套论文明确声明其方法用于 GLM-5.2。因此，本文使用“GLM-5 报告与 GLM-5.2 配套工作”这一表述，不把 GLM-5 报告中的全部机制直接写成 GLM-5.2 的独立消融结论。[1,3-4]

### 1.3 证据分层

| 证据层级 | 可以支持的结论 | 本文处理方式 |
|---|---|---|
| A：控制实验或理论分析 | 给定模型、任务和超参数下的因果效果 | 用于提出主要假设，同时保留外推边界 |
| B：大规模技术报告 | 真实训练管线采用了某项设计，且具备工程可行性 | 不等同于独立消融，不直接宣称普适最优 |
| C：新近预印本或边界论文 | 反例、机制解释和待复现实验 | 用于暴露冲突，不能单独支撑强结论 |

**写作规则**：下文凡是对已有系统、实验结果或机制做事实判断，均给出论文引用；没有被论文直接验证的内容统一标为“研究假设”“研究建议”或“待验证”。

### 1.4 两类漂移的统一视角

| 层次 | 漂移来源 | 直接风险 | 核心观测量 |
|---|---|---|---|
| 轨迹层 | policy lag、跨版本生成、环境失败、抢占恢复、压缩边界 | 行为策略不可识别、错误归因、梯度偏差、样本浪费 | staleness、ratio/KL、clip/mask、故障标签、恢复路径 |
| 能力层 | 顺序 RL、多专家训练、teacher mixture、蒸馏阶段与散度 | 遗忘、能力干扰、模式坍缩、只压缩不纠错 | 旧任务保留率、最差域下降、teacher gap、token/成功成本 |

---

## 2. 核心问题一：异步轨迹何时仍然可学习

### 2.1 研究问题 RQ1

> 当一条长轨迹跨越多个策略版本、环境状态和系统中断时，learner 如何识别真实行为策略、排除非策略失败，并在吞吐与偏差之间选择可验证的更新规则？

这个问题比“旧轨迹能否复用”更严格。轨迹的新鲜度只描述生成时间差，不能单独说明：

- 产生每个 action 的策略是否可识别；
- 恢复后的环境状态是否与中断前等价；
- 失败来自策略还是工具、网络或 sandbox；
- token、turn、segment 或 trajectory 哪个才是合理的优化单位。[1-5,7,9-11]

### 2.2 从同步屏障到异步偏差

长序列和多轮工具调用具有明显尾延迟，完全同步的 rollout-train 交替会让训练资源等待最慢样本。AReaL 通过生成与训练解耦、可中断生成和 replay buffer 提升并行度；Asynchronous RLHF 在摘要、数学和通用对话设置中报告了同等质量下的训练加速，但不同目标对 off-policy 数据的鲁棒性并不相同。[5-6]

因此，“提高吞吐必须接受强异步”并不是唯一选择。RolloutPipe 保持固定权重和完整 group 的 on-policy 语义，通过 group pipeline 与优先调度重叠 rollout 和训练，并在其 1.7B、四类推理任务设置下缩短总时长、降低 trainer 等待比例。[8] 这一结果给出重要对照：应先判断调度是否能够消除系统空泡，再判断是否值得引入 off-policy 修正。

Staleness-Learning Rate Scaling Laws 把异步 GRPO 的单步代理梯度偏差刻画为随最大 lag `S` 与学习率 `η` 的乘积增长，并指出稳定区间同时受局部 stale-rollout 条件和训练窗口内累计漂移约束。该结论建立在数学推理、二元可验证奖励和有限模型规模上，不能直接替代多轮 Agent 环境实验，但它说明“只设置最大 staleness 阈值”缺少学习率与更新幅度的信息。[7]

### 2.3 行为策略语义不是实现细节

GLM-5 报告在异步 Agent RL 中记录 rollout token 与 log-probability，采用直接双边重要性采样，并屏蔽偏离信任域的 token；SAO 进一步使用单 rollout 取消 GRPO 的组内等待，并通过冻结 critic attention、skip-observation GAE 等机制控制方差。[1,3]

Missing Old Logits 对这类近似提出了更严格的语义区分：rollout-policy ratio 可以修正训练与推理实现差异，却不自动恢复 PPO 所需的旧训练策略；当 exact old logits 缺失时，discrepancy correction 与 staleness correction 是两件不同的事。该论文比较了 snapshot、独立 old-logit model、暂停恢复计算和 EWMA 等方案，并在 agentic benchmark 上展示了修正精度与系统成本的权衡。[9]

**关键冲突**：GLM/SAO 路线把 rollout log-probability 视为可用的行为代理；Missing Old Logits 则指出它不一定恢复 proximal policy 的完整语义。[1,3,9] 后续研究不应只比较最终分数，而应直接测量行为策略重建误差及其对 clip、mask 和梯度方向的影响。

### 2.4 中断恢复与环境故障改变数据分布

DeepSeek-V4 使用 token 级 write-ahead log、KV cache 保存与 sandbox trajectory log 恢复被抢占任务。报告指出，从头重新生成未完成请求会使短响应更容易幸存，从而引入长度偏差；对非幂等工具操作，重放已缓存结果比重新执行更安全。[2]

GLM-5 则记录失败原因，排除 sandbox 崩溃等非策略失败，并按策略版本丢弃过旧轨迹。[1] 两份报告共同说明：恢复语义和故障归因不是数据管线的附属功能，它们会直接改变 learner 实际看到的样本分布。[1-2]

环境错误并非只影响吞吐。Demystifying RL for Long-Horizon Tool-Using Agents 在 TravelPlanner 中注入工具执行失败，观察到较高故障率会减慢收敛并增大训练波动；但其结论来自单一环境和特定模型规模，不能直接推出统一容错阈值。[11] 因此，“环境失败过滤”必须与故障归因准确率一起评价，否则过滤本身会造成难度相关的选择偏差。

### 2.5 优化粒度没有统一答案

SORL 认为 token-level importance sampling 与自然的多轮 turn 结构不匹配，并在搜索与医疗任务中使用 turn-level importance sampling 和 clipping-triggered normalization 抑制梯度尖峰。[10]

相对地，SAO 的附录实验中，token-level value/policy 更新优于两个 step-level GAE 变体；CompactionRL 也发现 token-level loss normalization 对变长 segment 的性能影响大于移除 cross-trajectory GAE。[3-4]

这些结果并不构成直接矛盾，因为论文同时改变了 action 定义、importance weight、advantage estimator、任务结构和 backbone。它们共同说明：token、turn、compaction segment 或完整 trajectory 不是先验正确的归一化单位，研究必须在同一管线中控制其他变量后比较。[3-4,10]

### 2.6 可检验假设

以下均为**研究假设**，不是已有论文已经证明的普适结论。

- **H1：联合稳定区间。** 稳定性主要由 `staleness × learning-rate × update-scale` 的联合量决定，而不是由 staleness 阈值单独决定。理论依据来自 [7]，需要在多轮 Agent 环境中复核。
- **H2：行为策略可识别性。** 跨版本轨迹中，exact/proxy old-policy 的重建误差比单纯 rollout age 更能预测训练坍缩。依据来自 [3,5,9] 的机制差异。
- **H3：故障归因质量。** 只有当环境错误分类具有足够精度时，failure-aware filtering 才提升有效样本效率；错误过滤会产生难度相关的选择偏差。依据来自 [1-2,11]，结论需要控制实验验证。
- **H4：粒度依赖任务结构。** 工具 action 边界清晰时，turn-level 校正可能更稳；长推理内部包含密集逻辑转移时，token-level critic 可能更有效。依据来自 [3-4,10] 的异质结果。

### 2.7 最小正交实验矩阵

主实验不要在同一次运行中同时替换算法、系统和数据。

| 实验轴 | 建议水平 | 要回答的问题 |
|---|---|---|
| 异步程度 | `S=0/1/4/8/16`；同时记录真实 token-age 分布 | 最大 lag 与分布尾部谁更能预测不稳定？ |
| 更新尺度 | 固定 `η`；按 `S` 缩放 `η`；固定 target-KL | 能否验证 `S×η` 或累计漂移的稳定区间？ |
| 行为策略 | latest-old、rollout-logit、snapshot exact、EWMA | 近似误差、系统成本与收敛如何权衡？ |
| 完成语义 | 从头重采样、WAL 续接、丢弃、partial rollout | 恢复方式是否引入长度或难度选择偏差？ |
| 优化粒度 | token、turn、compaction segment、trajectory | 哪种单位在何类任务上降低方差且不损失信用分配？ |
| 环境故障 | 0/1/5/10% 注入；控制故障标签准确率 | 过滤收益是否依赖故障归因质量？ |

### 2.8 必须报告的指标

主结果至少同时包含：

- 任务成功率与 OOD 成功率；
- KL、entropy、gradient norm、clip/mask ratio；
- critic explained variance；
- 行为策略重建误差与真实 token-age 分布；
- 轨迹丢弃率、有效训练 token 比例、故障误过滤率；
- GPU-hour、wall-clock time-to-target、单位成功轨迹成本。[3,5-11]

只报告吞吐或最终 reward，无法区分“更快地产生数据”和“更有效地学习数据”。

---

## 3. 核心问题二：多阶段能力如何合并而不退化

### 3.1 研究问题 RQ2

> 当 reasoning、coding、agent 与 general alignment 分别经过 SFT/RL 优化后，如何把多个专家或阶段 checkpoint 合并成一个策略，同时保留旧能力、吸收新能力，并控制教师前向成本？

### 3.2 从 mixed RL 转向学生分布上的能力合并

DeepSeek-V4 先以 SFT 和 GRPO 独立培养数学、代码、Agent、指令遵循等专家，再使用超过十个教师进行多教师 OPD；报告明确称其以 OPD 完全替换 mixed RL，并在学生生成轨迹上计算 reverse-KL。[2]

GLM-5 则顺序执行 Reasoning RL、Agentic RL、General RL，最后让前序阶段 checkpoint 作为教师进行 cross-stage on-policy distillation，以恢复被后续阶段削弱的能力。[1]

这两份报告证明了该路线在大规模训练管线中的工程可行性，但没有提供足以分离“专家训练质量、prompt mixture、教师权重、OPD 目标和基础模型规模”的统一消融。因此，技术报告可以支持“实际采用”，不能单独支持“OPD 必然优于 mixed RL”或“已经消除灾难性遗忘”的普遍结论。[1-2]

### 3.3 OPD 的基础证据与适用边界

MiniLLM 将蒸馏写成学生生成分布上的 reverse-KL 优化，并通过长度归一化、teacher mixing 和单步分解降低长序列方差；其主要实验针对较小学生模型和通用生成任务。[13]

GKD 系统比较 teacher-generated 与 student-generated 数据比例，以及 forward-KL、reverse-KL 和 JSD，显示 on-policy student data 能缓解训练分布与解码分布的错位，但不同散度的效果依赖任务与模型。[14]

这些工作解释了 OPD 为什么可能适合作为能力合并工具：监督发生在学生实际访问的状态上，教师对学生当前错误提供密集 token 分布。然而，它们最初研究的是模型压缩或单教师蒸馏，不是多个 RL 专家之间的冲突，因此只能为 DeepSeek-V4 与 GLM-5 的做法提供机制基础，不能替代多专家消融。[1-2,13-14]

### 3.4 新近结果表明 OPD 不是单一机制

OPSD Compresses What RLVR Teaches 在数学推理中将正确与错误 rollout 分开训练。对正确轨迹做 OPSD 能在较好保留准确率的同时缩短推理，而只使用错误轨迹会明显损害准确率；论文据此把 OPSD 定位为 SFT→RLVR→OPSD 管线中的 post-RL compaction，而不是可靠的失败轨迹修复器。[15] 这构成对“密集 token 教师信号天然比稀疏 outcome reward 更会纠错”的直接反例。

On-Policy Delta Distillation 不再直接模仿教师完整分布，而使用“教师相对其 base model 的变化”作为 delta signal，并在数学、科学和代码 benchmark 上报告了相对常规 OPD 的提升；代价是额外 teacher-base 前向与约 8%–28% 的训练时间开销。[16] 这提示教师的“增量能力”可能比教师全部偏好更适合作为迁移目标，但尚未在多轮 Agent 或多教师合并上验证。

SEED 将完成后的 Agent 轨迹转化为 hindsight skill，再比较普通上下文与 skill-augmented 上下文下的 action 概率差，形成与 outcome RL 联合优化的 OPD 信号。论文在 ALFWorld、Search QA、WebShop 和视觉 Agent 任务上报告成功率、样本效率和跨域提升，同时指出 self-analyzer 可能把错误解释固化为技能。[17] 这说明 OPD 可以补充稀疏 Agent reward，但教师或分析器本身的可信度会成为新的噪声源。

### 3.5 四个尚未解决的设计选择

- **教师内容**：蒸馏教师的完整分布、教师相对 base 的增量，还是带 privileged context 的自教师？三者分别更接近“复制能力”“抽取增量”和“利用事后信息”。[13-17]
- **教师路由**：DeepSeek-V4 使用多教师权重，GLM-5 使用阶段数据混合，但报告没有回答权重应静态设置、按任务标签设置，还是由当前学生状态动态路由。[1-2]
- **散度与估计**：DeepSeek-V4 认为 sampled-token KL 方差高并采用 full-vocabulary reverse-KL；GLM-5 使用 token log-ratio 形式提高吞吐；MiniLLM、GKD 和 Delta Distillation 又展示了不同近似与散度的行为差异。[1-2,13-14,16]
- **训练时机**：技术报告倾向最终统一蒸馏，OPSD 支持先 RL 再压缩，SEED 则把 OPD 与 Agent RL 联合进行。目前不存在一个经过统一实验验证的最佳阶段顺序。[1-2,15,17]

### 3.6 可检验假设

以下均为**研究假设**。

- **H5：增量教师。** 当教师包含大量与目标域无关的通用偏好时，teacher-minus-base 的 delta signal 比完整教师分布更能减少跨域干扰。依据来自 [16]，需要在多专家设置中验证。
- **H6：状态路由。** 按学生当前 prompt/state 动态选择教师，比固定全局权重更能提高最差域保留率。依据来自 [2] 的多教师形式，结论尚待验证。
- **H7：阶段依赖。** OPD 对“已有但冗长”的能力更像压缩，对“尚未可达”的失败能力不能替代 outcome RL。依据来自 [15]，需要扩展到 Agent 轨迹。
- **H8：联合训练条件。** 只有当 hindsight analyzer 的错误率受控时，RL+OPD 才比纯 outcome RL 更具样本效率；否则密集错误信号会累积。依据来自 [17] 的机制与局限。

### 3.7 最小正交实验矩阵

| 实验轴 | 建议水平 | 主要观测 |
|---|---|---|
| 训练结构 | mixed RL、sequential RL、final OPD、per-stage OPD、joint RL+OPD | 平均能力与最差域保留率 |
| 教师信号 | full teacher、teacher-base delta、privileged self-teacher | 迁移收益、错误放大与计算成本 |
| 教师路由 | 固定权重、任务标签、student-state gating | 域间干扰与教师前向次数 |
| 散度/估计 | full-vocab RKL、top-k RKL、sampled-token、JSD/FKL | 梯度方差、稳定性、吞吐 |
| 轨迹筛选 | all、correct-only、incorrect-only、置信度门控 | 纠错、压缩与选择偏差 |
| 蒸馏时机 | RL 前、RL 中、RL 后、每阶段后 | 可达能力、收敛速度与遗忘曲线 |

### 3.8 必须报告的指标

评价应以多域 Pareto 而不是单一平均分为主：

- 每个阶段前后的域内性能；
- 旧任务 retention ratio；
- 最差域下降；
- 正/负迁移矩阵；
- 输出长度与任务成功的联合曲线；
- teacher forward FLOPs；
- full-logit 缓存开销；
- wall-clock time-to-target。[1-2,13-17]

对 OPD 的结论还应区分三种不同效果：**能力恢复、失败纠正、轨迹压缩**。

---

## 4. 建议的最小研究路线

下面的路线优先追求可归因性，而不是一开始复制前沿模型的完整训练规模。每一阶段都设置停止条件，避免系统工程掩盖算法问题。该路线是本文建议，实验变量来自前述证据冲突。[1-17]

1. **阶段 0：建立可回放环境。** 选择一个搜索 Agent 环境和一个可执行代码/终端环境；记录 token、policy version、log-probability、turn/segment 边界、环境错误类型和恢复事件。先验证同一轨迹可确定性重放。
2. **阶段 1：完成 RQ1 小规模因果实验。** 固定 3B–8B backbone、数据与 reward，只改变 staleness、行为策略恢复、粒度和故障处理；至少三次独立运行，绘制 time-to-target 与稳定性曲线。
3. **阶段 2：完成 RQ2 两域实验。** 分别训练 reasoning 与 agent expert，比较 mixed/sequential/final-OPD；随后加入 delta teacher、动态路由和 correct/incorrect 分组，测量完整遗忘矩阵。
4. **阶段 3：验证交互效应。** 只选择阶段 1、2 中最稳的两种配置，研究 asynchronous learner 是否改变 OPD 的 teacher/student mismatch，避免全排列式成本爆炸。
5. **阶段 4：扩大模型与环境。** 只有当小规模机制可重复、指标能区分失败原因后，再迁移到 SWE/Terminal 长轨迹和更大 MoE backbone。

### 4.1 里程碑与停止条件

| 里程碑 | 最小产出 | 继续条件 | 停止/回退条件 |
|---|---|---|---|
| M0 数据正确性 | 可重放日志与故障标签 | 恢复前后状态一致 | 非幂等操作无法追踪 |
| M1 异步机制 | 稳定区间与成本曲线 | 至少一项机制跨两个环境复现 | 收益仅来自更短输出或数据差异 |
| M2 能力合并 | 多域迁移/遗忘矩阵 | 最差域下降可控且总成本透明 | 平均分上升但旧能力系统退化 |
| M3 联合验证 | async × OPD 交互结果 | 结论在第二个 backbone 保持 | 结果对单一 seed 或阈值敏感 |

### 4.2 优先级建议

如果只能选择一条主线先做，建议先做 **RQ1 的行为策略可识别性与恢复语义**。原因不是它一定比 OPD 更重要，而是 RQ2 的教师/学生比较同样依赖可靠的学生轨迹；如果轨迹本身跨版本且恢复语义不明，OPD 的收益和失败也难以归因。[2-3,5,9]

---

## 5. 研究执行中的方法学约束

- 先报告数据流，再报告算法名。必须明确 rollout policy、old/proximal policy、current learner、reference/teacher 各自的版本和更新时间。[3,5,9]
- 区分环境 observation 与模型 action。只有模型生成 token 进入 policy loss 时，需要说明 advantage 如何跨 observation、turn 和 compaction boundary 传播。[3-4,10]
- 同时报告质量与成本。吞吐、GPU-hour、teacher forward、被丢弃 token 和 wall-clock time-to-target 应与任务成功率并列。[5-9,13-16]
- 至少提供训练曲线和多个 seed。最终 checkpoint 分数可能隐藏中途坍缩、后期退化或 early saturation。[3,7,10,15-16]
- 报告适用边界。数学 RLHF、搜索 Agent、SWE Agent、TravelPlanner 和 embodied environment 的 horizon、奖励密度与工具错误结构不同，不能直接互相外推。[3-6,10-12,17]
- 技术报告只作为工程可行性证据。若没有独立消融，不把大模型最终能力归因于某一个模块。[1-2]

---

## 6. 结论：后续研究应回答什么

第一条主线最终要回答的不是“异步 RL 是否更快”，而是：在给定 wall-clock 预算下，系统能否证明每条进入 learner 的轨迹来自可识别的行为策略、保留正确的交互状态，并把环境故障与策略失败分开。AReaL、SAO、DeepSeek-V4 与 Missing Old Logits 已提供互补机制，但尚未形成统一的统计—系统正确性标准。[2-3,5,7-9]

第二条主线最终要回答的不是“OPD 是否有效”，而是：它在什么条件下复制能力、抽取教师增量、压缩既有轨迹，或真正修复失败策略。DeepSeek-V4 与 GLM-5 展示了大规模多阶段合并的可行性，MiniLLM/GKD 提供了机制基础，OPSD、Delta Distillation 与 SEED 则暴露了作用边界和新的教师噪声问题。[1-2,13-17]

> **最终指导原则**：把“轨迹是否可学”和“能力是否可合”作为两个独立判据。任何新方法只有同时给出行为策略语义、数据利用率、稳定性曲线、跨域保留率和计算成本，才足以支持面向长程 Agent 的优化结论。

---

## 参考文献

1. GLM-5 Team. *GLM-5: from Vibe Coding to Agentic Engineering*. arXiv:2602.15763, 2026. [arXiv](https://arxiv.org/abs/2602.15763)
2. DeepSeek-AI. *DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence*. arXiv:2606.19348, 2026. [arXiv](https://arxiv.org/abs/2606.19348)
3. Zhenyu Hou, Yujiang Li, Jie Tang, and Yuxiao Dong. *Single-Rollout Asynchronous Optimization for Agentic Reinforcement Learning*. arXiv:2607.07508, 2026. [arXiv](https://arxiv.org/abs/2607.07508)
4. Yujiang Li, Zhenyu Hou, Yi Jing, Jie Tang, and Yuxiao Dong. *CompactionRL: Reinforcement Learning with Context Compaction for Long-Horizon Agents*. arXiv:2607.05378, 2026. [arXiv](https://arxiv.org/abs/2607.05378)
5. Wei Fu et al. *AReaL: A Large-Scale Asynchronous Reinforcement Learning System for Language Reasoning*. arXiv:2505.24298, 2025. [arXiv](https://arxiv.org/abs/2505.24298)
6. Michael Noukhovitch et al. *Asynchronous RLHF: Faster and More Efficient Off-Policy RL for Language Models*. ICLR 2025; arXiv:2410.18252. [arXiv](https://arxiv.org/abs/2410.18252)
7. Jingwei Song et al. *Staleness-Learning Rate Scaling Laws for Asynchronous RLHF*. arXiv:2607.01083, 2026. [arXiv](https://arxiv.org/abs/2607.01083)
8. Rongjian Chen, Jianmin Hu, Kejiang Ye, and Minxian Xu. *RolloutPipe: Overlapping Pipelined Rollout and Training in Disaggregated On-Policy LLM Reinforcement Learning*. arXiv:2606.26997, 2026. [arXiv](https://arxiv.org/abs/2606.26997)
9. Zhong Guan et al. *Missing Old Logits in Asynchronous Agentic RL: Semantic Mismatch and Repair Methods for Off-Policy Correction*. arXiv:2605.12070, 2026. [arXiv](https://arxiv.org/abs/2605.12070)
10. Chenliang Li et al. *Stabilizing Off-Policy Training for Long-Horizon LLM Agent via Turn-Level Importance Sampling and Clipping-Triggered Normalization*. arXiv:2511.20718, 2025/2026 revision. [arXiv](https://arxiv.org/abs/2511.20718)
11. Xixi Wu et al. *Demystifying Reinforcement Learning for Long-Horizon Tool-Using Agents: A Comprehensive Recipe*. arXiv:2603.21972, 2026. [arXiv](https://arxiv.org/abs/2603.21972)
12. Zhiheng Xi et al. *AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning*. arXiv:2509.08755, 2025. [arXiv](https://arxiv.org/abs/2509.08755)
13. Yuxian Gu, Li Dong, Furu Wei, and Minlie Huang. *MiniLLM: On-Policy Distillation of Large Language Models*. ICLR 2024; arXiv:2306.08543. [arXiv](https://arxiv.org/abs/2306.08543)
14. Rishabh Agarwal et al. *On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes*. ICLR 2024; arXiv:2306.13649. [arXiv](https://arxiv.org/abs/2306.13649)
15. Jaehoon Kim and Dongha Lee. *OPSD Compresses What RLVR Teaches: A Post-RL Compaction Stage for Reasoning Models*. arXiv:2605.06188, 2026. [arXiv](https://arxiv.org/abs/2605.06188)
16. Byeongho Heo, Jaehui Hwang, Sangdoo Yun, and Dongyoon Han. *On-Policy Delta Distillation*. arXiv:2607.15161, 2026. [arXiv](https://arxiv.org/abs/2607.15161)
17. Jinyang Wu et al. *SEED: Self-Evolving On-Policy Distillation for Agentic Reinforcement Learning*. arXiv:2607.14777, 2026. [arXiv](https://arxiv.org/abs/2607.14777)

---

## 附录 A：核心观点—证据对照

| 核心观点 | 主要证据 | 当前缺口 |
|---|---|---|
| 异步收益不能只用吞吐衡量 | AReaL [5]、Async RLHF [6]、RolloutPipe [8] | 缺少统一的有效样本成本口径 |
| staleness 必须与学习率和更新幅度联合评价 | Staleness Law [7] | 尚未在真实长程 Agent 环境系统验证 |
| rollout logits 不一定等价于 proximal old policy | SAO [3]、Missing Old Logits [9] | 需要直接测量策略重建误差与梯度偏差 |
| 中断恢复会引入长度或状态选择偏差 | DeepSeek-V4 [2]、GLM-5 [1] | 缺少恢复策略的独立消融 |
| 环境失败过滤依赖故障归因质量 | GLM-5 [1]、DeepSeek-V4 [2]、Demystifying [11] | 缺少标签噪声与选择偏差的联合实验 |
| token/turn/segment 不存在先验最优粒度 | SAO [3]、CompactionRL [4]、SORL [10] | 需要固定管线后的正交比较 |
| OPD 能缓解学生分布与教师分布错位 | MiniLLM [13]、GKD [14] | 主要证据不是多专家 Agent 合并 |
| 大模型管线已采用 OPD 合并阶段或专家能力 | GLM-5 [1]、DeepSeek-V4 [2] | 缺少统一的 mixed RL/OPD 独立消融 |
| OPD 可能只压缩成功能力，不能自动纠错 | OPSD [15] | 需要扩展到多轮 Agent 失败轨迹 |
| delta teacher 可能减少无关教师偏好 | Delta Distillation [16] | 尚未验证多教师与多轮 Agent 设置 |
| hindsight OPD 能补充稀疏奖励，但会引入分析器噪声 | SEED [17] | 需要控制 self-analyzer 错误率 |
