# 02. 从连续性方程到 Conditional Flow Matching

本文默认变量位于欧氏空间 ℝ^d，密度足够光滑，速度场满足局部 Lipschitz 与可积条件，从而 ODE 解存在且唯一。研究中使用定理时，应回到原文核查正则性假设。

> **2026-10-13 补充**：每一节后面加了「🤖 机器人里这是什么」，都用 `01` 里的绕瓶例子来解释：$y$ 是夹爪经过瓶子时的横向偏移，示范是 $\pm1$ 各一半。另外新增 **第 5.5 节**，把整套推导在这个例子上完整手算一遍，最终得到一个能直接画出来的速度场公式。**建议先读 5.5，再回头看 5–7 节的一般推导。**
>
> 下文的 $X$ 在机器人里就是「一份动作草稿」：1D 例子里是一个数，真实策略里是一个 $H\times d_a$ 的 action chunk。

## 1. ODE 如何搬运一个分布？

给定速度场 $u_t(x)$，定义 flow map：

$$
\frac{d}{dt}\psi_t(x)=u_t(\psi_t(x)),\qquad \psi_0(x)=x.
$$

若 $X_0\sim p_0$，令 $X_t=\psi_t(X_0)$，则 $X_t$ 的密度记作 $p_t$，即

$$
p_t=(\psi_t)_\#p_0.
$$

这里 $\#$ 表示 push-forward：先按 $p_0$ 采样，再经过 $\psi_t$ 映射所得的分布。

> 🤖 **机器人里这是什么**：$p_0$ 是「随机抽的动作草稿」的分布，$\psi_1$ 是「整个推理过程」，$(\psi_1)_\#p_0$ 是「这个策略会输出的动作的分布」。训练的目标就是让它等于专家示范的分布 $q(A\mid o)$。

## 2. 连续性方程的弱形式直觉

取任意光滑测试函数 $f$。由链式法则，

$$
\frac{d}{dt}\mathbb E[f(X_t)]
=\mathbb E[\nabla f(X_t)^\top u_t(X_t)].
$$

写成密度积分：

$$
\frac{d}{dt}\int f(x)p_t(x)dx
=\int \nabla f(x)^\top u_t(x)p_t(x)dx.
$$

对右侧分部积分并忽略无穷远边界项：

$$
\int \nabla f^\top(p_tu_t)dx
=-\int f\,\nabla\cdot(p_tu_t)dx.
$$

由于这对任意 $f$ 成立，得到

$$
\boxed{\partial_t p_t+\nabla\cdot(p_tu_t)=0.}
$$

它是速度场生成概率路径的判据。

> 🤖 **机器人里这是什么**：测试函数 $f$ 可以随便选，选一个有物理意义的就好懂了。取 $f(y)=\mathbb 1[y>0]$（「草稿是否在远侧」），$\mathbb E[f(X_t)]$ 就是「此刻在远侧的草稿占多少」。上面的推导说的是：这个比例的变化率，完全由速度场在分界线 $y=0$ 处把多少草稿推过去决定。草稿不会凭空出现或消失，所以最终远侧的比例，等于一路上被推过分界线的净量。实测这个比例是 49.7%，和示范一致（`01` 第 3 节）。

## 3. 沿轨迹的密度变化

沿 $X_t$ 求导：

$$
\frac{d}{dt}\log p_t(X_t)
=\partial_t\log p_t(X_t)
+\nabla\log p_t(X_t)^\top\dot X_t.
$$

将连续性方程展开：

$$
\partial_t p_t
=-u_t^\top\nabla p_t-p_t\nabla\cdot u_t.
$$

除以 $p_t$ 并用 $\dot X_t=u_t(X_t)$，可得交叉项抵消：

$$
\boxed{
\frac{d}{dt}\log p_t(X_t)=-\nabla\cdot u_t(X_t).
}
$$

这给出 CNF 的 likelihood 公式：

$$
\log p_1(X_1)=\log p_0(X_0)-\int_0^1\nabla\cdot u_t(X_t)dt.
$$

传统 maximum-likelihood CNF 训练需要在训练环内求解 ODE，并对解反向传播；FM 通过预先设计概率路径，把问题改造成局部回归。

