# Round 03 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r02
- File: `proposals/WAM-P1_occlusion_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（信息隔离合格；Bayes/association 更新存在重复计证据歧义）

## 实际变更核验

r02 已把 OA-WAM/POT/3D-ALP 写成正文级对象，加入 MHT、SCALOR/SAVi、ReferFormer 与 `JPDA+same WAM+language anchor`，并把 identifiability proof 放入 evaluator-only 独立 shard。多假设状态、unknown mass、冻结 Hungarian 对齐和 passive/active 分解均实际存在。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 长遮挡 referent 身份错误是持久对象 WAM 的直接失败。 |
| D2 失败模式清晰度 | 4.5 | identifiable/partial/symmetric 三档及 switch/control 后果清楚。 |
| D3 创新性/最近邻 | 4.0 | 多假设 tracking 不新；增量是 action/contact likelihood 与 marginal control 的机器人组合。 |
| D4 机制因果闭环 | 4.0 | evidence→posterior→marginal action 链完整，但 likelihood 更新公式有歧义。 |
| D5 技术正确性 | 3.5 | `A_mj` 若由 `ℓ_mj` 得到，再乘 `A_mjℓ_mj` 会重复计同一证据。 |
| D6 可观测性/泄漏 | 4.5 | future identity/GT matching 只作 target/metric，proof shard schema隔离明确。 |
| D7 数据可得性 | 4.0 | exact-reset identity 数据可生成；真机 referent GT 依赖外部 marker。 |
| D8 算力/工程 | 4.0 | M≤4+residual 可控，M=8 覆盖消融合理。 |
| D9 可证伪性 | 4.5 | JPDA组合、likelihood删除、belief shuffle 与 symmetric proper scoring 强。 |
| D10 基线强度 | 4.5 | 经典 tracker、probabilistic slot、language tracker 与当前 WAM 均覆盖。 |
| D11 消融充分性 | 4.5 | likelihood、contact、covariance、M、active/passive 均可分解。 |
| D12 OOD/真机 | 4.0 | 真实同类物体有外效度，需按 detector recall/identifiability 分层。 |
| D13 复现性 | 3.5 | 缺 association matrix、miss/false列与 frozen matching 的数值伪代码。 |
| D14 CVPR 契合度 | 4.5 | 视觉跟踪、不确定性与机器人控制结合紧密。 |
| D15 风险/负结果 | 4.5 | 对称不可辨识和 tracker+WAM 退化均被诚实承认。 |

平均分：**4.20/5.00**。D3=4.0、D5=3.5、D6=4.5、D9=4.5；round<10 且 D5 未过硬门槛，R3 不通过。

## Top 问题与证据缺口

1. **major/technical — association evidence 可能被重复计算。** 正文先用 learned likelihood 形成 Sinkhorn `A_mj`，再写 `w_m^+∝w_m^-Σ_j A_mjℓ_mj`。若 `A` 已由同一 `ℓ` 归一化，乘回 `ℓ` 等于平方似然，posterior 过度自信，直接损坏 calibration 主张。
2. **major — proper scoring 的事件空间未完全定义。** `NLL=-logΣ_m w_m1[anchor_m=referent_GT]` 未明确 unknown/none、top-M residual、missed detection 和多个 component 对同一物体时如何计分；symmetric 档的理论均匀分布也应定义在可交换 orbit 上。
3. **minor — GT Hungarian 的用途需拆开。** 遮挡前 GT trajectory matching 可用于 evaluator/target label，但不得成为部署 anchor 初始化；当前文字容易把 metric matching 与 student anchor 构造混读。

## 具体修改动作

1. 给出标准 generative JPDA 更新：明确 assignment posterior 的未归一化因子、Sinkhorn 只作近似归一还是独立 proposal；每个 measurement likelihood 只能使用一次。用小型 2-track/2-detection 数值例验证概率和为1。
2. 定义完整 outcome space `{candidate identities, unknown/none, residual}` 及 log score/Brier；在 symmetric orbit 上给 oracle entropy 与 excess NLL。
3. 画清 deploy anchor（pre-occlusion detector/language）与 evaluator Hungarian（GT-only）的两条路径，并用 schema 阻止 GT trajectory 进入 model loader。
4. 增加 posterior sharpness/coverage 检查，防止平方似然看似降低 switch 却 ECE 恶化。

## Round 04 验收条件

- [ ] association posterior 有不重复计证据的归一化公式和数值单测。
- [ ] unknown/residual/missed/false/symmetric orbit 的 proper score 全部定义。
- [ ] deploy anchor 与 evaluator matching 明确分离，GT schema test 可执行。
- [ ] calibration 指标能捕捉过度自信而非只看 ID switch。

