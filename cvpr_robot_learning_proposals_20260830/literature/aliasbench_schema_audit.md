# IntentVLA AliasBench 官方代码字段审计

- 审计日期：2026-08-30
- 官方仓库：https://github.com/ZGC-EmbodyAI/IntentVLA
- 审计 commit：`6d513c8118e8041fcb1db218cce2201a27a9b58c`
- 脚本：`literature/audit_aliasbench.py`
- 范围：当前公开的 AliasBench task code；README 明确 full IntentVLA model implementation 仍待发布。

## 可复现结果

脚本对 `envs/*.py` 做 AST 扫描：12 个任务文件，46 次 `_init_aliasbench_trace/_set_aliasbench_trace` 调用；公开调用字段仅为 `intent,destination,ambiguous,control`。仓库代码中未发现 `pair_index`、LPIPS/depth/proprio current-frame tolerance、reachability/action/state hash、candidate-Q/value-set 字段；trace 调用也未传 `sim_state/future_reward/future_frame/seed/episode_id`。

因此，当前公开 release 确实提供自然 alias 任务与意图/歧义窗口标记，但**没有发布** Counterfactual-Alias 所要求的逐 pair same-current tolerance、双 rollout reachability 证明或双向 cross-value action-set 标签。这个结论只针对上述 commit 的公开 task code，不能外推到未发布的模型/私有数据。

## 四字段判定

| 字段 | 公开代码证据 | 判定 |
|---|---|---|
| 当前帧严格匹配 | 无 pair index 与 LPIPS/depth/proprio tolerance | 未覆盖本 proposal 的 strict contract |
| history control | 任务代码显式标 `intent/ambiguous/control`，但无双 rollout hash | 部分覆盖自然 history context；未覆盖 reachability proof |
| value incompatibility | 无 candidate-Q/value-set 字段 | 未覆盖双向 cross-value 检验 |
| 泄漏字段 | trace 调用仅四个语义字段，无 future/state/seed/episode ID | 当前公开 trace API 未见这些泄漏；仍需运行时数据导出审计 |

审计限制：未安装 RoboTwin2，因此没有执行仿真 rollout；这是静态 schema/code audit，不宣称证明自然帧的视觉相似度或 task correctness。
