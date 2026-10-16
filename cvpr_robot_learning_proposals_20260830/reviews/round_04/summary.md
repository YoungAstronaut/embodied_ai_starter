# Round 04 Summary — 技术正确性压力测试

- Review date: 2026-08-30
- Input revisions: 12/12 均为 r03，且 `Responds-To-Review: round_03`
- Refinement logs: 12/12 均含 `## round_03 / r03`
- Individual reviews: 12/12 已完成
- Round policy: round<10，全部 **FAIL / REVISE**
- Score range: 4.03–4.30

## 汇总表

| Proposal-ID | Revision | 平均分 | 关键低维 | Fatal flaw | R4结论 | 下一轮首要动作 |
|---|---:|---:|---|---|---|---|
| GEO-P1 | r03 | 4.13 | D5/D8=3.5 | 否（R3 fatal解除） | FAIL | 闭合离散`π*`与连续policy支持；置换不变token matching |
| GEO-P2 | r03 | 4.30 | D3/D5=4.0 | 否 | FAIL | survival/censor NLL；拆开fixed-candidate score与selection success |
| GEO-P3 | r03 | 4.30 | D3/D5=4.0 | 否 | FAIL | calibration-only固定coverage阈值；q/v一致decision rule |
| WAM-P1 | r03 | 4.03 | D4/D5=2.5 | **是** | FAIL / FATAL-IN-r03 | 分离referent R与assignment Z；修复恒为1的posterior |
| WAM-P2 | r03 | 4.30 | D3/D5=4.0 | 否 | FAIL | incremental age cost；cross-fit Bellman max偏差 |
| WAM-P3 | r03 | 4.30 | D3/D4/D5=4.0 | 否 | FAIL | predictive-space belief shift；部署input/监督target分离 |
| STR-P1 | r03 | 4.27 | D3/D5/D6=4.0 | 否 | FAIL | simultaneous max-ΔQ CI；删除deploy oracle coverage |
| STR-P2 | r03 | 4.30 | D5=3.5 | 否 | FAIL | 修正conformal guarantee；adaptive k后coverage；共享fallback |
| STR-P3 | r03 | 4.30 | D8=3.0 | 否 | FAIL | 3.28e8 env steps全预算；pair-local shared library；Q scale |
| JEP-P1 | r03 | 4.23 | D8=3.5 | 否 | FAIL | 多同类role-instance canonicalization；node/edge metric |
| JEP-P2 | r03 | 4.30 | D3/D5=4.0 | 否 | FAIL | transaction group置换不变；abstain risk-coverage |
| JEP-P3 | r03 | 4.13 | D4/D5=3.0 | **是** | FAIL / FATAL-IN-r03 | true-e conditional predictor与learned-q marginal objective分离 |

## Fatal 结论

### WAM-P1：assignment row sum不是referent posterior

当前每个track在任一合法assignment中必然“匹配某检测或miss”，因此`Σ_jA_mj+A_m,miss=1`。正文据此定义的`w_m^+`对所有m恒为1。更严重的是每个assignment都乘完整`∏_m w_m^-`，这是assignment无关常数，会在归一化时消掉。必须显式建模referent变量R与多目标assignment Z并边缘化`p(R,Z|D)`；只验证七个assignment概率和为1不能验出该错误。

### JEP-P3：错误e标签污染条件分布

真实cell target来自`e_true`，却有2/3 batch把q-sampled/corrupted `e'`作为predictor条件并仍对`Y(e_true)`做NLL。最小例`Y=e`表明这会把本应确定的`P(Y|e)`训练成混合分布，主动抹平`f_e/f_ae`。条件factorial predictor只能用true-e cell；learned-q鲁棒性必须通过`∫p(Y|a,e)q(e|h)de`的边缘化或planner层distillation处理。

## 已解除的前轮问题

1. GEO-P1 的 checker relation type不再进入student：主结果使用部署预测soft type/no-type，checker type只target/oracle，R3 fatal解除。
2. WAM-P2 已把myopic VOC升级为finite-horizon continuation value，`Y=[0,-1,4]`反例方向正确。
3. STR-P1 deployed gate已直接使用paired reset value，不再以intent probability替代utility。
4. STR-P2 继续保持标准chunk-flow与SFP physical streaming的时间/输出对象分离。
5. STR-P3 的连续policy/离散Q支持错配已通过M=64 retrieval闭合，且AliasBench公开commit审计artifact真实存在。

## 跨Proposal技术共性

1. **归一化通过不等于posterior正确。** WAM-P1说明“概率和为1”只能检查形式，必须在非均匀prior/可辨识likelihood上验数值方向。
2. **target与student必须共享estimand，不是共享字段。** GEO-P1的离散有效动作分布与连续flow、JEP-P3的true-e cell与corrupted-e输入都出现测度/support错位。
3. **选择后不确定性需重校准。** STR-P1的max候选CI、STR-P2的max-k deadline、GEO-P3的fixed coverage均涉及adaptive selection；单候选/单阈值coverage不能直接沿用。
4. **“固定动作”与closed-loop success不能同时含混。** GEO-P2/JEP-P2中wrong intermediate variable若改变最终selection，则实际执行动作并不固定；应拆成score intervention与selection intervention。
5. **新支持域会重写算力账。** STR-P3为每pair补齐64-action Q后，主数据约327.68M env steps，必须重新go/no-go。

## Round 05 统一验收条件 — 实验与可证伪性

1. 先解除WAM-P1/JEP-P3两个fatal，并用最小数值例而非措辞证明。
2. 每份锁定一个primary endpoint、统计单元、最小效应、CI/多重比较与明确kill criterion；不得用多个次指标补救主失败。
3. oracle upper bound、故意错误intervention与最强同预算baseline必须在同一candidate/data/latency切片。
4. adaptive selection后的coverage/CI需要独立calibration或simultaneous guarantee。
5. 数据/算力乘法账要覆盖rejected samples、oracle calls、all candidates/seeds/horizon、存储和端到端wall-clock。

## Round 05 优先级

- **P0**：WAM-P1、JEP-P3（公式fatal）。
- **P1**：GEO-P1、STR-P1、STR-P2、STR-P3（support/selection/成本）。
- **P2**：GEO-P2、GEO-P3、WAM-P2、WAM-P3、JEP-P1、JEP-P2（实验合同前的技术细化）。

