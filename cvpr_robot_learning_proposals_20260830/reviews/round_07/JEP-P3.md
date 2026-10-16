# Round 07 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r06
- File: `proposals/JEP-P3_stochastic_exogenous/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已将non-JEPA/MDN-RSSM纳入winner，拆出deploy 2×2与oracle triangle，并加入observational/factorial×generic/ANOVA 2×2、claim ladder和K-pilot gate。R6 comparator缺口已响应，actual K-pilot=0明确。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | action×外生交互重要。 |
| D2 失败模式清晰度 | 4.5 | mean/variance/mode反例强。 |
| D3 创新性/最近邻 | 4.0 | 组合创新需数据×objective验证。 |
| D4 机制因果闭环 | 4.5 | factorial→q mixture→ranking闭合。 |
| D5 技术正确性 | 4.5 | 条件/边缘梯度路径稳定。 |
| D6 可观测性/泄漏 | 4.5 | true-e仅target。 |
| D7 数据可得性 | 3.5 | ExoManip-12与history/q数据尚未pilot。 |
| D8 算力/工程 | 3.5 | K账文字矛盾且未乘H/模型网格。 |
| D9 可证伪性 | 4.5 | claim ladder强。 |
| D10 基线强度 | 4.5 | non-JEPA same-objective已纳入。 |
| D11 消融充分性 | 4.5 | 两个2×2与oracle triangle充分。 |
| D12 OOD/真机 | 4.0 | 外生shift自然，真机仍外测。 |
| D13 复现性 | 4.0 | measure/kernel细，data/compute manifest欠完整。 |
| D14 CVPR契合度 | 4.5 | 视觉JEPA与动态操作契合。 |
| D15 风险/负结果 | 4.5 | 可逐层删除贡献。 |

平均分：**4.27/5.00**。D3/D7/D8/D13未达门槛；round<10，不通过。

## 数据/资源攻击面

1. full `15k×16×4=960k outcomes`与额外`500×16×(8+16+32)=448k`均正确；但R6称“500-group K4/8/16/32的448k”，若包含K4应为480k。需明确448k只是额外K8/16/32，K4复用full subset。
2. outcome不是env step；全部还要乘rollout horizon H，H未冻结。生成到factorial current state的history cost与q(e|h)监督序列也未计。
3. 两个2×2、5类winner、native/adapter和多seed训练共享outcome但不共享全部GPU forward/optimizer；8×A100×10天缺模型网格推导。
4. 500-group K calibration subset必须train-only且按task/state family隔离，否则用其选择K会影响test。15k groups在12 tasks、4类场景的cell分配未列。

## 具体修改动作

1. 改写总账：full K4=960k；subset额外K8/16/32=448k；总unique outcomes=1.408M，env steps=`×H`，并列history-to-state成本。
2. 冻结H、每outcome bytes、q-history长度与生成成本；K4必须是K32 nested prefix。
3. 列model-grid×seed GPU-hours/forward calls；MVP只跑最小必要格，进入full前由K误差/throughput/power三gate共同决定。
4. 给task×scenario×action/e cell表和train/calibration/test group split；K subset只来自train/calibration，绝不触碰test shift。

## Round 08 验收条件

需修正448k措辞、闭合H/history/model-grid总账与cell split。R8再检查外生OOD是否可在真机独立操纵，以及q失配下的安全风险。
