# Round 02 Review — JEP-P2

- Proposal-ID: JEP-P2
- Reviewed-Revision: r01
- File: `proposals/JEP-P2_object_contact_slots/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（R1 action-conditioning fatal 已解除；graph-dynamics组合创新风险仍高）

## 实际变更核验

r01 已闭合 `G_t+a_i→typed concurrent edits→executor→JEPA/scorer`，primitive只Add/Del typed edges，compound derived、transfer atomic，主teacher current/past-only，并有action×edit 2×2与NRI/Interaction Networks。R1 fatal解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | contact topology改变动力学是重要缺口。 |
| D2 失败模式清晰度 | 4.5 | typed edges/transactions/legality与任务族清楚。 |
| D3 创新性/最近邻 | 3.5 | 动态graph edits相对OA/POT新；但NRI/Interaction Networks/C-SWM已覆盖action/object relation dynamics，JEPA应用可能是组合。 |
| D4 机制因果闭环 | 4.5 | candidate action→edit→future→ranking，2×2定向干预强。 |
| D5 技术正确性 | 4.0 | 循环/ontology已修；Horizon endpoint edits丢失中间attach-detach transient的风险。 |
| D6 可观测性/泄漏 | 4.5 | causal association主teacher、full trajectory只oracle。 |
| D7 数据可得性 | 4.0 | extractor/abstain/noise轴可执行。 |
| D8 算力/工程 | 3.5 | graph+JEPA+N candidates+320真机工作量仍高。 |
| D9 可证伪性 | 4.5 | NRI/ContactWorld/teacher gap/edit 2×2判负清楚。 |
| D10 基线强度 | 4.5 | OA/POT/NRI/IN/contact/tactile/oracles齐全；C-SWM/graph transformer可补。 |
| D11 消融充分性 | 4.5 | operator/legality/cycle/contact/tracker/teacher/edit全面。 |
| D12 OOD/真机 | 4.5 | edit类型/遮挡/noise/真机事件分轴。 |
| D13 复现性 | 3.5 | algebra/extractor显著增强；仍缺版本/seed/schema artifact。 |
| D14 CVPR 契合度 | 4.5 | dynamic scene graph预测有明显视觉贡献。 |
| D15 风险/负结果 | 4.5 | causal-teacher gap与topology benchmark有价值。 |

平均分：**4.20/5.00**。D3=3.5、D5=4.0、D6=4.5、D9=4.5；未过创新/技术/mean gate。

## Top 问题

1. **major — 图动力学+JEPA可能是直接组合**：[Interaction Networks 1612.00222](https://arxiv.org/abs/1612.00222)、[NRI 1802.04687](https://arxiv.org/abs/1802.04687)、[C-SWM 1911.12247](https://arxiv.org/abs/1911.12247) 已学习对象关系/结构化world dynamics。新意必须是 contact topology **edit algebra/transactions under occlusion**，不是graph predictor。
2. **major — ContactWorld/ViTac字段仍未正文级定案**：表写“依原模型”，无法排除已有contact graph/force topology。
3. **major — endpoint edit set可能遗漏关键transient**：H内attach后又detach时G0/GH最小edit为空，但中间contact决定动作风险；当前label extractor会把机制抹掉。

## 具体修改动作

1. 增加C-SWM/graph world model/temporal scene graph逐项表；将贡献限定为event sequence/transaction，而非graph dynamics。
2. 从`G0/GH edit set`升级为带timestamp/partial order的edit event sequence，或明确主claim只覆盖persistent topology并排除transient。
3. 正文核查ContactWorld/ViTac/TouchWorld是否含body graph/attachment/ownership；把官方代码状态列出。
4. 加`action-conditioned NRI + same typed event labels`基线，检验JEPA是否必要。

## Round 03 验收条件

- [ ] graph-world-model/C-SWM最近邻完整，graph/JEPA本身不当新。
- [ ] transient contact事件不会被endpoint cancellation静默丢弃。
- [ ] ContactWorld系字段来自正文且代码状态明确。
- [ ] action-conditioned NRI+typed labels与JEPA公平对照进入判负。

