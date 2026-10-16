# Round 06 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r05
- File: `proposals/WAM-P3_hidden_physics_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已锁定第2次被动交互后的 normalized action regret，最强比较者由 Robot-Factored+PEARL/RMA 与 generic recurrent mixture 在 validation 选择，并共享 deploy fields、64 samples、CVaR planner；predictive MMD 也已标准化。R5 endpoint/fairness 主缺口基本解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 隐动力学适应直接影响接触控制。 |
| D2 失败模式清晰度 | 4.5 | dynamics 与 controller/vision/contact nuisance 可分层。 |
| D3 创新性/最近邻 | 4.0 | PEARL/RMA/system-ID 强，增量在 nominal-realization predictive belief。 |
| D4 机制因果闭环 | 4.5 | residual→belief update→CVaR ranking 闭合。 |
| D5 技术正确性 | 4.5 | predictive equivalence 与 CVaR sampling口径正确。 |
| D6 可观测性/泄漏 | 4.5 | θ 仅分层，t=0 泄漏检查明确。 |
| D7 数据可得性 | 4.0 | 两模拟器可做，64/1024 sampling昂贵。 |
| D8 算力/工程 | 4.0 | 共享64 calls可比，reference成本需实测。 |
| D9 可证伪性 | 4.5 | regret、nuisance ratio 和 oracle边界明确。 |
| D10 基线强度 | 4.0 | winner合理，但 RMA/PEARL 训练信息与 posterior能力未对齐。 |
| D11 消融充分性 | 4.0 | nuisance factorial强，核心 factorization×belief 未完整正交。 |
| D12 OOD/真机 | 4.5 | hidden-dynamics OOD 与真机外测自然。 |
| D13 复现性 | 4.5 | fields/history/samples/planner合同清楚。 |
| D14 CVPR契合度 | 4.5 | 视觉预测适应与机器人控制兼具。 |
| D15 风险/负结果 | 4.5 | 传感不可辨识/容量解释均可判负。 |

平均分：**4.33/5.00**。D3/D10/D11 未达关键门槛；round<10，不通过。

## Top 问题与证据缺口

1. **RMA/PEARL 的“最公平可用信息”仍不够可复现。** RMA 常含 privileged teacher/estimator 路径，PEARL posterior 的上下文/reward字段也可能超出本法 deploy fields；必须逐字段拆开 native 与 deploy-equal 版本。
2. **当前 2×2×2×2 是数据干扰因素，不是方法贡献消融。** 它能检验归因，但不能隔离 nominal realization factorization 与 distributional belief 各自贡献。
3. **generic recurrent mixture 可能同时改变容量、posterior family和 factorization。** 若不参数/likelihood匹配，`差≤2%来自容量`的判负也无法解释反方向结果。

## 具体修改动作

1. 加主方法 2×2：`dynamics representation {raw recurrent, nominal-realization residual}` × `adaptation {point context, calibrated distributional belief}`；四格同 encoder/decoder、latent dim、samples、planner、loss 数和参数±5%。
2. PEARL/RMA 各给 native 与 deploy-equal adapter；表中列 training privileged fields、deployment fields、context horizon、posterior samples、reward/contact labels。
3. validation winner 需在同一冻结 t=2 primary 上选，不能跨 future NLL/success 多指标挑选；选择后 test 只比较一次。
4. 把 innovation family `i.i.d./AR1/state-dependent`变为所有强基线共享的 decoder option或单独容量对照，避免本法独享更强随机模型。

## Round 07 验收条件

需补 representation×belief 2×2、PEARL/RMA native/deploy-equal 信息表、统一 posterior/innovation capacity 与 validation selection rule；R7 同时给64/1024采样的 pilot bias/runtime。
