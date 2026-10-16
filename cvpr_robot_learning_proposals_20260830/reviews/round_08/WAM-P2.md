# Round 08 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r07
- File: `proposals/WAM-P2_value_of_imagination/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已统一primary S16、将S4/8/32改为nested bias，补WAM/model-grid/validation账、40/10/10 split与吞吐输出；R7技术/资源矛盾解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 计算价值部署重要。 |
| D2 失败模式清晰度 | 4.5 | non-myopic/harmful compute明确。 |
| D3 创新性/最近邻 | 4.0 | paired visual VOC是有限增量。 |
| D4 机制因果闭环 | 4.5 | CRN→continuation→gate闭合。 |
| D5 技术正确性 | 4.5 | S16与资源现一致。 |
| D6 可观测性/泄漏 | 4.5 | target-only严格。 |
| D7 数据可得性 | 4.0 | task split清楚。 |
| D8 算力/工程 | 4.0 | gate可执行但full很重。 |
| D9 可证伪性 | 4.5 | success/oracle/prevalence判负明确。 |
| D10 基线强度 | 4.5 | winner+myopic closed test强。 |
| D11 消融充分性 | 4.5 | target×stopping完整。 |
| D12 OOD/真机 | 3.5 | 真机仅“校准gate”，无独立评测协议。 |
| D13 复现性 | 4.5 | CRN/模型账已闭合。 |
| D14 CVPR契合度 | 4.5 | WAM与实时控制契合。 |
| D15 风险/负结果 | 4.5 | feasibility-only降级合理。 |

平均分：**4.33/5.00**。D3/D12未达门槛；round<10，不通过。

## OOD/真机攻击面

1. 40/10/10 unseen tasks未说明来自同benchmark template还是跨benchmark；task OOD、WAM model-error OOD和hardware jitter应分轴。
2. “真机只校准gate”没有calibration/test隔离和trial数；若同任务调threshold再评估，不能称外部效度。没有真机counterfactual target也意味着只能测closed-loop Pareto。
3. resource λ、deadline chance与continuation head可能随硬件漂移；新hardware若重校准，就不是zero-shot hardware OOD。
4. fallback或k=0路径可能贡献主要success；需按selected K、deadline/miss和fallback分层。

## 修改与R9验收

1. 冻结OOD矩阵：held-out task template、held-out WAM checkpoint/error family、held-out device trace，分别报告；不混成一个平均。
2. 真机至少calibration tasks与held-out evaluation tasks分离，给root trials/method顺序/资源预算；只报success-latency-energy Pareto，不声称真机VOC target被验证。
3. zero-shot hardware表保持λ/threshold冻结；50-shot/recalibration另表。
4. 报K=0…4选择率、fallback-only、conditional success、deadline/energy和age strata；fallback dominance触发compute-scheduler降级。

R9应把“paired continuation target in simulation”与“real-time gate transfer”拆成两个claim，避免真机target不可得被审稿人一票否决。
