# Round 05 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r04
- File: `proposals/GEO-P1_counterfactual_geometry/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r04 已用同一M=64候选库和`-logΣ_{S*}p`闭合support，并加入deploy Hungarian+null set matching、type CE辅助定位及primary selection regret。R4公式问题已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 几何捷径问题重要。 |
| D2 失败模式清晰度 | 4.5 | pair/hard negative清楚。 |
| D3 创新性/最近邻 | 4.0 | relation intervention增量待实验。 |
| D4 机制因果闭环 | 4.5 | set-mass→selection闭合。 |
| D5 技术正确性 | 4.5 | 共同support和set matching已修。 |
| D6 可观测性/泄漏 | 4.5 | checker字段隔离。 |
| D7 数据可得性 | 4.0 | 20k pair可尝试。 |
| D8 算力/工程 | 3.5 | pair生成/64候选/CEM成本仍缺全账。 |
| D9 可证伪性 | 4.0 | primary endpoint与H1的OOD action claim尚不一致。 |
| D10 基线强度 | 4.5 | 最近邻充分。 |
| D11 消融充分性 | 4.5 | 2×2/type/swap齐全。 |
| D12 OOD/真机 | 4.0 | 外测合理。 |
| D13 复现性 | 4.0 | schema好，regret定义/功效缺。 |
| D14 CVPR契合度 | 4.0 | 几何VLA契合。 |
| D15 风险/负结果 | 4.5 | selection bias/unmappable边界明确。 |

平均分：**4.20/5.00**。D3=4.0、D9=4.0；round<10且关键维未达门槛。

## 实验攻击面

1. **primary与H1错位。** H1强调背景OOD action稳定/任务关系敏感，primary却只是在oracle筛选的同库selection regret；可在合成库上下降而closed-loop OOD无收益。
2. **selection regret未定义utility。** 是相对最佳valid action的0/1 regret、checker cost还是short-horizon reward？不同定义会改变20%效应。
3. **无功效/样本层级。** 20k attempted不是accepted数；pair嵌套task/snapshot，简单pair bootstrap会把同task相关样本当独立。
4. **baseline训练预算。** Cofact/CAST等必须拿相同accepted+rejected/control数据与64候选，否则SCM方法多拿标签。

## 修改与R6验收

1. primary改为预注册的held-out causal/nuisance pair selection regret，并把几何OOD episode success设key secondary、要求方向一致；若success<3pp则只保留diagnostic claim。
2. 写出regret公式、reward horizon与oracle coverage。
3. 按task→snapshot/pair层级bootstrap或mixed model，给accepted率下检测20%相对下降所需样本。
4. 所有强基线共享attempted pool/accepted labels/64 candidates；额外SCM标签成本单列。

