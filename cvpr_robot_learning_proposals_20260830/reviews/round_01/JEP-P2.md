# Round 01 Review — JEP-P2

- Proposal-ID: JEP-P2
- Reviewed-Revision: r00
- File: `proposals/JEP-P2_object_contact_slots/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / FATAL-IN-r00**（未来 topology operation 未条件化候选动作）

## 文件变更核验

r00 已从固定 persistent slot 改为 attach/detach/transfer/merge/split graph operator，包含 reversible compound view、future graph target 隔离、graph-edit/反向编辑和无拓扑任务特异性判据。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 抓持复合体、handover、开盖/拆装确实改变动力学关系，固定 slot 易失败。 |
| D2 失败模式清晰度 | 3.5 | 操作族和遮挡后果具体；merge/split/ownership/attachment 的图语义有重叠。 |
| D3 创新性/最近邻 | 4.0 | 不是普通 persistent slot/contact head，突出可逆拓扑操作；graph dynamics/scene graph 最近邻尚缺。 |
| D4 机制因果闭环 | 3.5 | operator→graph→JEPA→planning，含 wrong edit 与无拓扑特异性；action causation 缺失。 |
| D5 技术正确性 | 2.5 | 下一 topology operation 由当前 observation 预测但不条件化 candidate action；在 planning 中同状态不同动作导致不同 attach/detach，当前图不可用。 |
| D6 可观测性/泄漏 | 4.0 | future graph/operation 只作 target；offline association 使用全轨迹可能把未来身份写入 target，需 causal teacher 对照。 |
| D7 数据可得性 | 3.5 | 仿真 graph labels 和 marker eval 可生成；ontology/association error/多接触标注成本未写。 |
| D8 算力/工程 | 3.5 | 规模和预算合理；动态图 executor、detector、JEPA planner 与 320 真机 trials 偏重。 |
| D9 可证伪性 | 4.0 | F1/rollout/success/无拓扑特异性/wrong edit/oracle 上界阈值明确。 |
| D10 基线强度 | 4.0 | OA/POT/object-JEPA/contact head/tactile/fixed/oracle/random 齐全。 |
| D11 消融充分性 | 4.0 | operator/contact/cycle/persistence/tracker/tactile/shuffle/edit/leak 均拆；action conditioning 缺失。 |
| D12 OOD/真机 | 4.0 | 多 operation、遮挡、同类物体与真机；跨 detector/contact noise 分轴尚弱。 |
| D13 复现性 | 3.0 | 无 graph ontology、edge/node ID 规则、operation precedence、版本/seed/artifact 清单。 |
| D14 CVPR 契合度 | 4.5 | 动态对象图与视觉预测表征具有明显 CVPR 价值。 |
| D15 风险/负结果 | 4.0 | offline association 泄漏、reversible view 与 topology benchmark 负产出明确。 |

平均分：**3.73/5.00**。关键门槛：D3=4.0、D5=2.5、D6=4.0、D9=4.0。当前有可修复的技术 fatal flaw。

## Top 问题

1. **fatal-in-r00 — graph transition 缺 action 条件**：同一 graph 下 grasp/avoid/release 等候选动作产生不同下一 operation；不输入 action 的 operator 只能预测行为数据均值，不能用于候选规划。
2. **major — ontology 不一致**：attach/detach 是 edge operation；merge/split 是 node/view operation；transfer 可能是两条 ownership edge 更新。混在单一 CE label 会产生并发/优先级歧义。
3. **major — “正确 identity 已知”与 full-trajectory target 冲突**：若未来 association 赋予稳定 ID，student 可能被一个部署不可达的完美 teacher 隐式解难。

## 最近邻冲突与证据缺口

- [OA-WAM 2605.06481v1](https://arxiv.org/abs/2605.06481) / [POT-VLA 2607.18016](https://arxiv.org/abs/2607.18016) 是 persistent object 表示强基线。
- [ContactWorld 2606.13877](https://arxiv.org/abs/2606.13877)、[ViTacWorld 2607.22530](https://arxiv.org/abs/2607.22530) 覆盖 contact/tactile world modeling；需核查它们是否已有 contact graph/attachment 状态。
- Action-conditioned graph networks、neural relational inference、object-centric dynamics 与 manipulation scene graph 是直接邻域，当前 related work 不完整。

## 必须修改的动作

1. 画出 `current graph + candidate action -> distribution over concurrent graph edits -> future graph/latent -> candidate cost`；部署表增加 candidate action。
2. 定义 typed graph ontology 和 edit algebra：edge attach/detach/ownership、compound view、并发 edits、合法性约束与 cycle；不要用一个互斥 CE 处理全部。
3. 将 current/past-only association teacher 作为主监督，full-trajectory teacher 仅 oracle；量化两者 gap 和 ID noise。
4. 加入 wrong-action/right-edit、right-action/wrong-edit 2×2 干预，证明 graph update 而非动作标签本身驱动 planning。

## Round 02 验收条件

- [ ] operator 明确条件化 candidate action，planner 信息图闭合。
- [ ] typed edit algebra 可处理并发和非法操作，label extractor 有伪代码。
- [ ] 主结果不用 full-trajectory association oracle，未来 teacher gap 单列。
- [ ] 最近邻表补 action-conditioned graph/object dynamics，并核查 ContactWorld/ViTacWorld 字段。
- [ ] refinement log 记录 fatal 修复并升为 r01。

