# 05. 核心论文笔记与阅读问题

本文件不是按发表时间罗列摘要，而是按研究问题分组：先解决“FM 为什么成立”，再解决“路径怎样更好”，最后解决“怎样进入机器人控制”。

## 第一类：建立 Flow Matching 的数学与实现基线

### 1. Flow Matching for Generative Modeling

- 作者：Yaron Lipman 等
- arXiv：2210.02747；ICLR 2023
- 本地：`papers/Flow_Matching_2210.02747.pdf`

论文面对的核心矛盾是：CNF 表达灵活，但 maximum-likelihood 训练需要昂贵的 ODE simulation；diffusion 可 simulation-free 训练，却把概率路径限制在特定随机加噪构造中。论文提出直接回归生成给定概率路径的速度场，并用 conditional paths 把不可计算的边缘目标化成可采样的逐样本目标。

最本质的两个结论：第一，条件速度的后验平均生成条件路径混合后的边缘概率路径；第二，FM 与 CFM 的目标相差一个与参数无关的常数，因此梯度相同。Gaussian conditional paths 只是该框架的一个易算实例。

优点是训练不解 ODE、目标是普通 MSE、可以直接选择非 diffusion 路径。原文的 conditional OT path 在单样本条件下是直线且具有好的经验采样效率，但不能把它误解成任意数据分布间的全局最优运输。

阅读问题：

1. 式 (8) 中的边缘速度为什么要按后验 $p(x_1\mid x_t)$ 加权？
2. Theorem 2 的“loss 相差常数”与“样本标签完全相同”有何区别？
3. 论文报告的 NFE 优势中，哪些来自 path，哪些来自 parameterization？

### 2. Flow Matching Guide and Code

- 作者：Yaron Lipman 等
- arXiv：2412.06264
- 本地：`papers/Flow_Matching_Guide_2412.06264.pdf`
- 官方代码：<https://github.com/facebookresearch/flow_matching>

这篇 83 页教程是本包的首选教材。它把 Flow Matching 分解成 flow、probability path、continuity equation、marginalization trick、CFM loss、coupling、guidance 等组件，并扩展到 Riemannian、discrete 和 general generator matching。

最值得掌握的是第 2 节 quick tour、第 3.5–3.7 节连续性方程与 CNF、第 4 节 FM，以及第 10 节与 diffusion 的关系。第 7 页的 standalone code 与本包 toy script 对应。

弱点不是方法问题，而是阅读成本：其统一框架远超初学所需。第一次不要从 discrete/CTMP 开始，否则容易在抽象层迷失。

阅读问题：

1. Figure 9 中 flow、velocity、probability path 三列的箭头分别表示什么？
2. Bregman divergence 为什么仍能学习条件期望？
3. 第 10 节为什么说 diffusion 的训练可看作特定 Gaussian path 下的 FM 参数化？

## 第二类：改善路径、coupling 和少步采样

### 3. Flow Straight and Fast: Rectified Flow

- 作者：Xingchao Liu, Chengyue Gong, Qiang Liu
- arXiv：2209.03003
- 本地：`papers/Rectified_Flow_2209.03003.pdf`

论文把独立端点之间的直线插值视为非因果路径，再回归 $E[X_1-X_0\mid X_t=x]$ 得到可由 ODE 实现的因果速度场。ODE 轨迹不能交叉，因此会在插值线交点处重新接线，同时保持每个时刻的边缘分布。

其区别性贡献是 rectification/reflow：用当前 flow 产生的端点 coupling 再训练下一代 flow，使实际轨迹逐渐变直；更直的轨迹允许粗步长乃至一步 Euler，再可蒸馏成一步模型。

优点是目标极简、理论上不增加凸 transport cost，并把少步采样和轨迹几何联系起来。弱点是 reflow 需要额外生成数据和重新训练；有限模型误差下的“越来越直”不是免费保证，原始工作的一步图像结果也不能直接外推到闭环机器人。

阅读问题：

1. 为什么线性插值 $X_t$ 可以交叉，而 ODE flow $Z_t$ 不能交叉？
2. marginal-preserving 与 trajectory-joint-preserving 有何区别？
3. reflow 改变了路径、coupling，还是目标分布？

### 4. Improving and Generalizing Flow-Based Generative Models with Minibatch OT

- 作者：Alexander Tong 等
- arXiv：2302.00482；TMLR 2024
- 本地：`papers/OT_CFM_2302.00482.pdf`
- 官方代码：<https://github.com/atong01/conditional-flow-matching>

论文把 CFM 推广到任意 source distribution 和任意可采样 coupling，并用 minibatch OT 近似 source-target 配对。相比独立 coupling，OT pairing 通常减少条件速度方差、降低路径能量，使训练更快、固定 NFE 下积分误差更小。

其价值不只是“加了 OT”，而是清楚区分条件 OT path 与边缘 dynamic OT：单个条件高斯/直线路径最优，不意味着混合后的边缘路径全局最优；只有在合适 transport plan 下才逼近 dynamic OT。

限制是需要闭式条件流；高维 minibatch OT 近似会产生误差，batch 大小和 cost 的选择也引入新计算与归纳偏置。

阅读问题：

1. I-CFM 与 OT-CFM 唯一变化是否只是端点 joint distribution？
2. 为什么更好的 coupling 会降低回归 target variance？
3. 对机器人 action chunk，欧氏 OT cost 是否真的表示任务相似性？

### 5. Stochastic Interpolants

- 作者：Michael S. Albergo, Nicholas M. Boffi, Eric Vanden-Eijnden
- arXiv：2303.08797；JMLR 2025
- 本地：`papers/Stochastic_Interpolants_2303.08797.pdf`

这篇工作从一个显式随机插值过程出发，例如

