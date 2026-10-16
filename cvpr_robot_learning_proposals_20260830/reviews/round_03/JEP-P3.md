# Round 03 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r02
- File: `proposals/JEP-P3_stochastic_exogenous/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（R1 independence fatal 持续解除；随机分布上 ANOVA 的作用对象尚不明确）

## 实际变更核验

r02 已明确 ANOVA/两 latent 不算创新，逐公式比较 CoCo 并要求同 4×4×K 数据运行；加入连续 `μ_train(e)` centering、q 的 NLL/ECE/CRPS/coverage、`e-target→q→mixture planner` 路径与 non-JEPA+同 objective。旧 independence loss 已删除，并加入 `Y=a·e` 最小反例。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 任务相关外生动态会混淆 action effect，直接影响规划。 |
| D2 失败模式清晰度 | 4.5 | XOR conveyor 与 action×exo held-out cell 是清楚反例。 |
| D3 创新性/最近邻 | 4.0 | functional ANOVA/stochastic WM 已知；增量是机器人 factorial benchmark+planner 后果。 |
| D4 机制因果闭环 | 4.0 | factorial target→q/predictor→mixture utility→ranking 基本闭合。 |
| D5 技术正确性 | 3.5 | 公式对 predictive mean 写 ANOVA，却用分布 NLL；方差/模式交互的分解对象不明确。 |
| D6 可观测性/泄漏 | 4.5 | e intervention label 只作 target，部署只从 history估 q。 |
| D7 数据可得性 | 4.0 | 4×4×K factorial 可生成，15k groups 成本可量化。 |
| D8 算力/工程 | 4.0 | mixture samples和全基线较重但有 MVP 阶段。 |
| D9 可证伪性 | 4.5 | CoCo/Sawada/strong stochastic/non-JEPA 同数据均能否定主张。 |
| D10 基线强度 | 4.5 | 最近邻和同目标非品牌 backbone 完整。 |
| D11 消融充分性 | 4.5 | main/interaction/stochastic/q/centering/planner均可分解。 |
| D12 OOD/真机 | 4.5 | held-out action×e、速度/相位与 conveyor/第二臂真机直接对应。 |
| D13 复现性 | 3.5 | 缺 distributional ANOVA 参数化、q/p sample 数与 synchronization schema。 |
| D14 CVPR 契合度 | 4.5 | 视觉随机动力学与 manipulation planning 契合。 |
| D15 风险/负结果 | 4.5 | 可删除 JEPA 或 interaction objective，保留 benchmark/失效边界。 |

平均分：**4.23/5.00**。D3=4.0、D5=3.5、D6=4.5、D9=4.5；round<10 且 D5 未过硬门槛，R3 不通过。

## Top 问题与证据缺口

1. **major/technical — ANOVA 分解对象不一致。** 公式 `Y=μ+f_a+f_e+f_ae+ε` 像条件均值分解，训练却是 `-log p(Y|s,a,e)`。若 action×e 主要改变方差、mode weight 或 contact发生概率，mean ANOVA 可以为零而 ranking 仍强依赖 interaction。
2. **major — teacher forcing 到 learned q 的分布移位。** predictor 训练时条件于真 e label，部署条件于 q samples；若 q 校准稍差，planner gap可很大。当前只设 oracle-q gap阈值，缺 posterior-sampled training/robustness。
3. **technical — intervention measure 的 action 侧也需固定。** 连续 e 已定义 `μ_train(e)`，但局部 candidate actions 也可能随 proposer/state变化；`μ_a` 若每组不同，跨 state 比较 `f_a/f_ae` 需明确只评 prediction而非分量值可比。

## 具体修改动作

1. 明确 ANOVA 作用于哪些 distribution parameters：例如 mixture logits/means/scales，或用 energy-score/kernel embedding 做 distributional functional decomposition；分别评 mean、variance、mode interaction。
2. 训练时加入 posterior-sampled e、q corruption 和 oracle-e/learned-q 三角比较，确保 predictor 不只适配 one-hot teacher label。
3. 固定局部 `μ_a×μ_e` 的定义、candidate generator 和 held-out-cell规则；分量只在同 measure 下比较。
4. 加纯 variance-interaction 最小例，要求 additive-mean model失败而 distributional interaction恢复 ranking。

## Round 04 验收条件

- [ ] stochastic predictive distribution 上的 ANOVA 作用对象与 identifiability约束明确。
- [ ] mean、variance、mode-probability interaction 有独立最小例与指标。
- [ ] teacher-e 到 learned-q 的训练/部署 shift 有 robustness 方案和 gap阈值。
- [ ] action/exo intervention measure 固定且不随 test distribution 重定义。

