# Round 09 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r08
- File: `proposals/WAM-P1_occlusion_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已将唯一主线改为benchmark proper score，全文降为simulator-certified ε-symmetric，加入4–6实例OOD、residual/fallback、logger/guard与control可删除规则；R8 overclaim已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | referent identity ambiguity重要。 |
| D2 失败模式清晰度 | 4.5 | identifiable/partial/ε-symmetric清楚。 |
| D3 创新性/最近邻 | 4.0 | 近同构JPDA使方法创新有限，benchmark较强。 |
| D4 机制因果闭环 | 4.5 | posterior→proper score/control闭合。 |
| D5 技术正确性 | 4.5 | posterior/proof语义严谨。 |
| D6 可观测性/泄漏 | 4.5 | evaluator/logger隔离。 |
| D7 数据可得性 | 4.0 | generator gate可行。 |
| D8 算力/工程 | 4.0 | beam与proof cap明确。 |
| D9 可证伪性 | 4.5 | L11与control删除规则强。 |
| D10 基线强度 | 4.5 | JPDA ladder危险且公平。 |
| D11 消融充分性 | 4.5 | evidence×decision充分。 |
| D12 OOD/真机 | 4.5 | instance OOD与root外测清楚。 |
| D13 复现性 | 4.5 | proof/schema/lineage完整。 |
| D14 CVPR契合度 | 4.5 | benchmark+视觉跟踪价值明确。 |
| D15 风险/负结果 | 4.5 | tracking benchmark可独立成立。 |

平均分：**4.40/5.00**。D3=4.0且round<10，不通过。

## 模拟审稿攻击

1. **“This is JPDA with a WAM.”** 不要回避：L11近同构必须主表第一行；只有action/contact evidence与marginal control主效应独立成立才保留方法贡献。
2. **“Identity is unobservable under symmetry.”** proper scoring和ε-symmetric是论文卖点，不是局限脚注；摘要应明确不追求猜中ID。
3. **“Simulator certifies its own benchmark.”** proof tolerance sweep、rerender failure atlas、真机tracking metrics需要与control分开。

## 修改与R10验收

标题建议 **Occlusion-ID: Calibrated Referent Beliefs under Long Occlusion**，不必把WAM放标题中心。贡献顺序：benchmark/metric→near-isomorphic JPDA test→control secondary。主图只画referent posterior与logger隔离。R10准备L11持平时纯benchmark摘要，且不得在结论继续保留“novel belief update”。
