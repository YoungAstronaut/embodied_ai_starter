# Round 10 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r09
- File: `proposals/GEO-P3_geometry_confidence/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 把不可删除对象改为 LOFO Geometry Reliability Atlas：三branch outcome、repair validity/noise、coverage/route/fallback同表；明确不是省算方法。UAOR/VLA calibration 仍未覆盖 relation-failure-specific action regret，因此窄协议的新颖边界成立。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 错几何高置信风险重要。 |
| D2 失败模式清晰度 | 4.5 | 反光/遮挡/动态等类型化。 |
| D3 创新性/最近邻 | 4.5 | LOFO Atlas超出通用confidence/router。 |
| D4 机制因果闭环 | 4.5 | bad-event regret→校准→route闭合。 |
| D5 技术正确性 | 4.5 | frozen coverage与regret CDF一致。 |
| D6 可观测性/泄漏 | 4.5 | GT relation只作target/eval。 |
| D7 数据可得性 | 4.0 | repair与corruption rollouts昂贵。 |
| D8 算力/工程 | 4.0 | 三branch全算成本已诚实计入。 |
| D9 可证伪性 | 4.5 | relation deletion/valid-wrong/placebo可判负。 |
| D10 基线强度 | 4.5 | pooled/regret-only同预算校准。 |
| D11 消融充分性 | 4.5 | risk target×calibrator完整2×2。 |
| D12 OOD/真机 | 4.0 | LOFO主线、真机只secondary。 |
| D13 复现性 | 4.5 | splits、coverage CI与成本清楚。 |
| D14 CVPR契合度 | 4.5 | reliability atlas是视觉系统贡献。 |
| D15 风险/负结果 | 4.5 | router失败仍保留Atlas。 |

平均分：**4.37/5.00**；关键维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **generic/regret-only持平：** 删除relation-aware router claim，Atlas仍比较几何失效类型。
- **repair acceptance/noise不达标：** 删除repair branch，只保留reject/fallback评估。
- **OOD/真机coverage失效：** 不宣称部署校准，报告LOFO coverage break和条件化结果。

## 未决非致命风险与最终修改

route/fallback条件均值可能掩盖大量repair attempts。r10 必须在主表固定报告 attempted/accepted/selected 三个分母、每branch fallback率和总pipeline latency，并加入 round_10/r10 log。当前9次refine，生命周期门槛未过。
