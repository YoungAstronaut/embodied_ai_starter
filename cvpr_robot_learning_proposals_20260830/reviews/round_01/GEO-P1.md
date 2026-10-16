# Round 01 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r00
- File: `proposals/GEO-P1_counterfactual_geometry/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / REVISE**（round<10；当前无不可修复 fatal flaw）

## 文件变更核验

这是首轮独立评审。已核对 r00 元数据、正文和 `refinement_log.md`；文件确实包含 nuisance/causal exact-reset pairs、K-token bottleneck、swap 干预、可见性表、等预算基线和判负阈值，与交接摘要一致。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 指向几何 probe 与动作因果依赖脱钩，影响几何 VLA 的建模结论；尚无失败发生率/跨 backbone 先验。 |
| D2 失败模式清晰度 | 4.0 | 给出保持必要几何和只改变必要关系的两类干预；“必要关系”仍由何种 oracle 定义不清。 |
| D3 创新性/最近邻 | 4.0 | 正面区分 VGA、MECo、ST-VLA/GuidedVLA，并写出新意失效条件；逐项训练图差异仍待 R2。 |
| D4 机制因果闭环 | 3.5 | 有 gate、selected/background swap 和 reliance 指标；`L_med` 与 OOD success 的中介估计未形式化。 |
| D5 技术正确性 | 3.0 | `L_sens` 只要求动作不同，不约束正确方向；`L_inv` 只让 mask 相同，不保证动作/表示对 nuisance 不变；配对可行性未证明。 |
| D6 可观测性/泄漏 | 4.0 | train/test 表、future-mask、故意泄漏阳性对照齐全；离线“必要关系标签”是否利用完整状态需字段级审计。 |
| D7 数据可得性 | 3.5 | RoboTwin 配对生成可行并有规模；exact-reset 字段、许可证、pair acceptance rate 和 DROID 对齐尚缺。 |
| D8 算力/工程 | 3.5 | 给出 MVP/完整 GPU 预算和冻结降级；未给 token 提取吞吐、缓存体积和两月真机占用。 |
| D9 可证伪性 | 4.5 | 有 pp/CI/reliance/swap 比率和 random-K 判负，可区分容量正则替代解释。 |
| D10 基线强度 | 4.0 | 最近邻、简单控制、oracle 齐全；VGA/MECo 是否可在同 backbone/data 下真正复现尚未知。 |
| D11 消融充分性 | 4.0 | 监督、K、层、teacher、语义通路和 swap 较完整；pair 数量/质量与 mask 稳定性交互未列。 |
| D12 OOD/真机 | 4.0 | 四 OOD 轴、LIBERO-Plus、真机配对均有；30 trial/task 的功效和 exact-reset 容差未算。 |
| D13 复现性 | 3.0 | 有总体协议，无 schema、版本/commit、seed 表、生成器验收测试或 artifact 清单。 |
| D14 CVPR 契合度 | 4.0 | 视觉几何表示及其因果诊断是主问题，具备视觉分析价值。 |
| D15 风险/负结果 | 4.0 | 明确 gate 塌缩、teacher 失效和负结果 benchmark；真实干预安全/数据偏差仍较粗。 |

平均分：**3.80/5.00**。关键门槛：D3=4.0、D5=3.0、D6=4.0、D9=4.5；未达 hardened gate，且轮次不足。

## Top 问题

1. **major — “必要几何”标签存在循环定义**：若用专家动作/完整模拟器状态挑关系，方法可能学到标签工程而非可部署的因果几何；若用当前 policy 动作敏感性挑选，又会把 policy 偏差写回监督。
2. **major — 最小反例没有数学闭合**：`L_sens` 能被“任意大幅改变错误动作”满足；`L_inv` 只约束 mask，不约束被选 token 数值和最终动作不变。
3. **major — 中介 claim 过强**：`Δaction_causal-Δaction_nuisance` 不是中介效应估计，尚不能支持“解释 OOD success 的主要增益”。

## 最近邻冲突与证据缺口

- [ST-VLA 2603.13788v1](https://arxiv.org/abs/2603.13788) 已声称 task-relevant 3D-4D masks；必须证明本方案不是用 exact-reset 标签替代其 learned mask。
- [MECo-WAM 2607.05468v1](https://arxiv.org/abs/2607.05468) 已做 action-aware temporal geometric distillation；需逐项比较关系选择信号、student 可见信息和部署图。
- [VGA 2604.12908v2](https://arxiv.org/abs/2604.12908) 与 [GAM 2606.17046v2](https://arxiv.org/abs/2606.17046) 要求把 backbone scaling 与因果瓶颈收益拆开；GAM 的强预训练下辅助目标弱增益尤其是反证压力。

## 必须修改的动作

1. 写出 pair 生成器最小结构因果模型：可干预变量、保持变量、oracle 来源、拒绝条件；列出至少 3 个 positive pair、3 个 hard negative 和不可生成情形。
2. 将 `L_sens` 改为对专家/有效动作分布的方向性 ranking 或 distribution matching；新增最终动作 nuisance-invariance，而非只约束 mask。
3. 把“中介”降为 intervention-based reliance，或给出可识别假设、treatment/mediator/outcome 和估计器；不要用差分指标冒充中介效应。
4. 增加 pair acceptance rate、标签噪声注入和 oracle-label ablation；明确 DROID 只能提供自然对照，不能参与 exact-counterfactual 主结论。

## Round 02 验收条件

- [ ] proposal 含一张变量级 pair SCM/生成表，且必要关系标签不进入 student/action query。
- [ ] 公式保证 causal pair 的动作朝正确 target 变化、nuisance pair 的最终动作保持，而非仅 mask 保持。
- [ ] 将中介 claim 要么形式化，要么显式收缩为 reliance 诊断。
- [ ] 新增 ST-VLA、MECo、VGA/GAM 的逐项最近邻表（输入/监督/训练图/部署图/结论）。
- [ ] refinement log 逐条回应以上四项并升为 r01。

