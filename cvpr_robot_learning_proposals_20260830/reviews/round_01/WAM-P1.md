# Round 01 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r00
- File: `proposals/WAM-P1_occlusion_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / REVISE**（round<10；无不可修复 fatal flaw）

## 文件变更核验

首轮核对确认 r00 不再把 persistent slot 当贡献，而是维护 identity/pose/contact-owner 多假设、因果更新、identity-swap benchmark、校准指标、泄漏阳性对照与 oracle identity。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 长遮挡后指代对象身份错误是长程 manipulation 的真实瓶颈，超越常规 tracking。 |
| D2 失败模式清晰度 | 4.0 | 相似实例交换/仅一只被操作/重现后抓错清楚；完全对称不可辨识情形未单列。 |
| D3 创新性/最近邻 | 4.0 | 明确超越 OA-WAM 固定地址与 POT/3D-ALP 持久 token；belief tracking 经典最近邻未覆盖。 |
| D4 机制因果闭环 | 3.5 | belief 置乱、identity/background swap、success 中介均有；“正确重关联”与“校准承认不知道”混为同一机制。 |
| D5 技术正确性 | 3.0 | instance ID 有置换不变性；JPDA/Sinkhorn 与 learned WAM 的状态/更新公式、belief calibration target 尚未定义。 |
| D6 可观测性/泄漏 | 4.5 | future association 仅 target，时间表与阳性泄漏清楚；接触标签延迟亦声明。 |
| D7 数据可得性 | 3.5 | exact-reset 50k 和真机设计具体；身份 GT/遮挡生成 schema、SAM 许可和数据发布未写。 |
| D8 算力/工程 | 3.5 | M≤4/pruning 和两档预算合理；检测、WAM、policy 联合吞吐与 400 真机 paired trials 占用未算。 |
| D9 可证伪性 | 4.0 | switch/ECE/success/oracle 上界/置乱阈值明确；不可辨识 subset 上“准确率”预期未注册。 |
| D10 基线强度 | 4.0 | OA/POT/3D-ALP、tracker、single belief、oracle/random 齐全且承诺同预算。 |
| D11 消融充分性 | 4.0 | M/contact/covariance/calibration/filter/active look/swap 完整；association evidence 与 dynamics prior 未正交拆分。 |
| D12 OOD/真机 | 4.5 | 遮挡时长、交叉、接触交换逐轴，4×100 真机 paired trials；可执行但成本高。 |
| D13 复现性 | 3.0 | 无 ID canonicalization、permutation matching、calibration binning、版本/脚本与 artifact 清单。 |
| D14 CVPR 契合度 | 4.0 | 视觉对象表示、遮挡记忆与预测闭环明确。 |
| D15 风险/负结果 | 4.0 | detector recall 分层、oracle detection 和不可辨识边界产出合理。 |

平均分：**3.87/5.00**。关键门槛：D3=4.0、D5=3.0、D6=4.5、D9=4.0；未达 hardened gate。

## Top 问题

1. **major — 对称场景中身份不可辨识**：两个完全相同物体在完全遮挡后对称交换，任何 causal observer 都只能保持多峰/0.5 posterior；不能同时要求低 switch 和正确重关联。此时方法价值应是 calibrated ambiguity 与稳健动作，不是猜中 ID。
2. **major — identity metric 受任意 label permutation 影响**：NLL/ECE、slot switch、语言 referent 的 canonical anchor 尚未定义，可能把全局换名当错误或把每帧 Hungarian 掩盖真实 switch。
3. **major — belief-to-control 链条未分解**：success 可能来自 entropy 高时短 horizon/active look，而非更好关联；当前主方法已提到这些行为但未固定。

## 最近邻冲突与证据缺口

- [OA-WAM 2605.06481v1](https://arxiv.org/abs/2605.06481) 已有 persistent address 与 causal slot-swap；需逐项确认其地址重置/association protocol。
- [POT-VLA 2607.18016](https://arxiv.org/abs/2607.18016) 与 [3D-ALP 2604.11302](https://arxiv.org/abs/2604.11302) 的遮挡/接触恢复强度需正文级核查。
- 多目标 Bayesian tracking/JPDA 是方法核心来源；只列机器人 WAM 邻居不够，R2 要补经典/近期 object-centric belief tracking 并说明视觉学习贡献。

## 必须修改的动作

1. 将 benchmark 分为 identifiable、partially identifiable、provably symmetric 三档；为对称档预注册 proper scoring/NLL 最优而 top-1 不可能提升。
2. 定义 permutation-invariant identity state、语言 referent anchor、重现 association 的 NLL/ECE 和 switch 计算伪代码。
3. 主实验固定 passive policy；active look/short horizon 另作扩展，分别测“belief estimation gain”和“uncertainty-aware action gain”。
4. 写出 prediction、association、pruning、posterior update 方程与退化保护；说明 M=4 如何覆盖 3 实例多时段组合。

## Round 02 验收条件

- [ ] proposal 明确不可辨识最小反例并收缩“正确重关联”claim。
- [ ] ID NLL/ECE/switch 对 slot permutation 不敏感且语言 referent 锚定可复现。
- [ ] passive belief 与 active information gathering 两条结果分开。
- [ ] OA/POT/3D-ALP 及 belief-tracking 最近邻逐项对比。
- [ ] refinement log 记录改动并升为 r01。

