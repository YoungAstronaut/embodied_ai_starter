# Round 03 Review — GEO-P2

- Proposal-ID: GEO-P2
- Reviewed-Revision: r02
- File: `proposals/GEO-P2_contact_transition/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（R1 fatal 持续解除；action-field-scorer 的梯度防串谋仍不充分）

## 实际变更核验

r02 确实补入 ContactGuard 以及 ContactWorld/TouchWorld/ViTacWorld/Where-to-Touch 的字段与版本状态，加入 latent-only/field-only/combined/oracle 四路，并把 N=8 batched runtime 写为 ≤100ms。主 DAG 仍是 proposer→candidate-conditioned contact field→scorer，未回退到无动作的场景预测。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 候选动作接触后果是操作规划中的核心缺口。 |
| D2 失败模式清晰度 | 4.5 | mode/time/normal/body-pair/censoring 的局部转移定义明确。 |
| D3 创新性/最近邻 | 4.0 | ContactGuard 压缩空间后，增量是 typed local transition field 对 ranking 的独立价值。 |
| D4 机制因果闭环 | 4.0 | action→field→score 链已闭合，但联合训练允许 field 退化为 action code。 |
| D5 技术正确性 | 4.0 | extractor 与 censoring 已定义；每候选 exact-reset 标签及 `L_cons` 仍需形式化。 |
| D6 可观测性/泄漏 | 4.5 | GT pose/contact/future 仅 target，部署 detector/GFM fallback 清楚。 |
| D7 数据可得性 | 4.0 | 仿真 contact manifold 可得；真实标签与 causal association 仍昂贵。 |
| D8 算力/工程 | 4.0 | N=8/100ms 给出硬预算，但需端到端测量而非只计 predictor。 |
| D9 可证伪性 | 4.5 | latent/field 2×2、action×event 干预及 oracle 上界均可判负。 |
| D10 基线强度 | 4.5 | ContactGuard 和多类 contact WM 已覆盖。 |
| D11 消融充分性 | 4.5 | 四路机制及 mode/time/normal 消融充分。 |
| D12 OOD/真机 | 4.0 | 无触觉主结果+触觉 oracle 合理；真机 extractor gap 需量化。 |
| D13 复现性 | 3.5 | 缺 candidate rollout manifest、stop-gradient 位置和端到端 profile 脚本。 |
| D14 CVPR 契合度 | 4.5 | 视觉接触预测与机器人规划均强。 |
| D15 风险/负结果 | 4.5 | 可退化为 contact benchmark/latent monitor 的边界诚实。 |

平均分：**4.23/5.00**。D3=4.0、D5=4.0、D6=4.5、D9=4.5；round<10 且 D3/D5 未到 4.5，R3 不通过。

## Top 问题与证据缺口

1. **major — field/action 串谋。** 后半程“联合训练”未说明 scorer 梯度是否回到 operator/predictor。若回传，event latent 可编码 action identity 或 proposer score 而不预测真实 contact，scorer 仍可提高 success，破坏“接触中介”解释。
2. **major — candidate target 支持域未闭合。** 训练若只有 logged action 的 contact label，部署 N=8 扰动候选将落到外推区。正文需要明确每个 snapshot 对全部候选 exact-reset 执行，或定义 off-policy/censored likelihood。
3. **minor — fallback 路径缺成本/性能分解。** detector、GFM frame 和 contact field 的端到端延迟、失败率没有在同一表中计入，100ms 可能只覆盖 batched field head。

## 具体修改动作

1. 采用离散 typed-field bottleneck，并在主结果对 field→scorer stop-gradient；另设 end-to-end 与 action-only codebook probe。若 probe 从 field latent 恢复 candidate ID 的准确率远超由真实 field 可解释水平，判串谋。
2. 写清 `snapshot × N candidates × seeds` 数据单元、哪些候选真实执行、censoring、负 contact 与 truncated horizon；报告 proposer train/test support overlap。
3. 将 2×2 扩成 `right action/right predicted field`、`right action/wrong field` 等 score intervention，wrong field 必须在固定 action 下改变 ranking 才支持机制。
4. 端到端 profile 包括 proposer、detector/GFM、field、scorer、copy 与 safety check，报告 mean/p95/p99。

## Round 04 验收条件

- [ ] scorer→field/proposer 的梯度边界明确，action-code probe 与 stop-gradient 主设置已预注册。
- [ ] 所有候选的 target 支持、exact-reset 数量与 censored 样本处理可复现。
- [ ] 固定 action 的 field intervention 对 ranking/success 有独立验收阈值。
- [ ] 100ms 改为全链路 mean/p95/p99 合同。

