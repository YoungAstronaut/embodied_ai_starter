# Round 03 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r02
- File: `proposals/WAM-P2_value_of_imagination/proposal.md`
- Checked: 2026-08-30
- Round focus: 机制因果链、训练/部署信息路径与泄漏
- Verdict: **FAIL / REVISE**（paired target 信息路径合格；一步停止规则与非单调计算收益冲突）

## 实际变更核验

r02 已把 claim 收缩为视觉 WAM 的 common-random-number paired decision-value target，补齐 When-to-Trust/HarmoWAM/CheckVLA/PonderNet/Selecting Computations，给出 5k/20k 的 env-step、record 和存储乘法账，并加入 task/step blocked split 与 compute-only/visual-stat shuffle。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 固定实时预算下额外想象是否值得是 WAM 部署核心问题。 |
| D2 失败模式清晰度 | 4.5 | 同 snapshot/candidate/seed 的 `Y_{k+1}-Y_k` 定义具体。 |
| D3 创新性/最近邻 | 4.0 | VOC/halting 已知；增量仅是视觉 WAM 可执行 paired target/data。 |
| D4 机制因果闭环 | 3.5 | 当前信息→一步 VOC→stop，但未处理跨越负边际后的未来正收益。 |
| D5 技术正确性 | 3.5 | 明示 `D_k` 可负、再正，却以 `VOC_k≤0` 立即停，决策规则不一致。 |
| D6 可观测性/泄漏 | 4.5 | exact-reset returns 只作 stop-gradient target，部署只读 partial rollout 与 clock。 |
| D7 数据可得性 | 4.0 | 5.12M/20.48M steps 与 early go/no-go 已量化。 |
| D8 算力/工程 | 4.0 | 存储和 sim throughput 有上限；真实 all-chain latency 仍需 profile。 |
| D9 可证伪性 | 4.5 | compute-only、shuffle、oracle upper bound 与 blocked transfer 可判负。 |
| D10 基线强度 | 4.5 | gating、adaptive compute、myopic VOC 和 compact future 均覆盖。 |
| D11 消融充分性 | 4.5 | 时间/视觉/序贯/target-noise/尾延迟分解完整。 |
| D12 OOD/真机 | 4.0 | unseen task/hardware 和真机 gate 外效度合理。 |
| D13 复现性 | 3.5 | 缺 stopping Bellman target、branch simulator 与 timing schema 的实现合同。 |
| D14 CVPR 契合度 | 4.5 | 视觉世界模型与实时机器人决策契合。 |
| D15 风险/负结果 | 4.5 | “额外计算有害/无价值”的负结果仍有明确产出。 |

平均分：**4.17/5.00**。D3=4.0、D5=3.5、D6=4.5、D9=4.5；round<10 且 D4/D5 未过硬门槛，R3 不通过。

## Top 问题与证据缺口

1. **major/technical — myopic stopping 与非单调收益自相矛盾。** 文中正确删除 monotonic loss，并允许 `D_k<0,D_{k+1}>0`；但部署在第一个 `VOC_k≤0` 就停止，永远看不到后续较大的正收益。当前机制只能估计 myopic one-step VOC，不能称最优 sequential stopping。
2. **major — 计算代价可能双计或尺度不一致。** `Y_k` 已含 deadline-miss penalty，`VOC` 又减 `λ_timeΔt`；二者可以共存，但必须解释一个是离散控制失败、一个是连续资源成本，并在不同硬件上归一化。
3. **minor — target policy 的随机性需锁定。** common seed 锁了环境与候选，但若 WAM expansion/dropout/排序还有随机性，`D_k` 方差会混入非外生噪声。

## 具体修改动作

1. 二选一：将 claim 明确收缩为 myopic marginal gate；或定义 finite-horizon optimal stopping target `V_k=max(Y_k, E[V_{k+1}|I_k]-cost)`，训练 continuation advantage，并与 one-step VOC 强基线比较。
2. 加最小三步反例 `[D_0<0,D_1≫0]`，验证 myopic 与 continuation-value gate 的差异；预注册非单调 pattern 的 prevalence。
3. 把 deadline miss、wall-clock、energy 和 observation age 分成有单位的 reward/cost 表，做 λ 灵敏度及跨硬件归一。
4. 固定 WAM/candidate/randomness 的 CRN schema；无法共享的随机源进入 variance estimator，而不是隐藏在标签噪声中。

## Round 04 验收条件

- [ ] 停止规则与“收益可非单调”相容，或明确只声称 myopic gate。
- [ ] 三步非单调反例、continuation baseline 与 prevalence 审计进入正文。
- [ ] deadline miss 与连续 compute cost 不重复且单位可解释。
- [ ] CRN 覆盖环境、候选、WAM 采样和 evaluator 随机源。

