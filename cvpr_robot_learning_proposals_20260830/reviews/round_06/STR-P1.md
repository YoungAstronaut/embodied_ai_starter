# Round 06 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r05
- File: `proposals/STR-P1_event_intent_reset/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已把 recovery 明确定义为回到 pre-event progress/trajectory tube 并连续 L=3，设置 H=64 右删失；唯一 primary 为 event-family macro RMRT，并有同 proposer comparator、FWER 与功效。R5 的恢复指标和统计问题解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 事件后错误意图延续是长程控制痛点。 |
| D2 失败模式清晰度 | 4.5 | shift/slip/obstruction/false visual 可观测。 |
| D3 创新性/最近邻 | 4.0 | event gate/BOCPD 既有，增量在 reset-worthy value evidence。 |
| D4 机制因果闭环 | 4.5 | innovation→ΔQ LCB→reset→recovery 闭合。 |
| D5 技术正确性 | 4.5 | 时序、conformal 多头与 censoring 已一致。 |
| D6 可观测性/泄漏 | 4.5 | deployment gate 不读 intent oracle。 |
| D7 数据可得性 | 4.0 | 反事实候选价值生成可行但昂贵。 |
| D8 算力/工程 | 4.0 | K4/HQ16 可做，事件覆盖需 pilot。 |
| D9 可证伪性 | 4.5 | 单 primary 与 detector-only 降级明确。 |
| D10 基线强度 | 4.5 | 同 proposer validation winner 是强合同。 |
| D11 消融充分性 | 3.5 | innovation 与 value/reset-worthiness 尚未正交。 |
| D12 OOD/真机 | 4.5 | 多事件家族与低速真事件反向对照好。 |
| D13 复现性 | 4.5 | tube、L/H、cluster与阈值清楚。 |
| D14 CVPR契合度 | 4.5 | 视觉事件理解与VLA控制结合紧。 |
| D15 风险/负结果 | 4.5 | 低控制收益自动降级。 |

平均分：**4.33/5.00**。D3=4.0、D11=3.5；round<10，不通过。

## Top 问题与证据缺口

1. **当前比较仍混合“发现变化”与“判断应重置”。** CheckVLA/BOCPD/learned gate 用不同 trigger object 与标签；本法又同时拥有 innovation 和 S=8/HQ16 的 ΔQ target。RMRT 改善无法判断来自更强监督还是 AND/LCB 机制。
2. **删除 ΔQ head 不是正交证据。** 还需纯 ΔQ、纯 innovation、generic concat gate 与结构化 combined gate，且都用同训练事件/候选价值标签。
3. **validation winner 规则未说明 label-native 与 label-equal。** BOCPD 无需反事实标签，CheckVLA用风险标签；需要两条赛道，否则“公平”没有唯一含义。

## 具体修改动作

1. 主 2×2 固定 `change evidence {off/on}` × `reset-value evidence {off/on}`：两者皆 off 用 matched-rate gate；单因子格分别纯 innovation/纯 ΔQ；双因子格用 proposed rule，另加同参数 generic concat MLP。
2. 所有 learned gate 共享 K4 proposer、S8/HQ16 target pool、训练事件数、fallback、reset budget；同时保留各论文 native-target 结果，不混表。
3. 最强 comparator 从 label-equal gates 的 validation RMRT winner 冻结；native winner 作为外部可用系统比较。不同 threshold 都只在同 validation split 调一次。
4. 把 visual/proprio evidence OR 的模态消融做成 equal-rate matched threshold，避免触发频率不同伪造RMRT收益。

## Round 07 验收条件

正文需出现 change×value 2×2、generic concat control、native/label-equal 两类 winner 与 equal-rate threshold 规则；并给每 event-family 的 target acceptance/右删失 pilot 比例。