> 🤖 **机器人里这是什么**：这个公式就是「这个 flow policy 输出动作 $A$ 的对数概率 $\log\pi(A\mid o)$」。行为克隆用不到它，但**用 PPO 之类的强化学习微调 flow policy 时必须用到**。它要求沿整条轨迹积分散度：动作是 32 维时，每一步都要算一个 32×32 Jacobian 的迹，既贵又不稳定。DPPO、ReinFlow 这些工作都是在想办法绕开它（`04` 第 11 节）。

## 4. 理想的 Flow Matching 目标

设我们规定了概率路径 $p_t$，并有一个生成它的目标速度 $u_t$。参数化速度 $v_\theta$ 的目标为

$$
\mathcal L_{\mathrm{FM}}(\theta)
=\mathbb E_{t\sim U[0,1],X_t\sim p_t}
\|v_\theta(X_t,t)-u_t(X_t)\|^2.
$$

若损失为零，则 $v_\theta=u_t$（在 $p_t$ 几乎处处意义下），其 ODE 生成同一概率路径。

真正困难的是 $u_t(x)$ 往往依赖未知数据密度和全数据积分，不能直接作为逐样本标签。

> 🤖 **机器人里这是什么**：「全数据积分」的意思是，要知道草稿在某个位置该往哪推，你得**同时**考虑所有示范、判断它最像哪一条。第 5.5 节会看到，1D 绕瓶例子里这件事刚好能写成一个 tanh。但真实的 action chunk 有上万条示范，每条还对应不同的观测，没有人写得出这个积分。

## 5. 条件路径的边缘化

引入条件变量 $Z\sim p_Z$。它可以是：

- 单个目标样本 $X_1$；
- 一对端点 $(X_0,X_1)$；
- 具有配对关系的 source-target 样本；
- 更一般的桥接变量。

对每个 $z$，设计条件路径 $p_t(x\mid z)$ 与条件速度 $u_t(x\mid z)$，使其满足

$$
\partial_t p_t(x\mid z)
+\nabla\cdot[p_t(x\mid z)u_t(x\mid z)]=0.
$$

定义边缘路径：

$$
p_t(x)=\int p_t(x\mid z)p_Z(z)dz.
$$

再定义

$$
u_t(x)
=\frac{\int u_t(x\mid z)p_t(x\mid z)p_Z(z)dz}{p_t(x)}.
$$

利用 Bayes 公式，可写成

$$
\boxed{
u_t(x)=\mathbb E[u_t(X_t\mid Z)\mid X_t=x].
}
$$

把条件连续性方程对 $z$ 积分：

$$
\begin{aligned}
\partial_t p_t(x)
&=\int \partial_t p_t(x\mid z)p_Z(z)dz\\
&=-\nabla\cdot\int p_t(x\mid z)u_t(x\mid z)p_Z(z)dz\\
&=-\nabla\cdot[p_t(x)u_t(x)].
\end{aligned}
$$

因此这个后验平均速度确实生成边缘概率路径。这就是 marginalization trick。

## 5.5 在绕瓶例子上把整套推导手算一遍

这一节把第 4–5 节的每个抽象对象都算成具体公式。数字可以用 `code/robot_1d_intuition.py` 复现。

**设定。**

- 示范分布：$q=\tfrac12\delta_{+1}+\tfrac12\delta_{-1}$，也就是一半远侧（$+1$），一半近侧（$-1$）。
- 条件变量就取那条示范本身：$Z=y_1\in\{+1,-1\}$。
- 线性路径：$X_t=(1-t)\varepsilon+t\,y_1$，其中 $\varepsilon\sim\mathcal N(0,1)$。

**第 1 步：条件路径。** 固定一条示范 $y_1$，草稿在进度 $t$ 时的分布是

$$
p_t(x\mid y_1)=\mathcal N\big(x;\ t\,y_1,\ (1-t)^2\big).
$$

意思是：一份**注定要去 $y_1$** 的草稿，在 $t$ 时刻的位置是「已经走了 $t$ 成路程」，再加上剩余的 $(1-t)$ 份噪声。

