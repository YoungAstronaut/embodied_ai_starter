# Round 01 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r00
- File: `proposals/GEO-P3_geometry_confidence/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / REVISE**（round<10；当前无不可修复 fatal flaw）

## 文件变更核验

首轮核对确认 r00 已把总体 VLA confidence 与几何证据置信度分开，给出三路 router、GeometryCorrupt、选择性指标、等 FLOPs controls 和非安全声明。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 错误高置信几何会让融合策略劣于 RGB，是部署相关问题；尚无各 corruption 的基线退化先验。 |
| D2 失败模式清晰度 | 4.0 | 透明/高光/遮挡/运动/视角分轴且 exact-reset；“关系误差”与 action failure 的映射仍泛。 |
| D3 创新性/最近邻 | 4.0 | 区分 UAOR、总体 VLA calibration 和 always-geometry；选择性几何路由的精确最近邻仍需 R2 搜索。 |
| D4 机制因果闭环 | 3.5 | 有坏几何拒绝、oracle/error gate 与延迟约束；未定义关系级拒绝如何聚合为 episode action 决策。 |
| D5 技术正确性 | 3.0 | 推理时 `L_act(k)` 不可知，RGB fallback 也没有 geometry error；约束优化式不能按现文部署。single-view photometric residual 来源含混。 |
| D6 可观测性/泄漏 | 4.0 | GT depth/pose/future track 仅 target；当前增强可部署。motion/跨视图统计所需历史/视角未完整列出。 |
| D7 数据可得性 | 3.5 | exact-reset corruption 和真机物体可得；GT relation-error 定义、校准 split、域转移标签成本未写。 |
| D8 算力/工程 | 3.5 | 预计算、两 backbone、延迟/FLOPs 均有；多增强/多层实时预算与 RGB/geometry 分支缓存不具体。 |
| D9 可证伪性 | 4.0 | AURC/ECE/ID/latency 和 UAOR/oracle gap 有阈值；90% coverage 的动作语义未定义。 |
| D10 基线强度 | 4.0 | action entropy、MC-dropout、ensemble、oracle/random reject 齐全并考虑 FLOPs。 |
| D11 消融充分性 | 4.0 | 输入、calibrator、fallback、epsilon、ensemble、capacity 均拆；缺校准数据量/shift 与误拒绝代价。 |
| D12 OOD/真机 | 4.0 | 四轴五级与透明/金属/遮挡真机；真实动态物和试验数/功效不明。 |
| D13 复现性 | 3.0 | 有指标和预算，无 corruption parameter schema、calibration protocol、commit、seed/artifact 清单。 |
| D14 CVPR 契合度 | 4.0 | 视觉几何可靠性/校准与动作影响紧密结合。 |
| D15 风险/负结果 | 4.0 | 明确 ensemble 成本、domain drift、50-shot recalibration 和 error atlas 负产出。 |

平均分：**3.77/5.00**。关键门槛：D3=4.0、D5=3.0、D6=4.0、D9=4.0；未达 hardened gate。

## Top 问题

1. **major — router 目标在部署时不可计算**：`argmin L_act(k)` 使用未知动作损失；对 RGB fallback 施加 geometry-error chance constraint 也无统一事件空间。
2. **major — coverage 定义不成立**：关系级接受率、frame-level geometry 使用率和 episode selective success 混在一起；90% coverage 下比较可能通过改变拒绝粒度作弊。
3. **major — 几何误差未与动作相关性分开**：全局 depth/pose 误差低不代表 task-relevant relation 正确，calibrator 可能回到普通几何 benchmark，而不是“何时融合会害动作”。

## 最近邻冲突与证据缺口

- [Confidence Calibration in VLA 2507.17383v2](https://arxiv.org/abs/2507.17383) 已提供 prompt ensemble/action-wise Platt；必须在相同标签预算下比较。
- [UAOR 2602.18020v2](https://arxiv.org/abs/2602.18020) 以 action entropy 触发 observation reinjection；仅“gate 变量不同”不够，需 paired disagreement cases。
- [VGA 2604.12908v2](https://arxiv.org/abs/2604.12908) / [GAM 2606.17046v2](https://arxiv.org/abs/2606.17046) 的多层几何特征是否已有 confidence/reliability 信号尚未正文级核完。

## 必须修改的动作

1. 把 router 写成可部署的决策规则：预测每个分支的**action regret/失败风险**或使用 geometry bad-event 的阈值，不得出现未知 `L_act`；说明三路输出如何训练。
2. 分别定义 relation coverage、frame routing coverage、episode coverage 和对应 risk；主终点选择一个，禁止跨粒度 AURC。
3. 把 calibration target 从通用 depth error 收缩为 task-relevant relation bad-event，并加入“几何错但动作不受影响 / 几何小错但动作翻转”的 hard pairs。
4. 写清 single-model layer disagreement、augmentation、photometric/motion residual 的输入帧数和在线代价；没有多视角时不得写跨视图一致性。

## Round 02 验收条件

- [ ] router 推理公式只含部署可见量，RGB fallback 与 geometry branch 处于统一可比较风险空间。
- [ ] coverage/risk 的统计单位和拒绝粒度唯一且可执行。
- [ ] GeometryCorrupt 增加 action-relevant/error-irrelevant 的交叉 hard pairs。
- [ ] 与 UAOR/VLA calibration/VGA/GAM 做字段级最近邻表及相同 calibration-label 预算。
- [ ] refinement log 记录上述改动并升为 r01。

