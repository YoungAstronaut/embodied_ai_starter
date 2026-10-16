# Round 03 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r02
- File: `proposals/GEO-P3_geometry_confidence/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（信息路径基本合格；repair-based risk target 与三分支部署成本仍需闭合）

## 实际变更核验

r02 已加入 SelectiveNet/Learning-to-Defer 和 generic routers，明确 GT relation 只作 target，给出 2k/10k label 到 env-step 的换算、公平预算及 relation-deletion 判负。现有主结果是 current-feature router 预测三分支 action-regret risk，并锁定 frame-level coverage，而非读取未知 `L_act`。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 几何失败可校准路由直接影响可靠操作。 |
| D2 失败模式清晰度 | 4.5 | 关系错误类型、hard pairs 与 selective routing 明确。 |
| D3 创新性/最近邻 | 4.0 | selective prediction 本身已知；增量是 geometry-failure-type regret routing。 |
| D4 机制因果闭环 | 4.0 | relation repair→branch regret→routing 成链，但 repair 可能离开模型流形。 |
| D5 技术正确性 | 4.0 | action-regret/quantile 比未知 loss 正确；branch risk 和 coverage 单元还需统一。 |
| D6 可观测性/泄漏 | 4.5 | GT relation/outcome 仅 target，student features 与部署一致。 |
| D7 数据可得性 | 4.0 | exact-reset 三分支标签昂贵但预算已量化。 |
| D8 算力/工程 | 4.0 | 标签成本公平；部署可能需同时跑三分支，尚未计全。 |
| D9 可证伪性 | 4.5 | relation deletion、generic router、hard pair 和 coverage-risk 均可判负。 |
| D10 基线强度 | 4.5 | SelectiveNet、defer、通用 confidence 和最近邻均覆盖。 |
| D11 消融充分性 | 4.5 | router/label/branch 组合与 relation deletion 足够。 |
| D12 OOD/真机 | 4.0 | 多失效类型与真机有外效度，需按 detector shift 分层。 |
| D13 复现性 | 3.5 | 缺 relation-repair operator、branch runtime 与 coverage unit 的 schema。 |
| D14 CVPR 契合度 | 4.5 | 视觉几何不确定性与机器人选择性预测契合。 |
| D15 风险/负结果 | 4.5 | generic router 持平即否定几何特异机制，负结论清楚。 |

平均分：**4.23/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10 且关键维未到 4.5，R3 不通过。

## Top 问题与证据缺口

1. **major — repair target 的因果有效性。** 把单个预测 relation 替换成 GT 后，其余 latent/token 仍与错误 relation 共适应；所得“repaired action”可能是 off-manifold artifact，不一定估计该 relation 的可实现干预效应。
2. **major — routing 的部署成本未闭合。** router feature 含 branch action disagreement，就必须先运行多个分支。若三分支均已计算，方法是 reliability selector 而非省算 routing；所有 branch FLOPs/latency 应计入主结果。
3. **technical — coverage 单元可能混淆。** 主 endpoint 固定 frame coverage，但 action regret 是 branch×frame 标签；需说明拒绝/路由一个 frame 时多个 branch 风险如何汇总，并避免用多数容易 branch 稀释危险 branch。

## 具体修改动作

1. 增加 on-manifold repair：用独立 relation editor/decoder 检查重构与 detector consistency；与 random relation、semantically valid wrong relation、full oracle geometry 三档比较。
2. 明确部署策略是否预计算三分支。若是，报告全分支成本并删除 compute-saving 表述；若否，action disagreement 不得作为前置 router feature。
3. 定义 `frame→branch decision→executed action` 的唯一聚合公式，预注册 per-branch 与 per-frame coverage-risk，危险 branch 不得被平均隐藏。
4. 在 detector shift/OOD 下分别校准，并禁止从评测 failure-type metadata 选择 calibration model。

## Round 04 验收条件

- [ ] relation repair 有 on-manifold/置换/placebo 检验，主效应不依赖 artifact。
- [ ] 三分支计算与 router feature 的实际部署顺序、FLOPs 和 p95 latency完整记账。
- [ ] branch risk 到 frame coverage 的聚合公式与最小反例给出。
- [ ] calibration 只用可部署输入，failure-type metadata 仅 evaluator 可见。

