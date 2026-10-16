# Round 05 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r04
- File: `proposals/GEO-P3_geometry_confidence/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r04 已在独立calibration拟合冻结90%coverage，q/v由单一regret CDF导出，q优先决策，并为repair加入density/decoder/policy-latent/placebo门槛。R4问题已实质解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.5 | 可靠几何路由重要。 |
| D2 | 4.5 | corruption/hard pairs清楚。 |
| D3 | 4.0 | geometry-specific defer待证。 |
| D4 | 4.5 | CDF→route闭合。 |
| D5 | 4.5 | fixed coverage/repair合同已修。 |
| D6 | 4.5 | GT只target。 |
| D7 | 4.0 | 标签预算闭合。 |
| D8 | 4.0 | 三分支成本诚实。 |
| D9 | 4.0 | risk/AURC/ECE/success仍同时被称主结果。 |
| D10 | 4.5 | defer/selective强基线足。 |
| D11 | 4.5 | router/repair/placebo充分。 |
| D12 | 4.0 | OOD/真机合理。 |
| D13 | 4.0 | threshold合同清楚，统计功效缺。 |
| D14 | 4.5 | 契合CVPR。 |
| D15 | 4.5 | error atlas负价值强。 |

平均分：**4.30/5.00**。D3/D9=4.0；round<10，R5不通过。

## 实验攻击面

1. **endpoint层级仍不唯一。** 90%coverage下binary regret risk最贴合H1；AURC/ECE/success应分为mechanism/key secondary，不能任一显著即过。
2. **calibration与OOD边界。** 若calibration已看同类透明/遮挡/运动等级，test只换对象并非新corruption；需预注册level/family holdout。
3. **geometry-aware vs regret-only比较有多重选择。** 判负写“success≥3pp或AURC≥.03”，OR规则提高假阳性。
4. **power缺失。** 每轴5级、3 seeds且按frame计会产生严重时序伪重复；episode/trajectory才是cluster。

## 修改与R6验收

1. primary锁定calibration-frozen 90%coverage下selected-branch binary regret risk；其余指标有固定层级。
2. 增加unseen corruption-family与unseen severity两种test，50-shot recalibration另列adaptation协议。
3. geometry-aware相对generic/regret-only用预注册单一primary，不用success/AURC二选一。
4. episode-cluster paired CI、按corruption family多重校正，并给检测25%相对risk下降的样本功效。

