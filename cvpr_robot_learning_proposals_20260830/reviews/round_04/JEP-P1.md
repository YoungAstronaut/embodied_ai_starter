# Round 04 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r03
- File: `proposals/JEP-P1_action_equivalence/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / REVISE**（metric扩展原则成立；重复semantic role与canonical实例索引仍未闭合）

## 实际变更核验

r03 已使用固定canonical role、截断`min(c0,2C)`与null cost C，明确CRN只作方差降低，并加入same-action/different-state、state-conditioned shuffle和adapter字段/单位合同。R3提出的metric/shortcut问题得到实质响应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | action-effect geometry重要但应用较专门。 |
| D2 失败模式清晰度 | 4.5 | 非传递与action-code shortcut最小例清楚。 |
| D3 创新性/最近邻 | 4.0 | pseudometric不新，contact-rich视觉实证待证。 |
| D4 机制因果闭环 | 4.5 | metric→latent→value/planner闭合。 |
| D5 技术正确性 | 4.0 | truncated-null metric原则正确；role实例唯一性不足。 |
| D6 可观测性/泄漏 | 4.5 | future/outcome只target，robot spec可部署。 |
| D7 数据可得性 | 4.0 | variance MVP可行。 |
| D8 算力/工程 | 3.5 | full 20k×32×seeds/OT较重。 |
| D9 可证伪性 | 4.5 | triangle/shortcut/Action-Bisim/non-JEPA强。 |
| D10 基线强度 | 4.5 | 直接理论与同监督baseline充分。 |
| D11 消融充分性 | 4.5 | metric字段/S/horizon/value/canonical全面。 |
| D12 OOD/真机 | 4.0 | embodiment/相机/对象和安全微扰合理。 |
| D13 复现性 | 4.0 | 单位/null/adapter增强；实例index未定义。 |
| D14 CVPR 契合度 | 4.5 | JEPA视觉表示与机器人规划契合。 |
| D15 风险/负结果 | 4.5 | 可删JEPA/跨embodiment claim。 |

平均分：**4.23/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10且D3/D5未达门槛，R4不通过。

## Top 问题与技术证据

1. **major — semantic role不是唯一对象索引。** 场景可有多个obstacle/tool/target候选；若都映射到同一“obstacle”role，固定role求和会丢实例，若按pair重新匹配又回到可能破坏triangle的问题。需要全局可复现的role-instance slots。
2. **major — deploy role来源未完全定义。** target adapter用sim UUID生成role GT，student虽拒绝UUID，但部署如何从language/detector分配`target#1/obstacle#2`需给出；错误分配应进入metric noise而非被oracle修正。
3. **technical — contact graph TV与单role cost的关系含混。** contact graph是跨role边，不宜在每个role重复加TV；应定义product outcome的node/edge metric一次。
4. **minor — 10万随机triangle测试不是证明。** 可作为实现回归测试，但数学通过来自明确metric构造；需要加入adversarial重复role/缺失object案例。

## 具体修改动作

1. 使用任务schema固定最大role-instance slots及canonical排序（语言referent、初始几何排序等），并对交换相同实例单列symmetry处理。
2. 主结果用deploy detector/language分配，GT UUID只oracle；报告role assignment error与coverage。
3. 把outcome metric写成固定node slots SE(3)项+全局edge/contact项+collision项，避免重复计边。
4. 增加两同类障碍、一个缺失、三元状态的triangle/identity最小例。

## Round 05 验收条件

- [ ] 多同类实例有全局固定且部署可得的canonical slot。
- [ ] GT UUID只oracle，主metric包含role assignment误差。
- [ ] node/edge/contact cost不重复并保持metric。
- [ ] adversarial missing/duplicate-role测试通过。

