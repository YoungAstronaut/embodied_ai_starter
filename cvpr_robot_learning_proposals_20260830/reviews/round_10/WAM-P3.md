# Round 10 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r09
- File: `proposals/WAM-P3_hidden_physics_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 已把主张收缩为 functional predictive belief，不声称真实质量/摩擦参数识别；部署相同的 PEARL/RMA/generic recurrent mixture 位于首列，Robot-Factored residual只是可观测输入契约。该边界避开CoCo的一般action controllability。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 隐动力学导致重复接触失败。 |
| D2 失败模式清晰度 | 4.5 | 相同视觉/命令、不同后果明确。 |
| D3 创新性/最近邻 | 4.5 | action-realization residual下的predictive-equivalence边界清楚。 |
| D4 机制因果闭环 | 4.5 | nominal→residual→belief→planner闭合。 |
| D5 技术正确性 | 4.5 | fractional CVaR、MMD/W1和noise过程正确。 |
| D6 可观测性/泄漏 | 4.5 | 参数/logger仅stratify/eval。 |
| D7 数据可得性 | 4.0 | 物性×nuisance cells生成成本较高。 |
| D8 算力/工程 | 4.0 | nested K/reference账目清楚但昂贵。 |
| D9 可证伪性 | 4.5 | t=2 regret与held-out-action shift会否定claim。 |
| D10 基线强度 | 4.5 | PEARL/RMA/generic winner同部署字段。 |
| D11 消融充分性 | 4.5 | raw/residual×point/distributional 2×2。 |
| D12 OOD/真机 | 4.0 | physics drift真机仅secondary。 |
| D13 复现性 | 4.5 | sample counts、PIT/ACF、manifest完整。 |
| D14 CVPR契合度 | 4.5 | 视觉与控制残差融合问题明确。 |
| D15 风险/负结果 | 4.5 | 可降级为predictive adaptation/system-ID诊断。 |

平均分：**4.40/5.00**；关键维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **deploy-equal generic/PEARL-RMA持平：** 删除新belief方法，保留residual protocol。
- **t=2 regret不改善：** 表征/校准结果不能替代决策claim。
- **真机physics drift失败：** 不声称物性迁移，报告guard/fallback条件。

## 未决非致命风险与最终修改

innovation residual仍可能只编码视觉/接触定位误差。r10 必须加入 innovation-shuffle、wrong-controller 与 held-out-action 三个负控的联合验收行，并明确任一shortcut probe成功即删functional-belief claim；追加 round_10/r10 log。当前只有9次refine。
