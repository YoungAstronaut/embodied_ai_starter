# Round 04 Review — STR-P3

- Proposal-ID: STR-P3
- Reviewed-Revision: r03
- File: `proposals/STR-P3_counterfactual_history/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / REVISE**（Q support与官方audit已闭合；新离散库造成未记账的大规模仿真成本）

## 实际变更核验

r03 已将action head改为M=64同库检索分布，每个sampled action都有Q target；加入CEM512 coverage阈值。官方IntentVLA commit `6d513c...`、`audit_aliasbench.py`和报告均实际存在，静态AST结果确为12 task files/46 trace calls/四个keyword字段，并明确未运行RoboTwin。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | history aliasing根本且重要。 |
| D2 失败模式清晰度 | 4.5 | 双可达/same-current/cross-value严格。 |
| D3 创新性/最近邻 | 4.5 | 当前公开AliasBench commit未覆盖strict合同，边界已有实际证据。 |
| D4 机制因果闭环 | 4.5 | pair→全库Q→retrieval→swap/success闭合。 |
| D5 技术正确性 | 4.5 | 连续policy/Q支持错配已解除。 |
| D6 可观测性/泄漏 | 4.5 | future/state仅target，audit边界诚实。 |
| D7 数据可得性 | 4.0 | 可生成但acceptance/库覆盖仍有风险。 |
| D8 算力/工程 | 3.0 | 20k pairs×2 states×64×8×16≈327.68M env steps，正文未记账。 |
| D9 可证伪性 | 4.5 | 两backbone/only-video/coverage/audit kill criteria强。 |
| D10 基线强度 | 4.5 | IntentVLA/Remember/BeT/普通Transformer充分。 |
| D11 消融充分性 | 4.5 | 模态/pair/backbone/泄漏拆分完整。 |
| D12 OOD/真机 | 4.0 | 自然transfer和near-match边界合理。 |
| D13 复现性 | 4.0 | commit/script/report冻结；candidate生成细节仍缺。 |
| D14 CVPR 契合度 | 4.5 | benchmark+视觉历史+控制强。 |
| D15 风险/负结果 | 4.5 | feasibility/audit负结果有价值。 |

平均分：**4.30/5.00**。D8=3.0；round<10且并非全维≥4，R4不通过。

## Top 问题与技术证据

1. **major/feasibility — 成本扩大约64倍却未重算。** 目标10k relevant+10k irrelevant pairs，每pair有A/B两snapshot；每snapshot `64 actions×8 seeds×16 steps`，总计约327,680,000 env steps，尚不含CEM512 oracle与被拒pair。此前4×A100/5天预算已不可信。
2. **major — library是否全局固定不明确。** 全局64 chunks难覆盖跨task连续控制；若每state由proposer生成，A/B必须共享同一候选并冻结生成随机源，train/test coverage定义也需改变。
3. **technical — `L_cross`缺显式margin/normalization。** 不同task Q尺度会改变梯度；需要per-task固定reward scale或advantage normalization。
4. **audit边界。** AST只检查attribute call的keyword args，会漏位置参数、dict/serialized fields；报告已诚实称静态API审计，正文不可进一步升级成数据无泄漏证明。

## 具体修改动作

1. 给attempted/accepted全漏斗乘法账、sim steps/s/存储/CPU-GPU职责；先做≤2k pairs go/no-go或减少M/S并做方差/coverage曲线。
2. 明确candidate library生成：每pair共享的state-local library更可信；保存proposer seed/hash并对A/B完全相同。
3. Q转为有界advantage或按任务预注册scale，给2-task尺度反例。
4. 把CEM512调用计入总预算，且只作抽样oracle时说明抽样率。

## Round 05 验收条件

- [ ] 全数据含拒绝样本/CEM的真实乘法账与go/no-go预算。
- [ ] A/B共享candidate library的生成/seed/hash唯一。
- [ ] Q尺度/normalization使loss跨task可比。
- [ ] AliasBench结论继续限定静态公开commit，不外推私有数据。

