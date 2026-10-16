# Round 07 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r06
- File: `proposals/WAM-P1_occlusion_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已加入JPDA evidence×MAP/marginal L00–L11 ladder、OA/POT native/adapter、同likelihood/capacity、validation winner及stratum/resource gate。R6近同构基线缺口已补，actual episodes=0如实标注。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 长遮挡referent错误重要。 |
| D2 失败模式清晰度 | 4.5 | 三种可辨识层级清楚。 |
| D3 创新性/最近邻 | 4.0 | 对JPDA增量需实验。 |
| D4 机制因果闭环 | 4.5 | posterior到marginal control闭合。 |
| D5 技术正确性 | 4.5 | 联合后验公式稳定。 |
| D6 可观测性/泄漏 | 4.5 | evaluator proof隔离。 |
| D7 数据可得性 | 3.5 | proof-computable与stratum比例未知。 |
| D8 算力/工程 | 3.5 | 50k episode无frame/assignment成本上界。 |
| D9 可证伪性 | 4.5 | calibration/control降级明确。 |
| D10 基线强度 | 4.5 | L11近同构比较很强。 |
| D11 消融充分性 | 4.5 | evidence×decision 2×2闭合。 |
| D12 OOD/真机 | 4.0 | 同类实例真机合理但规模有限。 |
| D13 复现性 | 4.0 | posterior schema好，generator/proof版本不够。 |
| D14 CVPR契合度 | 4.5 | 视觉跟踪与控制契合。 |
| D15 风险/负结果 | 4.5 | symmetric边界与benchmark降级充分。 |

平均分：**4.27/5.00**。D3/D7/D8/D13未达门槛；round<10，不通过。

## 数据/资源攻击面

1. 50k episode没有`frames/episode`、遮挡事件数、detection数或每帧assignment枚举上限；JPDA复杂度依赖tracks×detections/假设数，A100×天无法验证。
2. “provably symmetric”需在置换下检查历史observation/action likelihood不变，但未说明是解析sim状态证明、rerender数值检验还是模型likelihood；三种定义成本与可信度完全不同。
3. train/test只写纹理和episode ID独立，未明确asset instance、task template、occlusion path与action history family隔离，可能同模板泄漏。
4. 4 tasks×100真机paired trials与50k sim之间的detector/identity GT协议未版本化；AprilTag只评测仍需防tag像素进入RGB。

## 具体修改动作

1. 给资源公式 `N_episode×T_frame×(detector forward + hypotheses enumerated/pruned + WAM forward)`，冻结max detections/tracks/M/prune beam和peak RAM。
2. 定义proof算法：输入字段、置换集合、rerender次数、数值容差、失败code；报告proof-computable率而非笼统accepted。
3. split按asset identity+task template+occlusion trajectory+history policy family分组，并给hash去重断言。
4. 真机RGB裁除/遮蔽tag，GT视频与model视频分别保存；版本化detector、标注器和同步误差。

## Round 08 验收条件

需闭合episode/frame/assignment成本、proof算法和family-level split。R8将检验新纹理不足以构成OOD、真机相同物体与长遮挡是否覆盖主claim。
