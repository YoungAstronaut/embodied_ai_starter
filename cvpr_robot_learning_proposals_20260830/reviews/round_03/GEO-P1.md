# Round 03 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r02
- File: `proposals/GEO-P1_counterfactual_geometry/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / FATAL-IN-r02**（`type_embedding` 来源未闭合，按现文可能直接使用 simulator checker 类型）

## 实际变更核验

r02 的确加入 CofactVLA/CAST、`generic/geometry feature × generic/SCM deconfounding` 2×2、token permutation、动作码本 coverage-regret，并清理了旧 loss 名。该修改实质回应 R2，而非只补引用。新问题出现在方法内部：checker 输出 typed entity pair，随后 relation adapter 直接拼接 `type_embedding`；正文只说明 mask 在部署时来自 detector，却没有说明 type 的部署来源。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 区分几何因果依赖与一般视觉去偏仍重要。 |
| D2 失败模式清晰度 | 4.5 | nuisance/causal/hard-negative 与 exact-reset checker 已形成可观察反例。 |
| D3 创新性/最近邻 | 4.0 | 已承认 CofactVLA/CAST；可保留增量收缩为 task-relation geometry intervention。 |
| D4 机制因果闭环 | 3.5 | token swap、directional KL 与动作 JS 尚未排除 oracle type/selection 作为旁路。 |
| D5 技术正确性 | 4.0 | 方向分布和码本近似已修；`L_swap` 在“诊断”与训练 loss 中的角色仍矛盾。 |
| D6 可观测性/泄漏 | 3.0 | `type_embedding` 可能来自 full-state checker；若进入 student 即是部署不可得 oracle。 |
| D7 数据可得性 | 4.0 | 接受率、unmappable 分层和动作码本审计可执行。 |
| D8 算力/工程 | 3.5 | checker 枚举和成对缓存仍缺具体吞吐/存储预算。 |
| D9 可证伪性 | 4.5 | 2×2、置换、coverage-regret 与明确判负较强。 |
| D10 基线强度 | 4.5 | VGA/GAM/MECo/ST-VLA/CofactVLA/CAST 已进入同预算比较。 |
| D11 消融充分性 | 4.0 | 关键 2×2 已有；缺 relation-type 来源与 pair-selection 正交消融。 |
| D12 OOD/真机 | 4.0 | 四轴 OOD 和真机外效度保留，但 type parser 的 OOD 未覆盖。 |
| D13 复现性 | 3.5 | 缺 typed relation schema、字段 provenance 与 accepted/rejected manifest。 |
| D14 CVPR 契合度 | 4.0 | 视觉几何表征与机器人因果诊断契合。 |
| D15 风险/负结果 | 4.5 | 标签噪声、拒绝率和退化为一般去偏均有价值。 |

平均分：**3.97/5.00**。D3=4.0、D5=4.0、D6=3.0、D9=4.5；存在 D6 fatal，R3 不通过。

## Top 问题与证据缺口

1. **fatal — relation type 的 provenance 断裂。** 当前链条是 `simulator checker → typed entity pair → relation adapter[type_embedding] → action`。只有 entity masks 被明确替换成部署 detector；type 没有同样的部署定义。即使 GT type 只用于 pair 生成，只要 embedding 仍来自 checker，主结果就是 oracle-conditioned policy。
2. **major — oracle 筛选可形成选择捷径。** `Y*`/full-state checker 决定哪些 pair 被接受，模型可能从被筛选后的像素分布学习 acceptance/collider 线索。现在没有与 accepted pair 匹配的 rejected-but-observationally-similar 控制。
3. **major — `L_swap` 合同不一致。** 总损失包含 `λ4 L_swap`，但后文又把 swap 称作 diagnosis。若训练 swap 的 token 由 target `G_task` 选择，它还可能通过 token index 泄漏 relation identity。

## 具体修改动作

1. 画字段级 DAG，并为 relation type 二选一：部署时由语言+当前 detector/GFM 预测 soft type distribution；或彻底删除 type input，只把 checker type 当 stop-gradient target。为 loader 加 schema test，禁止 checker type/id 进入 student batch。
2. 增加三组控制：predicted-type、no-type、oracle-type（仅上界）；主结果只能用前两者。故意把 checker type 喂给 student 应出现异常跃升并被标为泄漏阳性。
3. 对 accepted/rejected pair 做相同 RGB/objectness/detector-confidence/码本覆盖匹配；训练仅用 accepted，评估 acceptance classifier 是否能从 nuisance 统计预测，AUROC 过高则说明筛选偏差。
4. 明确 `L_swap` 是训练项还是纯评测；若训练，token selector 必须只读部署可得变量并 stop-gradient，另报 target-selected oracle swap。

## Round 04 验收条件

- [ ] relation type 的训练、部署、target 来源逐字段闭合，主 student 不读 checker type。
- [ ] predicted/no/oracle type 三档与 schema rejection test 落入正文。
- [ ] pair-selection 偏差有 matched rejected control 与 AUROC 审计。
- [ ] `L_swap` 的 token selector、梯度和部署角色唯一且可实现。

