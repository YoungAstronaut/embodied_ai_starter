# Round 05 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r04
- File: `proposals/WAM-P1_occlusion_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**（R4 posterior fatal已解除）

## 实际变更核验

r04 已显式建`p(R,Z,D)`，prior只随R一次，`w_m^+=Σ_Zp(R=m,Z|D)`；0.8/0.2→0.3077/0.6923手算正确，miss保留身份、unknown独立。R4 fatal解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.5 | 身份belief重要。 |
| D2 | 4.5 | 三可辨识档清楚。 |
| D3 | 4.0 | action/contact posterior增量待证。 |
| D4 | 4.5 | R/Z→belief→control闭合。 |
| D5 | 4.0 | posterior已修，但指标段仍写“miss映射unknown”，与方法冲突。 |
| D6 | 4.5 | evaluator隔离。 |
| D7 | 4.0 | 50k episodes可得。 |
| D8 | 4.0 | M≤4可行。 |
| D9 | 4.0 | NLL/ECE/switch/success多重门槛未分层。 |
| D10 | 4.5 | JPDA+WAM等强。 |
| D11 | 4.5 | 消融充分。 |
| D12 | 4.0 | 真机合理。 |
| D13 | 4.0 | 数值单测增强，metric语义需清理。 |
| D14 | 4.5 | 契合CVPR。 |
| D15 | 4.5 | 对称边界价值强。 |

平均分：**4.27/5.00**。D3/D5/D9=4.0；round<10，R5不通过。

## 实验攻击面

1. **内部矛盾。** 方法明确miss保留R质量，指标段仍称“miss映射unknown”；这会改变NLL标签和coverage。
2. **primary不唯一。** switch、ECE、NLL、passive success均有阈值；应以proper log score作为belief主张primary，success为key secondary。
3. **stratum混合。** identifiable与symmetric的最优预测不同，不能混成一个NLL均值；需预注册macro/stratum权重。
4. **50k episode不等于50k独立。** 同task/template/trajectory高度相关，task与episode双层CI及真机block功效缺失。

## 修改与R6验收

1. 统一miss/unknown语义并更新metric loader。
2. primary锁定≥2s identifiable+partial的permutation-invariant log score；symmetric excess NLL单独boundary endpoint，passive success key secondary。
3. 预注册stratum macro权重，不按结果重加权。
4. task-stratified episode cluster CI；真机paired template/block功效及baseline同轨迹。

