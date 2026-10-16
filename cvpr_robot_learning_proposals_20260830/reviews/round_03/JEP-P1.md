# Round 03 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r02
- File: `proposals/JEP-P1_action_equivalence/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（R1 非传递 fatal 持续解除；可变对象集下 ground metric 的数学合同仍需补齐）

## 实际变更核验

r02 已逐公式比较 Action-Bisimulation，定义 0.10m/π/contact/collision ground cost，加入 S=4/8/16 对 S=32 的 estimator audit、non-JEPA+同 metric loss，并画清 target→student→planner 的字段路径。旧“equivalence class”已彻底废弃为 action-effect pseudometric。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | action representation 与真实后果拓扑对齐重要，但主应用范围较专门。 |
| D2 失败模式清晰度 | 4.5 | 三动作非传递反例和 metric distortion/ranking 终点清楚。 |
| D3 创新性/最近邻 | 4.0 | pseudometric 已被 Action-Bisim覆盖；增量依赖 contact-rich视觉实证。 |
| D4 机制因果闭环 | 4.0 | outcome metric→latent distance→value head→planner 已闭合。 |
| D5 技术正确性 | 4.0 | W1 构造原则正确；dustbin/对象匹配若为 pairwise 最优会影响 triangle 证明。 |
| D6 可观测性/泄漏 | 4.5 | future outcome/contact/seed 仅 target，部署 planner 只读 current predictor。 |
| D7 数据可得性 | 4.0 | variance MVP 可行，完整 20k×32 较重但有 go/no-go。 |
| D8 算力/工程 | 3.5 | 全量 action×seed simulation 和 OT/CI 成本仍高。 |
| D9 可证伪性 | 4.5 | Action-Bisim、CoCo、non-JEPA 与 label shuffle 均能否定主张。 |
| D10 基线强度 | 4.5 | 直接理论基线、JEPA邻居和非JEPA同监督已覆盖。 |
| D11 消融充分性 | 4.5 | metric字段、S、horizon、canonical、value separation 均可拆。 |
| D12 OOD/真机 | 4.0 | embodiment/对象/相机拆分与安全微扰合理。 |
| D13 复现性 | 3.5 | 缺 canonical object correspondence、dustbin cost 和 OT solver 细则。 |
| D14 CVPR 契合度 | 4.5 | 视觉表示、JEPA 与机器人 action geometry 契合。 |
| D15 风险/负结果 | 4.5 | 可删除 JEPA/跨 embodiment claim，保留 metric dataset。 |

平均分：**4.17/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10 且 D3/D5 未达硬门槛，R3 不通过。

## Top 问题与证据缺口

1. **major/technical — 可变对象集的 metric 性未完成。** 正文称正权 metric 之和满足 triangle，但对象缺失使用“预注册 dustbin cost”，对象对应关系又可能按 pair 最优匹配。若 dustbin cost 或匹配规则不是一个全局 assignment metric，三角不等式仍可能失败。
2. **major — matched seeds 与 W1 的角色需区分。** W1 对两个经验分布做最优运输，不利用 seed pairing本身；shared seed 是方差降低设计。不得把 matched pairing 当作 W1 的 causal correspondence证明。
3. **major — latent 可能只编码 action code。** predictor 接收 candidate action，metric loss 可由 action embedding lookup 拟合局部距离而不读视觉 state；action label shuffle 不足以排除 state-conditional lookup。

## 具体修改动作

1. 定义全局 canonical object index 或 unbalanced/assignment OT metric；给 dustbin cost 满足 triangle 的条件，并用随机三元组数值单测 triangle violation。
2. 把 paired-seed estimator 与 unpaired empirical W1 分开报告，验证 variance reduction而不改变 estimand。
3. 加 same action/different state 与 same state/action permutation 交叉干预；用 state-conditioned metric target shuffle 检验 predictor 是否真正读当前视觉。
4. 明确 canonical adapter 在 target 与部署各自读哪些 robot spec，跨 embodiment 的对象/接触单位如何归一。

## Round 04 验收条件

- [ ] dustbin、对象对应和 ground cost 构成可证明或数值无反例的 metric。
- [ ] shared-seed 只作为 estimator variance 设计，不被误写成 OT pairing定义。
- [ ] state-conditional action-code shortcut 有最小反例与干预阈值。
- [ ] canonical adapter 的 train/deploy 字段与单位转换可复现。

