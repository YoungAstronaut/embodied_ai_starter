"""Flow Matching 重拾实验台（单文件、CPU 可跑）。

四个实验，每个只回答一个问题：

  basics   为什么少步采样会坏？        vanilla FM 在 NFE=1..64 下的退化 + 轨迹曲率
  coupling 能不能把轨迹拉直？          independent coupling / minibatch OT / reflow 对比
  fewstep  不拉直，直接学"跳步"行不行？ FM vs Shortcut Model vs MeanFlow 在 1/2/4/8 步
  action   这对机器人意味着什么？       双模态绕障 action chunk：1 步 FM 会撞墙吗？
  action_raw 同上但不做动作归一化     演示「不归一化」本身就能毁掉少步生成

时间约定（全文件统一）：t=0 是噪声 x0~N(0,I)，t=1 是数据 x1；
线性路径 x_t=(1-t)x0+t x1，条件速度 x1-x0。
注意 MeanFlow 原文用的是相反约定（t=1 噪声），这里已改写成正向形式，见 meanflow_loss。

用法：
  python fm_lab.py basics
  python fm_lab.py all          # 依次跑完全部实验，M 系列 CPU 约 6 分钟（OT 配对占一半）
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import torch
from torch import Tensor, nn
from torch.func import jvp

ROOT = Path(__file__).resolve().parent / "results"
DEVICE = torch.device("cpu")  # 小 MLP 在 CPU 上比 MPS 快


# ---------------------------------------------------------------------------
# 网络：x + 若干标量（t / d / s,t），可选 Fourier 特征 + 可选条件
# ---------------------------------------------------------------------------
class Net(nn.Module):
    def __init__(self, x_dim: int, n_scalar: int, cond_dim: int = 0,
                 hidden: int = 256, depth: int = 4, n_freq: int = 0) -> None:
        # n_freq=0：时间类标量直接输入。实测 n_freq=4（最高频 8π）会让 MeanFlow 在 32 维动作上训崩：
        # 它的目标里有 ∂u/∂s，高频嵌入把这一项放大约 2πk 倍，自举目标噪声爆炸（见 04_实验记录.md §5）。
        super().__init__()
        self.n_freq = n_freq
        in_dim = x_dim + cond_dim + n_scalar * (1 + 2 * n_freq)
        layers: list[nn.Module] = [nn.Linear(in_dim, hidden), nn.SiLU()]
        for _ in range(depth - 1):
            layers += [nn.Linear(hidden, hidden), nn.SiLU()]
        layers.append(nn.Linear(hidden, x_dim))
        self.net = nn.Sequential(*layers)
        self.register_buffer("freqs", 2 * math.pi * torch.arange(1, n_freq + 1).float())

    def embed(self, s: Tensor) -> Tensor:  # s: [B,1]
        ang = s * self.freqs
        return torch.cat([s, torch.sin(ang), torch.cos(ang)], dim=-1)

    def forward(self, x: Tensor, scalars: list[Tensor], cond: Tensor | None = None) -> Tensor:
        feats = [x] + [self.embed(s.expand(x.shape[0], 1)) for s in scalars]
        if cond is not None:
            feats.append(cond)
        return self.net(torch.cat(feats, dim=-1))


# ---------------------------------------------------------------------------
# 数据
# ---------------------------------------------------------------------------
R_MODE, STD_MODE = 3.5, 0.22
CENTERS = R_MODE * torch.stack([torch.cos(torch.arange(8) * 2 * math.pi / 8),
                                torch.sin(torch.arange(8) * 2 * math.pi / 8)], -1)


def sample_8g(n: int) -> Tensor:
    return CENTERS[torch.randint(0, 8, (n,))] + STD_MODE * torch.randn(n, 2)


# 机器人玩具：从 (0,0) 到 (1, goal_y)，中间 (0.5,0) 有半径 0.15 的圆形障碍。
# 示范一半从上方绕、一半从下方绕。action chunk = 16 个 2D 路点 -> 32 维。
H, OBST, OBST_R = 16, torch.tensor([0.5, 0.0]), 0.15
TAU = torch.linspace(1 / H, 1.0, H)


def sample_action(n: int) -> tuple[Tensor, Tensor]:
    goal_y = (torch.rand(n, 1) - 0.5) * 0.4                 # [-0.2, 0.2]
    side = torch.where(torch.rand(n, 1) < 0.5, 1.0, -1.0)  # 上绕 / 下绕
    amp = 0.30 + 0.10 * torch.rand(n, 1)
    xs = TAU.expand(n, H)
    ys = goal_y * TAU + side * amp * torch.sin(math.pi * TAU) + 0.01 * torch.randn(n, H)
    return torch.stack([xs, ys], -1).reshape(n, 2 * H), goal_y


# ---------------------------------------------------------------------------
# 三种训练目标
# ---------------------------------------------------------------------------
def fm_loss(net: Net, x0: Tensor, x1: Tensor, cond: Tensor | None = None) -> Tensor:
    t = torch.rand(x0.shape[0], 1)
    xt = (1 - t) * x0 + t * x1
    return ((net(xt, [t], cond) - (x1 - x0)) ** 2).mean()


SC_M = 128  # Shortcut 最小步长 1/128


def d_feat(d: Tensor) -> Tensor:
    """把步长 d∈{0, 1/128, ..., 1} 映射到 [0,1]：d=0 -> 0，1/128 -> 1/8，1 -> 1。"""
    return torch.where(d > 0, (torch.log2(d.clamp_min(1e-9) * SC_M) + 1) / 8, torch.zeros_like(d))


def shortcut_loss(net: Net, x0: Tensor, x1: Tensor, cond: Tensor | None = None,
                  frac_sc: float = 0.25) -> Tensor:
    """Frans et al. 2410.12557：网络 s(x,t,d) 满足 x_{t+d} ≈ x_t + d·s。
    (a) d=0 时退化为 FM；(b) 一大步 2d = 两小步 d 的平均方向（自洽，自举）。"""
    b = x0.shape[0]
    nb = int(b * frac_sc)
    # (a) flow-matching 部分
    t = torch.rand(b - nb, 1)
    xt = (1 - t) * x0[nb:] + t * x1[nb:]
    c_a = cond[nb:] if cond is not None else None
    loss_fm = ((net(xt, [t, torch.zeros_like(t)], c_a) - (x1[nb:] - x0[nb:])) ** 2).mean()
    # (b) self-consistency 部分
    k = torch.randint(0, int(math.log2(SC_M)), (nb, 1)).float()  # d = 2^k/128, k=0..6
    d = 2 ** k / SC_M
    n_slot = (1 / (2 * d)).round()
    t = torch.floor(torch.rand(nb, 1) * n_slot) * 2 * d          # t 对齐到 2d 的整数倍
    xt = (1 - t) * x0[:nb] + t * x1[:nb]
    c_b = cond[:nb] if cond is not None else None
    dq = torch.where(k == 0, torch.zeros_like(d), d)             # 最小步用 d=0（FM）自举
    with torch.no_grad():
        s1 = net(xt, [t, d_feat(dq)], c_b)
        s2 = net(xt + d * s1, [t + d, d_feat(dq)], c_b)
        target = 0.5 * (s1 + s2)
    loss_sc = ((net(xt, [t, d_feat(2 * d)], c_b) - target) ** 2).mean()
    return (loss_fm * (b - nb) + loss_sc * nb) / b


def meanflow_loss(net: Net, x0: Tensor, x1: Tensor, cond: Tensor | None = None,
                  frac_neq: float = 0.5, p: float = 0.0) -> Tensor:
    """Geng et al. 2505.13447，改写为正向约定。
    平均速度 u(x_s,s,t) = 1/(t-s)∫_s^t v dτ，于是 x_t = x_s + (t-s)u。
    对起点 s 求导得 MeanFlow 恒等式： u = v + (t-s)·d/ds u，
    其中 d/ds u = ∂_x u·v + ∂_s u，用一次 JVP（切向量 (v,1,0)）算出。

    与原文的两处差异（toy 上实测后改的，见 04_实验记录.md §3）：
      - 原文 25% 样本 s≠t；这里默认 50%。
      - 原文自适应权重 p=1；这里默认 p=0（普通 MSE）。p=1 把 L2 变成鲁棒损失，
        最优解不再是条件均值，在 8-Gaussian 上会让各模式的比例明显失衡（TV 0.03 → 0.1~0.2）。"""
    b = x0.shape[0]
    a, c = torch.rand(b, 1), torch.rand(b, 1)
    s, t = torch.minimum(a, c), torch.maximum(a, c)
    s = torch.where(torch.rand(b, 1) < frac_neq, s, t)  # 其余样本 s=t，即普通 FM
    xs = (1 - s) * x0 + s * x1
    v = x1 - x0
    u, du_ds = jvp(lambda x_, s_, t_: net(x_, [s_, t_], cond),
                   (xs, s, t), (v, torch.ones_like(s), torch.zeros_like(t)))
    target = (v + (t - s) * du_ds).detach()
    err = ((u - target) ** 2).sum(-1, keepdim=True)
    w = 1.0 / (err.detach() + 1e-3) ** p                 # 论文的自适应权重；p=0 即普通 MSE
    return (w * err).mean()


# ---------------------------------------------------------------------------
# 采样器
# ---------------------------------------------------------------------------
@torch.no_grad()
def sample_fm(net: Net, x0: Tensor, nfe: int, cond: Tensor | None = None,
              solver: str = "euler", keep: bool = False):
    """nfe 是网络调用次数：Euler 每步 1 次，Heun 每步 2 次。"""
    steps = nfe if solver == "euler" else max(1, nfe // 2)
    x, traj, vs = x0.clone(), [x0.clone()], []
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        v0 = net(x, [torch.full((1, 1), t0)], cond)
        vs.append(v0)
        if solver == "euler":
            x = x + (t1 - t0) * v0
        else:
            v1 = net(x + (t1 - t0) * v0, [torch.full((1, 1), t1)], cond)
            x = x + 0.5 * (t1 - t0) * (v0 + v1)
        traj.append(x.clone())
    return (x, traj, vs) if keep else x


@torch.no_grad()
def sample_shortcut(net: Net, x0: Tensor, nfe: int, cond: Tensor | None = None) -> Tensor:
    d = 1.0 / nfe
    x = x0.clone()
    for i in range(nfe):
        x = x + d * net(x, [torch.full((1, 1), i * d), d_feat(torch.full((1, 1), d))], cond)
    return x


@torch.no_grad()
def sample_meanflow(net: Net, x0: Tensor, nfe: int, cond: Tensor | None = None) -> Tensor:
    x = x0.clone()
    for i in range(nfe):
        s, t = i / nfe, (i + 1) / nfe
        x = x + (t - s) * net(x, [torch.full((1, 1), s), torch.full((1, 1), t)], cond)
    return x


# ---------------------------------------------------------------------------
# 指标
# ---------------------------------------------------------------------------
def sliced_w2(a: Tensor, b: Tensor, n_proj: int = 256) -> float:
    g = torch.Generator().manual_seed(0)
    th = torch.randn(a.shape[1], n_proj, generator=g)
    th = th / th.norm(dim=0, keepdim=True)
    pa, _ = torch.sort(a @ th, 0)
    pb, _ = torch.sort(b @ th, 0)
    return float(((pa - pb) ** 2).mean().sqrt())


def metrics_8g(x: Tensor, ref: Tensor) -> dict:
    dist, mode = torch.cdist(x, CENTERS).min(1)
    prop = torch.bincount(mode, minlength=8).float() / len(x)
    return {
        "sw2": round(sliced_w2(x, ref), 4),                                      # 越小越好；见 sw2_floor
        "off_manifold": round(float((dist > 3 * STD_MODE).float().mean()), 4),  # 离最近模式 >3σ 的比例
        "mode_tv": round(float(0.5 * (prop - 1 / 8).abs().sum()), 4),          # 各模式占比 vs 均匀；0 最好
    }


def straightness(net: Net, x0: Tensor) -> float:
    """Liu et al. 的直线度 S = E_t ||(x1 - x0) - v(x_t,t)||²，用 128 步 Euler 轨迹近似。0 = 完全直。"""
    x1, _, vs = sample_fm(net, x0, 128, keep=True)
    disp = x1 - x0
    return float(torch.stack([((disp - v) ** 2).sum(-1).mean() for v in vs]).mean())


def metrics_action(a: Tensor, goal_y: Tensor) -> dict:
    pts = a.reshape(-1, H, 2)
    hit = ((pts - OBST).norm(dim=-1) < OBST_R).any(1)
    mid_y = pts[:, H // 2 - 1, 1]
    return {
        "collision": round(float(hit.float().mean()), 4),
        "top_ratio": round(float((mid_y > 0).float().mean()), 4),
        "goal_err": round(float((pts[:, -1, 1] - goal_y[:, 0]).abs().mean()), 4),
    }


# ---------------------------------------------------------------------------
# 训练循环
# ---------------------------------------------------------------------------
def train(net: Net, loss_fn, batch_fn, steps: int, lr: float = 1e-3, tag: str = "") -> float:
    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=0.0)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    t0, ema = time.perf_counter(), None
    for step in range(1, steps + 1):
        loss = loss_fn(net, *batch_fn())
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        sched.step()
        ema = loss.item() if ema is None else 0.99 * ema + 0.01 * loss.item()
        if step % max(1, steps // 4) == 0:
            print(f"  [{tag}] step {step}/{steps} loss_ema={ema:.4f}")
    dt = time.perf_counter() - t0
    print(f"  [{tag}] done in {dt:.0f}s")
    return dt


def batch_indep(bs: int = 512):
    return lambda: (torch.randn(bs, 2), sample_8g(bs))


def batch_ot(bs: int = 512):
    from scipy.optimize import linear_sum_assignment

    def fn():
        x0, x1 = torch.randn(bs, 2), sample_8g(bs)
        r, c = linear_sum_assignment(torch.cdist(x0, x1).pow(2).numpy())
        return x0[r], x1[c]
    return fn


def save(exp: str, obj: dict) -> Path:
    out = ROOT / exp
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(obj, indent=2, ensure_ascii=False))
    return out


def scatter_grid(rows: dict[str, list[Tensor]], cols: list[str], path: Path, ref: Tensor) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(len(rows), len(cols) + 1, figsize=(2.4 * (len(cols) + 1), 2.4 * len(rows)))
    axes = np.atleast_2d(axes)
    for r, (name, xs) in enumerate(rows.items()):
        for c, x in enumerate(xs):
            ax = axes[r, c]
            ax.scatter(x[:2000, 0], x[:2000, 1], s=1, alpha=0.4)
            ax.set_xlim(-5.5, 5.5); ax.set_ylim(-5.5, 5.5); ax.set_xticks([]); ax.set_yticks([])
            if r == 0:
                ax.set_title(cols[c], fontsize=9)
            if c == 0:
                ax.set_ylabel(name, fontsize=9)
        ax = axes[r, -1]
        ax.scatter(ref[:2000, 0], ref[:2000, 1], s=1, alpha=0.4, color="tab:orange")
        ax.set_xlim(-5.5, 5.5); ax.set_ylim(-5.5, 5.5); ax.set_xticks([]); ax.set_yticks([])
        if r == 0:
            ax.set_title("data", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 实验
# ---------------------------------------------------------------------------
def exp_basics(steps: int) -> dict:
    print("== basics: vanilla FM 的 NFE 退化")
    torch.manual_seed(0)
    net = Net(2, 1)
    train(net, fm_loss, batch_indep(), steps, tag="FM")
    x0, ref = torch.randn(4000, 2), sample_8g(4000)
    res, row_e, row_h, cols = {}, [], [], []
    for nfe in [1, 2, 4, 8, 16, 64]:
        xe = sample_fm(net, x0, nfe, solver="euler")
        res[f"euler_nfe{nfe}"] = metrics_8g(xe, ref)
        row_e.append(xe); cols.append(f"NFE={nfe}")
        if nfe >= 2:
            xh = sample_fm(net, x0, nfe, solver="heun")
            res[f"heun_nfe{nfe}"] = metrics_8g(xh, ref)
            row_h.append(xh)
        else:
            row_h.append(torch.full_like(xe, float("nan")))
    res["straightness"] = round(straightness(net, x0[:2000]), 4)
    res["sw2_floor"] = round(sliced_w2(ref, sample_8g(4000)), 4)  # 两份真数据之间的 SW2：低于它的差异都是噪声
    out = save("basics", res)
    scatter_grid({"Euler": row_e, "Heun": row_h}, cols, out / "samples.png", ref)
    torch.save(net.state_dict(), out / "fm.pt")
    return res


def exp_coupling(steps: int) -> dict:
    print("== coupling: independent / minibatch-OT / reflow")
    x0, ref = torch.randn(4000, 2), sample_8g(4000)
    nets, res = {}, {}
    torch.manual_seed(0)
    nets["I-CFM"] = Net(2, 1); train(nets["I-CFM"], fm_loss, batch_indep(), steps, tag="I-CFM")
    torch.manual_seed(0)
    nets["OT-CFM"] = Net(2, 1); train(nets["OT-CFM"], fm_loss, batch_ot(), steps, tag="OT-CFM")
    # 2-rectified flow：用 I-CFM 的 ODE 生成确定性配对 (z0, ODE(z0))，再在配对上训练
    with torch.no_grad():
        z0 = torch.randn(100_000, 2)
        z1 = sample_fm(nets["I-CFM"], z0, 64, solver="heun")
    reflow = Net(2, 1); reflow.load_state_dict(nets["I-CFM"].state_dict())
    def batch_pairs(bs=512):
        idx = torch.randint(0, len(z0), (bs,))
        return z0[idx], z1[idx]
    train(reflow, fm_loss, batch_pairs, steps, tag="2-Reflow")
    nets["2-Reflow"] = reflow
    rows, cols = {}, [f"NFE={n}" for n in [1, 2, 4, 16]]
    for name, net in nets.items():
        res[name] = {"straightness": round(straightness(net, x0[:2000]), 4)}
        rows[name] = []
        for nfe in [1, 2, 4, 16]:
            x = sample_fm(net, x0, nfe)
            res[name][f"nfe{nfe}"] = metrics_8g(x, ref)
            rows[name].append(x)
    out = save("coupling", res)
    scatter_grid(rows, cols, out / "samples.png", ref)
    return res


def exp_fewstep(steps: int, n_seeds: int = 3) -> dict:
    print("== fewstep: FM vs Shortcut vs MeanFlow")
    x0, ref = torch.randn(4000, 2), sample_8g(4000)
    specs = [("FM", fm_loss, 1, sample_fm), ("Shortcut", shortcut_loss, 2, sample_shortcut),
             ("MeanFlow", meanflow_loss, 2, sample_meanflow)]
    nfes = [1, 2, 4, 8, 64]
    runs: dict[str, list[dict]] = {k[0]: [] for k in specs}
    rows: dict[str, list[Tensor]] = {}
    secs: dict[str, float] = {}
    for seed in range(n_seeds):
        for name, loss, n_s, sampler in specs:
            torch.manual_seed(seed)
            net = Net(2, n_s)
            secs[name] = round(train(net, loss, batch_indep(), steps, tag=f"{name}-seed{seed}"))
            outs = [sampler(net, x0, n) for n in nfes]
            runs[name].append({f"nfe{n}": metrics_8g(x, ref) for n, x in zip(nfes, outs)})
            if seed == 0:
                rows[name] = outs
    res = {"train_seconds_per_model": secs, "n_seeds": n_seeds,
           "sw2_floor": round(sliced_w2(ref, sample_8g(4000)), 4)}
    for name, rs in runs.items():
        res[name] = {k: {m: f"{np.mean([r[k][m] for r in rs]):.3f}±{np.std([r[k][m] for r in rs]):.3f}"
                         for m in rs[0][k]} for k in rs[0]}
    out = save("fewstep", res)
    scatter_grid(rows, [f"NFE={n}" for n in nfes], out / "samples.png", ref)
    return res


def exp_action(steps: int, normalize: bool = True, n_seeds: int = 3) -> dict:
    """normalize=True：动作按维度 z-score、条件缩放到 [-1,1]，这是 Diffusion Policy / π0 的标准做法。
    normalize=False：保留原始尺度（动作幅度约 0.3，噪声 std=1），用来演示「不归一化」会出什么问题。"""
    tag = "action" if normalize else "action_unnormalized"
    print(f"== {tag}: 双模态绕障 action chunk")
    a_ref, g_ref = sample_action(2000)
    if normalize:
        big, _ = sample_action(200_000)
        mu, sd = big.mean(0), big.std(0).clamp_min(1e-3)
        enc, dec, cs = (lambda a: (a - mu) / sd), (lambda z: z * sd + mu), 1 / 0.2
    else:
        enc, dec, cs = (lambda a: a), (lambda z: z), 1.0
    torch.manual_seed(1)
    x0 = torch.randn(2000, 2 * H)

    def batch(bs=512):
        a, g = sample_action(bs)
        return torch.randn(bs, 2 * H), enc(a), g * cs

    samplers = {"FM": sample_fm, "Shortcut": sample_shortcut, "MeanFlow": sample_meanflow}
    nfes = [1, 2, 4, 16]
    runs: dict[str, list[dict]] = {k: [] for k in samplers}
    trajs: dict[str, list[Tensor]] = {}
    for seed in range(n_seeds):
        for name, loss, n_s in [("FM", fm_loss, 1), ("Shortcut", shortcut_loss, 2), ("MeanFlow", meanflow_loss, 2)]:
            torch.manual_seed(seed)
            net = Net(2 * H, n_s, cond_dim=1)
            train(net, loss, batch, steps, tag=f"{tag}-{name}-seed{seed}")
            outs = [dec(samplers[name](net, x0, n, g_ref * cs)) for n in nfes]
            runs[name].append({f"nfe{n}": metrics_action(a, g_ref) for n, a in zip(nfes, outs)})
            if seed == 0:
                trajs[name] = outs
    res = {"demo": metrics_action(a_ref, g_ref), "n_seeds": n_seeds}
    for name, rs in runs.items():  # 汇总为 均值±标准差
        res[name] = {}
        for k in rs[0]:
            res[name][k] = {m: f"{np.mean([r[k][m] for r in rs]):.3f}±{np.std([r[k][m] for r in rs]):.3f}"
                            for m in rs[0][k]}
    # 1 步 FM 的理论落点是 E[A|c]：直接算出来对照
    if normalize:
        res["FM_nfe1_dist_to_conditional_mean"] = round(float(
            (trajs["FM"][0] - _cond_mean_action(g_ref)).abs().mean()), 4)
    out = save(tag, res)
    _plot_actions(trajs, nfes, a_ref, out / "trajectories.png")
    return res


def _cond_mean_action(goal_y: Tensor) -> Tensor:
    """E[A | goal_y]：左右绕行各一半，sin 项抵消，只剩 goal_y·τ 的直线。"""
    xs = TAU.expand(len(goal_y), H)
    return torch.stack([xs, goal_y * TAU], -1).reshape(len(goal_y), 2 * H)


def _plot_actions(trajs: dict, nfes: list[int], demo: Tensor, path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(len(trajs), len(nfes) + 1, figsize=(2.6 * (len(nfes) + 1), 2.2 * len(trajs)))
    def draw(ax, a, color):
        p = a[:80].reshape(-1, H, 2)
        for q in p:
            ax.plot(np.r_[0, q[:, 0]], np.r_[0, q[:, 1]], lw=0.6, alpha=0.5, color=color)
        ax.add_patch(plt.Circle(OBST.tolist(), OBST_R, color="tab:red", alpha=0.35))
        ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.6, 0.6); ax.set_xticks([]); ax.set_yticks([])
        ax.set_aspect("equal")
    for r, (name, xs) in enumerate(trajs.items()):
        for c, a in enumerate(xs):
            draw(axes[r, c], a, "tab:blue")
            if r == 0:
                axes[r, c].set_title(f"NFE={nfes[c]}", fontsize=9)
        axes[r, 0].set_ylabel(name, fontsize=9)
        draw(axes[r, -1], demo, "tab:orange")
        if r == 0:
            axes[r, -1].set_title("demos", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("exp", choices=["basics", "coupling", "fewstep", "action", "action_raw", "all"])
    ap.add_argument("--steps", type=int, default=6000, help="每个模型的训练步数")
    args = ap.parse_args()
    torch.set_num_threads(max(1, torch.get_num_threads()))
    exps = ["basics", "coupling", "fewstep", "action", "action_raw"] if args.exp == "all" else [args.exp]
    table = {"basics": exp_basics, "coupling": exp_coupling, "fewstep": exp_fewstep,
             "action": exp_action, "action_raw": lambda st: exp_action(st, normalize=False)}
    summary = {}
    for e in exps:
        summary[e] = table[e](args.steps)
        print(json.dumps(summary[e], indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
