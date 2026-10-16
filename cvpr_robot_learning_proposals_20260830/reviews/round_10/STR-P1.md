# Round 10 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r09
- File: `proposals/STR-P1_event_intent_reset/proposal.md`
- Checked: 2026-08-30
- Round focus: 最终压力测试
- Verdict: **FAIL / FINAL INCORPORATION REQUIRED**

## 实际变更核验

r09 把唯一命题写成 reset-worthiness from change + intervention value，而非change-point/CUSUM或intent token；label-equal pure-ΔQ/change/generic gates同proposer，family-macro restricted mean recovery time为唯一primary。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 错误历史惯性影响长任务恢复。 |
| D2 失败模式清晰度 | 4.5 | false/missed reset与recovery tube清楚。 |
| D3 创新性/最近邻 | 4.5 | change×value reset-worthiness区别BOCPD/IntentVLA。 |
| D4 机制因果闭环 | 4.5 | t−1预测→t创新→reset→action时序正确。 |
| D5 技术正确性 | 4.5 | simultaneous LCB与删失RMRT合理。 |
| D6 可观测性/泄漏 | 4.5 | 部署仅visual/proprio/contact与predicted ΔQ。 |
| D7 数据可得性 | 4.0 | 多事件family target生成较重。 |
| D8 算力/工程 | 4.0 | K proposer与Hrec分账清楚。 |
| D9 可证伪性 | 4.5 | change-only/value-only反向事件可判负。 |
| D10 基线强度 | 4.5 | 同proposer、equal-rate gate公平。 |
| D11 消融充分性 | 4.5 | change×value 2×2及truth table充分。 |
| D12 OOD/真机 | 4.0 | seen-family跨任务，compositional仅stress。 |
| D13 复现性 | 4.5 | lineage、target、censor/resource gate完整。 |
| D14 CVPR契合度 | 4.5 | 流式视觉策略的可恢复性问题明确。 |
| D15 风险/负结果 | 4.5 | detector/EventAlias降级仍有价值。 |

平均分：**4.40/5.00**；关键维均4.5，无fatal，内容门槛通过。

## 三结果压力测试

- **label-equal gates持平：** 删除reset方法，只保留reset-worthiness benchmark。
- **control success <3pp：** RMRT改善不得被写成任务收益。
- **root-event真机失败：** 删除real transfer，保留sim seen-family结论。

## 未决非致命风险与最终修改

ΔQ target与同episode未来可能形成隐含事件标签。r10 必须新增target-shard独立性断言、未来字段schema test及一组视觉闪烁/低速真事件的盲评混淆矩阵，并追加 round_10/r10 log。当前9次refine，暂不PASS。
