# Round 04 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r03
- File: `proposals/GEO-P3_geometry_confidence/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / REVISE**（repair/cost/aggregation已闭合；fixed-coverage操作规则仍缺）

## 实际变更核验

r03 已加入 independent editor/decoder 的 on-manifold gate与random/valid-wrong/oracle placebo，明确三分支全预计算、方法是 reliability selector而非省算，并把主指标唯一聚合为selected branch的frame risk/coverage。R3问题均有实质修改。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 高置信错误几何的部署风险重要。 |
| D2 失败模式清晰度 | 4.5 | 四类corruption与关键关系hard pair明确。 |
| D3 创新性/最近邻 | 4.0 | geometry-specific regret router区别尚待实证。 |
| D4 机制因果闭环 | 4.5 | repair target→risk head→selected action链完整。 |
| D5 技术正确性 | 4.0 | branch risk定义正确；固定90% coverage如何由部署规则实现未定义。 |
| D6 可观测性/泄漏 | 4.5 | GT relation/outcomes仅target/evaluator。 |
| D7 数据可得性 | 4.0 | label env-step预算闭合。 |
| D8 算力/工程 | 4.0 | 三分支成本诚实计入。 |
| D9 可证伪性 | 4.5 | generic/regret-only/placebo/relation deletion强。 |
| D10 基线强度 | 4.5 | defer/selective/UAOR/通用confidence充分。 |
| D11 消融充分性 | 4.5 | geometry项、cost、cheap router、repair四档齐全。 |
| D12 OOD/真机 | 4.0 | corruption轴与真机外测合理。 |
| D13 复现性 | 4.0 | 聚合和schema改善；coverage阈值算法缺失。 |
| D14 CVPR 契合度 | 4.5 | 几何置信/选择性视觉机器人契合。 |
| D15 风险/负结果 | 4.5 | 通用defer持平即可否定geometry-specific claim。 |

平均分：**4.30/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10 且 D3/D5未达硬门槛，R4不通过。

## Top 问题与技术证据

1. **major — 90% geometry coverage缺少部署可实现的阈值规则。** `argmin(v_k+λCost_k)`给一个route，但不会自然保证full+coarse恰为90%；若在测试集后调λ达到90%，AURC会有look-ahead偏差。
2. **major — q与v可能给冲突排序。** 选择用quantile `v_k`，fallback用event probability `q_k`；两head独立训练时可出现`v_full<v_RGB`但`q_full≫q_RGB`，需要预注册一致性/冲突处理。
3. **minor — on-manifold是必要非充分。** decoder重构通过只说明token可解码，不证明policy训练分布内；placebo差异应作为主验收而非附加图。

## 具体修改动作

1. 用独立calibration split拟合coverage约束的threshold/Lagrange multiplier并冻结；测试只评一次。报告coverage偏差CI与完整risk-coverage曲线。
2. 定义唯一decision risk，例如同一预测分布同时导出quantile与tail probability；给三branch冲突最小例和fallback优先级。
3. on-manifold validity同时检查editor likelihood/density和policy latent distance；placebo effect低于阈值即禁用B target。
4. fixed coverage下成本也要报告，不能以coverage匹配隐藏三分支预计算。

## Round 05 验收条件

- [ ] 90% coverage阈值只在calibration split拟合并冻结，test无回调。
- [ ] q/v来自一致风险分布或有确定冲突规则。
- [ ] repair density/policy-latent与placebo共同构成有效性门槛。
- [ ] coverage、risk、cost三者同时报告。

