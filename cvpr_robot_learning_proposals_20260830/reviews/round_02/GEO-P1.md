# Round 02 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r01
- File: `proposals/GEO-P1_counterfactual_geometry/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（R1 fatal 无；R2 新邻居使创新边界未过硬门槛）

## 实际变更核验

r01 确实新增 `S=(G_task,G_nui,A_exo)`、checker-based `Y*`、3+3+3 pair 表、directional expert KL、最终动作 JS、acceptance/noise ablation 和五字段邻居表；同时把 mediation claim 收缩为 intervention reliance。不是只改措辞。发现一处未清理旧内容：消融仍写“去 `L_inv/L_sens/L_med`”，但现公式已改为 `L_dir/L_nui/L_swap`。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 几何表征是否真正影响动作仍重要。 |
| D2 失败模式清晰度 | 4.5 | SCM、接受/拒绝和 hard negatives 使最小反例闭合。 |
| D3 创新性/最近邻 | 3.5 | 几何 relation intervention 有差异，但新检出的 CofactVLA/CAST 已覆盖 VLA counterfactual deconfounding/labels；当前表遗漏。 |
| D4 机制因果闭环 | 4.0 | direction KL、nuisance JS、swap 与 success 形成干预链，但 relation token 对齐仍间接。 |
| D5 技术正确性 | 3.5 | R1 方向性错误已修；旧消融名、有限动作码本对“充分集”的离散偏差仍未处理。 |
| D6 可观测性/泄漏 | 4.5 | checker/Y* 只筛 pair/作 loss，字段白名单清楚。 |
| D7 数据可得性 | 4.0 | acceptance go/no-go、噪声曲线和 DROID 边界已加。 |
| D8 算力/工程 | 3.5 | 两档预算有，但 checker 枚举、缓存/真机配对成本未细化。 |
| D9 可证伪性 | 4.5 | random-K、swap ratio、noise fragility 和明确降级齐全。 |
| D10 基线强度 | 4.0 | VGA/GAM/MECo/ST-VLA 齐全；缺 CofactVLA/CAST 直接反事实控制。 |
| D11 消融充分性 | 3.5 | 多数正交，但保留已删除 loss 名表明实验契约未同步。 |
| D12 OOD/真机 | 4.0 | 四轴+LIBERO-Plus+真机外效度；功效仍未算。 |
| D13 复现性 | 3.0 | 仍缺 schema/版本/seed/伪代码 artifact 契约。 |
| D14 CVPR 契合度 | 4.0 | geometry representation/causal diagnosis 清楚。 |
| D15 风险/负结果 | 4.5 | 拒绝率、标签噪声和诊断 benchmark 的负结果价值强。 |

平均分：**3.93/5.00**。D3=3.5、D5=3.5、D6=4.5、D9=4.5；R2 不通过。

## Top 问题

1. **major — 新冲突未回应**：[CofactVLA 2608.04396v1](https://arxiv.org/abs/2608.04396) 已在 action/feature 两层做 counterfactual deconfounding；[CAST 2508.13446](https://arxiv.org/abs/2508.13446) 已用 counterfactual labels 改善 VLA 指令遵循。新意只能是 geometry-SCM relation intervention，不能是“反事实去捷径”。
2. **major — token-level novelty未闭合**：pair-level `Y*` 监督 action distribution，但没有 relation-token ground truth；gate 可选择语义/objectness proxy，仍可能复现 CofactVLA 式视觉去偏而非几何充分集。
3. **minor/technical — stale contract**：旧 loss 消融名必须删除，否则评测无法对应方法。

## 具体修改动作

1. 增加 CofactVLA/CAST 行，逐项比较 intervention source、counterfactual branch、action/feature objective、几何变量、部署图；将标题/claim 中 deconfounding 新意收缩到 relation geometry。
2. 加 `CofactVLA-style language-mask` 和 CAST-style counterfactual-label baseline；再做 geometry-token replacement vs generic visual-feature replacement 2×2。
3. 明确 GFM relation token 与 `G_task` 的映射/不可映射情况；加 token-semantic permutation、objectness-matched control。
4. 清理旧 loss 名并把有限动作码本大小/覆盖误差列为正交消融。

## Round 03 验收条件

- [ ] CofactVLA/CAST 已进入正文表和强基线，claim 不再把 counterfactual 本身当新。
- [ ] 有 geometry-token vs generic-feature 2×2，能排除一般视觉去偏解释。
- [ ] `G_task→token` 映射及动作码本近似误差可核查。
- [ ] 所有消融名称与 r02 实际公式一致，日志逐项回应。

