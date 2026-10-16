# Round 02 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r01
- File: `proposals/WAM-P2_value_of_imagination/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（无 fatal；paired decision-value target 有差异，但 VOC 本身不是新概念）

## 实际变更核验

r01 已定义 common-seed `Y_k/D_k`、Hc=16、S=8/CI abstain，删除 monotone loss，增加 harmful compute、compute-only/shuffled visual stats、完整 latency/energy Pareto 与 PonderNet/ACT。R1 主要错误实质修复。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 实时 WAM 的计算价值重要。 |
| D2 失败模式清晰度 | 4.5 | decision epoch/potential outcomes/harmful compute清楚。 |
| D3 创新性/最近邻 | 4.0 | exact-reset paired marginal decision value有可检验差异；但 value-of-computation/rational metareasoning本身经典。 |
| D4 机制因果闭环 | 4.0 | visual stats→VOC→stop→ranking→reward，shuffle control强。 |
| D5 技术正确性 | 4.0 | 非单调target与CRN已修；跨任务reward权重和off-policy候选仍待深审。 |
| D6 可观测性/泄漏 | 4.5 | deployment只读partial rollout/time，future reward仅target。 |
| D7 数据可得性 | 3.5 | 20k×k×8成本巨大，真实校准无反事实target。 |
| D8 算力/工程 | 3.5 | 完整Pareto增强，但分支生成预算与4天估计不相称。 |
| D9 可证伪性 | 4.5 | oracle-positive prevalence、shuffle、compute-only、budget slices明确。 |
| D10 基线强度 | 4.5 | 直接WAM gates、compact path、adaptive compute、oracle齐全。 |
| D11 消融充分性 | 4.5 | reward horizon/noise/视觉统计/时间tail全面。 |
| D12 OOD/真机 | 4.0 | 多硬件/jitter/模型错误分层；视觉域OOD尚弱。 |
| D13 复现性 | 3.5 | potential schema明确，仍缺trace/reward evaluator版本与artifact。 |
| D14 CVPR 契合度 | 4.0 | visual rollout error contribution已由shuffle/分层隔离。 |
| D15 风险/负结果 | 4.5 | oracle VOC<10%早停与有害想象边界价值强。 |

平均分：**4.10/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；未过 hardened gate/mean。

## Top 问题

1. **major — 新意必须限定在 target，不是 VOC/halting**：PonderNet/ACT只是一部分邻域；应补 rational metareasoning/value-of-computation 与 adaptive planning budget 工作，避免把经典概念重命名。
2. **major — 与 When-to-Trust/Harmo/CheckVLA 的字段仍基于摘要级概述**：是否已有 success/progress proxy、sequential calls或相同cost项需要正文复核。
3. **major — paired target规模可能不可行**：20k decision epochs×多k×8 seeds×候选执行不是4 GPU/4天的自然结果；若只能小数据，VOC head可能学task lookup。

## 具体修改动作

1. 将贡献写成“机器人视觉WAM的 CRN paired marginal decision-value dataset/objective”，明确不宣称发明VOC/halting。
2. 补 rational metareasoning/adaptive planning compute 最近邻表；逐正文核验 When-to-Trust/Harmo/CheckVLA 的target与停止粒度。
3. 写出分支总rollout数、模拟step/s、存储、GPU-hours；给5k go/no-go后的可执行完整规模。
4. 增加 state/task ID blocked split 和 cross-task VOC transfer，防head只记task/step。

## Round 03 验收条件

- [ ] claim只落在paired visual decision-value target与数据，不把VOC/halting当新。
- [ ] rational metareasoning与三篇直接WAM邻居逐项核验。
- [ ] 数据/算力乘法账闭合并有降级实验矩阵。
- [ ] VOC head 的task/step捷径有blocked split和shuffle审计。

