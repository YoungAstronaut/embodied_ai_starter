# Round 05 Review — STR-P2

- Proposal-ID: STR-P2
- Reviewed-Revision: r04
- File: `proposals/STR-P2_deadline_anytime_flow/proposal.md`
- Checked: 2026-08-30
- Round focus: 实验设计、统计与可证伪性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r04 已改per-k/Mondrian α/4 marginal quantile+union bound，并做selected-policy replay；fallback全baseline共享且另报no-fallback，mode cluster在teacher train上冻结。R4问题已实质解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 | 4.5 | deadline控制重要。 |
| D2 | 4.5 | burst反例清楚。 |
| D3 | 4.0 | 组合创新待证。 |
| D4 | 4.5 | scheduler/CAS闭合。 |
| D5 | 4.5 | conformal表述已诚实。 |
| D6 | 4.5 | 无future trace。 |
| D7 | 4.0 | trace可得。 |
| D8 | 4.0 | 系统可实现。 |
| D9 | 4.0 | success/miss/jerk/violation/MMD多重合取，primary未锁。 |
| D10 | 4.5 | 同对象baseline强。 |
| D11 | 4.5 | 消融充分。 |
| D12 | 4.5 | unseen jitter/真机强。 |
| D13 | 4.0 | trace schema好，统计unit缺。 |
| D14 | 4.5 | 契合CVPR。 |
| D15 | 4.5 | benchmark负价值强。 |

平均分：**4.33/5.00**。D3/D9=4.0；round<10，R5不通过。

## 实验攻击面

1. **无唯一primary。** 至少五个门槛可导致部分成功；H1最直接是预注册resource constraint下closed-loop success。
2. **mean/p95±5%后验匹配。** 不同方法compute分布可能不重叠；应在validation选统一deadline/预算，而不是test切片。
3. **trace伪重复。** 同一5-cycle burst内episode相关，3 seeds不足以表示device/time trace变化；trace block应是cluster。
4. **“至少三种unseen traces”多重比较。** 要求每种都过、macro过或任意三种过需明确。

## 修改与R6验收

1. validation冻结一个deadline/energy budget，primary为该预算下episode success；miss/jerk是安全约束，MMD机制secondary。
2. 所有baseline在同trace replay、同observation、同随机动作环境paired运行。
3. 按trace-block×episode cluster CI，预注册unseen trace families与macro/最坏组规则。
4. 多重比较对最强fixed/multi-exit baseline用闭合检验；不从多个k/trace挑最好test结果。

