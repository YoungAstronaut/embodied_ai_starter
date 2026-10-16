# Round 03 Review — STR-P3

- Proposal-ID: STR-P3
- Reviewed-Revision: r02
- File: `proposals/STR-P3_counterfactual_history/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（target 隔离合格；连续策略 loss 对离散 Q-library 的定义未闭合）

## 实际变更核验

r02 已把贡献顺序改为 benchmark/generator→paired supervision→跨 backbone，加入 AliasBench 四字段 overlap audit、IntentVLA/普通 causal Transformer 两 backbone 三格、Q-set target whitelist 以及 only-past-video 判负门槛。主 pair 只接受双合法 rollout 可达的 physical hidden-state pairs。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | POMDP aliasing 是历史策略是否必要的根本问题。 |
| D2 失败模式清晰度 | 4.5 | same-current、双可达、双向 value incompatibility 定义严格。 |
| D3 创新性/最近邻 | 4.0 | history encoder 不新；数据合同可能有新意，取决于 AliasBench audit。 |
| D4 机制因果闭环 | 4.0 | pair→set/rank target→history-conditioned action→swap/control 闭合。 |
| D5 技术正确性 | 3.5 | `E_{a~π}Q(a)` 对固定离散 candidate library 外的连续动作未定义。 |
| D6 可观测性/泄漏 | 4.5 | hidden state/future/seed/task ID 仅 target，student shard 白名单明确。 |
| D7 数据可得性 | 4.0 | acceptance 可能低，但逐级漏斗与 go/no-go 已预注册。 |
| D8 算力/工程 | 4.0 | 10k+10k pairs×S=8 可行，需给 candidate/rollout 乘法账。 |
| D9 可证伪性 | 4.5 | 两 backbone、random pair、only-video 和 overlap kill criteria 强。 |
| D10 基线强度 | 4.5 | IntentVLA、memory、BeT/Diffusion 与普通 Transformer 充分。 |
| D11 消融充分性 | 4.5 | history modality、pair type、matching tolerance 与 leakage controls 齐全。 |
| D12 OOD/真机 | 4.0 | 自然 AliasBench 外测与真机 near-match 边界诚实。 |
| D13 复现性 | 3.5 | 官方 AliasBench schema 尚未实际审计；Q interpolation/target support 未定义。 |
| D14 CVPR 契合度 | 4.5 | 视觉历史、数据生成与机器人 POMDP 强契合。 |
| D15 风险/负结果 | 4.5 | strict-pair feasibility/静态捷径 audit 即使负结果仍有价值。 |

平均分：**4.20/5.00**。D3=4.0、D5=3.5、D6=4.5、D9=4.5；round<10 且 D5 未过硬门槛，R3 不通过。

## Top 问题与证据缺口

1. **major/technical — Q target 的支持域不匹配。** pair generator 只对固定 candidate library 估 `Q_A/Q_B`，但 action flow 的 `π_A` 可输出库外连续动作；当前 `L_cross=E_{a~π_A}Q_B(a)` 无可计算定义。用 learned critic 插值又会引入未审计的 model bias。
2. **major — oracle-filtered pair 分布可能过于合成。** strict acceptance 由 future Q 与 full state 筛选，模型虽不直接读字段，却可能只在高度筛选的生成分布上成功；自然 AliasBench 外测需按同可观察 difficulty 匹配。
3. **major — novelty 仍取决于官方 audit。** 正文正确标“待 schema 脚本核验”，因此 D3 不能超过4.0；这不是可用将来时替代当前证据。

## 具体修改动作

1. 二选一闭合 loss：把 action head离散化/检索到同一候选库；或对每个 policy sample 运行 exact-reset Q target。若用 critic，必须独立 held-out calibration、error bound 和 oracle-Q sensitivity。
2. 给出 candidate coverage/regret：library oracle 相对 continuous oracle 的 gap，gap 大时不得把训练失败归因 history。
3. 实际运行 `audit_aliasbench.py`，产出 schema/pair/split 证据；若四字段已有重合，立即触发预注册降级/判重。
4. 为 synthetic strict pairs 与 natural alias frames 做 visual/proprio/action-history difficulty matching 和跨域 transfer。

## Round 04 验收条件

- [ ] `L_cross` 对每个 sampled action 的 Q 来源可计算、可审计且支持域闭合。
- [ ] candidate library coverage/regret 与 critic误差（若使用）有硬阈值。
- [ ] AliasBench 官方 schema audit 已实际完成，不再写“待核验”。
- [ ] strict-pair 收益可迁移到匹配难度的自然 alias split。

