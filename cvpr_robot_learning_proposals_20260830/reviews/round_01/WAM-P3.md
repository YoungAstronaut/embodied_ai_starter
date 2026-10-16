# Round 01 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r00
- File: `proposals/WAM-P3_hidden_physics_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / REVISE**（新题方向可行；当前 latent calibration 定义矛盾）

## 文件变更核验

r00 确实放弃 CoCo 已覆盖的一般 action controllability，改为 nominal action-realization 分解、跨周期 response residual、hidden-physics belief、触觉 oracle 与 exact-reset 物性 OOD；日志与交接一致。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 同视觉/同命令下 hidden dynamics 造成持续错误是 WAM 的关键物理缺口。 |
| D2 失败模式清晰度 | 4.0 | mass/friction/compliance 与首次/后续交互区分清楚；传感不可辨识最小例未形式化。 |
| D3 创新性/最近邻 | 4.0 | 已实质换题并区分 Robot-Factored、DELE、VT-WM、CoCo；system identification/POMDP 邻居缺失。 |
| D4 机制因果闭环 | 3.5 | residual→belief→sample future→robust action→success，含 belief shuffle；适应收益与 probe action 收益未分开。 |
| D5 技术正确性 | 3.0 | θ 声称不逐维对应真实物性，却报告 posterior NLL/ECE；无可观测/等价类定义时这些指标无意义。 |
| D6 可观测性/泄漏 | 4.5 | nominal path 部署可算、actual response 下一周期才进入、GT physics 禁止输入，时序清楚。 |
| D7 数据可得性 | 3.5 | 物性采样和真机材料可得；真实 friction/compliance 标定、控制器日志和许可证未写。 |
| D8 算力/工程 | 3.5 | 两档预算合理；机器人 rendering 分离、controller mismatch 与 480 paired trials 工程量偏乐观。 |
| D9 可证伪性 | 4.0 | success、pose error、belief intervention、tactile/oracle 与 DELE 判负明确。 |
| D10 基线强度 | 4.0 | Robot-Factored、DELE、RSSM ensemble、CoCo、system-ID/tactile oracle 齐全。 |
| D11 消融充分性 | 4.0 | belief/point/history/factor/residual/probe/latent/GTθ/tactile 并有干预；首次交互 vs 适应阶段未拆。 |
| D12 OOD/真机 | 4.5 | 质量/摩擦/顺应、两引擎与真机配对具体；平台可行性仍需预实验。 |
| D13 复现性 | 3.0 | 无物性测量 protocol、nominal controller 版本、residual schema、seed/artifact 清单。 |
| D14 CVPR 契合度 | 4.0 | 视觉 latent dynamics 的可辨识性与预测分析可形成强 CVPR 问题。 |
| D15 风险/负结果 | 4.5 | 明确不可辨识时只称 predictive equivalence class，并给传感边界数据产出。 |

平均分：**3.90/5.00**。关键门槛：D3=4.0、D5=3.0、D6=4.5、D9=4.0；未达 hardened gate。

## Top 问题

1. **major — latent 与物理标签的评价自相矛盾**：若 θ 只是一组不可解释 predictive factors，无法直接计算 mass/friction posterior NLL/ECE；若用 GT θ 做 calibration，则已对齐并监督了物性。
2. **major — 第一次交互前不可能识别**：相同历史/视觉但不同物性的两个 episode 在首次作用前后验必须相同。论文必须把 prior performance、identification actions、适应后 performance 分开。
3. **major — nominal residual 不唯一归因于物性**：controller tracking error、robot compliance、视觉 encoder drift、接触定位错都进入 `e_t`；只用 Robot-Factored baseline 不能完成归因。

## 最近邻冲突与证据缺口

- [Robot-Factored WM 2607.22535v1](https://arxiv.org/abs/2607.22535) 是 action realization 分解直接基线。
- [DELE-w0.5 2608.22067v3](https://arxiv.org/abs/2608.22067) / LaWAM / LiLa-WAM 压缩 latent-action bridge，需在同 history 下比较是否 recurrence 已足够。
- 经典 online system identification、Bayes-adaptive control、PEARL/RSSM latent context 和视觉物性估计 literature 未被覆盖；R2 不能只对 WAM 论文。

## 必须修改的动作

1. 选择评价对象：若是物理 θ posterior，明确 supervised/weakly supervised alignment；若是 predictive equivalence belief，改用 held-out future log-likelihood、calibration of outcome sets 和 action regret，不报告 θ-NLL。
2. 拆成 t=0 prior、被动交互更新、主动 probe 三阶段，分别给 oracle 上界/成本与判负。
3. 在 residual 生成模型中显式加入 controller error、observation noise、contact localization 和 object dynamics；做可控 factorial interference。
4. 将 robust action objective（期望、CVaR、minimax 或 information gain）写清，避免“后验下稳健”成为不可复现措辞。

## Round 02 验收条件

- [ ] latent calibration 指标与是否对齐 GT physics 完全一致，无 θ-NLL 矛盾。
- [ ] 首次交互、被动适应、主动 probe 的 claim/metric 独立。
- [ ] residual confounder 有生成模型与正交实验。
- [ ] 最近邻表补 online system-ID/Bayes-adaptive/latent-context 工作并保持 Robot-Factored/DELE 强对照。
- [ ] refinement log 记录换题与本轮修改并升为 r01。

