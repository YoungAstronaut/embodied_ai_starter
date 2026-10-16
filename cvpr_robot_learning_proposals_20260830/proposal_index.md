# Proposal 索引

更新时间：2026-08-30

本目录采用 `方向缩写-P序号` 作为稳定 ID。每个 ID 对应一个不同的可观察失败模式，而不是同一架构的命名变体。

| ID | 最终建议标题 | 独立科研缺口 | 状态/评分 |
|---|---|---|---|
| GEO-P1 | Geometry Counterfactual Ranking | 通用几何精度不等于relation token的动作排序价值 | PASS / 4.37 |
| GEO-P2 | Action-Conditioned Contact Transition Fields | latent failure monitor不显式定位接触时刻、模式与法向拓扑 | PASS / 4.40 |
| GEO-P3 | When Should Geometry Be Rejected? | 几何分支在新corruption family上可能自信出错 | PASS / 4.37 |
| WAM-P1 | Occlusion-ID | 长遮挡和同类实例下，单假设身份无法表达可辨识性边界 | PASS / 4.40 |
| WAM-P2 | Paired Continuation-Value Targets | myopic/固定频率想象不能估计非单调的后续计算价值 | PASS / 4.40 |
| WAM-P3 | Functional Predictive Beliefs | 同动作在未见dynamics下的实现残差需要分布式适应 | PASS / 4.40 |
| STR-P1 | Reset-Worthiness from Change and Intervention Value | change被检测到不等于值得reset | PASS / 4.40 |
| STR-P2 | Deadline-Valid Complete-Chunk Exits | solver-time exit、wall-clock deadline与atomic control commit未闭合 | PASS / 4.50 |
| STR-P3 | Counterfactual-Alias | 普通示范缺少当前观测近似相同但action value冲突的可达历史对 | PASS / 4.40 |
| JEP-P1 | ActMetric-3D | 通用action pseudometric缺少local 3D contact matched-outcome与assignment审计 | PASS / 4.37 |
| JEP-P2 | TopoManip: Ordered Contact Transactions | endpoint graph会抹掉attach→detach等transient sequence | PASS / 4.40 |
| JEP-P3 | ExoManip | 普通数据不支持balanced action×exogenous distributional interaction检验 | PASS / 4.40 |

## 被最新最近邻否决的种子

| ID | 已放弃种子 | 直接覆盖工作 | 替代机制（不是改写旧措辞） |
|---|---|---|---|
| WAM-P3 | 反事实动作可辨识 4D latent | CoCo 2608.04653v1 已含 inverse/zero action、镜像动作/空间反事实与 same-state multi-action 指标 | 分解部署可得 nominal action realization，并从跨周期残差更新质量/摩擦/顺应性 belief |
| JEP-P3 | 风险校准的 JEPA 候选排序 | JEPA Safety 2608.17496v1 已含 action-conditioned rollout、calibrated risk/progress heads、reranking、deterministic shield/fallback；CheckVLA 亦覆盖 conformal 验证/重写 | 以 action×exogenous factorial interventions 分解 controllable/exogenous stochastic dynamics，不输出安全概率、不做 suffix rewrite |

## 统一评审约束

- 每个 Proposal 单独保留 `proposal.md` 与 `refinement_log.md`。
- 每轮同时响应独立评审的多维意见，至少完成 `round_01` 至 `round_10`。
- 最终通过条件由 `evaluation_rubric.md` 与 reviewer 证书决定；未通过则继续迭代。

最终状态：12/12 为 r10，均完成10次实际refine，并经round_11 actual-diff核验为PASS。评分与认证边界见 `final_certification.md`；MVP顺序见 `final_recommendations.md`。本状态只认证Proposal设计，实验尚未执行。
