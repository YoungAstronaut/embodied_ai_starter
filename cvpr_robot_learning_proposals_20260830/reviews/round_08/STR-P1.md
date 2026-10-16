# Round 08 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r07
- File: `proposals/STR-P1_event_intent_reset/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已分账history/640 target/Hrec，加入root_snapshot lineage、10/3/3 task split与smoke/ICC分离；R7资源与cluster问题解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 事件后意图重置重要。 |
| D2 失败模式清晰度 | 4.5 | 四family+hard pairs具体。 |
| D3 创新性/最近邻 | 4.0 | change×value是有限增量。 |
| D4 机制因果闭环 | 4.5 | event→value→reset→recovery闭合。 |
| D5 技术正确性 | 4.5 | conformal/censor/resource一致。 |
| D6 可观测性/泄漏 | 4.5 | event GT/ΔQ仅target。 |
| D7 数据可得性 | 4.0 | 16-task split可行。 |
| D8 算力/工程 | 4.0 | 分段账合理。 |
| D9 可证伪性 | 4.5 | family-level降级明确。 |
| D10 基线强度 | 4.5 | native/equal winner强。 |
| D11 消融充分性 | 4.5 | change×value完整。 |
| D12 OOD/真机 | 4.0 | 4×100较好，但无family OOD/安全约束。 |
| D13 复现性 | 4.5 | root/task split具体。 |
| D14 CVPR契合度 | 4.5 | 视觉事件与控制强。 |
| D15 风险/负结果 | 4.5 | detector/Pareto产出明确。 |

平均分：**4.37/5.00**。D3/D12未全达门槛；round<10，不通过。

## OOD/真机攻击面

1. 10/3/3只形成task OOD，四event family仍全部见过。对unseen event正文只报empirical coverage是正确的，但摘要不能声称event-family generalization。
2. 可加入一类compositional held-out event（如双事件/延迟后果），但不能把Mondrian guarantee外推；只作stress test。
3. 真机4×100未定义root template、event severity/time、method顺序和GT同步。机械滑落/目标移位只覆盖两类，不覆盖false visual/jam。
4. primary RMRT没有collision/jerk硬安全约束；激进reset可能恢复更快但更危险。fallback/reset budget也可能主导。

## 修改与R9验收

1. 主claim限定seen-family cross-task；另设held-out compositional event empirical stress，不做coverage guarantee。
2. 真机按root trajectory/event block随机方法，至少覆盖visual false event与physical slip/shift；GT logger只评测。
3. 将collision rate、jerk和false-reset ceiling设为primary可行约束，所有方法共享force/workspace stop。
4. 报reset/fallback频率、conditional RMRT和matched-rate安全Pareto；安全约束不满足即只保留detector。

R9需把“不是change-point detector，而是reset-worthiness”作为唯一主线，并明确coverage只在seen Mondrian strata成立。
