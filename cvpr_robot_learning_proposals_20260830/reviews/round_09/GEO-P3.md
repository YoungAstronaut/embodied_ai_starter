# Round 09 Review — GEO-P3

- Proposal-ID: GEO-P3
- Reviewed-Revision: r08
- File: `proposals/GEO-P3_geometry_confidence/proposal.md`
- Checked: 2026-08-30
- Round focus: 论文主线与审稿攻击面
- Verdict: **FAIL / REVISE**

## 实际变更核验

r08 已前置reliability非省算，补LOFO/severity、coverage CI可行条件、route/fallback conditional、真机root/stop与atlas降级；R8 OOD/fallback攻击面已实质响应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | geometry rejection有部署价值。 |
| D2 失败模式清晰度 | 4.5 | bad relation/corruption明确。 |
| D3 创新性/最近邻 | 4.0 | selective routing既有，B target是增量。 |
| D4 机制因果闭环 | 4.5 | repair-B→risk→route闭合。 |
| D5 技术正确性 | 4.5 | coverage/repair/资源一致。 |
| D6 可观测性/泄漏 | 4.5 | validity/calibration/GT分开。 |
| D7 数据可得性 | 4.0 | repair gate合理。 |
| D8 算力/工程 | 4.0 | 非省算但成本已计。 |
| D9 可证伪性 | 4.5 | coverage/fallback硬失败。 |
| D10 基线强度 | 4.5 | generic/regret-only equal。 |
| D11 消融充分性 | 4.5 | supervision×structure强。 |
| D12 OOD/真机 | 4.5 | LOFO与root外测已闭合。 |
| D13 复现性 | 4.5 | repair/cell/route合同完整。 |
| D14 CVPR契合度 | 4.0 | 需正面承认三分支全算。 |
| D15 风险/负结果 | 4.5 | atlas降级有价值。 |

平均分：**4.33/5.00**。D3/D14未达门槛；round<10，不通过。

## 模拟审稿攻击

1. **“Three policies for a calibration paper is impractical.”** 正文第一句话就应写reliability selector而非efficiency；主表计总latency/energy，cheap router仅secondary。
2. **“Oracle repair labels create the result.”** same-B generic pooled head必须是最危险基线；B noise/acceptance曲线进正文。
3. **“Risk improves because the system stops.”** route/stop/fallback/progress utility与coverage可行条件必须在primary同表。

## 修改与R10验收

标题建议 **When Should Geometry Be Rejected? Relation-Aware Reliability for VLA Branches**。贡献不写“calibration guarantee”，只写validation-frozen selective risk。主图画三分支并行与target-only repair。R10需准备relation-B无效时的**Geometry Reliability Atlas**降级稿，并确保标题/摘要不暗示省算或distribution-free保证。
