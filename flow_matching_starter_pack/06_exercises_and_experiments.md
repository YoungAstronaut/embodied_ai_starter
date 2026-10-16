# 06. 习题、最小实验与一周学习计划

## 1. 一周计划

### Day 1：建立基本对象

- 读 `01_core_concepts.md`。
- 读 Guide 的 Quick Tour（PDF 第 4–7 页）。
- 手写解释 $x_t$、$p_t$、ψ_t、$u_t$ 的区别。

验收：不看笔记写出 linear CFM 的训练和采样伪代码。

### Day 2：完成数学推导

- 读 `02_formula_derivations.md`。
- 读原始 FM 论文第 2–4 节。
- 独立推导连续性方程弱形式与 CFM 梯度等价。

验收：能解释“随机条件速度标签为什么学出确定边缘速度”。

### Day 3：跑通二维实验

- 运行 `code/toy_flow_matching.py`。
- 比较 Euler/Heun 以及 NFE = 4, 8, 16, 32。
- 保存相同随机种子的轨迹图和终点样本。

验收：画出 sample quality 对 NFE 的曲线，并区分训练误差和 solver 误差。

### Day 4：理解 Rectified Flow 与 coupling

- 读 `03_diffusion_rectified_flow_comparison.md`。
- 读 Rectified Flow 第 2 节、OT-CFM 第 3 节。
- 在二维脚本中尝试一个粗糙 minibatch matching，观察交叉和 NFE。

验收：说明“conditional straight”为什么不等于“marginal trajectories straight”。

### Day 5：理解机器人 action chunk

- 读 `04_robotics_vla_application.md`。
- 读 Diffusion Policy 第 2–4 节。
- 把二维脚本的数据变量替换成 $H\times d_a$ 的 synthetic action chunk。

验收：清楚区分 flow time 与 robot time。

### Day 6：精读 π0 与 Streaming Flow Policy

- π0 第 IV 节逐式对应 CFM。
- Streaming Flow Policy 第 2–5 节，重点看稳定条件流。
- 写一页对比：标准 action-chunk FM vs streaming flow。

验收：指出 SFP 的 marginal-only 限制，并构造一个会失败的交叉轨迹例子。

### Day 7：形成研究计划

- 选择一个变量：geometry conditioning、coupling、path、time sampling、solver 或 streaming。
- 写出一个可证伪假设、主要指标、两个强基线和最小资源预算。
- 不先堆大 VLA；先在低维/小型 imitation benchmark 验证机制。

## 2. 公式习题

### 习题 1：边缘速度

给定 $X_t=(1-t)X_0+tX_1$，证明平方回归的最优解是

$$
v^*(x,t)=E[X_1-X_0\mid X_t=x].
$$

提示：对固定 ((x,t)) 使用条件均方误差分解。

### 习题 2：Gaussian path

对 $X_t=\alpha_tX_1+\sigma_t\epsilon$，推导条件速度的两种形式：

$$
\dot\alpha_tX_1+\dot\sigma_t\epsilon
$$

与

$$
\frac{\dot\sigma_t}{\sigma_t}(X_t-\alpha_tX_1)+\dot\alpha_tX_1.
$$

指出第二式在何种端点可能数值不稳定。

### 习题 3：连续性方程

考虑一维 $u_t(x)=c$ 常速度，初始密度 $p_0$。证明

$$
p_t(x)=p_0(x-ct)
$$

满足连续性方程，并解释这是分布平移。

### 习题 4：确定性与多模态

构造一个一维源高斯到双峰 Gaussian mixture 的概念性 ODE。无需写解析速度，但要说明随机性位于哪里、给定初值后为何仍确定。

### 习题 5：CFM 梯度方差

当多个条件路径在同一 $(x,t)$ 给出方向差异很大的速度时，CFM 的均值仍正确，但优化会怎样？说明 minibatch OT 或 better conditioning 为什么可能有帮助。

### 习题 6（机器人）：推导绕瓶例子的速度场

示范是 $\pm1$ 各一半，线性路径。不看 `02` 第 5.5 节，自己推出

$$
u_t(x)=\frac{\tanh\big(x\,t/(1-t)^2\big)-x}{1-t},
$$

并回答：$t=0$ 时速度是多少？为什么这意味着 1 步 Euler 一定撞瓶？

### 习题 7（机器人）：示范比例不均

如果 70% 的示范从远侧绕，速度场公式里的 tanh 要怎么改？推理时远侧的比例会变成多少？对照 `01` 第 3 节的连续性方程解释为什么。

**提示**：后验比要多乘一个先验比 $0.7/0.3$，所以 tanh 里多一个 $\tfrac12\ln(0.7/0.3)$。

### 习题 8（机器人）：条件能降低标签方差吗？

假设相机能看到「示范者今天习惯从哪边绕」（比如桌上一个提示物），把它作为条件 $c$ 输入网络。速度场会变成什么样？1 步 Euler 还会撞瓶吗？

这就是 `06` 第 5 节假设 A（几何条件降低速度标签歧义）的最小版本。

<details>
<summary>习题 6–8 参考答案</summary>

**习题 6**：$t=0$ 时 $\tanh(0)=0$，速度为 $-x$，1 步正好走到 0。原因是 $t=0$ 时草稿就是纯噪声，和它最终要去的示范无关，网络只能指向平均值。

**习题 7**：

$$
\mathbb E[y_1\mid x]=\tanh\!\Big(\tfrac{xt}{(1-t)^2}+\tfrac12\ln\tfrac{0.7}{0.3}\Big).
$$

推理时远侧比例约 70%。连续性方程保证草稿只被搬运，不增不减，所以终点的比例等于示范的比例。