$$
x_t=(1-t)x_0+t x_1+\sqrt{2t(1-t)}z,
$$

证明其时间边缘密度既可由 transport equation/ODE 实现，也可由一族带可调噪声的 Fokker–Planck/SDE 实现，并给出速度、score 与 likelihood 的二次回归目标。

它提供了比“FM vs diffusion”二分法更准确的观点：概率路径的设计、学习哪些场、以及用确定性还是随机过程采样，可以部分解耦。同一 $p_t$ 不代表相同的跨时间 joint law。

优点是统一性和理论深度；弱点是设计空间很大，实践中要同时选择 interpolant、latent noise 和 diffusion coefficient，初学者容易失去最小闭环。建议掌握 vanilla CFM 后再读。

阅读问题：

1. ODE 与 SDE 共享边缘密度，为什么 sample trajectories 仍不同？
2. latent $z$ 与 sampling SDE 中的 Brownian noise 是同一个角色吗？
3. 对控制问题，我们关心 marginal 还是跨时间 joint law？

## 第三类：机器人动作生成

### 6. Diffusion Policy

- 作者：Cheng Chi 等
- arXiv：2303.04137；IJRR 版本
- 本地：`papers/Diffusion_Policy_2303.04137.pdf`
- 项目：<https://diffusion-policy.cs.columbia.edu/>

它把 visuomotor behavior cloning 表示为条件 action diffusion $p(A_t\mid O_t)$，从高斯噪声迭代去噪出 action sequence，并配合 receding horizon。论文的关键贡献不只在 DDPM，而是 action sequence prediction、视觉条件只编码一次，以及适合时序动作的 CNN/Transformer 结构。

优点是能表达多模态和高维动作块、训练稳定、闭环实验广。弱点是比简单显式策略有更高 latency；它仍继承 behavior cloning 的数据覆盖与 covariate shift 问题。

把它放进 FM 学习包，是为了建立机器人 action-generative-policy 的基线：FM policy 与其共享“生成 action chunk”的范式，但训练参数化和采样动力学不同。

阅读问题：

1. prediction horizon 与 execution horizon 为什么必须分开？
2. 视觉 conditioning 为什么不参与 joint diffusion？
3. 公平比较 diffusion 与 FM 时，应固定哪些变量？

### 7. π0: A Vision-Language-Action Flow Model for General Robot Control

- 作者：Kevin Black 等
- arXiv：2410.24164；RSS 2025
- 本地：`papers/pi0_VLA_Flow_Model_2410.24164.pdf`
- 项目：<https://www.physicalintelligence.company/blog/pi0>

π0 的问题是：自回归离散 action tokens 难以高频、精确地生成灵巧连续动作；纯 action diffusion policy 又缺少大型 VLM 的语义先验。它在 PaliGemma VLM 上增加独立 action expert，用 CFM 生成 50 步连续 action chunk。

最值得初学者抓住的是第 IV 节：

$$
A^\tau=\tau A+(1-\tau)\epsilon,
\qquad u=A-\epsilon,
$$

训练时 MSE 回归速度，推理时从噪声以 10 个 Euler steps 积分。VLM 负责图文条件表示，action expert 负责连续动作场；两者并不是把动作强行当词表 token。

优点是把互联网语义、跨 embodiment 数据和连续高频动作统一到一个 VLA；弱点是训练数据与算力门槛极高，论文难以仅凭公开信息完整复现，且 FM 本身与大规模数据配方的贡献需要消融区分。

阅读问题：

1. π0 的 action token 为什么是 sequence slot 而不是离散词表 ID？
2. beta time sampling 改变了什么优化权重？
3. KV cache 能减少哪些计算，不能减少哪些计算？

### 8. Streaming Flow Policy

- 作者：Sunshine Jiang 等
- arXiv：2505.21851
- 本地：`papers/Streaming_Flow_Policy_2505.21851.pdf`
- 项目：<https://streaming-flow-policy.github.io/>

论文批评常规 diffusion/flow policy 实际上在采样“action trajectories 的 flow trajectory”：每个生成步都维护一个完整动作块，中间块被丢弃，必须等去噪完成后才能执行。它改为把物理 action trajectory 直接当作 flow trajectory，从上一动作附近开始积分，每个积分点立即成为可执行动作。

条件速度

$$
v_\xi(a,t)=\dot\xi(t)-k(a-\xi(t))
$$

把轨迹跟随与稳定反馈结合，再用 CFM 混合多个示范。优点是低首动作延迟、可流式执行、适合 receding horizon；核心限制是只保证每个时刻的 marginal action distribution，不保证整条轨迹 joint distribution。

这篇论文提供一个重要提醒：机器人中的 flow time 未必只是“生成迭代时间”，也可与物理轨迹时间对齐；但这样做会改变建模对象与理论保证。

阅读问题：

1. 标准 action-chunk FM 的状态空间是 ᴀ^H，SFP 的状态空间为什么更接近 ᴀ？
2. 稳定项 $k$ 对噪声方差和闭环鲁棒性分别有何影响？
3. 哪些任务必须保留 trajectory joint distribution？

## 结论：如何把八篇论文串起来

第一类工作给出 CFM 的可计算性与统一语言；第二类工作指出“目标分布相同”并不意味着训练难度和采样成本相同，coupling、路径曲率和随机性都是可设计变量；第三类工作把数据变量替换为 action chunk 或 action trajectory，并加入视觉、语言、状态条件。

因此，读机器人 flow policy 时不应只问“用了几步 Euler”，而应从四层拆解：生成变量是什么、条件是什么、概率路径/coupling 如何定义、部署闭环如何执行。论文的创新往往发生在其中一层，而不是重新发明整个 FM 定理。

