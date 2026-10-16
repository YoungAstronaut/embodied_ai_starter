# Round 08 Review — STR-P3

- Proposal-ID: STR-P3
- Reviewed-Revision: r07
- File: `proposals/STR-P3_counterfactual_history/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已将history+value+evaluator总cap设为1B，明确M16仅smoke/M64 primary，闭合new-seed/H32/reward/checkpoint复用与lineage/model-grid；R7可行性P0解除但仍属高风险数据工程。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | history aliasing重要。 |
| D2 失败模式清晰度 | 4.5 | strict legal pair强。 |
| D3 创新性/最近邻 | 4.0 | benchmark/generator是主增量。 |
| D4 机制因果闭环 | 4.5 | pair→Q-set→history policy闭合。 |
| D5 技术正确性 | 4.5 | evaluator/资源边界稳定。 |
| D6 可观测性/泄漏 | 4.5 | target隔离严格。 |
| D7 数据可得性 | 3.5 | acceptance=0且1B cap高风险。 |
| D8 算力/工程 | 3.5 | 可闭合但规模极重。 |
| D9 可证伪性 | 4.5 | self-consistency/architecture降级明确。 |
| D10 基线强度 | 4.5 | 三backbone强。 |
| D11 消融充分性 | 4.5 | data×objective完整。 |
| D12 OOD/真机 | 3.0 | AliasBench/真机均仅模糊外测。 |
| D13 复现性 | 4.5 | lineage/evaluator矩阵具体。 |
| D14 CVPR契合度 | 4.5 | benchmark可吸引，但真实机器人证据弱。 |
| D15 风险/负结果 | 4.5 | pair tool与审计仍有价值。 |

平均分：**4.23/5.00**。D3/D7/D8/D12未达门槛；round<10，不通过。

## OOD/真机攻击面

1. synthetic strict-pair primary与官方AliasBench success不是同endpoint；后者没有pair/Q，不能验证cross-value机制，只能测是否一般化到自然任务。
2. “两模拟器”没有冻结train-generator与held-out-generator角色；若两边共同训练，不构成simulator OOD。
3. 真机near-match没有任务、trial、matching tolerance、hidden state操纵或安全协议，当前不能支持任何real claim。
4. policy在synthetic pair上可能利用renderer/history artifacts；需要held-out simulator/asset/history policy和独立perceptual auditor。

## 修改与R9验收

1. 冻结sim-A train/pair generation、sim-B zero-shot external test；sim-B不fit matching/Q阈值，recalibration另表。
2. AliasBench只报告native success/history ablation，明确“不验证cross-value”。
3. 若保留真机，定义2–3可达near-matched任务、root blocks、当前观测容差、独立GT与≥80 trials/task；否则删除真机措辞。
4. 跨renderer/asset/history-policy family去重并报告acceptance/coverage；部署共享collision/workspace guard。

R9主叙事应定位为“可证伪的history-alias benchmark与监督”，而不是过度声称自然/真机普适记忆方法。
