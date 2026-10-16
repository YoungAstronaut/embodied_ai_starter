# Round 01 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r00
- File: `proposals/WAM-P2_value_of_imagination/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / REVISE**（round<10；无不可修复 fatal flaw）

## 文件变更核验

r00 已实际包含 paired k/k+1 counterfactual target、sequential VOC stopping、anytime ranking、固定 p95 wall-clock、oracle VOC 及 When-to-Trust/Harmo/CheckVLA/DELE 基线，符合交接。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | WAM 计算是否产生净决策价值关系到实时部署；未量化现有 WAM 在多少状态中 oracle VOC 为正。 |
| D2 失败模式清晰度 | 4.0 | 固定预算下过算/欠算和 tail latency 清楚；`R(a_k)` 的 horizon/奖励单位未定义。 |
| D3 创新性/最近邻 | 4.0 | 从 gate 收缩为 paired marginal VOC 与序贯停止，差异可信；metareasoning/VOC 最近邻缺失。 |
| D4 机制因果闭环 | 3.5 | paired target→VOC→stop→ranking→success 路径存在；ranking 改变是否正确和延迟代价如何耦合仍粗。 |
| D5 技术正确性 | 3.0 | `L_monotone` 可能错误：额外计算的边际价值不必单调；binary episode reward 使单步 VOC target 高方差且反事实分支定义不全。 |
| D6 可观测性/泄漏 | 4.5 | exact-reset reward 只作 target，部署只看 partial stats/time；未来 frame/success 禁止清楚。 |
| D7 数据可得性 | 3.5 | 仿真 paired branch 可生成；真实数据 calibration target、reward 定义和 trace 发布未明确。 |
| D8 算力/工程 | 3.5 | 统一 WAM/NFE/p95 与硬回退；50 tasks×paired branches 和真机 jitter 成本、scheduler overhead 未估。 |
| D9 可证伪性 | 4.0 | 等 p95、forward 降幅、AUROC/ECE、oracle 上界/简单 gate 阈值明确。 |
| D10 基线强度 | 4.5 | always/never/random、直接邻居、compact path 与 oracle 齐全，承诺统一 checkpoint/候选/NFE。 |
| D11 消融充分性 | 4.0 | 时间/miss/序贯/统计/jitter/tail latency 均拆；reward horizon/target noise/selection bias 未拆。 |
| D12 OOD/真机 | 4.0 | 多硬件/网络 trace、动态/contact tasks 和 400 真机 trials；任务 OOD 与模型误差 OOD 尚弱。 |
| D13 复现性 | 3.0 | 无 trace schema、clock 边界、reward evaluator、checkpoint/seed/artifact 清单。 |
| D14 CVPR 契合度 | 3.5 | 视觉 world rollout 的价值是核心，但容易被审成 scheduling/metareasoning 系统论文，需视觉错误分析。 |
| D15 风险/负结果 | 4.0 | sim-to-real、全链路延迟和无价值经验定律均有明确处理。 |

平均分：**3.80/5.00**。关键门槛：D3=4.0、D5=3.0、D6=4.5、D9=4.0；未达 hardened gate。

## Top 问题

1. **major — VOC target 没有决策单位**：`R(a_k)` 是候选一次执行、H 步回报还是 episode success？k/k+1 改变排序后实际执行分支不同，必须定义 common-random-number potential outcome。
2. **major — monotonicity 假设可能技术错误**：更多 rollout 能因模型 bias 让排序变差，边际 VOC 可正负交替；`L_monotone` 可能正好抹去需要检测的 harmful imagination。
3. **major — CVPR 视觉命题不足**：若性能只取决于 deadline/设备负载，贡献是 scheduler。必须证明 partial visual rollout 的可诊断统计决定 VOC，并分析模型错误类型。

## 最近邻冲突与证据缺口

- [When to Trust Imagination 2605.06222v2](https://arxiv.org/abs/2605.06222) 与 [HarmoWAM 2605.10942v1](https://arxiv.org/abs/2605.10942) 已做 adaptive execution/gating；需复核它们是否实际上也估计决策收益 proxy。
- [CheckVLA 2607.26789v1](https://arxiv.org/abs/2607.26789) 的 latency-aware intervention 与 conformal trigger 是强近邻。
- 经典 value-of-computation / adaptive computation / early-exit literature 未进入 related work；科学命题可能不是机器人独有但必须承认。

## 必须修改的动作

1. 给出一个 decision epoch 的 potential-outcome 定义：共同初态/外生 seed、k 与 k+1 的候选、执行 horizon、reward、deadline penalty；说明 target 方差估计。
2. 删除无依据的 monotone loss，或证明只约束可证明单调的 quantity；保留 harmful-compute labels。
3. 分解 VOC gain：compute-only scheduler、rollout uncertainty、rollout semantic/geometry error、ranking margin；加入 shuffled-rollout-stat control。
4. 同时匹配 mean、p95、NFE、候选数和控制频率；报告 scheduler 本身耗时，不只 success/GPU-second。

## Round 02 验收条件

- [ ] `VOC_k` 的 potential outcomes、reward horizon、common randomness 和延迟状态完全定义。
- [ ] monotonicity 要么有证明/正确约束，要么删除。
- [ ] 增加 compute-only 与 shuffled visual-stat controls，能区分视觉 world-model 贡献。
- [ ] 最近邻表补 metareasoning/adaptive-compute，并逐项对比 When-to-Trust/Harmo/CheckVLA。
- [ ] refinement log 记录改动并升为 r01。

