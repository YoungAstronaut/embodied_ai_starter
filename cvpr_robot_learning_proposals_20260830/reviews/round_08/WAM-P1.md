# Round 08 Review — WAM-P1

- Proposal-ID: WAM-P1
- Reviewed-Revision: r07
- File: `proposals/WAM-P1_occlusion_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已闭合episode×frame×detector/beam/WAM资源，冻结det/track/M/beam，操作化4!×8 rerender proof、family split及tag裁除/同步审计；R7复现缺口基本解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 长遮挡身份belief重要。 |
| D2 失败模式清晰度 | 4.5 | 三strata清楚。 |
| D3 创新性/最近邻 | 4.0 | JPDA后增量待证。 |
| D4 机制因果闭环 | 4.5 | belief→marginal control闭合。 |
| D5 技术正确性 | 4.5 | posterior/proof定义稳定。 |
| D6 可观测性/泄漏 | 4.5 | tag/evaluator隔离增强。 |
| D7 数据可得性 | 4.0 | 50k与proof gate可行。 |
| D8 算力/工程 | 4.0 | beam cap明确。 |
| D9 可证伪性 | 4.5 | L11/控制降级清楚。 |
| D10 基线强度 | 4.5 | 近同构JPDA强。 |
| D11 消融充分性 | 4.5 | evidence×decision完整。 |
| D12 OOD/真机 | 4.0 | family split和4×100较好，极端域仍欠。 |
| D13 复现性 | 4.5 | proof code/lineage具体。 |
| D14 CVPR契合度 | 4.5 | 视觉身份与控制结合强。 |
| D15 风险/负结果 | 4.5 | 可辨识边界有独立价值。 |

平均分：**4.37/5.00**。D3/D12未全达最终门槛；round<10，不通过。

## OOD/真机攻击面

1. 当前数据仅2/3同类实例，部署cap track8/M4；应有4+ objects/超过M的OOD，验证residual mass而不是只在训练支持内。
2. rerender pixel/percept likelihood相等只能证明数值近似，不是严格“provably symmetric”；论文应改称simulator-certified approximate symmetry并报告容差敏感性。
3. 真机AprilTag即使裁图，也可能通过反射、遮挡轮廓或重量变化影响观测/动力学；tag应在model不可见侧或独立overhead GT，并审计mask残留。
4. 4×100 paired trials未说明method顺序、occlusion trajectory block、detector failure/fallback和安全；belief controller抓错对象可能造成碰撞。

## 修改与R9验收

1. 加instance-count/M-support OOD：2/3 train，4–6 test；报告residual calibration、fallback与conditional success。
2. 全文把“provably symmetric”降为“simulator-certified ε-symmetric”，给ε sweep与proof failure atlas。
3. 真机以root trajectory×object set为block随机方法顺序；tag/overhead GT不进入model camera，报detector recall strata与同步误差。
4. 加workspace/collision/force guard与wrong-object abort；fallback-only和oracle detection单列。

R9需把主贡献排序为Occlusion-ID benchmark→calibrated referent posterior→control secondary，主动化解“只是JPDA+WAM”的攻击。
