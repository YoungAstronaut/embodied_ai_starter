"""Static schema audit for the official IntentVLA AliasBench release.

Usage: python audit_aliasbench.py PATH_TO_INTENTVLA_REPO
Prints JSON only; it does not modify the checked repository.
"""
from __future__ import annotations

import ast
import json
import pathlib
import subprocess
import sys


def main() -> None:
    root = pathlib.Path(sys.argv[1]).resolve()
    envs = root / "envs"
    calls = []
    task_files = []
    for path in sorted(envs.glob("*.py")):
        if path.name.startswith("_"):
            continue
        task_files.append(path.name)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr not in {"_init_aliasbench_trace", "_set_aliasbench_trace"}:
                continue
            calls.append({
                "file": path.name,
                "line": node.lineno,
                "method": node.func.attr,
                "keyword_fields": sorted(k.arg for k in node.keywords if k.arg),
            })
    tracked_fields = sorted({f for c in calls for f in c["keyword_fields"]})
    all_text = "\n".join(p.read_text(encoding="utf-8") for p in envs.glob("*.py"))
    commit = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    result = {
        "repo": "https://github.com/ZGC-EmbodyAI/IntentVLA",
        "commit": commit,
        "task_file_count": len(task_files),
        "trace_call_count": len(calls),
        "trace_keyword_fields": tracked_fields,
        "has_pair_index": "pair_index" in all_text,
        "has_current_frame_tolerance": any(x in all_text for x in ["LPIPS", "depth_mae", "proprio_tolerance"]),
        "has_reachability_hash": any(x in all_text for x in ["reachability_hash", "action_hash", "state_hash"]),
        "has_candidate_q": any(x in all_text for x in ["Q_A", "Q_B", "candidate_q", "value_set"]),
        "has_hidden_or_future_fields_in_trace_calls": bool(set(tracked_fields) & {
            "sim_state", "future_reward", "future_frame", "seed", "episode_id"
        }),
        "calls": calls,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
