"""单元测试：用解析解验证 fm_lab.meanflow_loss 里 MeanFlow 恒等式的符号与切向量。

设定：数据 x1 ~ N(m, σ²I)，独立 coupling，线性路径。此时边缘概率路径仍是高斯
p_t = N(t·m, σ_t² I)，σ_t = sqrt((1-t)² + t²σ²)，flow map 有闭式解
    X_{s→t}(x) = t·m + (σ_t/σ_s)(x − s·m)。
把精确的平均速度 u=(X−x)/(t−s) 和精确的边缘速度 v 代入 u = v + (t−s)·d/ds u，残差应为 0。
"""
import torch
from torch.func import jvp

m, sig = torch.tensor([2.0, -1.0]), 0.5
sigma = lambda t: torch.sqrt((1 - t) ** 2 + (t * sig) ** 2)


def v_exact(x, t):
    dsig = (-(1 - t) + t * sig ** 2) / sigma(t)
    return m + dsig / sigma(t) * (x - t * m)


def u_exact(x, s, t):
    X = t * m + sigma(t) / sigma(s) * (x - s * m)
    return (X - x) / (t - s)


torch.manual_seed(0)
b = 4096
a, c = torch.rand(b, 1), torch.rand(b, 1)
s, t = torch.minimum(a, c), torch.maximum(a, c) + 1e-3
x = torch.randn(b, 2) * 2
v = v_exact(x, s)
u, du_ds = jvp(u_exact, (x, s, t), (v, torch.ones_like(s), torch.zeros_like(t)))
res_ok = ((u - (v + (t - s) * du_ds)) ** 2).sum(-1).mean().item()
res_flip = ((u - (v - (t - s) * du_ds)) ** 2).sum(-1).mean().item()
print(f"正向约定恒等式残差  u = v + (t-s)·du/ds : {res_ok:.2e}  （应≈0）")
print(f"把符号写反          u = v - (t-s)·du/ds : {res_flip:.2e}  （应明显 >0）")
assert res_ok < 1e-8 and res_flip > 1e-2, "MeanFlow 恒等式检验失败"
print("PASS")
