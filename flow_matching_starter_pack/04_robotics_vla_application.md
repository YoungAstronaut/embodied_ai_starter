# 04. Flow Matching 在机器人与 VLA 中怎么用

## 1. 从“生成图片”到“生成动作”只换了什么？

在视觉生成中，一个训练样本可以是图像 $x_1\in\mathbb R^{C\times H\times W}$。在机器人策略中，把训练样本换成未来动作块：

$$
A_t=[a_t,a_{t+1},\ldots,a_{t+H-1}]
\in\mathbb R^{H\times d_a}.
$$

条件观测为

$$
o_t=(I_t^{1:n},\ell_t,q_t,h_t),
$$

可包括多视角 RGB、语言指令、本体状态和历史。策略要表示条件分布

$$
p(A_t\mid o_t).
$$

Flow Matching 不负责决定视觉编码器、语言模型或控制器，它只提供连续动作分布的生成头和训练目标。

## 2. 标准 action-chunk CFM

取专家动作块 $A^1\sim p_{\mathrm{data}}(A\mid o)$，噪声动作块 $A^0\sim\mathcal N(0,I)$，flow time $τ\sim U[0,1]$：

$$
A^\tau=(1-\tau)A^0+\tau A^1.
$$

监督速度为

$$
U^\tau=A^1-A^0.
$$

训练：

$$
\boxed{
\mathcal L(\theta)=
\mathbb E\left[
\|v_\theta(A^\tau,\tau,o)-(A^1-A^0)\|_2^2
\right].
}
$$

推理从 $A^0\sim\mathcal N(0,I)$ 开始：

$$
\frac{dA^\tau}{d\tau}=v_\theta(A^\tau,\tau,o),
\qquad \tau:0\rightarrow1.
$$

数值积分得到完整 action chunk，然后执行前 $H_{exec}\le H$ 个动作，再读取新观测并重规划。这就是 receding-horizon execution。

### 2.1 🤖 用绕瓶例子走一遍完整的「看—想—做」循环

设定：chunk 长度 $H=16$ 个路点，每个路点 $(x,y)$，执行前 $H_{exec}=8$ 个后重新规划，推理用 10 步 Euler。

| 阶段 | 发生了什么 | 张量形状 | 机器人在干嘛 |
|---|---|---|---|
| ① 看 | 相机拍一帧，编码器把图像（瓶子、杯子在哪）和关节角编码成条件 $o$ | 图像 → 特征向量 | 停着，或在执行上一个 chunk |
| ② 抽草稿 | `A = torch.randn(16, 2)`：一条完全随机、乱七八糟的轨迹 | $16\times2$ | 同上 |
| ③ 想（flow $t:0\to1$） | 循环 10 次：`A = A + 0.1 * net(A, t, o)`。前几次草稿被拉向两种绕法的平均，后几次「站队」到远侧或近侧 | $16\times2$ | 同上。**这 10 次全在一次推理内部** |
| ④ 做（机器人时间） | 把 $A$ 反归一化成真实坐标，按控制频率依次发给控制器，执行前 8 个路点 | 每次一行 $1\times2$ | 真的在动 |
| ⑤ 重复 | 回到 ①。新的草稿是重新抽的，可能抽到另一边（mode jumping，见第 11 节） | — | — |

**两个「时间」在这张表里一目了然**：③ 里的 $t$ 是 flow 时间，④ 才是机器人时间。

## 3. 两个“时间”必须分清

- **robot time** $t$：动作序列中的物理控制时刻；
- **flow time** $τ$：从噪声动作块到干净动作块的生成进度。

标准 flow policy 生成 $H$ 步动作时，网络内部沿 $τ$ 做若干次迭代；每次迭代都更新整个 $H\times d_a$ 张量。生成完成后，机器人再沿物理时间执行动作。

这也解释了延迟：若 action expert 每次前向需要 $T_{net}$，solver 需要 (NFE) 次网络评估，则仅生成头的粗略延迟约为

$$
T_{infer}\approx NFE\cdot T_{net}+T_{vision}+T_{overhead}.
$$

action chunk 能把该成本摊到多个控制步，但 chunk 太长会降低对新观测的响应性。

## 4. π0 的具体实例

π0 将预训练 PaliGemma VLM 与独立的 action expert 结合。观测包含 2–3 张 RGB、语言和关节角；目标是 $H=50$ 的 action chunk。

论文采用线性 Gaussian 路径：

