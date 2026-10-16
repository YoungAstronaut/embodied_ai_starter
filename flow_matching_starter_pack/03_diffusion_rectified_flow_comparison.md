# 03. Flow Matching、Diffusion 与 Rectified Flow

## 1. 先给结论

- **CNF/ODE flow**：生成模型的动力系统形式。
- **Flow Matching/CFM**：训练这个速度场的 simulation-free 回归框架。
- **Rectified Flow**：使用端点线性插值的相关框架，并通过 rectification/reflow 让实际生成轨迹更直、更适合少步采样。
- **Diffusion model**：通常从数据出发定义随机加噪过程，学习 score/noise，再用 reverse SDE 或 probability-flow ODE 采样。
- **Stochastic Interpolants**：更一般的统一视角；同一概率路径可由 ODE 或一族 SDE 实现。

它们不是五个互斥模型类别，而是在“动力系统—路径设计—学习参数化”三个层面有交叉。

## 2. 对比表

| 维度 | Vanilla linear FM | Rectified Flow | 典型 DDPM/score diffusion |
|---|---|---|---|
| 源与目标时间 | $t=0$ 噪声，$t=1$ 数据 | 常用同一约定 | 文献常用 $t=0$ 数据，末端噪声 |
| 训练对象 | velocity | velocity | noise/score/data/v-prediction |
| 条件路径 | 常用线性/CondOT | 线性插值 | 由前向 SDE/离散加噪链给出 Gaussian path |
| 训练时解 ODE/SDE | 否 | 否 | 通常否 |
| 推理过程 | ODE | ODE；可经 reflow/distill 减少步数 | reverse SDE、DDIM 或 probability-flow ODE |
| 随机性 | 初始噪声 | 初始噪声 | 初始噪声，SDE 采样还可逐步加噪 |
| 主要设计难点 | coupling、path、time weighting、solver | 交叉路径、reflow 成本、蒸馏 | noise schedule、参数化、采样器、步数 |

## 3. 为什么有人说 diffusion 是 FM 的特例？

要把这句话限制在合适语境中。对 Gaussian affine probability path，diffusion 的前向加噪过程给出

$$
X_t=\alpha_tX_1+\sigma_t\epsilon.
$$

其 score、noise prediction 与 velocity 可由 scheduler 相关的线性公式转换；probability-flow ODE 又与 diffusion SDE 具有相同的边缘分布。因此可以用 FM 视角训练与采样同一族边缘概率路径。

但“整个 diffusion 方法就是 vanilla FM”仍过于粗糙，因为：

1. diffusion 还规定了随机前向过程以及 reverse-time/SDE 采样视角；
2. FM 可以使用非 diffusion 的路径、非 Gaussian source 或不同 coupling；
3. 同一边缘路径可以有 ODE 与多种 SDE 实现，样本的跨时间联合分布并不相同。

准确说法是：**常见 diffusion 的 Gaussian probability paths 和 score/noise 训练，可嵌入更广义的 FM/Generator Matching 视角；在 probability-flow ODE 采样下，两者有直接等价关系。**

## 4. Rectified Flow 和 linear FM 到底有何区别？

二者共享核心回归：

$$
X_t=(1-t)X_0+tX_1,\qquad
\min_\theta E\|v_\theta(X_t,t)-(X_1-X_0)\|^2.
$$

从这一步看，它们高度重合。Rectified Flow 的额外重点是：

1. 把线性插值看作待“因果化”的非因果轨迹；
2. 学到的 ODE 会在相交处重新接线，保持每个时刻的边缘分布；
3. 通过一次或多次 reflow，用上一个模型产生的端点 coupling 重新训练，使生成 ODE 的实际轨迹更直；
4. 更直的轨迹可用更粗的 Euler 步长，甚至进一步蒸馏为一步模型。

关键误区：**条件插值线是直线，不保证第一次训练后学到的边缘 ODE 轨迹就是直线。** 当大量独立配对直线交叉时，网络回归的是条件速度均值，实际 ODE 必须避免轨迹交叉。

> 🤖 **绕瓶例子**：看 `01` 图 3 的右边。第一次训练出来的轨迹明显是弯的：前期往中间收，后期再分开。所以 1 步 Euler 会撞瓶。
>
> Reflow 的做法是：
> 1. 用这个模型给每份噪声跑出它最终去的地方，得到一批确定的配对。在 1D 例子里就是「正噪声 → +1，负噪声 → −1」。
> 2. 再拿这些配对重新训练。
>
> 这一次，同一个点不会再收到相反的标签，速度场几乎沿直线指向 $\pm1$，**1 步就能走对**。新包 `fm_lab.py` 的 8-Gaussian 实测：直线度从 2.59 降到 0.0006，1 步时「落在模式之外」的比例从 100% 降到 11%。

