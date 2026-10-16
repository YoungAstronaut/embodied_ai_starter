# Round 10 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r09
- File: `proposals/WAM-P1_occlusion_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 将论文科学对象锁为 identifiable/partial/ε-symmetric strata、orbit proper score 与 instance-support/proof-failure protocol；L11 JPDA+same-WAM 放在首行，method可以删除而benchmark仍成立。这与OA-WAM/POT-VLA的persistent slot不同，D3可升至4.5。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 长遮挡错身份是核心操作失败。 |
| D2 失败模式清晰度 | 4.5 | 三identifiability strata清楚。 |
| D3 创新性/最近邻 | 4.5 | proper-score分层协议超出persistent slots。 |
| D4 机制因果闭环 | 4.5 | posterior→association/update→决策完整。 |
| D5 技术正确性 | 4.5 | 联合posterior及手算单测修正正确。 |
| D6 可观测性/泄漏 | 4.5 | evaluator shard/GT schema隔离。 |
| D7 数据可得性 | 4.0 | ε-symmetry与rerender需专门生成。 |
| D8 算力/工程 | 4.0 | beam/detector/WAM账目可控。 |
| D9 可证伪性 | 4.5 | L11胜负、stratum score可直接推翻method。 |
| D10 基线强度 | 4.5 | JPDA/MHT/OA/POT同预算。 |
| D11 消融充分性 | 4.5 | evidence×inference L00–L11完整。 |
| D12 OOD/真机 | 4.0 | benchmark主线，真机控制可删。 |
| D13 复现性 | 4.5 | codes、family split、support gate完整。 |
| D14 CVPR契合度 | 4.5 | 身份可观测性benchmark有视觉价值。 |
| D15 风险/负结果 | 4.5 | method失败仍保留proper-score协议。 |

平均分：**4.40/5.00**；关键维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **L11 JPDA持平/胜出：** 删除Belief-WAM方法贡献，保留Occlusion-ID benchmark。
- **control success <3pp：** 不把proper-score改善写成控制改善，二者分表。
- **真机instance support不足：** 删除real transfer，只报告simulator-certified ε-symmetric strata。

## 未决非致命风险与最终修改

“ε-symmetric”仍可能被误读成现实可证明对称。r10 必须新增 orbit 构造、支持数、证书失败率与 null/uniform predictor proper score 的显式表，并在摘要固定写 simulator-certified；追加 round_10/r10 log。当前只有9次refine，暂不认证。
