# Round 04 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r03
- File: `proposals/WAM-P1_occlusion_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / FATAL-IN-r03**（新assignment公式不能更新referent posterior）

## 实际变更核验

r03 确实删除 `A_mjℓ_mj` 的重复计似然，给出7个合法assignments的2-track/2-detection枚举，补Ω、unknown/residual/miss/false、symmetric-orbit proper score，并分开deploy anchor与GT evaluator。修改是实质的，但新公式引入了更根本的posterior错误。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 长遮挡referent不确定性重要。 |
| D2 失败模式清晰度 | 4.5 | 可辨识分层和identity swap明确。 |
| D3 创新性/最近邻 | 4.0 | action/contact likelihood+control增量仍可能成立。 |
| D4 机制因果闭环 | 2.5 | 写出的assignment posterior无法产生候选referent权重更新。 |
| D5 技术正确性 | 2.5 | `Σ_jA_mj+A_m,miss=1`，故`w_m^+=1`；prior weights也在归一化中抵消。 |
| D6 可观测性/泄漏 | 4.5 | GT/evaluator shard隔离仍合格。 |
| D7 数据可得性 | 4.0 | benchmark可生成。 |
| D8 算力/工程 | 4.0 | M≤4计算可控。 |
| D9 可证伪性 | 4.5 | calibration/symmetric/JPDA组合判负强。 |
| D10 基线强度 | 4.5 | 经典tracker与WAM组合充分。 |
| D11 消融充分性 | 4.5 | likelihood、M、controller、active/passive均覆盖。 |
| D12 OOD/真机 | 4.0 | 真机同类实例合理。 |
| D13 复现性 | 3.5 | 有单测意图但测试只验assignment和为1，没验referent posterior正确。 |
| D14 CVPR 契合度 | 4.5 | 视觉跟踪与控制契合。 |
| D15 风险/负结果 | 4.5 | 对称不可辨识边界价值高。 |

平均分：**4.03/5.00**。D4=2.5、D5=2.5、D6=4.5、D9=4.5；存在公式fatal，R4不通过。

## Fatal 证明

对每个track m，合法assignment中它必然要么匹配某个detection、要么miss，因此按定义
`Σ_j A_mj + A_m,miss = Σ_z p(z|D)=1`。
所以正文的 `w_m^+=Σ_jA_mj+A_m,miss` 对每个m恒等于1，不能表达referent identity belief。

同时 `\tilde p(z)` 对每个assigned或missed track都乘一次 `w_m^-`；每个z都包含全部track，故 `∏_m w_m^-` 是z无关常数，在归一化中完全消掉。7-assignment“和为1”单测不会发现这两个错误。

## 具体修改动作

1. 显式区分 referent变量 `R∈Ω` 与多目标assignment `Z`，定义 `p(R,Z,D)`；最终 `w_m^+=Σ_z p(R=m,Z=z|D)`，而不是track association row sum。
2. 若不需要完整JPDA，可用规范mixture update `w_m^+∝w_m^-[p_miss+Σ_j p(d_j|R=m)]`，再对Ω归一；一对一排他时再引入Z。
3. miss不得自动映射unknown：短时漏检通常应保留原candidate identity质量；unknown/none是另一个referent hypothesis。
4. 单测必须用非均匀prior（如0.8/0.2）和可辨识likelihood，验证posterior向正确candidate移动、对称likelihood保持prior/按定义趋均匀。

## Round 05 验收条件

- [ ] R与Z分离，`w^+`归一且在非平凡例中发生正确变化。
- [ ] prior权重不在assignment归一中抵消。
- [ ] miss、unknown、residual的语义互不偷换。
- [ ] 数值单测同时验posterior值，不只验assignment概率和为1。

