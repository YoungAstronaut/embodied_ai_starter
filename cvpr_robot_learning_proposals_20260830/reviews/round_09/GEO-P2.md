# Round 09 Review — GEO-P2

- Proposal-ID: GEO-P2
- Reviewed-Revision: r08
- File: `proposals/GEO-P2_contact_transition/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已限定无触觉sim typed ranking主claim，加入sim1/2/real语义与摩擦材质bins、真机双标、安全abort和fallback降级；R8外部效度边界已响应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | contact-rich ranking重要。 |
| D2 失败模式清晰度 | 4.5 | onset/mode/normal具体。 |
| D3 创新性/最近邻 | 4.5 | candidate typed transition相对latent monitor差异明确。 |
| D4 机制因果闭环 | 4.5 | candidate→event→executor/scorer闭合。 |
| D5 技术正确性 | 4.5 | hazard/censor/语义单位一致。 |
| D6 可观测性/泄漏 | 4.5 | GT/force target-only。 |
| D7 数据可得性 | 4.0 | 两sim+真机可行。 |
| D8 算力/工程 | 4.0 | 100M cap。 |
| D9 可证伪性 | 4.5 | latent/typed/控制降级明确。 |
| D10 基线强度 | 4.5 | ContactGuard equal强。 |
| D11 消融充分性 | 4.5 | target×executor完整。 |
| D12 OOD/真机 | 4.5 | cross-engine与3×100较强。 |
| D13 复现性 | 4.5 | ontology/units/audit具体。 |
| D14 CVPR契合度 | 4.5 | 视觉接触与规划强契合。 |
| D15 风险/负结果 | 4.5 | diagnostic降级清楚。 |

平均分：**4.43/5.00**。已接近硬门槛但round<10，不通过。

## 模拟审稿攻击

1. **“Hand-engineered ontology.”** 回应不能只是更多F1；必须用typed-vs-generic equal-label和wrong-field fixed-action干预证明ontology影响ranking。
2. **“ContactGuard already predicts post-contact failure.”** 最近邻表必须把planned chunk、anchor、rollout、abort接口逐字段放正文，不依赖附录。
3. **“Sim contact labels do not transfer.”** 真机只验证语义/外部效度，不救sim primary；κ/MAE和fallback率需主表。

## 修改与R10验收

标题建议 **Action-Conditioned Contact Transition Fields for Candidate Ranking**，不要用“world model”泛化措辞。摘要唯一贡献句应同时包含`candidate-conditioned`、`typed time/mode/normal`和`label-equal latent monitor`。主表第一列为ContactGuard-equal；机制表第二列为2×2。R10准备ontology-only降级摘要，并验证所有强claim均有单一判负阈值。