**第 2 步：条件速度。** 由 $x=(1-t)\varepsilon+t\,y_1$ 反解出 $\varepsilon=\frac{x-t\,y_1}{1-t}$，代入 $y_1-\varepsilon$：

$$
u_t(x\mid y_1)=\frac{y_1-x}{1-t}.
$$

意思是：直直地朝目标示范走，剩余时间越少，走得越快。

**第 3 步：边缘路径。** 把两条示范的条件路径按 50/50 混起来：

$$
p_t(x)=\tfrac12\,\mathcal N(x;\ t,(1-t)^2)+\tfrac12\,\mathcal N(x;\ -t,(1-t)^2).
$$

这就是 `01` 里图 2 画的那五个形状：$t$ 小时两个高斯重叠成一团，$t$ 大时分开成两包。

**第 4 步：后验。** 「草稿在 $x$ 时，它来自远侧示范的概率」用贝叶斯公式算。两个高斯方差相同，指数部分相减后只剩一项：

$$
P(y_1=+1\mid X_t=x)
=\frac{\mathcal N(x;t,(1-t)^2)}{\mathcal N(x;t,(1-t)^2)+\mathcal N(x;-t,(1-t)^2)}
=\mathrm{sigmoid}\!\left(\frac{2xt}{(1-t)^2}\right).
$$

因此

$$
\mathbb E[y_1\mid X_t=x]=2P-1=\tanh\!\left(\frac{x\,t}{(1-t)^2}\right).
$$

**第 5 步：边缘速度**（也就是训练到完美时网络会学成的样子）。对条件速度取后验平均：

$$
\boxed{\;
u_t(x)=\mathbb E\!\left[\frac{y_1-x}{1-t}\,\Big|\,X_t=x\right]
=\frac{\tanh\!\big(x\,t/(1-t)^2\big)-x}{1-t}
\;}
$$

**读这个公式：**

- $t=0$：$\tanh(0)=0$，所以 $u_0(x)=-x$。所有草稿都被拉向 $0$，也就是瓶子。走 1 步 Euler 正好落在 $0$。这就是 `01` 第 9 节「1 步撞瓶」的精确来源。
- $t$ 增大：$\frac{t}{(1-t)^2}$ 迅速变大，$\tanh$ 很快变成 $\pm1$ 的硬判断，草稿被果断推向自己那一侧。
- $x=0$：速度永远是 $0$。恰好停在正中间的草稿永远犹豫不决。不过一份草稿恰好等于 $0$ 的概率是 0。

> 🤖 **机器人里这是什么**：网络每一步其实都在**隐式地做贝叶斯推断**——「看草稿现在的样子，它最可能是在模仿哪条示范？」然后朝那些示范的加权平均走。早期证据不足，只能往平均值走；后期证据充分，才果断选边。**少步生成之所以危险，就是因为它在证据还不足的早期就迈了一大步。**

## 6. 为什么 CFM 与 FM 的梯度相同？

定义可计算的 CFM：

$$
\mathcal L_{\mathrm{CFM}}(\theta)
=\mathbb E_{t,Z,X_t\sim p_t(\cdot\mid Z)}
\|v_\theta(X_t,t)-u_t(X_t\mid Z)\|^2.
$$

对平方项展开。简记 $V=v_\theta(X_t,t)$、$U_c=u_t(X_t\mid Z)$、$U=\mathbb E[U_c\mid X_t]$：

$$
\mathbb E\|V-U_c\|^2
=\mathbb E\|V\|^2-2\mathbb E[V^\top U_c]+\mathbb E\|U_c\|^2.
$$

由 tower property，

$$
\mathbb E[V^\top U_c]
=\mathbb E\{V^\top\mathbb E[U_c\mid X_t]\}
=\mathbb E[V^\top U].
$$

而

$$
\mathcal L_{\mathrm{FM}}
=\mathbb E\|V\|^2-2\mathbb E[V^\top U]+\mathbb E\|U\|^2.
$$

因此

$$
\mathcal L_{\mathrm{CFM}}
=\mathcal L_{\mathrm{FM}}
+\underbrace{\mathbb E\|U_c\|^2-\mathbb E\|U\|^2}_{\text{与 }\theta\text{ 无关}},
$$

