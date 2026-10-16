# Round 02 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r01
- File: `proposals/GEO-P3_geometry_confidence/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（无 fatal；创新性仍需证明不是通用 branch selection）

## 实际变更核验

r01 已删除未知 `L_act`，以 three-branch exact-reset action regret 训练可部署 risk/quantile；coverage 统一为 frame geometry-routing，关系 target 改为 action-regret bad-event，并加入两类 hard pairs与同 label/FLOPs 表。R1 技术问题实质修复。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 几何错误导致负迁移是实际部署问题。 |
| D2 失败模式清晰度 | 4.5 | 大几何错但动作不变/小错却动作翻转的交叉例强。 |
| D3 创新性/最近邻 | 4.0 | 相对 VLA calibration/UAOR 的 target 与粒度差异成立；尚未找到完全等价工作，但通用 expert routing 风险仍大。 |
| D4 机制因果闭环 | 4.0 | relation repair→branch regret→frame route→success；branch outcome target 成本/偏差仍可能主导。 |
| D5 技术正确性 | 4.0 | 部署公式可计算；`min q>ε` 时强制 RGB/stop 与 argmin quantile 的一致性需 R4。 |
| D6 可观测性/泄漏 | 4.5 | motion仅t−1:t、无伪多视角、outcome仅target。 |
| D7 数据可得性 | 4.0 | 2k/10k label budgets、hard pairs、split 清楚。 |
| D8 算力/工程 | 4.0 | single-model default、FLOPs/latency明确；三分支全 forward 是否真≤1.25×待证。 |
| D9 可证伪性 | 4.5 | UAOR/VLA-calibration/oracle/hard-pair判负齐全。 |
| D10 基线强度 | 4.5 | 直接、简单、ensemble、oracle 和同标签/算力均有。 |
| D11 消融充分性 | 4.5 | hard-pair/input/labels/shift/router/capacity全拆。 |
| D12 OOD/真机 | 4.0 | 四轴五级+三真机任务，功效未给。 |
| D13 复现性 | 3.5 | risk/coverage契约已清楚；仍缺schema/commit/seed/artifact。 |
| D14 CVPR 契合度 | 4.0 | 几何可靠性视觉分析明确。 |
| D15 风险/负结果 | 4.5 | 跨域校准失效与 error atlas 有强价值。 |

平均分：**4.17/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；未达 hardened gate/mean。

## Top 问题

1. **major — 科学新意可能退化成通用 mixture-of-experts router**：三支 action regret 校准并不专属几何；relation `B_ij` 若删除后不影响 routing，标题中的 geometry 只剩 branch 名。
2. **major — 最近邻表只覆盖 VLA 内部**：需补 selective prediction/risk-coverage、learning-to-defer、mixture router 的机制邻域，并说明为何 geometry hard pairs 产生新视觉结论。
3. **major — 三支标签获取代价可能使“轻量校准”叙事失真**：每 snapshot 三次 short-horizon execution 比 Platt/action entropy 多得多，必须按环境交互成本匹配而不只 episode count。

## 具体修改动作

1. 增加 generic learned branch router（只读 shared visual/action features）、learning-to-defer/selective prediction baseline；做无 relation bad-event 的 regret-only router。
2. 预注册：relation calibrator 删除若差≤2pp，则收缩为通用 branch selection，不宣称几何专属机制。
3. 公平预算增加环境 rollout/label seconds，而不只 calibration episode 数；对 UAOR/VLA calibration 提供等交互预算与等标签预算两套。
4. 在 R3 画清 `B_ij` teacher 使用 oracle repair 的生成路径，排除未来/完整几何泄漏到 router features。

## Round 03 验收条件

- [ ] generic router、regret-only router、geometry-aware router 三者正交比较。
- [ ] 最近邻表补 selective prediction/learning-to-defer 并保持 VLA calibration/UAOR。
- [ ] label/environment-interaction cost 公平性明确。
- [ ] `B_ij` oracle repair 的 target-only 信息路径可逐字段审计。