### 4.1 关于这一节的两个说明

- **Reflow 的代价**：要先训练一个模型，再用它生成一大批配对，再训练一次。而且第一个模型的误差会被固化进配对里。实测 reflow 之后，多步质量反而略有下降。
- **机器人里要注意条件**：配对必须在**同一个观测**下做。不同场景的示范不能互相配对，因为瓶子在左边时的噪声，不应该被配给瓶子在右边时的动作。

## 5. coupling 为什么重要？

线性 CFM 需要一个 joint distribution π₀,₁ 产生端点对 $(X_0,X_1)$。最简单的是独立 coupling：

$$
\pi_{0,1}(x_0,x_1)=p_0(x_0)q(x_1).
$$

它容易采样，但随机端点配对可能导致大量交叉，增加条件速度标签方差和 ODE 曲率。可选方案包括：

- 数据天然配对，例如低分辨率图像与高分辨率图像；
- minibatch optimal transport coupling；
- reflow 后由当前模型诱导的 deterministic coupling；
- 任务结构提供的 coupling。

OT-CFM 在 minibatch 内近似较短的 source-target 配对，从而降低回归目标方差并让流更易积分。其限制是高维 minibatch OT 本身是近似，且 CFM 仍要求可构造闭式条件流。

> 🤖 **绕瓶例子**：在 1D 里，最优传输配对就是**排序配对**：把 256 份噪声从小到大排好，把 256 个示范也从小到大排好，一一对应。结果是负噪声全部配给 −1，正噪声全部配给 +1。
>
> 这样训练时，「噪声 +0.3 被配给近侧」这种交叉配对就消失了。在 $t=0$ 时，速度不再是「指向平均值 0」，而是「指向自己那一侧的 ±1」，1 步就不会撞瓶。
>
> 代价有两个：
> - 高维 action chunk 里，OT 只能在一个 minibatch 内近似地做，batch 内配对会把相邻模式的样本连起来，在模式之间留下「桥」；
> - 计算更慢。新包实测 CPU 上的匈牙利算法让训练慢了约 16 倍。
>
> **「任务结构提供的 coupling」在机器人里很自然**：比如按末端位姿的距离、或按抓取方式来配对，而不是只用动作向量的欧氏距离。这是一个开放的研究点，见 `06` 假设 B。

## 6. “更直”为什么可能更快？

Euler 局部截断误差与轨迹曲率/速度变化有关。若真轨迹近似

$$
x_t=x_0+t(x_1-x_0),
$$

速度几乎恒定，则少量步也能准确积分。应区分三件事：

1. 条件路径直；
2. 学到的边缘流轨迹直；
3. 神经网络在少数离散时刻的误差小。

第一项并不自动保证后两项。研究中至少应报告 NFE–性能曲线，而不是只报告训练 loss。

> 🤖 **绕瓶例子：把「积分误差」和「网络误差」分开。** `01` 第 9 节用的是**解析的完美速度场**，网络误差为 0。即便如此，只改 NFE，碰撞率就从 100%（1 步）降到 24%（2 步）、1.9%（4 步）、0%（10 步）。这部分全是积分误差，来源是轨迹的弯曲。
>
> 换成真实训练的网络（新包 `fm_lab.py` 的 action 实验），1 步碰撞 95.7%，16 步还有 0.6%。多出来的那部分才是网络误差。**写实验报告时，最好像这样把两部分分开报告。**

## 7. ODE 与 SDE：不要简单说谁“更强”

在只关心每个时刻的边缘分布时，ODE 与 SDE 可以生成相同 $p_t$。但它们的单条样本路径与跨时间联合分布不同。

- ODE：给定初值后确定、可逆性直观、可用高阶自适应 solver、likelihood 公式明确。
- SDE：采样中保留随机性，可能对模型估计误差更鲁棒，但数值模拟和分析更复杂。

Stochastic Interpolants 表明：路径设计与采样过程可以部分解耦；给定插值密度，可构造 ODE 和带可调 diffusion coefficient 的 SDE。对机器人控制，SDE 的逐步随机性是否有益必须用闭环任务检验，不能由生成图像的结论直接推出。

> 🤖 **绕瓶例子里两者的区别**：
>
> - **ODE**（π0 这种）：最终去远侧还是近侧，**一开始就由噪声的正负号决定了**（`01` 表 5：100% 一致），中途不会换边。
> - **SDE**（DDPM 式的 Diffusion Policy，每一步都再加一点噪声）：一份草稿走到一半还可能被新加的噪声「踢」到另一边。两者最终远侧、近侧各占一半的比例是一样的，但**单份草稿的经历不同**。
>
> 这对机器人有两个实际影响：
> 1. SDE 在网络某一步出错时，有机会被后面的噪声「救回来」。这是它可能更鲁棒的直觉。
> 2. **用强化学习微调时**，SDE 的每一步都是一个高斯转移，可以直接算 $\log\pi$。DPPO 就是这样做的。ReinFlow 则反过来：往 ODE 里主动注入可学习的噪声，目的正是为了拿到似然（`04` 第 11 节）。

