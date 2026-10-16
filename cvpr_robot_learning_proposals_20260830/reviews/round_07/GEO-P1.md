# Round 07 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r06
- File: `proposals/GEO-P1_counterfactual_geometry/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已实际加入 native/label-equal 双合同、四adapter validation winner、relation/generic×objective 2×2、共享Hungarian和manifest gate；R6监督公平问题已响应。正文明确 actual pilot=0，没有伪造可行性证据。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 几何捷径具有部署影响。 |
| D2 失败模式清晰度 | 4.5 | pair与hard negative清楚。 |
| D3 创新性/最近邻 | 4.0 | 增量仍需SCM 2×2证明。 |
| D4 机制因果闭环 | 4.5 | pair到selection闭合。 |
| D5 技术正确性 | 4.5 | 主方法公式稳定。 |
| D6 可观测性/泄漏 | 4.5 | checker字段隔离严格。 |
| D7 数据可得性 | 3.5 | acceptance实际为0，20k扩展未经验证。 |
| D8 算力/工程 | 3.0 | env/storage账出现数量级错误。 |
| D9 可证伪性 | 4.5 | 低acceptance/低power会自动降级。 |
| D10 基线强度 | 4.5 | native/equal winner充分。 |
| D11 消融充分性 | 4.5 | 主2×2与matching共享。 |
| D12 OOD/真机 | 4.0 | LIBERO/真机仅secondary。 |
| D13 复现性 | 3.5 | manifest框架好，但单位/资源算术不可信。 |
| D14 CVPR契合度 | 4.0 | 几何VLA契合。 |
| D15 风险/负结果 | 4.5 | 探索性降级诚实。 |

平均分：**4.13/5.00**。D3/D7/D8/D13未达门槛；round<10，不通过。

## 数据/资源攻击面

1. **存储算术错三个数量级。** `64KB × 20k ≈ 1.28GB`，不是`1.3TB`。如果真实target含M64×两成员的rollout/frame引用，就不能先写“每pair 64KB”；必须列字段字节数推导。
2. **env steps疑似漏掉pair的第二成员。** 一对causal/nuisance样本若两边都执行M64×S4×H16，应为`2×64×4×16=8192` steps/pair；当前4096只覆盖一个snapshot。20k应为163.84M而非81.92M，除非明确定义只执行一边并说明另一边utility来源。
3. **2k accepted与1k attempted gate逻辑不闭合。** acceptance阈值35%时，1k attempted最多约350 accepted，无法估2k档I/O/功效；需分smoke、MVP与full三阶段。
4. manifest尚缺pair两成员、干预类型、checker版本和拒绝原因的不可变row schema，以及RoboTwin/VGGT/VGA确切版本/许可证。

## 具体修改动作

1. 逐字段重算：`N_pair × 2 members × M × S × H`、是否复用seed/branch、frame去重前后bytes；用GiB/GB一致口径。
2. 写三阶段gate：1k attempted smoke只估acceptance；达到阈值后生成≥2k accepted MVP；pilot ICC再决定功效所需accepted clusters，禁止固定20k。
3. manifest增加pair_id/member_id/intervention/reject_code/checker_commit/renderer_seed/candidate_hash，给train/calibration/test按task+asset+snapshot family的去重断言。
4. 明确四个2×2格共享同一target shard，资源生成不乘4；student训练GPU-hours按格相加另列。

## Round 08 验收条件

必须修正两成员env-step与存储算术，给可执行schema/版本/许可证/去重断言和三阶段资源上限。R8再压力测试几何OOD是否真跨asset/renderer及真机30 trial的有效性。