$$
q(A^\tau\mid A)=\mathcal N(\tau A,(1-\tau)^2I),
$$

等价采样写法为

$$
A^\tau=\tau A+(1-\tau)\epsilon,
\qquad \epsilon\sim\mathcal N(0,I).
$$

目标速度：

$$
u(A^\tau\mid A)=A-\epsilon.
$$

因此 π0 的 action loss 是

$$
\mathcal L_\tau(\theta)
=\mathbb E\|v_\theta(A^\tau,o)- (A-\epsilon)\|^2.
$$

推理从 $A^0\sim\mathcal N(0,I)$ 出发，用 10 个 Euler steps：

$$
A^{\tau+\delta}=A^\tau+\delta v_\theta(A^\tau,o),
\qquad \delta=0.1.
$$

π0 还使用非均匀的 beta time distribution，偏向较低、噪声更强的 $τ$。这提醒我们：路径公式相同，time sampling 也可能显著改变训练。

模型结构上，图像/文本前缀由 VLM backbone 处理，状态和动作 token 由约 300M 参数的 action expert 处理；action tokens 使用双向注意力。推理时可缓存观测前缀的 KV，仅迭代动作后缀，降低多步 flow inference 的成本。

## 5. π0 与 Diffusion Policy 的结构差异

| 维度 | Diffusion Policy | π0 |
|---|---|---|
| 条件输入 | 视觉/状态历史 | 多图像 + 语言 + 本体状态 |
| 动作生成 | DDPM/DDIM 式 action diffusion | conditional flow matching |
| 骨干 | 1D U-Net 或 time-series transformer | 预训练 VLM + action expert |
| 监督输出 | 噪声/score 相关目标 | action-chunk velocity |
| 语义知识 | 主要来自机器人数据 | 继承互联网 VLM 预训练 |
| 共同点 | 高维 action sequence、条件生成、多模态、receding horizon | 同左 |

二者的关键共同思想不是“都迭代 10 次”，而是把 policy 从单点回归改成条件生成模型 $p(A\mid o)$。

## 6. Streaming Flow Policy 为什么是另一种 flow policy？

标准 flow/diffusion policy 的生成变量是完整 action trajectory $A\in\mathcal A^H$：flow time 每前进一步，整个动作块被更新一次；中间结果通常不能直接执行。

Streaming Flow Policy 把**物理 action trajectory 本身**当作 flow trajectory。它从上一动作附近的窄高斯开始：

$$
a(0)\sim\mathcal N(a_{prev},\sigma_0^2I),
$$

并沿

$$
\frac{da(t)}{dt}=v_\theta(a(t),t\mid h)
$$

逐步积分；每个新积分点本身就是下一动作，因此可以边积分边执行。

对一条 demonstration trajectory ξ$t$，论文构造稳定条件速度：

$$
v_\xi(a,t)=\dot\xi(t)-k(a-\xi(t)).
$$

第一项沿示范轨迹前进，第二项像比例反馈一样把偏离点拉回轨迹。诱导的条件边缘分布为

$$
p_\xi(a\mid t)=
\mathcal N\left(a\mid\xi(t),\sigma_0^2e^{-2kt}I\right).
$$

再用 CFM 学习历史条件速度：

$$
\mathcal L=
\mathbb E_{(h,\xi),t,a\sim p_\xi(\cdot\mid t)}
\|v_\theta(a,t\mid h)-v_\xi(a,t)\|^2.
$$

### 它的关键收益

- 不必等待整个 action chunk 的去噪/flow 完成；
- 只计算实际要执行的轨迹前缀；
- 天然适合 receding horizon 和紧密 sensorimotor loop；
- 稳定项可减轻行为克隆中的分布偏移。

### 它的重要限制

论文保证匹配每个物理时刻的动作边缘分布，但不保证整条轨迹的 joint distribution：

$$
p(a_t\mid h)\ \text{匹配}
\quad\not\Rightarrow\quad
p(a_{0:H}\mid h)\ \text{匹配}.
$$

当示范轨迹相交时，生成轨迹可能把不同示范片段重新组合。对需要严格时序关联的任务，这可能是致命弱点，也可能被视为组合泛化的来源。

