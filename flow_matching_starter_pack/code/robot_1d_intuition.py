"""贯穿全包的机器人例子：绕开水瓶去拿杯子。只用 1 个数，速度场有精确解，不需要训练任何网络。

场景
----
夹爪从桌子左边移到右边的杯子处，正中间放着一瓶水。人类示范了很多次：
大约一半从瓶子“远侧”绕（经过瓶子时横向偏移 +10cm），一半从“近侧”绕（-10cm）。

我们只关心一个数 y = “经过瓶子那一刻的横向偏移”，并按 10cm 归一化：
    示范里 y = +1（远侧绕） 或 y = -1（近侧绕），各占一半
    |y| < 0.3 就会碰到瓶子

这一个数的“数据分布”就是两根尖峰：q(y) = 0.5·δ(y-1) + 0.5·δ(y+1)。

为什么能有精确解
--------------
线性路径 y_t = (1-t)·ε + t·y1，ε~N(0,1)。给定 y1，y_t ~ N(t·y1, (1-t)²)。
用贝叶斯公式可以算出“草稿在 y_t=x 时，它的目标是 +1 的概率”，进而得到
    E[y1 | y_t = x] = tanh( x·t / (1-t)² )
    v*(x, t)        = ( tanh(x·t/(1-t)²) - x ) / (1-t)
这就是一个“训练到完美”的 flow policy 的速度场。下面所有数都来自这个公式。

用法
----
    python robot_1d_intuition.py            # 打印文档里用到的数字表，并把 4 张图存到 ../figures/
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

FIG = Path(__file__).resolve().parent.parent / "figures"
OBST = 0.3  # |y| < 0.3 视为碰撞


def posterior_mean(x: np.ndarray | float, t: float) -> np.ndarray:
    """E[y1 | y_t = x]：草稿当前在 x 时，“它最终要去的示范”的加权平均。"""
    return np.tanh(np.asarray(x) * t / max(1 - t, 1e-6) ** 2)


def velocity(x: np.ndarray | float, t: float) -> np.ndarray:
    """完美训练的 flow policy 速度场 v*(x,t)。"""
    return (posterior_mean(x, t) - np.asarray(x)) / max(1 - t, 1e-6)


def euler(x0: np.ndarray, nfe: int, t_end: float = 1.0) -> np.ndarray:
    x = np.array(x0, dtype=float)
    for i in range(nfe):
        t0 = i / nfe * t_end
        x = x + (t_end / nfe) * velocity(x, t0)
    return x


def tables() -> None:
    print("表 1：草稿在 x、进度 t 时，网络（完美情况下）给出的“目标估计”和“速度”")
    print(f"{'t':>5} {'x':>6} {'P(远侧)':>8} {'E[y1|x]':>8} {'v*':>8}")
    for t in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9]:
        for x in [0.0, 0.2, 0.5]:
            m = float(posterior_mean(x, t))
            print(f"{t:5.1f} {x:6.2f} {(1 + m) / 2:8.3f} {m:8.3f} {float(velocity(x, t)):8.3f}")
    print()

    print("表 2：同一个噪声 ε=+0.3，用不同步数（NFE）的 Euler 积分，最后落在哪")
    for nfe in [1, 2, 3, 4, 6, 10, 20, 100]:
        print(f"  NFE={nfe:3d}  ->  y = {float(euler(np.array([0.3]), nfe)[0]):+.3f}")
    print()

    print("表 3：Euler 2 步的逐步过程（ε=+0.3）")
    x, nfe = 0.3, 2
    for i in range(nfe):
        t0 = i / nfe
        m, v = float(posterior_mean(x, t0)), float(velocity(x, t0))
        x_new = x + (1 / nfe) * v
        print(f"  第{i + 1}步 t={t0:.1f}: x={x:+.3f}, E[y1|x]={m:+.3f}, v={v:+.3f} -> x={x_new:+.3f}")
        x = x_new
    print()

    print("表 4：同一个“完美”速度场，只改步数，10000 个噪声的碰撞率（|y|<0.3）")
    rng = np.random.default_rng(0)
    eps = rng.standard_normal(10000)
    for nfe in [1, 2, 3, 4, 6, 10, 20, 100]:
        y = euler(eps, nfe)
        print(f"  NFE={nfe:3d}  碰撞率 = {np.mean(np.abs(y) < OBST):6.1%}   远侧比例 = {np.mean(y > 0):.1%}")
    print()

    y = euler(eps, 200)
    agree = np.mean(np.sign(y) == np.sign(eps))
    print(f"表 5：200 步积分后，最终绕行方向与初始噪声符号一致的比例 = {agree:.1%}")


def figures() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False
    if not FIG.exists():
        FIG.mkdir()

    # 图 1：数据分布 + 为什么不能用回归
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw={"width_ratios": [1.6, 1]})
    rng = np.random.default_rng(1)
    demos = np.where(rng.random(200) < 0.5, 1.0, -1.0) + 0.06 * rng.standard_normal(200)
    ax[0].hist(demos, bins=60, range=(-1.6, 1.6), color="tab:orange")
    ax[0].axvspan(-OBST, OBST, color="tab:red", alpha=0.2, label="水瓶（碰撞区）")
    ax[0].axvline(demos.mean(), color="k", ls="--", label=f"MSE 回归的答案 ≈ {demos.mean():+.2f}")
    ax[0].set_title("200 次示范：经过瓶子时的横向偏移 y")
    ax[0].set_xlabel("y（+1 远侧绕，-1 近侧绕）"); ax[0].set_ylabel("次数"); ax[0].legend(fontsize=8)
    ts = np.linspace(0, 1, 50)
    for s in [1, -1]:
        ax[1].plot(ts, s * np.sin(np.pi * ts), color="tab:orange", lw=2)
    ax[1].plot(ts, 0 * ts, "k--", lw=2, label="两种示范的平均 = 直穿瓶子")
    ax[1].add_patch(plt.Circle((0.5, 0), OBST, color="tab:red", alpha=0.3))
    ax[1].set_ylim(-1.3, 1.6); ax[1].set_xlabel("前进方向"); ax[1].set_ylabel("横向偏移 y")
    ax[1].set_title("俯视图：夹爪的两种合法路线"); ax[1].legend(fontsize=8, loc="upper center")
    fig.tight_layout(); fig.savefig(FIG / "fig1_data_distribution.png", dpi=150); plt.close(fig)

    # 图 2：概率路径 p_t —— 1000 份草稿在不同进度时的分布
    fig, axes = plt.subplots(1, 5, figsize=(13, 2.6), sharey=True)
    xs = np.linspace(-2.5, 2.5, 400)
    for ax_, t in zip(axes, [0.0, 0.25, 0.5, 0.75, 0.95]):
        s = max(1 - t, 1e-3)
        dens = 0.5 * (np.exp(-(xs - t) ** 2 / (2 * s * s)) + np.exp(-(xs + t) ** 2 / (2 * s * s))) / (s * np.sqrt(2 * np.pi))
        ax_.fill_between(xs, dens, color="tab:blue", alpha=0.5)
        ax_.axvspan(-OBST, OBST, color="tab:red", alpha=0.15)
        ax_.set_title(f"进度 t = {t}"); ax_.set_xlabel("草稿的 y")
    axes[0].set_ylabel("密度 p_t(y)")
    fig.suptitle("概率路径：同时扔很多份噪声草稿，它们的“整体形状”随进度 t 的变化", y=1.03)
    fig.tight_layout(); fig.savefig(FIG / "fig2_probability_path.png", dpi=150, bbox_inches="tight"); plt.close(fig)

    # 图 3：左＝训练时看到的条件直线（会交叉）；右＝速度场 + 推理时真正走的轨迹（不交叉）
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    rng = np.random.default_rng(3)
    for _ in range(40):
        e, y1 = rng.standard_normal(), rng.choice([-1, 1])
        ax[0].plot([0, 1], [e, y1], color="tab:green" if y1 > 0 else "tab:purple", alpha=0.5, lw=1)
    ax[0].set_title("训练时：随机配对（噪声 ε → 某条示范），一律走直线\n直线大量交叉，同一点会收到相反的标签")
    ax[0].set_xlabel("进度 t"); ax[0].set_ylabel("y"); ax[0].set_ylim(-2.5, 2.5)
    T, X = np.meshgrid(np.linspace(0, 0.97, 60), np.linspace(-2.5, 2.5, 60))
    V = np.vectorize(lambda x, t: float(velocity(x, t)))(X, T)
    im = ax[1].pcolormesh(T, X, np.clip(V, -4, 4), cmap="RdBu_r", shading="auto", alpha=0.8)
    fig.colorbar(im, ax=ax[1], label="速度 v*(y,t)（红=往上推，蓝=往下推）")
    for e in np.linspace(-2.2, 2.2, 24):  # 避开恰好 0（那条草稿会永远停在正中间，概率为 0）
        x, path = e, [e]
        for i in range(200):
            x = x + 0.005 * float(velocity(x, i * 0.005)); path.append(x)
        ax[1].plot(np.linspace(0, 1, 201), path, "k", lw=0.8)
    ax[1].set_title("推理时：网络学到的平均速度场，轨迹互不交叉\n前期犹豫（往中间收），后期“站队”（分到两边）")
    ax[1].set_xlabel("进度 t"); ax[1].set_ylim(-2.5, 2.5)
    fig.tight_layout(); fig.savefig(FIG / "fig3_velocity_field.png", dpi=150); plt.close(fig)

    # 图 4：同一个完美速度场，步数不同，终点分布不同
    fig, axes = plt.subplots(1, 5, figsize=(13, 2.6), sharey=True)
    eps = np.random.default_rng(0).standard_normal(10000)
    for ax_, nfe in zip(axes, [1, 2, 4, 10, 100]):
        y = euler(eps, nfe)
        ax_.hist(y, bins=80, range=(-1.6, 1.6), color="tab:blue")
        ax_.axvspan(-OBST, OBST, color="tab:red", alpha=0.2)
        ax_.set_title(f"NFE={nfe}  碰撞 {np.mean(np.abs(y) < OBST):.0%}"); ax_.set_xlabel("最终 y")
    fig.suptitle("同一个“训练完美”的速度场，只改推理步数：步数越少越往中间（瓶子）挤", y=1.03)
    fig.tight_layout(); fig.savefig(FIG / "fig4_nfe_collapse.png", dpi=150, bbox_inches="tight"); plt.close(fig)
    print(f"图已保存到 {FIG}")


if __name__ == "__main__":
    tables()
    figures()