所以

$$
\boxed{
\nabla_\theta\mathcal L_{\mathrm{CFM}}
=\nabla_\theta\mathcal L_{\mathrm{FM}}.
}
$$

从统计回归角度，MSE 对随机标签 $U_c$ 的最优预测就是条件均值 $E[U_c\mid X_t]$，它恰好是边缘速度 $u_t(X_t)$。

> 🤖 **机器人里这是什么：为什么训练 loss 降不到 0。** 那个「与 $\theta$ 无关」的常数项 $\mathbb E\|U_c\|^2-\mathbb E\|U\|^2=\mathbb E[\mathrm{Var}(U_c\mid X_t)]$，就是「同一份草稿收到的标签有多不一致」。在绕瓶例子里，早期的草稿一半时间被告知往远侧、一半时间被告知往近侧，这部分方差网络永远消除不了。
>
> 所以**训练一个 flow policy 时，loss 曲线停在一个明显大于 0 的平台上，是正常的，不代表没训好**。新包 `../flow_matching/code/fm_lab.py` 的 8-Gaussian 实验里，FM 的 loss 就一直停在 3.2 左右。判断训没训好要看采样结果，不看 loss 的绝对值。

## 7. 线性路径的完整推导

取任意 coupling $(X_0,X_1)\sim\pi_{0,1}$，并定义

$$
X_t=(1-t)X_0+tX_1.
$$

对一对固定端点 $(x_0,x_1)$，条件 flow 为

$$
\psi_t(x_0\mid x_1)=(1-t)x_0+t x_1.
$$

求导：

$$
\dot\psi_t=x_1-x_0.
$$

故 CFM 目标为

$$
\boxed{
\mathcal L(\theta)=
\mathbb E_{t,(X_0,X_1)\sim\pi_{0,1}}
\|v_\theta(X_t,t)-(X_1-X_0)\|^2.
}
$$

其最优边缘速度为

$$
v^*(x,t)=\mathbb E[X_1-X_0\mid X_t=x].
$$

注意：训练标签是某条条件直线的速度，但网络最终学到的是所有经过 $(x,t)$ 的条件直线速度的后验平均。若不同条件直线相交，ODE 的唯一性要求学到的边缘流在交点处“重新接线”，而不能同时沿多个方向穿过。

> 🤖 **机器人里这是什么**：看 `01` 的图 3。左图是训练时的条件直线：一份正噪声被随机配给了近侧示范，于是它的直线要穿过中线往下走，和别的直线大量交叉。右图是推理时网络真正走的轨迹：**互不交叉**，正噪声一律去远侧，负噪声一律去近侧。
>
> 这就是「重新接线」：训练时的配对是随机的，推理时的配对是网络自己重新排出来的，而且排得很「省力」（噪声在哪边就去哪边）。这也解释了为什么 reflow 和 OT coupling 能让轨迹变直：它们直接用这种省力的配对来训练（`03` 第 4–5 节）。

## 8. 一般 affine/Gaussian 路径

设

$$
X_t=\alpha_tX_1+\sigma_tX_0,
$$

其中 $X_0\sim\mathcal N(0,I)$，则

$$
X_t\mid X_1=x_1\sim
\mathcal N(\alpha_tx_1,\sigma_t^2I).
$$

直接求导得到条件监督：

$$
\boxed{
\dot X_t=\dot\alpha_tX_1+\dot\sigma_tX_0.
}
$$

若希望只用当前 $x=X_t$ 与目标 $x_1$ 表示，可由

$$
X_0=\frac{x-\alpha_t x_1}{\sigma_t}
$$

得到

$$
u_t(x\mid x_1)
=\frac{\dot\sigma_t}{\sigma_t}(x-\alpha_tx_1)
+\dot\alpha_t x_1.
$$

线性 CondOT scheduler 取 $\alpha_t=t,\ \sigma_t=1-t$，于是

$$
X_t=tX_1+(1-t)X_0,\qquad \dot X_t=X_1-X_0.
$$

