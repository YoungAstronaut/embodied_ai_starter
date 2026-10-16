# Round 06 Review — GEO-P2

- Proposal-ID: GEO-P2
- Reviewed-Revision: r05
- File: `proposals/GEO-P2_contact_transition/proposal.md`
- Checked: 2026-08-30
- Round focus: 最强基线、公平合同与正交消融
- Verdict: **FAIL / REVISE**

## 实际变更核验

r05 已把唯一 primary 改为 contact-rich selection regret，补全 1.024M attempted 标签漏斗、snapshot/task 功效、ContactGuard 比较及真机 paired-reset 降级。R5 多终点问题解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 接触时序错误是 manipulation 核心瓶颈。 |
| D2 失败模式清晰度 | 4.5 | onset/mode/normal/support 失败可直接观测。 |
| D3 创新性/最近邻 | 4.0 | ContactGuard/ContactWorld 后需靠 typed transition field 证明增量。 |
| D4 机制因果闭环 | 4.5 | candidate-conditioned field→scorer→selection 完整。 |
| D5 技术正确性 | 4.5 | hazard/censoring/多接触定义已闭合。 |
| D6 可观测性/泄漏 | 4.5 | GT pose 与 deploy frame 分开。 |
| D7 数据可得性 | 4.0 | 大规模 exact-reset 可生成但标签漏斗风险高。 |
| D8 算力/工程 | 4.0 | N8 批处理可行，1M+ rollout 昂贵。 |
| D9 可证伪性 | 4.5 | regret、field 门槛和控制降级清楚。 |
| D10 基线强度 | 4.0 | ContactGuard 强，但同标签定义可能改变其任务。 |
| D11 消融充分性 | 4.0 | latent/field 分解有，ontology 与 executor 尚未正交。 |
| D12 OOD/真机 | 4.5 | paired-reset 真机设计具体。 |
| D13 复现性 | 4.5 | hazard schema、support 与 runtime 有明确口径。 |
| D14 CVPR契合度 | 4.5 | 接触视觉预测和机器人规划强契合。 |
| D15 风险/负结果 | 4.5 | 持平、无控制收益、触觉依赖均有判负。 |

平均分：**4.33/5.00**。D3/D10/D11 未达关键门槛；round<10，不通过。

## Top 问题与证据缺口

1. **ContactGuard 的“同 accepted candidate labels”语义含混。** 原生 latent failure monitor 与本法 typed time/mode/normal 标签不同。给它全部 typed 标签会变成新方法；不给则本法多拿监督。必须同时报告 raw-rollout-equal 与 typed-label-equal 两种公平口径。
2. **field-only/latent-only 仍混入表示容量与监督差。** typed field 的维度、loss 数和 executor 都不同；`field-only > latent-only`不能单独证明 topology 是关键。
3. **没有把 ontology 与 action-conditioned predictor 正交。** 最可能的简单解释是“每候选多一个大 head”。需要同容量 generic hazard/tensor head，以及 typed ontology 是否通过 executor 起作用的因子实验。

## 具体修改动作

1. 增加 baseline-native 与 label-equal ContactGuard：前者复现原 binary/latent loss，后者从同 rollout 得同 typed 标签但用非结构化定长 tensor；两者共享 detector/frame/N8/scorer/fallback。
2. 预注册 `target {binary/generic tensor, typed transition}` × `execution {flat MLP score, typed executor}` 2×2；四格参数±5%、相同 label-seconds 与 runtime，oracle field 只作上界。
3. 将最强 deployable comparator 改为 validation winner `max(ContactGuard-native, ContactGuard-label-equal, generic-hazard+same scorer)`，而非先验固定一个名字。
4. mode/time/normal 删除消融要保持输出维数，使用 label shuffle/null channel，避免参数减少导致假结论。

## Round 07 验收条件

必须写清两种标签公平口径、完整 ontology×executor 2×2、validation winner 和每格参数/训练标签/推理调用账；同时给 attempted→support 的实际 pilot 数而非计划数。
