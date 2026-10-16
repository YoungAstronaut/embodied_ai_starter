# Round 09 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r08
- File: `proposals/WAM-P2_value_of_imagination/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已拆sim paired-target主claim与real gate secondary，分task/WAM/device OOD，加入真机cal/eval隔离、K/fallback条件与无held-out real test即删transfer；R8 claim错位已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 计算分配重要。 |
| D2 失败模式清晰度 | 4.5 | non-myopic compute反例强。 |
| D3 创新性/最近邻 | 4.5 | visual WAM paired continuation target边界清楚。 |
| D4 机制因果闭环 | 4.5 | CRN→Bellman→gate闭合。 |
| D5 技术正确性 | 4.5 | cross-fit/cost正确。 |
| D6 可观测性/泄漏 | 4.5 | sim target与real gate分开。 |
| D7 数据可得性 | 4.0 | target昂贵但gate明确。 |
| D8 算力/工程 | 4.0 | 完整账可执行。 |
| D9 可证伪性 | 4.5 | 2×2/winner/oracle强。 |
| D10 基线强度 | 4.5 | VOC/proxy gates充分。 |
| D11 消融充分性 | 4.5 | paired×continuation完整。 |
| D12 OOD/真机 | 4.0 | secondary边界诚实。 |
| D13 复现性 | 4.5 | CRN/resource manifest强。 |
| D14 CVPR契合度 | 4.5 | 世界模型与实时控制结合自然。 |
| D15 风险/负结果 | 4.5 | scheduler/variance-only降级明确。 |

平均分：**4.40/5.00**。round<10，不通过。

## 模拟审稿攻击

1. **“VOC and adaptive computation are old.”** 摘要不能说发明value of computation；只说视觉WAM中可执行的paired potential-outcome target与non-myopic prevalence test。
2. **“Millions of oracle rollouts buy 5pp.”** target×stopping 2×2、label-equal adapters与target generation cost必须主表，不藏resource appendix。
3. **“Real robot does not validate continuation labels.”** Claim B只写gate transfer Pareto，绝不能在结论合并成real-world VOC verification。

## 修改与R10验收

标题建议 **Paired Continuation-Value Targets for Budgeted World-Model Imagination**。摘要明确两claim但只一个primary；主图将exact-reset target worker与deploy gate分隔。R10需预写continuation-positive<5%、oracle上界<4pp和real transfer失败三种降级摘要，并确认不会换标题保留过强claim。
