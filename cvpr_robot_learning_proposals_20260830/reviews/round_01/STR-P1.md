# Round 01 Review — STR-P1

- Proposal-ID: STR-P1
- Reviewed-Revision: r00
- File: `proposals/STR-P1_event_intent_reset/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / REVISE**（round<10；时间索引和 event 语义需修）

## 文件变更核验

r00 已把 reset 从模糊 gate 改为预测创新 likelihood ratio + CUSUM，包含假闪烁/低速真事件、false/miss/recovery 指标、oracle reset 与因果可见性表。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | intent persistence 的稳定—反应矛盾影响实时控制；缺跨任务事件频率与损失量化。 |
| D2 失败模式清晰度 | 4.0 | 目标移动/滑落/障碍/闪烁正负例明确；外部事件不一定等于最优 intent change。 |
| D3 创新性/最近邻 | 4.0 | 与 IntentVLA、PACE、REMAC、history memory 有清晰差异；change-point policy 相关工作待补。 |
| D4 机制因果闭环 | 3.5 | innovation→CUSUM→reset→恢复/success，含 false/miss controls；事件标签与 intent change 的因果关系未定义。 |
| D5 技术正确性 | 3.0 | predictor 预测下一帧，reset 实际只能在下一观测到达后发生；公式/表把 `t` 和 `t+1` 混写。`p(change)` 密度如何估计未说明。 |
| D6 可观测性/泄漏 | 4.0 | 干预时刻仅 target、episode ID 移除、future-mask/阳性对照齐全；event score 的实际时间戳需改。 |
| D7 数据可得性 | 4.0 | paired event/no-event 数据和真机机械事件可生成；label ontology/强度分布/发布协议缺失。 |
| D8 算力/工程 | 4.0 | 轻量 predictor、两档预算、跨模态抗噪合理；真机触发/外部 GT 同步开销未量化。 |
| D9 可证伪性 | 4.0 | recovery、false/miss、success、fixed/oracle 上界均有阈值。 |
| D10 基线强度 | 4.0 | forget gate、PACE、entropy、REMAC、oracle/always/never/random 齐全。 |
| D11 消融充分性 | 4.0 | innovation modality、CUSUM、posterior、threshold、history、label shuffle/反向干预齐全。 |
| D12 OOD/真机 | 4.5 | 16 tasks、四事件、真机 paired event；跨平台阈值/未见事件 OOD 需后续。 |
| D13 复现性 | 3.0 | 无 event intensity schema、likelihood estimator、clock/index 伪代码、版本/seed/artifact 清单。 |
| D14 CVPR 契合度 | 4.0 | 视觉时序表征与 change detection 是主机制，不只是控制工程。 |
| D15 风险/负结果 | 4.0 | 感知噪声、跨模态一致性与 stability-reactivity Pareto 负产出明确。 |

平均分：**3.87/5.00**。关键门槛：D3=4.0、D5=3.0、D6=4.0、D9=4.0；未达 hardened gate。

## Top 问题

1. **major — event label 不是 intent-change label**：目标小幅移动可能无需改 intent，抓取滑落可能只需局部 residual；用干预时刻监督会把所有 novelty 都定义成 reset。
2. **major — 时间索引错位**：预测 `o_{t+1}` 的残差必须在 `o_{t+1}` 到达后计算，随后才能影响 `a_{t+1}`；目前“全部≤t”说法隐藏一周期延迟。
3. **major — alternative intent support 未定义**：CUSUM 超阈值之外还要求当前观测支持替代 intent，但没有候选 intent、posterior 或决策准则。

## 最近邻冲突与证据缺口

- [IntentVLA 2605.14712v2](https://arxiv.org/abs/2605.14712) 是固定历史 intent 强基线；需要精确复现其门控与 history latency。
- [PACE 2606.00537v2](https://arxiv.org/abs/2606.00537) 已用 phase transition 选 horizon；速度谷负控很好，但还需 change-point/novelty detector 文献。
- [Remember Smarter 2608.15269v1](https://arxiv.org/abs/2608.15269) 历史压缩可能自身带 learned forgetting，不能只当 memory encoder。

## 必须修改的动作

1. 把 event 定义为“在相同当前 observation 下，保持旧 intent 的最优 value 比重规划下降超过 δ”，并区分 environment novelty、control failure、intent change 三标签。
2. 重写时间图：`prediction at t-1 -> observation/residual at t -> reset decision -> action at t`，报告 detection-to-action 延迟。
3. 形式化 alternative intent candidates/posterior，加入“novelty 但无需 reset”和“无强视觉 novelty但必须 reset”两类 hard pairs。
4. false/miss 指标按 event prevalence 和 severity 分层，避免 0.5/1000 的任意阈值主导。

## Round 02 验收条件

- [ ] event 与 intent-change 的 oracle/label 操作定义分开且可生成。
- [ ] 所有公式与表使用一致时间索引，并计入一周期检测延迟。
- [ ] alternative intent support 可计算，hard pairs 至少各三类。
- [ ] 最近邻表补 change-point/novelty policy 工作并逐项对比 IntentVLA/PACE/Remember Smarter。
- [ ] refinement log 记录修改并升为 r01。

