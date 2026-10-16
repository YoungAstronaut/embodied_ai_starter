# Round 08 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r07
- File: `proposals/GEO-P1_counterfactual_geometry/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已修正8192 steps/pair、163.84M上限与1.28GB/1.19GiB，并加入smoke→MVP→ICC、lineage/group dedup及model-grid分账；R7资源P0解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 几何捷径重要。 |
| D2 失败模式清晰度 | 4.5 | causal/nuisance pair清楚。 |
| D3 创新性/最近邻 | 4.0 | relation-SCM增量待实证。 |
| D4 机制因果闭环 | 4.5 | pair→selection闭合。 |
| D5 技术正确性 | 4.5 | 资源与方法公式已一致。 |
| D6 可观测性/泄漏 | 4.5 | checker字段隔离强。 |
| D7 数据可得性 | 4.0 | 分阶段gate合理。 |
| D8 算力/工程 | 4.0 | 修正后可执行但仍重。 |
| D9 可证伪性 | 4.5 | OOD success不足会降级。 |
| D10 基线强度 | 4.5 | label-equal winner强。 |
| D11 消融充分性 | 4.5 | 2×2充分。 |
| D12 OOD/真机 | 3.5 | LIBERO/真机协议过于概括。 |
| D13 复现性 | 4.5 | lineage与单位已闭合。 |
| D14 CVPR契合度 | 4.0 | 控制外部效度决定上限。 |
| D15 风险/负结果 | 4.5 | benchmark降级有价值。 |

平均分：**4.27/5.00**。D3/D12未达门槛；round<10，不通过。

## OOD/真机攻击面

1. “四OOD轴”未列train/calibration/test取值；未见texture、camera、asset、task和renderer domain不是同一概念。LIBERO-Plus也可能被VGA/VGGT预训练覆盖，不能自动称零样本OOD。
2. M64候选在新域的coverage可能下降；OOD success变化会混入proposer support，而非geometry token。每域必须报告CEM oracle coverage regret并按support分层。
3. “每任务30真机配对”未说明任务数、物理干预、block randomization和独立单位。真实系统无法exact-reset背景/目标位姿，必须称near-paired external validity。
4. 没有真机安全/停止接口；checker只生成离线label，不代表部署candidate安全。

## 修改与R9验收

1. 冻结OOD矩阵：每轴train levels、calibration levels、held-out levels、asset/renderer/task group；LIBERO仅domain-transfer secondary，并声明foundation pretraining不可审计的不确定性。
2. OOD逐域报告candidate coverage、fallback/unmappable率、conditional-on-support regret和episode success。
3. 真机设≥3 tasks、30 root templates/task，method顺序按root block随机，报告reset偏差；GT/marker只评测且不进RGB。
4. 加collision/force/workspace checker与emergency stop，真机只外部效度、无power则不声称控制确认。

R9需把论文主叙事限定为sim exact-intervention ranking；真机/LIBERO只作为有预注册边界的secondary，避免审稿人以“伪因果+伪OOD”攻击。
