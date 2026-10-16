# Round 10 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r09
- File: `proposals/WAM-P2_value_of_imagination/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 已明确 Value-of-Computation/learned halting 不新，唯一命题是 common-random-number paired continuation-value target 在固定实时预算下能否优于 paired-myopic 与 validation winner；oracle rollouts、cost与real transfer均有删除式claim ladder。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | WAM何时值得计算直接影响实时控制。 |
| D2 失败模式清晰度 | 4.5 | harmful compute与deadline cost可观察。 |
| D3 创新性/最近邻 | 4.5 | 新边界是paired continuation target而非halting。 |
| D4 机制因果闭环 | 4.5 | CRN potential outcome→A_k→stop完整。 |
| D5 技术正确性 | 4.5 | incremental cost与cross-fit定义正确。 |
| D6 可观测性/泄漏 | 4.5 | future reward只进离线target。 |
| D7 数据可得性 | 4.0 | S16 branch record成本仍大。 |
| D8 算力/工程 | 4.0 | 资源分账可信但设备依赖明显。 |
| D9 可证伪性 | 4.5 | paired-myopic/winner与harmful compute可判负。 |
| D10 基线强度 | 4.5 | Ponder/ACT/When-to-Trust/CheckVLA均纳入winner。 |
| D11 消融充分性 | 4.5 | CRN×target 2×2与S敏感性充分。 |
| D12 OOD/真机 | 4.0 | real gate仅secondary且可删除。 |
| D13 复现性 | 4.5 | seeds、target records、latency/energy齐全。 |
| D14 CVPR契合度 | 4.5 | WAM实时决策价值契合机器人学习。 |
| D15 风险/负结果 | 4.5 | prevalence/oracle/transfer三层降级。 |

平均分：**4.40/5.00**；关键维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **paired-myopic/winner持平：** 删除continuation superiority，仅发布paired target/compute-harm诊断。
- **secondary success <3pp：** 不宣称控制收益，只报告离线decision-value calibration。
- **held-out WAM/device失败：** 删除transfer，限定训练WAM/设备下的预算结论。

## 未决非致命风险与最终修改

target 生成可能把昂贵oracle rollout优势隐含进标签。r10 必须加入 target-build compute、teacher quality 和部署决策 compute 三列分账，并声明目标构建不计入部署但计入研究成本；追加 round_10/r10 log。当前仅9次refine。