## 8. 参数化等价不等于优化等价

对同一 Gaussian path，理论上可以在 velocity、noise、score、data prediction 之间转换。但实践差异来自：

- 转换系数在 $t\to0$ 或 $t\to1$ 可能奇异；
- time sampling 改变不同噪声区间的梯度占比；
- 网络与优化器有有限容量；
- loss weighting 改变有限数据下的估计方差；
- 采样器对速度误差的敏感性不同。

所以论文对比应尽量固定 probability path、网络、训练预算和 NFE，再谈 objective/parameterization 的效果。

> 🤖 **机器人里最容易踩的一个**：**动作没归一化**。新包实测：动作幅度约 0.3、噪声 std=1 时，不做归一化，Shortcut 的 1 步碰撞率是 72%；按维度做 z-score 之后降到 9%。
>
> 原因是速度 $v=\hat x_1-x_0$ 里，噪声项 $x_0$ 比动作信号大三倍，网络要精确抵消一个很大的量，残差相对于动作就显得很大。所以 Diffusion Policy、openpi 都会先把每个动作维度归一化。还有，不同维度的量纲不同（米和弧度），不归一化时欧氏距离本身就不合理。

## 9. 常见误区速查

### 误区 A：FM 训练时不解 ODE，所以推理也一步完成

错误。simulation-free 指训练时无需 rollout。推理仍需积分，除非额外做 reflow、distillation/consistency 或直接训练一步映射。

🤖 绕瓶例子：π0 推理要调用 10 次网络。硬改成 1 次，就会撞瓶（`01` 第 9 节）。

### 误区 B：FM 就是把噪声逐渐去掉

不完整。去噪是 Gaussian noise-to-data 路径的一种解释；FM 可以连接任意可采样的 source/target，并使用非 Gaussian、配对或几何路径。

🤖 机器人例子：Streaming Flow Policy 的起点就不是纯噪声，而是「上一个动作附近的一个窄高斯」（`04` 第 6 节）。

### 误区 C：每个 $x_0$ 必须匹配一个真实 $x_1$

训练确实采端点对，但独立 coupling 并不表达语义配对。CFM 的正确性来自边缘化，而不是声称这对样本天然对应。

🤖 绕瓶例子：训练时噪声 +0.3 可能被配给近侧示范，这个配对没有任何含义。推理时 +0.3 照样去远侧。

### 误区 D：ODE 确定，所以不能表示多模态动作

错误。随机初值决定不同轨迹；同一观测条件下多次采噪声可落到不同动作模式。

🤖 绕瓶例子：噪声正负号决定绕行方向，两种绕法各占约一半。

### 误区 E：Straight conditional path 就是 global optimal transport

错误。单个点到点或特定 coupling 下是直线 transport，但独立 coupling 的整体边缘路径通常不是全局 OT。OT-CFM 或 reflow 才显式改善 coupling/轨迹。

### 误区 F：flow 时间就是机器人运动的时间

错误。flow 时间 $t$ 是「一份动作草稿改到第几成」，发生在一次推理的内部，这时机器人没动。整个 flow 跑完、拿到动作之后，机器人才开始执行。唯一的例外是 Streaming Flow Policy，它故意让两者重合（`04` 第 3、6 节）。

### 误区 G：simulation-free 就是不需要仿真器

错误。这里的 simulation 指数值积分 ODE，和 MuJoCo / Isaac 之类的物理仿真器无关。训练 flow policy 只需要示范数据；评测时用不用仿真器，是另一回事。

### 误区 H：训练 loss 降不下去，说明没训好

不一定。CFM loss 里有一个与参数无关的常数项（标签的条件方差），所以 loss 本来就停不到 0（`02` 第 6 节）。判断训没训好要看采样结果：碰撞率、成功率、模式覆盖。

## 10. 面向论文阅读的判断模板

看到一篇“flow policy”论文，依次问：

1. 生成变量是单动作、action chunk，还是整条物理时间轨迹？
2. flow time 与 robot time 是否为两个不同维度？
3. source distribution 是标准高斯、上一动作附近高斯，还是其他分布？
4. 条件路径和 coupling 是什么？
5. 网络输出 velocity、noise、score 还是 clean action？
6. 训练 time 如何采样、loss 如何加权？
7. 推理 solver、NFE、控制频率和 receding-horizon 参数是多少？
8. 论文保证的是每时刻 marginal，还是整个 action sequence 的 joint distribution？