> 🤖 **绕瓶例子能不能说明这个问题？** 原版的绕瓶例子说明不了。远侧和近侧两条路线只在起点和终点相遇，中途不交叉，SFP 不会把它们拼错。
>
> 把例子改一下就能看到问题：桌上有**两个**瓶子，示范 A 是「先从远侧绕第一个，再从近侧绕第二个」，示范 B 是「先近侧再远侧」。两条示范在两个瓶子之间的中线上**交叉**。
>
> SFP 只保证每个时刻夹爪的位置分布对得上，即每一刻都是一半在远侧、一半在近侧。它不保证「先远后近」这个组合关系，所以可能生成「先远侧、在交叉点之后还是远侧」这种示范里从没出现过的路线。在这个例子里新路线恰好也合法，但如果第二个瓶子只能从近侧绕，它就会撞上去。这正是 `06` 第 1 节 Day 6 要你构造的反例。

## 7. 机器人中 FM 的主要优势与真实代价

### 优势

1. **连续动作**：无需把关节动作量化成离散 token。
2. **多模态**：不同噪声初值可产生不同合法策略模式。
3. **action chunk**：联合建模多个未来动作，增强短期时序一致性。
4. **训练简单**：监督是随机时间点上的 MSE，无训练内 ODE rollout。
5. **与大模型兼容**：action expert 可作为 VLM 后缀或独立 decoder。

### 代价

1. 推理需要多次网络调用，实时性取决于 NFE、缓存和硬件。
2. 行为克隆的 covariate shift 并不会因使用 FM 自动消失。
3. 多模态生成不等于会选对模式；仍需条件信息、任务语义或价值信号。
4. action normalization、不同 embodiment 的维度/量纲和无效关节 mask 会直接影响路径几何。
5. 低训练 loss 不保证闭环成功；solver error 和闭环反馈会改变部署分布。

## 8. 实验设计必须报告什么？

### 生成侧

- probability path 与 source distribution；
- velocity/noise/data/score 参数化；
- time sampling distribution；
- train loss weighting；
- solver、步长、NFE；
- stochastic/deterministic sampling 设置。

### 控制侧

- observation horizon、prediction horizon、execution horizon；
- 控制频率、端到端 latency、是否 KV cache；
- position/velocity/delta action 表示与 normalization；
- receding-horizon 频率、action smoothing 或 temporal ensemble；
- 任务成功率之外的碰撞、jerk、超时和恢复指标。

### 公平对比

至少固定相同 encoder、action decoder 容量、训练步数和数据；报告 success–NFE 和 latency–success 曲线。只比较“FM 10 步 vs diffusion 100 步”不足以区分 objective、solver 和预算三个因素。

## 9. 值得做的研究问题

1. VGGT/VGGT-Ω 等几何表征作为条件，能否减少 action flow 在空间歧义处的条件速度方差？
2. 是否可依据任务几何自适应设计 action-space coupling，而不是独立配对噪声和动作？
3. 不同 action 维度量纲下，欧氏 MSE 是否是合适的几何？SE(3)/manifold FM 是否更合理？
4. 能否用 curvature 或 local truncation error 预测每个时刻所需 NFE，进行自适应实时推理？
5. Streaming Flow Policy 的 marginal-only 保证在哪类接触丰富任务上会破坏 joint temporal consistency？
6. action expert 的 register/scene/geometry tokens 应作为固定条件、动态条件，还是用于改变 probability path？

## 10. 一段可直接复用的机器人训练伪代码

```python
# observation: images, language, proprioception
# action: [B, H, action_dim]
context = encoder(observation)
action_data = batch["action_chunk"]
action_noise = torch.randn_like(action_data)
tau = sample_time(batch_size)                # [B, 1, 1]

action_tau = (1 - tau) * action_noise + tau * action_data
target_velocity = action_data - action_noise
pred_velocity = action_expert(action_tau, tau, context)

loss = ((pred_velocity - target_velocity) ** 2 * action_mask).sum() \
       / action_mask.sum()
```

推理时把 `action_noise` 作为初值，用 Euler/Heun 积分 `action_expert`，得到 action chunk；执行前若干步后重规划。

对应的推理代码（10 步 Euler）：

```python
@torch.no_grad()
def infer(observation, n_steps=10):
    context = encoder(observation)                     # 只算一次（π0 里就是 KV cache）
    A = torch.randn(1, H, action_dim)                  # 随机草稿
    for i in range(n_steps):
        tau = torch.full((1, 1, 1), i / n_steps)
        A = A + (1 / n_steps) * action_expert(A, tau, context)
    return unnormalize(A)                              # 别忘了反归一化
```

