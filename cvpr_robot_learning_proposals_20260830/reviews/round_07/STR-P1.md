# Round 07 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r06
- File: `proposals/STR-P1_event_intent_reset/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已加入change×value 2×2、generic concat、native/equal winner、equal-rate threshold及target/censor/resource gate；R6机制混叠已响应，actual pilot=0明确。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 事件后意图失配重要。 |
| D2 失败模式清晰度 | 4.5 | 四family与反向例明确。 |
| D3 创新性/最近邻 | 4.0 | 增量在change×value target。 |
| D4 机制因果闭环 | 4.5 | evidence→reset→recovery闭合。 |
| D5 技术正确性 | 4.5 | conformal与censor逻辑稳定。 |
| D6 可观测性/泄漏 | 4.5 | ΔQ target部署隔离。 |
| D7 数据可得性 | 4.0 | RoboTwin可造，实际family分布未知。 |
| D8 算力/工程 | 3.5 | 30k episode的Q/recovery总账缺失。 |
| D9 可证伪性 | 4.5 | family低power会降级。 |
| D10 基线强度 | 4.5 | native/equal winner充分。 |
| D11 消融充分性 | 4.5 | change×value 2×2闭合。 |
| D12 OOD/真机 | 4.5 | 多事件与可重复真机干预。 |
| D13 复现性 | 4.0 | manifest框架好，事件生成/split不全。 |
| D14 CVPR契合度 | 4.5 | 视觉事件与控制紧密。 |
| D15 风险/负结果 | 4.5 | detector-only降级清楚。 |

平均分：**4.33/5.00**。D3/D8/D13未过关键门槛；round<10，不通过。

## 数据/资源攻击面

1. 每event target实际有`z_old+K4=5`候选，每个S8×H16，即至少`5×8×16=640` env steps，不是只写“K4×S8×H16”即可。30k events对应19.2M target steps，尚未计生成到事件时刻和H64 recovery评测。
2. 30k episode与“每初态paired四类干预+3+3 hard pairs”关系未定义；同initial state的多个event必须是一个cluster，不能当独立episode。
3. 16 tasks没有train/calibration/test task/family/asset拆分；Mondrian calibration若每family/task cell过小，95% simultaneous coverage不现实。
4. equal-rate threshold需记录validation触发率与不确定区间；若基线触发率被强制匹配但事件严重度分布不同，仍可能不公平。

## 具体修改动作

1. 给完整公式：history-to-event rollout、5×S×HQ target、Hrec评测分别记账；同target shard在2×2间共享。
2. manifest加入root_snapshot/event_variant/family/severity/time/task/asset，使paired variants按root cluster；split按root snapshot与task template分组。
3. 列16 tasks的train/calibration/test与每family最小cluster；coverage cell不足时合并规则只能validation预定。
4. 每族50-event smoke只作acceptance/censor；另据root-cluster ICC做power，资源表列CPU sim/GPU proposer/student与存储字段。

## Round 08 验收条件

需闭合640-step target、事件生成与恢复成本、root-cluster schema和task/calibration split。R8再审查unseen event family/真机滑落与移位的外部有效性。
