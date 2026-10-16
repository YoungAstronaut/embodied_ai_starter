"""Minimal 2D conditional Flow Matching experiment.

The target distribution is an eight-component Gaussian mixture on a circle.
Training uses the linear conditional path

    x_t = (1 - t) * x_0 + t * x_1,
    target_velocity = x_1 - x_0.

Sampling integrates dx/dt = v_theta(x, t) from Gaussian noise with Euler or
Heun. The script is intentionally small enough to inspect line by line.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import torch
from torch import Tensor, nn


class VelocityMLP(nn.Module):
    """A small time-conditioned velocity field v_theta(x, t)."""

    def __init__(self, hidden_dim: int = 128) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, 2),
        )

    def forward(self, x: Tensor, t: Tensor) -> Tensor:
        if t.ndim == 0:
            t = t.expand(x.shape[0], 1)
        elif t.ndim == 1:
            t = t[:, None]
        elif t.shape[0] == 1 and x.shape[0] != 1:
            t = t.expand(x.shape[0], 1)
        return self.net(torch.cat([x, t], dim=-1))


def sample_target(batch_size: int, device: torch.device) -> tuple[Tensor, Tensor]:
    """Sample from eight Gaussian modes and return points and mode IDs."""

    mode_ids = torch.randint(0, 8, (batch_size,), device=device)
    angles = mode_ids.float() * (2.0 * math.pi / 8.0)
    centers = 3.5 * torch.stack([torch.cos(angles), torch.sin(angles)], dim=-1)
    points = centers + 0.22 * torch.randn(batch_size, 2, device=device)
    return points, mode_ids


def sample_source(batch_size: int, device: torch.device) -> Tensor:
    return torch.randn(batch_size, 2, device=device)


@torch.no_grad()
def ode_step(
    model: VelocityMLP,
    x: Tensor,
    t0: float,
    t1: float,
    solver: str,
) -> Tensor:
    """Take one fixed ODE step.

    Heun uses two neural function evaluations per step; Euler uses one.
    """

    dt = t1 - t0
    t0_tensor = torch.full((x.shape[0], 1), t0, device=x.device)
    velocity_0 = model(x, t0_tensor)
    if solver == "euler":
        return x + dt * velocity_0

    x_predict = x + dt * velocity_0
    t1_tensor = torch.full((x.shape[0], 1), t1, device=x.device)
    velocity_1 = model(x_predict, t1_tensor)
    return x + 0.5 * dt * (velocity_0 + velocity_1)


@torch.no_grad()
def sample_flow(
    model: VelocityMLP,
    num_samples: int,
    num_steps: int,
    solver: str,
    device: torch.device,
    seed: int,
) -> list[Tensor]:
    generator_state = torch.random.get_rng_state()
    cuda_states = torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    x = sample_source(num_samples, device)
    snapshots = [x.detach().cpu()]
    for step in range(num_steps):
        t0 = step / num_steps
        t1 = (step + 1) / num_steps
        x = ode_step(model, x, t0, t1, solver)
        snapshots.append(x.detach().cpu())

    torch.random.set_rng_state(generator_state)
    if cuda_states is not None:
        torch.cuda.set_rng_state_all(cuda_states)
    return snapshots


def mode_metrics(samples: Tensor) -> dict[str, float | int]:
    angles = torch.arange(8).float() * (2.0 * math.pi / 8.0)
    centers = 3.5 * torch.stack([torch.cos(angles), torch.sin(angles)], dim=-1)
    distances = torch.cdist(samples.float(), centers)
    nearest_distance, nearest_mode = distances.min(dim=1)
    counts = torch.bincount(nearest_mode, minlength=8).float()
    proportions = counts / counts.sum()
    uniform = torch.full_like(proportions, 1.0 / 8.0)
    total_variation = 0.5 * torch.abs(proportions - uniform).sum()
    mode_coverage = int((counts > 0.01 * counts.sum()).sum().item())
    return {
        "mean_nearest_mode_distance": float(nearest_distance.mean().item()),
        "mode_coverage_at_1_percent": mode_coverage,
        "mode_total_variation_from_uniform": float(total_variation.item()),
        "sample_mean_x": float(samples[:, 0].mean().item()),
        "sample_mean_y": float(samples[:, 1].mean().item()),
        "sample_std_x": float(samples[:, 0].std().item()),
        "sample_std_y": float(samples[:, 1].std().item()),
    }


def plot_snapshots(snapshots: list[Tensor], target: Tensor, output_path: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Plotting requires matplotlib. Install dependencies with "
            "`python -m pip install -r requirements.txt`."
        ) from exc

    indices = sorted({0, len(snapshots) // 4, len(snapshots) // 2, len(snapshots) - 1})
    fig, axes = plt.subplots(1, len(indices) + 1, figsize=(4 * (len(indices) + 1), 4))
    for axis, index in zip(axes[:-1], indices):
        points = snapshots[index]
        t = index / (len(snapshots) - 1)
        axis.scatter(points[:, 0], points[:, 1], s=4, alpha=0.45)
        axis.set_title(f"Flow samples, t={t:.2f}")
        axis.set_xlim(-5.5, 5.5)
        axis.set_ylim(-5.5, 5.5)
        axis.set_aspect("equal")

    axes[-1].scatter(target[:, 0], target[:, 1], s=4, alpha=0.45, color="tab:orange")
    axes[-1].set_title("Target samples")
    axes[-1].set_xlim(-5.5, 5.5)
    axes[-1].set_ylim(-5.5, 5.5)
    axes[-1].set_aspect("equal")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def train(args: argparse.Namespace) -> None:
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    device = torch.device(args.device if args.device else ("cuda" if torch.cuda.is_available() else "cpu"))
    model = VelocityMLP(args.hidden_dim).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)

    start_time = time.perf_counter()
    ema_loss: float | None = None
    final_loss = float("nan")
    model.train()

    for step in range(1, args.train_steps + 1):
        x_1, _ = sample_target(args.batch_size, device)
        x_0 = sample_source(args.batch_size, device)
        t = torch.rand(args.batch_size, 1, device=device)

        x_t = (1.0 - t) * x_0 + t * x_1
        target_velocity = x_1 - x_0
        predicted_velocity = model(x_t, t)
        loss = torch.mean((predicted_velocity - target_velocity) ** 2)

        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

        final_loss = float(loss.item())
        ema_loss = final_loss if ema_loss is None else 0.98 * ema_loss + 0.02 * final_loss
        if step == 1 or step % args.log_every == 0:
            print(f"step={step:6d} loss={final_loss:.6f} ema_loss={ema_loss:.6f}")

    training_seconds = time.perf_counter() - start_time

    model.eval()
    sampling_start = time.perf_counter()
    snapshots = sample_flow(
        model=model,
        num_samples=args.num_samples,
        num_steps=args.nfe,
        solver=args.solver,
        device=device,
        seed=args.sample_seed,
    )
    if device.type == "cuda":
        torch.cuda.synchronize()
    sampling_seconds = time.perf_counter() - sampling_start

    target, _ = sample_target(args.num_samples, torch.device("cpu"))
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_snapshots(snapshots, target, output_dir / "samples.png")

    metrics = {
        "train_steps": args.train_steps,
        "batch_size": args.batch_size,
        "hidden_dim": args.hidden_dim,
        "learning_rate": args.learning_rate,
        "device": str(device),
        "solver": args.solver,
        "solver_steps": args.nfe,
        "neural_function_evaluations": args.nfe if args.solver == "euler" else 2 * args.nfe,
        "num_samples": args.num_samples,
        "seed": args.seed,
        "sample_seed": args.sample_seed,
        "final_training_loss": final_loss,
        "ema_training_loss": ema_loss,
        "training_seconds": training_seconds,
        "sampling_seconds": sampling_seconds,
        **mode_metrics(snapshots[-1]),
    }

    torch.save(
        {"model_state_dict": model.state_dict(), "args": vars(args), "metrics": metrics},
        output_dir / "model.pt",
    )
    (output_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    print(f"Saved results to {output_dir}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-steps", type=int, default=5000)
    parser.add_argument("--batch-size", type=int, default=1024)
    parser.add_argument("--hidden-dim", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=2e-3)
    parser.add_argument("--nfe", type=int, default=16, help="Number of fixed ODE solver steps.")
    parser.add_argument("--solver", choices=["euler", "heun"], default="heun")
    parser.add_argument("--num-samples", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--sample-seed", type=int, default=17)
    parser.add_argument("--log-every", type=int, default=500)
    parser.add_argument("--device", type=str, default="", help="For example: cpu, cuda, cuda:0.")
    parser.add_argument("--output-dir", type=str, default="toy_results")
    return parser


if __name__ == "__main__":
    train(build_parser().parse_args())