**习题 8**：给定 $c$ 之后，示范只剩一个模式，后验不再有歧义，$\mathbb E[y_1\mid x,c]=\pm1$。速度在 $t=0$ 时就直接指向那一侧，1 步不会撞瓶。**能消除多模态的条件信息，同时也消除了少步的困难。**
</details>

## 3. 二维最小实验

### 环境

```bash
cd "/Users/youngastronaut/Documents/embodied ai/flow_matching_starter_pack/code"
PY=/Users/youngastronaut/.workbuddy/binaries/python/envs/default/bin/python   # 已装好 torch / numpy / matplotlib
$PY toy_flow_matching.py --help
```

依赖：PyTorch、Matplotlib。默认在 CPU 可运行；如果检测到 CUDA 会自动使用。

### 第 0 个实验（先做这个）：绕瓶例子，不用训练

```bash
$PY robot_1d_intuition.py
```

它会打印 `01` 里引用的全部数字表，并在 `../figures/` 下画出 4 张图。整个速度场是解析解，所以几秒钟就能跑完。建议边看 `01` 边改脚本里的参数：

- 把示范改成 70% 远侧、30% 近侧：在 `posterior_mean` 里给 tanh 加一个偏置项 $\tfrac12\ln(0.7/0.3)$，看远侧比例是不是变成 70%；
- 把瓶子 `OBST` 改大，看需要多少步才不碰撞。

### 基础运行

```bash
$PY toy_flow_matching.py --train-steps 5000 --nfe 16 --solver heun --output-dir toy_results
```

脚本将保存：

- `samples.png`：源噪声、若干中间 flow time、最终样本与真实数据；
- `model.pt`：模型权重和实验参数；
- `metrics.json`：最终训练 loss、采样矩和运行设置。

### NFE 消融

固定 checkpoint 和 sample seed，对 `nfe ∈ {2,4,8,16,32,64}` 采样。至少报告：

- 终点到最近目标 mode 的平均距离；
- mode coverage；
- 各 mode 样本占比的 KL/TV；
- wall-clock latency；
- Euler 与 Heun 的网络评估次数，而不是只报告 step 数。

## 4. 从二维数据改成 synthetic action chunk

先不要接入真实图像。令 condition $c\in\mathbb R^2$ 表示起点和目标，构造两种合法动作模式：从障碍物左侧或右侧绕行。每个动作块为

$$
A\in\mathbb R^{H\times2}.
$$

把网络输入从 `(x_t, t)` 改成 `(A_tau.flatten(), tau, c)`，输出同维 velocity。研究：

1. 相同条件下是否覆盖左右两个 mode？
2. action chunk 长度增加时需要多大网络容量？
3. 不同 NFE 对碰撞率和轨迹 jerk 的影响？
4. 只执行前 $H_{exec}$ 步并重规划，能否纠正模型误差？

## 5. 面向 CVPR 的最小可证伪研究模板

### 假设 A：几何条件降低速度标签歧义

假设：显式 3D geometry feature $g(o)$ 使

$$
\mathrm{Var}[U_c\mid A^\tau,\tau,o,g(o)]
<
\mathrm{Var}[U_c\mid A^\tau,\tau,o],
$$

从而提高少 NFE 下的成功率。

最小实验：在有遮挡/视角变化的 Push-T 或 LIBERO 子集上，固定 action decoder，只改变条件表示；测 gradient target variance proxy、trajectory curvature、success–NFE。

可证伪条件：加入 geometry 后 variance/curvature 不降，或同等 latency 下 success 不升。

### 假设 B：任务感知 coupling 优于独立 coupling

假设：以末端位姿/抓取拓扑定义的 minibatch cost 配对噪声 latent 与 action chunk，比纯欧氏 OT 或独立 coupling 更易学习。

最小实验：小型 transformer action decoder，三种 coupling，固定总训练 FLOPs；比较 convergence、NFE–success 和 mode coverage。

可证伪条件：收益只来自额外计算，或跨任务泛化下降。

### 假设 C：自适应 solver 能改善实时闭环

假设：用 velocity change/curvature 估计局部难度，按 observation 动态分配 NFE，在同平均 latency 下优于固定步数。

最小实验：固定训练模型，仅改 solver；报告 NFE 分布、P50/P95 latency、success、jerk 和紧急停止率。

可证伪条件：自适应误判导致尾延迟增加，或对成功率无显著改善。

### 假设 D：Streaming marginal mismatch 可被显式 joint regularizer 修复

假设：在 SFP 上加入短窗速度/加速度联合统计匹配，能保留流式低延迟同时减少轨迹拼接错误。

最小实验：先用两条相交 synthetic trajectories 精确展示失败，再扩展到 contact-rich manipulation。

可证伪条件：joint regularizer 破坏流式性质，或不减少错误组合模式。

## 6. 实验记录模板

每次实验至少记录：

```text
Experiment ID:
Hypothesis:
Data / split / seed:
Condition encoder:
Generated variable and shape:
Source distribution:
Coupling:
Probability path / scheduler:
Target parameterization:
Time sampling and loss weighting:
Network / parameters:
Optimizer / steps / batch:
Solver / NFE:
Prediction horizon / execution horizon / control Hz:
Latency P50/P95:
Offline metrics:
Closed-loop metrics:
Failure examples:
Conclusion and next falsification:
```

## 7. 完成标准

只有同时满足以下条件，才算真正入门：

1. 能从零写出 linear CFM 训练与 ODE 采样；
2. 能推导 marginalization trick 和 CFM 梯度等价；
3. 能解释 FM 与 diffusion 的重合边界；
4. 能区分 conditional path straight 与 learned trajectory straight；
5. 能把 π0 的公式逐项还原为 action-chunk CFM；
6. 能为一个机器人 FM 改进提出带强基线、资源预算和可证伪条件的实验。

