# Round 02 Review — GEO-P2

- Proposal-ID: GEO-P2
- Reviewed-Revision: r01
- File: `proposals/GEO-P2_contact_transition/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（R1 candidate-action fatal 已解除；新增 ContactGuard 强碰撞未处理）

## 实际变更核验

r01 的技术图已实质改成 proposer→candidate-action-conditioned event predictor→scorer；ontology 删除 approach，定义多接触/censoring/extractor、部署 detector fallback 和 action×field 定向干预。R1 fatal 解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | pre-contact ranking 对精细接触任务重要。 |
| D2 失败模式清晰度 | 4.5 | mode/time/normal/body-pair 和 directed corruptions 清楚。 |
| D3 创新性/最近邻 | 3.5 | 显式 contact topology field 可能新，但 ContactGuard 已做 planned-action-conditioned pre-contact latent rollout/abort；当前未列。 |
| D4 机制因果闭环 | 4.5 | candidate-conditioned field、定向 field error、ranking/success 闭环。 |
| D5 技术正确性 | 4.0 | 循环已消；scorer/rank target 与并发 Q=8 truncation 仍待深审。 |
| D6 可观测性/泄漏 | 4.5 | GT pose/contact 仅 target，部署 frame/fallback 清楚。 |
| D7 数据可得性 | 4.0 | ontology/extractor/跨引擎与真机 audit 可执行。 |
| D8 算力/工程 | 4.0 | N fixed 和两档预算有；多候选 predictor 延迟需 profile。 |
| D9 可证伪性 | 4.5 | wrong field 方向、oracle、latent deletion 与强判负明确。 |
| D10 基线强度 | 4.0 | ContactWorld/Touch/ViTac/Where-to-Touch 已列；缺 ContactGuard。 |
| D11 消融充分性 | 4.5 | conditioning/fields/frame/noise/staging/capacity 与定向干预全面。 |
| D12 OOD/真机 | 4.5 | 材质/摩擦、双引擎、三真机任务。 |
| D13 复现性 | 3.5 | ontology 已大幅加强；仍缺代码版本/seed/schema artifact。 |
| D14 CVPR 契合度 | 4.5 | 视觉 contact-event representation 是核心。 |
| D15 风险/负结果 | 4.5 | 视觉可辨识性、跨引擎标签和 fallback 负结果有价值。 |

平均分：**4.23/5.00**。D3=3.5、D5=4.0、D6=4.5、D9=4.5；未过创新/技术 hardened gate。

## Top 问题

1. **major — ContactGuard 直接压缩新意**：[ContactGuard 2608.13438v1](https://arxiv.org/abs/2608.13438) 已读取 planned action chunk、预测 post-contact latent、用 failure probe 在真机 pre-contact abort。candidate-action conditioning 与 contact前预测均不能再当贡献。
2. **major — 表格对现有工作仍写“按其原实现”**：这不是独立审计；ContactWorld/TouchWorld/Where-to-Touch 的动作条件、字段和 policy 使用必须从正文填实。
3. **major — 显式 field 的独立价值尚需与 latent monitor 隔离**：如果 ContactGuard latent+probe 在同候选预算等效，ontology 只是额外标签工程。

## 具体修改动作

1. 新增 ContactGuard 对比：pre-contact anchor、planned-action input、future representation、failure target、policy action（abort vs rank）、多候选成本、真机协议。
2. 把 ContactGuard latent/failure probe 作为同 candidate/scorer/label-budget 强基线；做 latent-only、field-only、latent+field、oracle-field 2×2。
3. 对 ContactWorld/TouchWorld/ViTacWorld/Where-to-Touch 填正文级字段和版本/代码状态，禁止“按原实现”。
4. 将唯一主创新表述锁定为 explicit multi-event topology field 提供**方向可诊断的 candidate ranking**，并写出若 ContactGuard 持平则放弃的方法 claim。

## Round 03 验收条件

- [ ] ContactGuard 已进入最近邻表、基线和判重条件。
- [ ] latent-only/field-only/combined 对照能区分标签工程与机制。
- [ ] 所有强邻居字段来自正文并注明版本/代码不确定性。
- [ ] 部署信息图逐 token 标出 N candidates×field predictor 的延迟与缓存。

