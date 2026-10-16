# Round 06 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r05
- File: `proposals/WAM-P1_occlusion_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已修正 miss 不映射 unknown，并把 ≥2s identifiable/partial 的 permutation-invariant log score 设为唯一 primary，固定 0.5/0.5 宏权重、同轨迹 cluster/power 与 success 降级。R5 的指标语义冲突已解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 长遮挡身份错误是对象操作真实痛点。 |
| D2 失败模式清晰度 | 4.5 | identifiable/partial/symmetric 三档明确。 |
| D3 创新性/最近邻 | 4.0 | JPDA/MHT 已有多假设，增量在 referent/contact/control 联合。 |
| D4 机制因果闭环 | 4.5 | 联合后验→边缘控制完整。 |
| D5 技术正确性 | 4.5 | `p(R,Z,D)` 与 proper score 已修正。 |
| D6 可观测性/泄漏 | 4.5 | evaluator shard 与 deploy anchor 分开。 |
| D7 数据可得性 | 4.0 | simulator 可生成三档但 proof 成本不低。 |
| D8 算力/工程 | 4.0 | M≤4 可做，50k episode 有工作量。 |
| D9 可证伪性 | 4.5 | score、switch、success 分层判负。 |
| D10 基线强度 | 4.5 | JPDA+same WAM 是危险直接基线。 |
| D11 消融充分性 | 4.0 | 删除项多，但 JPDA evidence 与 control marginalization 未正交。 |
| D12 OOD/真机 | 4.0 | 真机模板合理，实例数/遮挡域仍有限。 |
| D13 复现性 | 4.5 | posterior 单测、Ω 与匹配清楚。 |
| D14 CVPR契合度 | 4.5 | 视觉跟踪、WAM与控制结合自然。 |
| D15 风险/负结果 | 4.5 | 不可辨识边界与 calibration-only 降级诚实。 |

平均分：**4.33/5.00**。D3=4.0、D11=4.0；round<10，不通过。

## Top 问题与证据缺口

1. **JPDA baseline 的能力边界未冻结。** 若 `JPDA+same WAM+language anchor`只做视觉关联，而本法同时有 learned action/contact likelihood、unknown/residual、referent posterior marginal control，则一次比较混了至少三项。
2. **最危险的 baseline 是“完整 JPDA posterior + 同一 marginal controller”。** 若该 baseline 拿相同 detector、motion/action/contact likelihood和 referent candidates 后持平，论文只剩 benchmark；正文现在没有承诺跑这个近同构版本。
3. **active-look 2×2 与主 passive claim 无关。** R6 需要的是 evidence model 与 control rule 的 2×2，而非是否主动观察。

## 具体修改动作

1. 冻结四级 JPDA ladder：视觉+MAP、视觉+posterior marginal、视觉/action/contact+MAP、视觉/action/contact+posterior marginal；最后一格是最强近同构 comparator，所有格同 M、unknown/residual、pruning、WAM、controller calls。
2. 以 `evidence {visual-motion, +action/contact}` × `decision {MAP identity, posterior-marginal}` 为主 2×2；分别在 primary log score 与 passive success 上估主效应/交互。
3. filter vs transformer 只允许相同 likelihood family/latent dimension/参数±5%；否则表示容量不能解释为 Bayesian belief 贡献。
4. OA/POT/3D-ALP 代码不可得时同时报告正文忠实重实现和“加同 posterior head”适配版，不把缺失官方实现当优势。

## Round 07 验收条件

正文需给 JPDA ladder 的逐字段 contract、2×2、同一 marginal controller 接口和每格运行/内存；R7 再补 generator 中三种 stratum 的实际比例与 proof failure 漏斗。
