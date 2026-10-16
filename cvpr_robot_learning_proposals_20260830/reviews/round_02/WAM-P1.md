# Round 02 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r01
- File: `proposals/WAM-P1_occlusion_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（无 fatal；创新点已从 slot 转为 referent posterior，但仍需证明非 JPDA+WAM 组合）

## 实际变更核验

r01 已按可辨识性三分、定义冻结 Hungarian anchor、permutation-invariant proper scoring、prediction/association/update/pruning、M≤4+unknown、passive/active 2×2，并补 JPDA/JRDB。R1 对称不可辨识与 metric 缺口实质修复。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 长遮挡 referent 错误直接影响长程操作。 |
| D2 失败模式清晰度 | 4.5 | identifiable/partial/symmetric 使可解边界清楚。 |
| D3 创新性/最近邻 | 4.0 | 相对 OA/POT 的 posterior/calibration 增量明确；但核心可能是 JPDA/MHT 接 WAM 与 language anchor。 |
| D4 机制因果闭环 | 4.0 | passive belief 与 active control 已拆，belief shuffle/swap完善。 |
| D5 技术正确性 | 4.0 | 更新/锚定/unknown/pruning可实现；“provably symmetric”自动证明仍未给。 |
| D6 可观测性/泄漏 | 4.5 | full trajectory只target、匹配冻结、contact时序清楚。 |
| D7 数据可得性 | 4.0 | 三档生成字段和规模明确。 |
| D8 算力/工程 | 3.5 | detector+association+WAM+400真机仍重，profiling缺。 |
| D9 可证伪性 | 4.5 | 对称档proper scoring、passive success、oracle与active降级明确。 |
| D10 基线强度 | 4.0 | OA/POT/3D-ALP/JPDA/RALO/tracker/oracle齐全；MHT/learned probabilistic slot baseline缺。 |
| D11 消融充分性 | 4.5 | evidence/prior、M、contact/covariance/calibration/passive-active全面。 |
| D12 OOD/真机 | 4.5 | 遮挡、交叉、接触交换、可辨识分层和真机。 |
| D13 复现性 | 3.5 | 指标公式增强；仍缺版本/schema/evaluator tests/artifact。 |
| D14 CVPR 契合度 | 4.0 | 视觉对象身份与遮挡预测明确。 |
| D15 风险/负结果 | 4.5 | 不可辨识边界本身有出版价值。 |

平均分：**4.17/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；未过 hardened gate/mean。

## Top 问题

1. **major — “JPDA+语言锚点+WAM”组合创新风险**：[JRDB 1910.11792](https://arxiv.org/abs/1910.11792) 已以长遮挡/ID switch为核心，JPDA/MHT长期维护多假设。新科学命题必须是 action/contact-conditioned referent posterior 如何改变 manipulation，而非再次发明 association posterior。
2. **major — OA-WAM差异仍只按作者概述**：[OA-WAM 2605.06481v1](https://arxiv.org/abs/2605.06481) 的 slot-swap和address reset可能已比“单地址”描述更强；需从正文/代码核实。
3. **major — 可辨识性标签可能成为事后分组**：若用完整轨迹才能判 identifiable/symmetric，benchmark分析有效但模型训练/部署不能依赖；需要明确证明字段只用于分层。

## 具体修改动作

1. 增加 MHT/JPDA、probabilistic slots/object permanence、language-grounded tracking 三类直接邻居；逐项写是否 action/contact-conditioned、是否输出 posterior、是否连接 control。
2. 实现 `JPDA+same WAM+same language anchor` 强基线；只有 learned action/contact likelihood 或 posterior-marginal control超越它才能称新机制。
3. 对 OA-WAM/POT 逐正文填 address reset、occlusion update、uncertainty、swap test、代码状态，不能推断。
4. 把 identifiability proof字段列为 evaluator-only，并给不使用该字段训练的审计。

## Round 03 验收条件

- [ ] JPDA/MHT/probabilistic-slot/language-tracking 最近邻表完整。
- [ ] `JPDA+WAM` 同预算强基线进入判负。
- [ ] OA/POT 字段来自正文/代码并标不确定性。
- [ ] identifiability 分层不进入 student、loss或controller，信息图可审计。

