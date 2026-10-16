# Round 01 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r00
- File: `proposals/JEP-P1_action_equivalence/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / FATAL-IN-r00**（所定义关系通常不具传递性，不能直接作为 equivalence class）

## 文件变更核验

r00 已实际包含 same-state 32-action perturbations、类内/类间 loss、ranking regret、跨 embodiment canonical outcome、信息表、label reversal 和强 JEPA/CoCo baselines。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | latent 应对无效动作差异不敏感、对因果动作敏感，是 planning 表示的核心问题。 |
| D2 失败模式清晰度 | 3.5 | 局部动作扰动与 outcome 判据具体；“过拟合无效微差”尚无基线最小反例/发生率。 |
| D3 创新性/最近邻 | 4.0 | 与 VLA-JEPA、CoCo、Invariant JEPA 的差异落在新监督对象；动作抽象/等价文献仍缺。 |
| D4 机制因果闭环 | 3.5 | intra/inter→ranking regret→MPC success，含 label shuffle；不合法的类定义破坏闭环。 |
| D5 技术正确性 | 2.5 | 由阈值距离定义的 `a~a'` 通常不传递，不能形成 equivalence classes；Wasserstein outcome 又未给随机/估计协议。 |
| D6 可观测性/泄漏 | 4.5 | future outcome 只作 target、student causal、robot spec 明示、泄漏阳性对照齐全。 |
| D7 数据可得性 | 3.5 | exact-reset action grid 可生成；640k rollouts、oracle outcome distribution 与真机 reset 安全成本未算。 |
| D8 算力/工程 | 3.5 | 冻结 encoder 与两档预算合理；20k×32 和跨 embodiment/真机 workload 偏紧。 |
| D9 可证伪性 | 4.0 | distance ratio/regret/success/CoCo smoothing/label shuffle 阈值清楚。 |
| D10 基线强度 | 4.0 | V-JEPA2-AC、VLA-JEPA、JEPA-WM、CoCo、bisimulation、oracle 齐全。 |
| D11 消融充分性 | 4.0 | rho/epsilon/outcomes/contact/canonical/intra/inter/noise 均拆；class construction rule 未消融。 |
| D12 OOD/真机 | 4.0 | 物体/相机/embodiment split 和真机 reset groups；安全微扰空间/统计功效未定。 |
| D13 复现性 | 3.0 | 无 action metric/units、outcome estimator、reset tolerance、版本/seed/artifact 清单。 |
| D14 CVPR 契合度 | 4.5 | 对视觉预测 latent 的可控不变性给出一般表示学习问题。 |
| D15 风险/负结果 | 4.0 | 承认局部/horizon/task 边界及 proxy-control 脱钩负产出。 |

平均分：**3.77/5.00**。关键门槛：D3=4.0、D5=2.5、D6=4.5、D9=4.0。当前有可修复的定义级 fatal flaw。

## Top 问题

1. **fatal-in-r00 — 不是等价关系**：距离阈值可出现 `a~b`、`b~c`、但 `a!~c`；connected components 又会把链式远距离动作错误合并。标题、loss 和 retrieval 都依赖“类”，必须先解决。
2. **major — 随机 outcome 的判据未定义**：一次 rollout 的 success/contact 不能估 Wasserstein 分布；若相同 action 在外生随机下多模态，标签噪声会主导。
3. **major — task reward 写入 equivalence 可能导致不可迁移**：同物理 outcome 在不同语言/阶段下价值不同；需要分开 physical-effect abstraction 与 task-conditional action value。

## 最近邻冲突与证据缺口

- [VLA-JEPA 2602.10098v2](https://arxiv.org/abs/2602.10098)、[V-JEPA 2 2506.09985v1](https://arxiv.org/abs/2506.09985)、[JEPA-WM study 2512.24497v3](https://arxiv.org/abs/2512.24497) 覆盖 action-conditioned latent/planning。
- [CoCo 2608.04653v1](https://arxiv.org/abs/2608.04653) 已有 same-state multi-action controllability；差异必须建立在合法的“合并哪些动作”命题上。
- State/action abstraction、bisimulation metrics、successor features 和 option equivalence 是直接理论邻域，不能只引用 Invariant JEPA-WM。

## 必须修改的动作

1. 不要直接称 equivalence class。可改为局部 action-effect pseudometric/neighbor graph，并用 triplet/ranking loss；若坚持 quotient/class，给出满足反身/对称/传递的构造与边界。
2. 定义 outcome distribution 的采样：每个 `(s,a)` 多个 matched exogenous seeds，距离估计误差与 label confidence；加入 uncertain pairs abstain。
3. 将 physical outcome distance 与 task-conditioned value compatibility 分成两个量，报告任务变换时的稳定/变化预测。
4. 给出最小三动作反例，证明 naive smoothing/CoCo 无法同时保持类内不敏感和类间分离。

## Round 02 验收条件

- [ ] 不再把非传递阈值关系称作 equivalence class，或给出合法 class 构造证明。
- [ ] stochastic outcome 由 matched-seed 多 rollout 估计，含置信/拒绝规则。
- [ ] physical effect 与 task value 分离，跨任务/阶段 claim 可核查。
- [ ] 最近邻表补 action abstraction/bisimulation，并与 CoCo/VLA-JEPA 逐项比较。
- [ ] refinement log 记录定义级 fatal 修复并升为 r01。

