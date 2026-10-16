# Round 08 Review — GEO-P2

- Proposal-ID: GEO-P2
- Reviewed-Revision: r07
- File: `proposals/GEO-P2_contact_transition/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已补full公式、七类互斥漏斗、`contact_transition_v1`、smoke/ICC分离与100M cap；R7资源/标签复现缺口基本解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 接触预测重要。 |
| D2 失败模式清晰度 | 4.5 | typed event具体。 |
| D3 创新性/最近邻 | 4.0 | ContactGuard/World后边界仍需证明。 |
| D4 机制因果闭环 | 4.5 | action→field→selection闭合。 |
| D5 技术正确性 | 4.5 | censor/资源/schema一致。 |
| D6 可观测性/泄漏 | 4.5 | GT frame隔离。 |
| D7 数据可得性 | 4.0 | 两引擎可生成。 |
| D8 算力/工程 | 4.0 | cap与gate合理。 |
| D9 可证伪性 | 4.5 | regret/control降级明确。 |
| D10 基线强度 | 4.5 | native/equal充分。 |
| D11 消融充分性 | 4.5 | target×executor充分。 |
| D12 OOD/真机 | 4.0 | 三任务×100较强，域语义仍未闭合。 |
| D13 复现性 | 4.5 | ontology与字段来源具体。 |
| D14 CVPR契合度 | 4.5 | 视觉接触与操作契合。 |
| D15 风险/负结果 | 4.5 | ontology-only降级清楚。 |

平均分：**4.37/5.00**。D3/D12仍未过关键门槛；round<10，不通过。

## OOD/真机攻击面

1. 材质/摩擦OOD没有train/test数值区间；跨引擎的force、stick/slide与normal定义不同，`contact_transition_v1`不能假设语义天然一致。
2. support≥90%只应约束candidate action，不应要求OOD材质/asset重合；正文需要分开action-support和environment shift。
3. 真机标签用torque+vision，而仿真用contact manifold/force；500帧人工audit需输出mode/onset/normal各自一致性，不是单一accuracy。
4. detector/GFM failure fallback可能贡献大部分安全收益；必须报fallback-only、conditional non-fallback及其频率。插入/抽屉/刮刀还需force/velocity安全阈值。

## 修改与R9验收

1. 冻结sim1/sim2/real语义映射与单位、材质/摩擦train/cal/test bins；跨引擎阈值只用各自train fit。
2. 分别报告candidate support、environment OOD和detector failure strata。
3. 真机按task×root template配对随机方法顺序；500帧按事件类型分层双标，给κ/MAE/CI与同步误差。
4. 加force/torque/velocity/workspace abort，所有方法共享；fallback率>预设阈值时只称安全router/ontology，不称field planning。

R9需在摘要/贡献中把“无触觉部署”限定为主结果的输入合同，并把跨引擎/真机写成语义迁移压力测试而非同分布复现。
