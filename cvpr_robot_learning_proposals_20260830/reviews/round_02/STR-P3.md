# Round 02 Review — STR-P3

- Proposal-ID: STR-P3
- Reviewed-Revision: r01
- File: `proposals/STR-P3_counterfactual_history/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / REVISE**（无 fatal；strict causal pairs相对普通history encoder有清楚增量）

## 实际变更核验

r01 已把主claim限制为双合法rollout physical pairs，以S=8交叉value sets替代demo distance，state-edit/commitment降级，加入reachability hashes、acceptance与历史模态controls/BeT。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | history aliasing是长期VLA核心。 |
| D2 失败模式清晰度 | 4.5 | 双可达历史+交叉不兼容value sets很强。 |
| D3 创新性/最近邻 | 4.0 | 相对IntentVLA/Remember/BC的新对象是严格paired causal supervision；更广causal-sequence邻域待补。 |
| D4 机制因果闭环 | 4.5 | pair→history belief→swap→value set/success，模态controls全面。 |
| D5 技术正确性 | 4.0 | demo-style错误已修；Q-set估计方差和loss符号待R4。 |
| D6 可观测性/泄漏 | 4.5 | hidden/Q只oracle、合法history可部署。 |
| D7 数据可得性 | 4.0 | acceptance go/no-go与rejection字段明确。 |
| D8 算力/工程 | 3.5 | 20k pairs×actions×8 seeds与真机near-match成本高。 |
| D9 可证伪性 | 4.5 | cross-value、modal controls、random contrastive/oracle判负强。 |
| D10 基线强度 | 4.5 | Intent/Remember/BeT/Diffusion/long-window/oracle全面。 |
| D11 消融充分性 | 4.5 | pair type/reachability/tolerance/history modalities/leak全面。 |
| D12 OOD/真机 | 4.0 | asset/seed/natural AliasBench/真机near-match；机制OOD仍需分轴。 |
| D13 复现性 | 3.5 | hash/tolerance/acceptance增强；仍缺版本/seed/schema artifact。 |
| D14 CVPR 契合度 | 4.0 | visual temporal representation与paired benchmark明确。 |
| D15 风险/负结果 | 4.5 | feasibility<10%也能形成benchmark边界。 |

平均分：**4.17/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；未过 hardened gate/mean。

## Top 问题

1. **major — pair construction可能是主要贡献而训练loss只是常规ranking**：应诚实定位为 Counterfactual-Alias benchmark/supervision，而不是声称新history architecture。
2. **major — IntentVLA AliasBench的真实重叠尚未正文级量化**：[IntentVLA 2605.14712v2](https://arxiv.org/abs/2605.14712) 已显式研究alias；必须统计其是否已有same-current/different-history或近似pairs。
3. **major — 与causal representation/sequence counterfactual data工作未比**：仅加BeT解决multimodal BC，不覆盖paired causal supervision邻域。

## 具体修改动作

1. 将主贡献顺序写为 benchmark/generator→paired supervision→architecture-agnostic gain；至少在IntentVLA和普通transformer两种backbone验证。
2. 对AliasBench逐项审计当前帧匹配、history控制、value incompatibility、字段泄漏，给overlap table。
3. 补counterfactual sequence/causal representation/data-pairing邻域；明确本方案是机器人POMDP value-set特化。
4. 将only-video贡献设为必要claim gate，full history若只靠actions不得称视觉history辨识。

## Round 03 验收条件

- [ ] 贡献定位以paired benchmark/supervision为主，非新encoder命名。
- [ ] AliasBench overlap有可量化表和审计脚本计划。
- [ ] 至少两个history backbone共享pairs，架构增益与数据增益分开。
- [ ] Q-set/future oracle信息路径与only-video必要门槛明确。