---

## 11. 2024–2026 的三个新问题（白话版，配绕瓶例子）

> 原版资料包写于 2026-08，这一节补上它没覆盖、但做机器人 FM 绕不开的三件事。每一件都给出「问题是什么、现在怎么解、绕瓶例子里长什么样」。更完整的技术细节见新包 `../flow_matching/03_机器人中的FM.md`。

### 11.1 少步：能不能 1 步就出动作？

**问题。** 推理延迟大约等于 NFE 乘以单次网络时间。π0 用 10 步；如果能压到 1–2 步，控制频率能高很多。

**为什么直接减步数不行。** `01` 第 9 节已经说明：1 步 Euler 落在所有示范的平均值上，绕瓶例子里就是撞瓶。完美速度场 1 步碰撞率 100%；真实网络在 32 维 chunk 上也有 95.7%。

**现在的三条解法**（都已有机器人版本，arXiv 编号已核实）：

| 路线 | 一句话 | 机器人版本 |
|---|---|---|
| 蒸馏 | 先训练一个多步的老师，再教一个学生「一步跳到老师最终会到的地方」 | Consistency Policy（2405.07503） |
| 自洽 | 网络额外读一个「步长」输入，并要求「一大步 = 两小步」 | Shortcut Models（2410.12557，论文自带机器人实验） |
| 平均速度 | 不学「此刻往哪走」，直接学「从这里到终点的平均速度」 | MeanFlow（2505.13447）；机器人版 DMPO（2601.20701） |

**绕瓶例子实测**（新包 `../flow_matching/04_实验记录.md` 第 4 节，3 个种子）：1 步碰撞率，FM 95.7%，Shortcut 8.8%，MeanFlow 6.8%。

### 11.2 实时执行：推理期间机器人在干什么？

**问题。** 大模型推理要花好几个控制周期。RTC 论文给过一个例子：RTX 4090 上 3B 参数的 π0，光是图像和文本前缀的 KV 缓存就要 46ms，而控制目标是 50Hz（每 20ms 一步）。所以新 chunk 算出来之前，机器人只能继续执行旧 chunk。

**绕瓶例子里会出什么事。**

- 旧 chunk 是从远侧绕的，新 chunk 重新抽噪声，可能抽到了近侧。
- 两段接不上，夹爪会突然横跳，甚至在两种绕法之间来回摇摆（mode jumping）。

**现在的两代解法。**

- **推理期 RTC（2506.07339）**：新 chunk 的前 $d$ 步注定会被旧 chunk 覆盖执行，就把它们「冻结」成旧 chunk 的动作，只生成剩下的部分。实现方式是在**每一个 flow 步**加一项引导，把预测的干净动作 $\hat A^1$（`02` 第 9 节）往旧动作上拉。论文提到，步数少时这个引导不稳定，需要加裁剪。
- **训练期 RTC（2512.05964）**：训练时就随机把前 $d$ 个动作设成已知（干净），让网络学会「接着已知的开头往下写」。推理时直接把旧动作当条件输入，不需要引导，也没有额外开销。

**一个开放问题**：推理期引导需要多个 flow 步才有地方插手，少步模型（11.1）把这个空间压没了。两者怎么兼容，还没有系统的研究。

### 11.3 强化学习微调：示范不够好时怎么继续变强？

**问题。** 行为克隆最多学到和示范一样好。想用 PPO 之类的算法在仿真里继续提升，就需要 $\log\pi(A\mid o)$。flow policy 的这个量要沿整条轨迹积分散度（`02` 第 3 节），又贵又不稳定。

**绕瓶例子里会是什么样。** 假设近侧绕法其实更快。RL 要做的是把「去近侧」的概率从 50% 提高到 90%，也就是改变速度场，让更多噪声被推向近侧。

**现在的解法。**

| 方法 | 怎么拿到 $\log\pi$ |
|---|---|
| DPPO（2409.00588） | 把去噪链看成一串高斯转移（SDE 式，见 `03` 第 7 节），每一步的概率都能算 |
| ReinFlow（2505.22094） | 往 ODE 的每一步注入可学习的噪声，把它变成能算概率的马尔可夫链；能微调 1–4 步的少步策略 |
| 噪声空间 RL | 不改动策略本身，只学「该抽什么样的初始噪声」。绕瓶例子里就是「多抽负噪声」，因为负噪声对应近侧。**这条路线我只看到了标题，没读原文** |

