# Round 04 Review — JEP-P3

- Proposal-ID: JEP-P3
- Reviewed-Revision: r03
- File: `proposals/JEP-P3_stochastic_exogenous/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / FATAL-IN-r03**（q-sampled/corrupted e与true-e outcome配对会破坏条件分布分解）

## 实际变更核验

r03 已把ANOVA对象升级为characteristic-RBF kernel distribution embedding，加入mean/variance/mode三个最小例、true-e/q-sampled/q-corrupt 1:1:1训练、固定proposer seed与等权`μ_a`。旧mean-only问题被正面回应，但新增的robustness训练与factorial estimand冲突。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | action×外生随机交互重要。 |
| D2 失败模式清晰度 | 4.5 | XOR/variance/mode反例清楚。 |
| D3 创新性/最近邻 | 4.0 | factorial benchmark+planner增量待证。 |
| D4 机制因果闭环 | 3.0 | robustness batch把错误e与Y配对，破坏`P(Y|a,e)`后再用于mixture planner。 |
| D5 技术正确性 | 3.0 | 条件NLL的统计目标被错误标签污染，functional ANOVA不再对应预注册cells。 |
| D6 可观测性/泄漏 | 4.5 | e label仍只target，非泄漏问题。 |
| D7 数据可得性 | 4.0 | factorial模拟可生成。 |
| D8 算力/工程 | 4.0 | 规模可控但K=4分布估计偏少。 |
| D9 可证伪性 | 4.5 | CoCo/Sawada/non-JEPA/最小例强。 |
| D10 基线强度 | 4.5 | strong stochastic与同目标baseline充分。 |
| D11 消融充分性 | 4.5 | interaction/q/planner/centering全面。 |
| D12 OOD/真机 | 4.5 | held-out cells和真实外生动态贴合。 |
| D13 复现性 | 3.5 | RKHS outcome kernel、empirical embedding与mixed-e loss未定义。 |
| D14 CVPR 契合度 | 4.5 | 随机视觉世界模型/规划契合。 |
| D15 风险/负结果 | 4.5 | 可删JEPA/interaction，保留benchmark。 |

平均分：**4.13/5.00**。D4=3.0、D5=3.0、D6=4.5、D9=4.5；存在公式fatal，R4不通过。

## Fatal 最小反例

令真实条件分布为确定性`Y=e`，`e∈{-1,+1}`均衡。true-e batch会学到`P(Y|e)=δ_e`。若q-sampled e与true outcome独立，有一半样本输入`e'=+1`却target `Y=-1`；对这些样本做条件NLL后，最优解变成`P(Y|e'=+1)=0.5δ_{+1}+0.5δ_{-1}`。于是`f_e`被主动抹平，factorial cell不再表示intervention `e`。q-corrupt同理。该错误正好摧毁主张的`f_e/f_ae`与mixture planning。

## 具体修改动作

1. 条件predictor/ANOVA只用true-e cell训练，保持`P(Y|a,e)`estimand。
2. learned-q部署鲁棒性放到独立marginal objective：`-log∫p(Y|a,e)q(e|h)de`或planner distillation；不能把sampled错误e当true条件标签。
3. 若使用latent e无label数据，采用变分边缘化/importance weighting，并保持有label factorial shard独立。
4. 为混合SE(3)/contact/collision outcome定义product characteristic kernel与bandwidth；K=4需做4/8/16/32 embedding/MMD稳定性。

## Round 05 验收条件

- [ ] conditional cell predictor不再接收与Y不匹配的sampled/corrupt e。
- [ ] q鲁棒性通过正确边缘化或planner层目标实现。
- [ ] `P(Y|a,e)`、`q(e|h)`、`∫p q`三条loss/梯度路径分离。
- [ ] mixed outcome kernel与cell sample-size收敛可复算。

