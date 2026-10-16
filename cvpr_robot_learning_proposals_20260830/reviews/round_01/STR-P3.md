# Round 01 Review — STR-P3

- Proposal-ID: STR-P3
- Reviewed-Revision: r00
- File: `proposals/STR-P3_counterfactual_history/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / REVISE**（round<10；“示范承诺模式”标签可能无唯一正确动作）

## 文件变更核验

r00 已实际给出同当前 RGB/depth/语言/proprio/元数据的 relevant pairs、不同但同动作的 irrelevant pairs、字段删除、history swap、oracle hidden state 和 POMDP 边界。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | observation aliasing 是 history VLA 的核心识别问题，paired benchmark 有普适价值。 |
| D2 失败模式清晰度 | 4.0 | 同当前观测、不同历史/正确动作的定义明确；物理 hidden state 与示范 commitment 混合。 |
| D3 创新性/最近邻 | 4.0 | 不再是更长 memory，而是严格 factorial pairs/history-swap；counterfactual sequence learning 邻居待补。 |
| D4 机制因果闭环 | 3.5 | pair supervision→history belief→swap action→success；past action smoothing 替代解释仍未充分排除。 |
| D5 技术正确性 | 3.5 | loss 可实现；若两个动作都有效，`d(a_A*,a_B*)>δ` 不证明历史依赖，demo style 会制造伪标签。 |
| D6 可观测性/泄漏 | 4.5 | hidden/future/ID 均删除，history deployable，泄漏阳性对照完善。 |
| D7 数据可得性 | 3.5 | 仿真 save-state 可构造；expert optimality、pair reachability/acceptance rate、真机匹配成本未写。 |
| D8 算力/工程 | 3.5 | 规模与 GPU 预算合理；严格 pair validator 和 240 真机 paired trials 工作量偏乐观。 |
| D9 可证伪性 | 4.0 | ranking/swap/closed-loop、oracle/random contrastive 阈值清楚。 |
| D10 基线强度 | 4.0 | IntentVLA/Remember/long window/random pair/oracle 齐全；behavior cloning multimodality baseline 缺失。 |
| D11 消融充分性 | 4.0 | pair types/swap/matching/history modalities/field balance/泄漏均拆。 |
| D12 OOD/真机 | 4.0 | scene/seed split、AliasBench 外测与三真机任务；真机“严格同观测”只能近似，尚无容差协议。 |
| D13 复现性 | 3.0 | 无 reachability validator、hash tolerance、expert-set 定义、版本/seed/artifact 清单。 |
| D14 CVPR 契合度 | 4.0 | 视觉时序 alias benchmark 与 history representation 是中心。 |
| D15 风险/负结果 | 4.5 | 明确 POMDP 边界、静态捷径审计与工具型负产出。 |

平均分：**3.87/5.00**。关键门槛：D3=4.0、D5=3.5、D6=4.5、D9=4.0；未达 hardened gate。

## Top 问题

1. **major — “不同专家动作”不等于“不同正确动作”**：示范 commitment/style 可让同一 belief 下出现两条都成功的 action；强制 `L_sep/L_swap` 会把任意风格记忆化。
2. **major — pair 的因果可达性未验证**：从两段真实 causal history 到达相同当前可见状态，比直接编辑 hidden simulator state 更强；后者可能生成部署中不可能出现的历史—状态组合。
3. **major — 历史作用可能只是 last-action continuation**：past action 是合法输入，但若收益完全来自动作平滑，就不能宣称视觉 history disambiguation。

## 最近邻冲突与证据缺口

- [IntentVLA 2605.14712v2](https://arxiv.org/abs/2605.14712) 已有 AliasBench 与 VGGT history；需比较其 benchmark 是否包含严格 alias pairs。
- [Remember Smarter 2608.15269v1](https://arxiv.org/abs/2608.15269) 的 memory mechanism 需同历史长度和参数复现。
- Counterfactual sequence/causal representation 与 multimodal imitation literature 未列；尤其需要 set-valued optimal actions/behavior modes 的处理。

## 必须修改的动作

1. 将物理 hidden-state pairs 与 demonstrator-commitment pairs 分成两个数据集/claim；主 claim 优先使用可由 simulator value 验证的物理 pairs。
2. 用 action equivalence/value set 判断“交叉执行失败”：`a_A` 在 state B 明显差且 `a_B` 在 state A 明显差，而不只 action distance 大。
3. 给每个 pair 加 causal reachability test：两条历史都由合法 rollout 生成；直接 state edit 仅作诊断并单列。
4. 增加 only-last-action、only-past-proprio、only-past-video 及 action-history shuffled controls，拆出视觉历史贡献。

## Round 02 验收条件

- [ ] pair 正确性用交叉 value/success 判据而非专家动作距离。
- [ ] physical hidden state 与 demo commitment 不再混合主结论。
- [ ] 主测试 pairs 均有双历史 causal reachability 证明/validator。
- [ ] 加入 history modality controls，并与 IntentVLA/Remember Smarter 做字段级最近邻表。
- [ ] refinement log 记录改动并升为 r01。

