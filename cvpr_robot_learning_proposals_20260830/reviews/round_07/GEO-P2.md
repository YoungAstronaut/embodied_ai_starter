# Round 07 Review — GEO-P2

- Proposal-ID: GEO-P2
- Reviewed-Revision: r06
- File: `proposals/GEO-P2_contact_transition/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已加入ContactGuard native/equal、generic/typed target×flat/typed executor 2×2、等维null-channel、validation winner及resource/support pilot gate；R6的标签公平与机制混叠已响应，actual pilot明确为0。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | contact transition决定操作成败。 |
| D2 失败模式清晰度 | 4.5 | event/mode/normal/censor具体。 |
| D3 创新性/最近邻 | 4.0 | typed topology增量待实证。 |
| D4 机制因果闭环 | 4.5 | candidate field→executor/scorer闭合。 |
| D5 技术正确性 | 4.5 | hazard与信息路径稳定。 |
| D6 可观测性/泄漏 | 4.5 | GT pose与部署frame分开。 |
| D7 数据可得性 | 3.5 | support/event分布尚无pilot。 |
| D8 算力/工程 | 4.0 | 1.024M公式正确，但full与标签器成本不完整。 |
| D9 可证伪性 | 4.5 | support/power不足即benchmark降级。 |
| D10 基线强度 | 4.5 | native/equal危险基线齐。 |
| D11 消融充分性 | 4.5 | target×executor正交。 |
| D12 OOD/真机 | 4.5 | contact OOD和paired reset较实。 |
| D13 复现性 | 4.0 | manifest规划好，ontology/extractor版本仍欠。 |
| D14 CVPR契合度 | 4.5 | 视觉接触预测强契合。 |
| D15 风险/负结果 | 4.5 | 持平/低support/低成功均有降级。 |

平均分：**4.33/5.00**。D3/D7/D8/D13未过关键门槛；round<10，不通过。

## 数据/资源攻击面

1. MVP的`2k×8×4×16=1.024M`正确，但full写“6类任务各5k episodes”，没有说明每episode抽多少snapshot、是否仍8候选/4seed/16步，无法得到full env-step上限。
2. `accepted/censored/rejected`不是互斥层级：right-censored no-contact可能是合法训练样本而非被拒绝。漏斗需要`attempted→legal reset→support-valid→{event,no-event censored,truncated invalid}`，否则acceptance会被人为定义。
3. typed extractor依赖body IDs、force、closure、relative transform；需冻结ontology版本、阈值、单位、并发contact上限和detector/GFM版本。仅写schema不足以重现标签。
4. 200-snapshot smoke可测吞吐/覆盖，不能估task-level power；要分工程gate与统计pilot。

## 具体修改动作

1. 给full公式 `N_task×N_snapshot/task×N_candidate×S×H` 和target bytes；说明四格共享shard、GPU训练按格计。
2. 重画互斥漏斗并单列有效censor；报告每event type/body-pair/mode的cluster数和class imbalance。
3. 发布ontology YAML/JSON schema草案、extractor伪代码版本、阈值单位、legality/censor单测与hash字段。
4. smoke只冻结support/steps/s；另以≥任务数的pilot估ICC与每task snapshots，power不足时不进入confirmatory full。

## Round 08 验收条件

需闭合full成本、互斥漏斗、ontology/extractor版本与统计pilot层级。R8再检查摩擦/材质OOD及100 paired-reset trial是否对真机效应有足够功效。
