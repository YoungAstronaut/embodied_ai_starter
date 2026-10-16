# Round 08 Review — JEP-P1

- Proposal-ID: JEP-P1
- Reviewed-Revision: r07
- File: `proposals/JEP-P1_action_equivalence/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已冻结H16，闭合S32 16.384M steps、S8 prefix、240k OT records/13.44MB，并加入exact OT/cache、8-day gate与family split；R7资源缺口解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | action-effect metric有价值。 |
| D2 失败模式清晰度 | 4.5 | proxy/metric失败明确。 |
| D3 创新性/最近邻 | 4.0 | Action-Bisim边界仍窄。 |
| D4 机制因果闭环 | 4.5 | metric→ranking闭合。 |
| D5 技术正确性 | 4.5 | OT/ground metric一致。 |
| D6 可观测性/泄漏 | 4.5 | UUID/future隔离。 |
| D7 数据可得性 | 4.0 | 两sim与S gate可行。 |
| D8 算力/工程 | 4.0 | 资源已闭合但重。 |
| D9 可证伪性 | 4.5 | direct baseline/控制降级明确。 |
| D10 基线强度 | 4.5 | native/adapter强。 |
| D11 消融充分性 | 4.5 | metric×JEPA+target充分。 |
| D12 OOD/真机 | 4.0 | 3×6×80较具体，跨embodiment边界未冻结。 |
| D13 复现性 | 4.5 | OT/lineage具体。 |
| D14 CVPR契合度 | 4.0 | 需控制/迁移证据。 |
| D15 风险/负结果 | 4.5 | representation-only产出明确。 |

平均分：**4.30/5.00**。D3/D12未达最终门槛；round<10，不通过。

## OOD/真机攻击面

1. primary明确是单平台；跨embodiment只能secondary。若canonical adapter在target embodiment用target outcome训练，就不是zero-shot embodiment OOD。
2. object/camera/embodiment拆分需区分：新camera、新asset、新robot morphology分别报告，不能以一个macro掩盖失败。
3. 真机3 tasks×6 perturbations×80 reset groups较强，但“安全微扰”幅度、方法顺序、outcome GT和root unit未定义。
4. role assignment coverage在新embodiment可能崩溃；需把abstain/fallback与conditional ranking分开，防只在容易assigned states有效。

## 修改与R9验收

1. 冻结adapter regimes：target-free zero-shot、train-only morphology adapter、few-shot分别成表；主claim不混。
2. 分轴报告asset/camera/morphology OOD及canonicalizer coverage/error。
3. 真机root state为cluster，方法/扰动顺序随机；定义SE(3)/contact/collision GT、force/workspace stop与最大扰动。
4. 报abstain/fallback-only、conditional regret和assignment strata；coverage<90%严格判负。

R9必须把“pseudometric本身不新”写在related work/贡献前排，主张只保留视觉JEPA matched-outcome监督与canonicalization实证。
