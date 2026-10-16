# Round 08 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r07
- File: `proposals/JEP-P3_stochastic_exogenous/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已纠正full K4/额外448k/总1.408M，冻结H16与history8，补nested prefix、model-grid和task/scenario group split；R7资源算术问题解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 外生动态归因重要。 |
| D2 失败模式清晰度 | 4.5 | 三类分布反例强。 |
| D3 创新性/最近邻 | 4.0 | benchmark+interaction组合待证。 |
| D4 机制因果闭环 | 4.5 | factorial→q→mixture ranking闭合。 |
| D5 技术正确性 | 4.5 | measure/资源/梯度一致。 |
| D6 可观测性/泄漏 | 4.5 | e标签target-only。 |
| D7 数据可得性 | 4.0 | ExoManip可生成。 |
| D8 算力/工程 | 4.0 | 22.5M+grid可行但重。 |
| D9 可证伪性 | 4.5 | claim ladder完整。 |
| D10 基线强度 | 4.5 | non-JEPA same-objective强。 |
| D11 消融充分性 | 4.5 | 两2×2+oracle triangle充分。 |
| D12 OOD/真机 | 3.5 | μshift清楚，真机协议与安全缺失。 |
| D13 复现性 | 4.5 | cell/measure/seed具体。 |
| D14 CVPR契合度 | 4.5 | 动态视觉世界模型契合。 |
| D15 风险/负结果 | 4.5 | 数据/ANOVA/JEPA可逐层删除。 |

平均分：**4.33/5.00**。D3/D12未达门槛；round<10，不通过。

## OOD/真机攻击面

1. held-out action×e cells是组合泛化，不等于外推OOD；`μ_shift(e)`的speed/phase范围外推才是distribution shift，需分表。
2. learned q在μshift下可能严重失校；primary仍是held-out cells，OOD success secondary。若q失败，不能用oracle-q结果救部署claim。
3. 真机仅写“外部效度/两月完成”，没有任务/trial/e measurement/方法随机化。传送带和其他手臂共享空间还有明显安全风险。
4. real e encoder/belt phase/other-arm policy label只能评测，不能进入q；需要logger/model-camera隔离及fallback。

## 修改与R9验收

1. 三层报告：ID cells、combinatorial held-out cells、extrapolative μshift；分别给q calibration和ranking regret。
2. μshift下q coverage/ECE超阈值即禁用mixture planning并触发conservative baseline；oracle-q只上界。
3. 真机定义≥3 tasks×root blocks（belt phase/speed、rolling object、other-arm policy），e由独立encoder/logger评测，method顺序随机。
4. other-arm/obstacle实验用速度限制、空间shield、collision monitor和emergency stop；报告fallback/abstain与conditional success。

R9需把贡献层级写成balanced benchmark→interaction objective→JEPA可选；若non-JEPA持平，标题和摘要都必须删除JEPA主张。
