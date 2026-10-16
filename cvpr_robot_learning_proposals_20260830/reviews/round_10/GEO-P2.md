# Round 10 Review — GEO-P2

- Proposal-ID: GEO-P2
- Reviewed-Revision: r09
- File: `proposals/GEO-P2_contact_transition/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 将唯一命题锁为 candidate-conditioned typed contact transition ranking，ContactGuard-label-equal 位于主表首列，并保留 ontology-only 降级稿。官方刷新确认 ContactGuard v1 已覆盖 action-conditioned latent pre-contact abort 与真机，因此新意仅能来自 event time/mode/normal 的显式、可干预转移字段。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 接触失败直接决定操作成功。 |
| D2 失败模式清晰度 | 4.5 | mode/time/normal/body-pair均可观测。 |
| D3 创新性/最近邻 | 4.5 | 相对ContactGuard保留typed transition protocol。 |
| D4 机制因果闭环 | 4.5 | action→field→score→selection完整。 |
| D5 技术正确性 | 4.5 | cause-specific hazard含删失/无事件。 |
| D6 可观测性/泄漏 | 4.5 | GT pose/contact仅target/oracle。 |
| D7 数据可得性 | 4.0 | 密集接触事件标注有漏斗损耗。 |
| D8 算力/工程 | 4.0 | 1.024M attempted与100M cap透明。 |
| D9 可证伪性 | 4.5 | fixed-action错误field与selection regret直接。 |
| D10 基线强度 | 4.5 | ContactGuard-equal和latent/field组合齐全。 |
| D11 消融充分性 | 4.5 | target×executor 2×2及null channel。 |
| D12 OOD/真机 | 4.0 | 真机secondary且有共享abort。 |
| D13 复现性 | 4.5 | ontology、单位、同步、support均定义。 |
| D14 CVPR契合度 | 4.5 | 显式3D接触表示与视觉控制强相关。 |
| D15 风险/负结果 | 4.5 | ontology/router降级仍有价值。 |

平均分：**4.40/5.00**；关键维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **ContactGuard-equal持平：** method claim删除，只保留接触转移 ontology/benchmark。
- **typed field只提升F1、不降regret：** 机制链断裂，论文降为表示诊断，不报告控制收益。
- **sim→real失败或fallback>30%：** 删除transfer claim，并把传感同步/ontology mismatch作为负结果。

## 未决非致命风险与最终修改

annotation ontology 的一致性仍可能决定全部结果。r10 必须把双标者 κ、各event support、删失率和 timestamp tolerance 的敏感性纳入主验收表，并写入 round_10/r10 log。现有log只有9次refine，故暂不最终PASS。