> 🤖 **机器人里这是什么**：把 $\alpha_t=t,\ \sigma_t=1-t$ 代入第二个公式，得到 $u_t(x\mid x_1)=\frac{x_1-x}{1-t}$，和第 5.5 节第 2 步完全一样。第二个公式在 $t\to1$ 时分母趋于 0。在机器人里这一点很实际：网络如果在 $t$ 接近 1 的区域学得不准，误差会被放大。π0 用 beta 分布采 $t$、偏重噪声大的一端，部分原因就在这里。

## 9. velocity、data、noise、score 参数化的关系

对 Gaussian affine path，常见网络输出可以是：

- velocity：$u_t(x)$；
- data prediction：$\hat x_1(x,t)\approx E[X_1\mid X_t=x]$；
- noise prediction：$\hat x_0(x,t)\approx E[X_0\mid X_t=x]$；
- score：$s_t(x)\approx\nabla_x\log p_t(x)$。

边缘速度为

$$
u_t(x)=\dot\alpha_tE[X_1\mid X_t=x]
+\dot\sigma_tE[X_0\mid X_t=x].
$$

Gaussian 条件路径还给出

$$
\nabla_x\log p_t(x)
=-\frac{1}{\sigma_t}E[X_0\mid X_t=x].
$$

所以在给定 scheduler 时，各种参数化可以相互转换。理论等价不代表数值完全等价：端点附近的系数可能产生奇异或放大模型误差，time sampling 和 loss weighting 也会改变优化难度。

> 🤖 **机器人里这是什么：「预测的干净动作」最有用。** 对线性路径，$\hat x_1=x+(1-t)\,v$，意思是「如果从这里一步走到底，草稿会变成什么动作」。在绕瓶例子里它就是 $\tanh(xt/(1-t)^2)$。
>
> 这个量在机器人里经常被直接拿来用。例如 RTC 要让新 chunk 的开头对齐旧 chunk 已经在执行的那几步，它就是拿每一步的 $\hat A^1$ 和旧动作比较，再把差值反传回去修正速度（`04` 第 11 节）。在 $t$ 很小的时候，$\hat x_1$ 接近「所有示范的平均」，也就是那条穿过瓶子的路线。所以在早期做这种比较，参考价值有限。

## 10. 条件生成与机器人动作

若还有观测条件 $C=c$，目标是 $q(x\mid c)$。只需让速度网络读取条件：

$$
v_\theta(x_t,t,c).
$$

条件 CFM：

$$
\mathcal L(\theta)
=\mathbb E_{c,X_1\sim q(\cdot\mid c),X_0,t}
\left\|
v_\theta(X_t,t,c)-(X_1-X_0)
\right\|^2.
$$

机器人中可令 $X_1=A=[a_t,\dots,a_{t+H-1}]\in\mathbb R^{H d_a}$，条件 $c$ 是图像、语言和本体状态。这不是修改 FM 定理，而只是把“数据样本”换成 action chunk，并加入条件输入。

> 🤖 **机器人里这是什么**：把绕瓶例子从 1 个数升级成真实形状。假设 chunk 是 16 个路点、每个路点 $(x,y)$，那么 $A\in\mathbb R^{16\times2}$，展平后是 32 维。
>
> 一个训练 batch 里有 256 个样本，网络每次看到的就是：
> - 256 份 $16\times2$ 的草稿；
> - 256 个进度 $t$；
> - 256 组观测（瓶子和杯子在图像里的位置）。
>
> 它输出 256 份 $16\times2$ 的「修改方向」。条件 $c$ 的作用是：瓶子在正中间时，速度场有两个出口（远侧、近侧）；瓶子挪到偏远侧时，示范大多从近侧走，速度场就变成主要只有一个出口。**同一个网络，靠读 $c$ 切换不同的速度场。**

## 11. 研究时必须注明的假设

1. 速度场需要足够正则，使 ODE 解唯一；否则“flow map”未必良定义。
2. 边缘路径密度为正等条件常用于写后验平均；严格定理见原论文。
3. CFM 的无偏性是对总体期望而言；有限 batch 下仍有梯度方差。
4. 线性条件路径不意味着学到的边缘 ODE 轨迹都是直线。
5. 数值 ODE 误差、模型逼近误差与训练统计误差是三个不同误差源。

