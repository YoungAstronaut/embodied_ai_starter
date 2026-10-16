# Round 07 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r06
- File: `proposals/JEP-P1_action_equivalence/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已加入Action-Bisim native/adapter、四模型validation winner、同non-JEPA recursive/local target、assignment strata及S32/triangle/runtime gate。R6最强基线边界已响应，actual rollouts/triangle tests=0明确。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | action outcome metric有价值。 |
| D2 失败模式清晰度 | 4.5 | metric/assignment反例清楚。 |
| D3 创新性/最近邻 | 4.0 | Action-Bisim后边界仍窄。 |
| D4 机制因果闭环 | 4.5 | target metric到ranking闭合。 |
| D5 技术正确性 | 4.5 | metric定义与null cost稳定。 |
| D6 可观测性/泄漏 | 4.5 | future/UUID隔离。 |
| D7 数据可得性 | 3.5 | S32与跨embodiment数据尚无pilot。 |
| D8 算力/工程 | 3.5 | horizon、pairwise storage、full上限未闭合。 |
| D9 可证伪性 | 4.5 | direct baseline持平即判负。 |
| D10 基线强度 | 4.5 | native/adapter/target winner充分。 |
| D11 消融充分性 | 4.5 | backbone×metric+target对照强。 |
| D12 OOD/真机 | 4.0 | 跨平台secondary，真机安全扰动有限。 |
| D13 复现性 | 4.0 | manifest规划好，数据单位欠完整。 |
| D14 CVPR契合度 | 4.0 | 需控制收益支撑。 |
| D15 风险/负结果 | 4.5 | metric-only降级明确。 |

平均分：**4.20/5.00**。D3/D7/D8/D13未达门槛；round<10，不通过。

## 数据/资源攻击面

1. `2k×16×32=1.024M outcomes`正确，但仍要乘rollout horizon H；H未冻结，因此env steps和wall-clock未知。
2. W1 metric需每state的action pairs：16 actions是120 pairs，32 actions是496 pairs；full 20k约9.92M pair distances，target storage/OT计算未计。
3. S32 reference与S8 train是否使用nested seeds未说明。“S8另计”若独立会浪费，若prefix则应明确以paired bias估计。
4. train/test只按object/camera/embodiment拆分，没写task template、state reset family和role assignment detector训练split，可能跨split近重复。

## 具体修改动作

1. 冻结H并给`N_state×N_action×S×H` env steps、`N_state×C(N_action,2)` OT/target records及字节数。
2. S8为S32 prefix，共享outcome；列OT算法/正则/CPU-GPU实现、time complexity和cache。
3. 明确2k variance MVP只决定S/CI与assignment coverage；20k规模由cluster power和8天cap共同决定。
4. manifest加入state-family/task-template/asset/role-instance hash，按family group split；canonicalizer detector只用train资产。

## Round 08 验收条件

需闭合H、pairwise OT/storage与seed nesting，给family-level split。R8再审查跨embodiment canonical outcome是否真OOD而非adapter泄漏。
