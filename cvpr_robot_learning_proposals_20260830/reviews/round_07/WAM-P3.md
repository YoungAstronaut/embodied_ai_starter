# Round 07 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r06
- File: `proposals/WAM-P3_hidden_physics_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已加入PEARL/RMA native/deploy-equal、raw/residual×point/distributional 2×2、共享innovation与仅按t2 regret选winner；还设置64/1024 gate。R6信息公平已响应，actual pilot=0如实标注。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | hidden dynamics适应关键。 |
| D2 失败模式清晰度 | 4.5 | physics与nuisance分层明确。 |
| D3 创新性/最近邻 | 4.0 | predictive belief增量待强基线。 |
| D4 机制因果闭环 | 4.5 | residual belief→CVaR动作闭合。 |
| D5 技术正确性 | 4.5 | CVaR与predictive equivalence合理。 |
| D6 可观测性/泄漏 | 4.5 | t0与GT字段控制强。 |
| D7 数据可得性 | 3.5 | 50k episode与物性覆盖尚无漏斗。 |
| D8 算力/工程 | 3.0 | candidate数/episode长/1024 subset缺失，无法算总calls。 |
| D9 可证伪性 | 4.5 | bias/归因/oracle均有门槛。 |
| D10 基线强度 | 4.5 | deploy-equal winner充分。 |
| D11 消融充分性 | 4.5 | representation×belief 2×2闭合。 |
| D12 OOD/真机 | 4.5 | 物性区间错开和实物变量自然。 |
| D13 复现性 | 4.0 | manifest规划好，sample/candidate合同不完整。 |
| D14 CVPR契合度 | 4.5 | 视觉世界模型与适应控制契合。 |
| D15 风险/负结果 | 4.5 | 可辨识边界降级充分。 |

平均分：**4.27/5.00**。D3/D7/D8/D13未达门槛；round<10，不通过。

## 数据/资源攻击面

1. “每候选16×4=64 utilities”没有定义16与4分别是什么，也没有candidate数；总WAM calls无法从50k episodes推出。
2. 50k episode没有episode horizon、每episode第2次交互可用state数、Latin hypercube cells或train/test物性间隔，D7/D8不可审计。
3. 1024 reference只说固定subset，未给state数和candidate数；若200 pilot states每个多候选×1024，可能已经是百万级WAM rollout。
4. PEARL/RMA/四格×三innovation家族的训练数量与validation selection multiplicity未计，且同一50k数据是否跨simulator均衡未知。

## 具体修改动作

1. 定义`N_candidate`、16 physics/belief samples、4 innovation seeds各自含义，给公式`N_state×N_candidate×N_belief×N_noise×H`。
2. 给50k episode cell表：simulator/task/physics bin/nuisance bin/interactions/episode；按asset和physics interval做group split。
3. 固定1024 subset大小和seed nesting，64必须是1024的prefix以做paired bias；列cache复用与每格训练/规划calls。
4. 将2×2和innovation selection的模型数、训练seed、GPU-hours、validation calls列全；先200 states后根据bias重新计算power/预算。

## Round 08 验收条件

必须给candidate/sample/horizon闭合公式、50k cell/split与1024 subset规模。R8再审查物性OOD是否与视觉外观混淆、真机配重/摩擦/海绵是否能独立操纵。
