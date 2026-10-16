# Round 03 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r02
- File: `proposals/STR-P1_event_intent_reset/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（target 路径合格；部署 gate 没有使用其宣称的 reset value）

## 实际变更核验

r02 已把 event-triggered replanning、When-to-Trust、CheckVLA、REMAC 等放入逐字段表，所有非 oracle gate 共享 K=4 proposer；`C_t` 使用 snapshot、S=8、H=16 的 paired alternative-intent value target，且 target shard 删除 future/state/seed/task ID。时间图也已修为 t−1 prediction→t residual→reset→action t。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 意图惯性在突发变化后会直接造成连续失败。 |
| D2 失败模式清晰度 | 4.5 | novelty、control failure、reset-worthy 三标签及正反 hard pair 清楚。 |
| D3 创新性/最近邻 | 4.0 | change detection/replan 已知；增量是 common-seed reset-value supervision。 |
| D4 机制因果闭环 | 3.5 | 训练 value/posterior，但部署公式比较 intent log-probability，链条断开。 |
| D5 技术正确性 | 3.5 | 时间顺序已正确；gate 阈值量与 `ΔQ_reset` target 不一致。 |
| D6 可观测性/泄漏 | 4.5 | future rollout/state/seed 仅 target，部署输入 causal。 |
| D7 数据可得性 | 4.0 | EventAlias 与 paired rollout 可生成，真机 event 可重复。 |
| D8 算力/工程 | 4.0 | K×S×H 有限，需补 target 总乘法账与 latency profile。 |
| D9 可证伪性 | 4.5 | novelty-no-reset、low-visual-reset、shared proposer 与 oracle-K 强。 |
| D10 基线强度 | 4.5 | 事件控制、风险 gate、intent/memory 和固定 reset 均覆盖。 |
| D11 消融充分性 | 4.5 | CUSUM/模态/value posterior/候选覆盖率分解充分。 |
| D12 OOD/真机 | 4.0 | 多事件类型与真机外效度合理，跨 event family split 未细化。 |
| D13 复现性 | 3.5 | 缺 deployed score、阈值标定和 target 乘法账的唯一合同。 |
| D14 CVPR 契合度 | 4.5 | 视觉变化检测、时序策略和机器人恢复高度契合。 |
| D15 风险/负结果 | 4.5 | 可降级为 change benchmark/stability-reactivity Pareto。 |

平均分：**4.17/5.00**。D3=4.0、D5=3.5、D6=4.5、D9=4.5；round<10 且 D4/D5 未达硬门槛，R3 不通过。

## Top 问题与证据缺口

1. **major/technical — 训练 target 与部署决策量不一致。** 方法训练 `Brier(C)+L_value-rank`，却在部署用 `max_j log p(z_j)-log p(z_old)>κ`。高概率 intent 不等于高 reset utility；这会让核心 paired `ΔQ` target 变成辅助监督，而非决策中介。
2. **major — CUSUM 与 value gate 的组合未校准。** 强制 `g_t>τ_g AND utility>κ` 可能漏掉视觉创新小但接触/控制证据足够的 reset；反例虽提出，公式仍要求 innovation threshold。
3. **minor — `s_t` 符号来源模糊。** 时间图写 `o_t,s_t`，表中似为 proprio；必须避免被理解成 simulator state。

## 具体修改动作

1. 部署直接比较 student 预测的 `ΔQ_reset` 或 continuation advantage，并让 `P(C)` 只作 calibrated confidence；报告删 value head 后的下降。
2. 将 gate 写成可检查逻辑，例如 value evidence 可由 visual innovation 或 proprio/contact failure 任一路触发；用 low-visual-reset 三类验证不被 `g_t` 硬门槛挡住。
3. 给出二维阈值/decision surface 和 matched false-reset cost，所有 gate 在同 prevalence/utility scale 上标定。
4. 把 `s_t` 重命名为明确的 `q_t/proprio_t`，loader 白名单逐字段列出。

## Round 04 验收条件

- [ ] deployed reset score 明确使用 paired reset value，而非 intent frequency/probability替代。
- [ ] low-visual-reset 可绕过纯 visual CUSUM 硬门槛，逻辑和最小例一致。
- [ ] 阈值、成本、候选覆盖和 latency 有统一伪代码。
- [ ] 所有状态符号均标注部署来源，禁止 simulator state 歧义。

