# Round 04 Review — GEO-P1

- Proposal-ID: GEO-P1
- Reviewed-Revision: r03
- File: `proposals/GEO-P1_counterfactual_geometry/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / REVISE**（R3 relation-type fatal 已解除；动作分布支持与 token 对齐仍未定义）

## 实际变更核验

r03 确实禁止 checker type/id 进入 student，部署改用 language+detector/GFM 预测 soft `p_type`；no/predicted/oracle 三档、schema rejection、accepted/rejected 五字段匹配、AUROC门槛和纯评测 `L_swap` 均已写入。该 fatal 是实质解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 几何依赖与视觉捷径的区分重要。 |
| D2 失败模式清晰度 | 4.5 | SCM pair/hard negative/selection probe 均明确。 |
| D3 创新性/最近邻 | 4.0 | 新意已收缩为 relation-level intervention reliance。 |
| D4 机制因果闭环 | 4.0 | pair→type/gate→action 链基本闭合。 |
| D5 技术正确性 | 3.5 | `π*` 在离散码本、`π` 可能在连续 chunk 空间，KL 尚无共同支持；nuisance token 对齐也未定义。 |
| D6 可观测性/泄漏 | 4.5 | checker type/id schema拒绝，主路径部署可得。 |
| D7 数据可得性 | 4.0 | pair生成与拒绝匹配可执行。 |
| D8 算力/工程 | 3.5 | checker枚举、匹配probe和20k pairs仍缺实测乘法账。 |
| D9 可证伪性 | 4.5 | type三档、2×2、selection AUROC和码本regret强。 |
| D10 基线强度 | 4.5 | Cofact/CAST/MECo/ST-VLA等均已覆盖。 |
| D11 消融充分性 | 4.5 | relation/generic、type、swap、K和noise可分解。 |
| D12 OOD/真机 | 4.0 | 四轴/真机合理，relation matching OOD仍待定义。 |
| D13 复现性 | 4.0 | 字段schema明显增强；缺共同动作支持与set alignment伪代码。 |
| D14 CVPR 契合度 | 4.0 | 几何视觉表征/机器人动作均契合。 |
| D15 风险/负结果 | 4.5 | selection bias、unmappable和type无效均有降级。 |

平均分：**4.13/5.00**。D3=4.0、D5=3.5、D6=4.5、D9=4.5；round<10 且 D5 未达硬门槛，R4 不通过。

## Top 问题与技术证据

1. **major — directional KL 的测度空间未闭合。** checker 的 `Y*` 是有限动作码本上的有效集合，`π*` 因而是 categorical；原 VLA action head通常是连续 chunk distribution/flow。没有量化到同一候选库或定义积分/binning，就不能直接计算 `KL(π*||π)`。
2. **major — `||m(x)-m(x^n)||_1` 假定 token 一一对齐。** nuisance 相机/非目标实例干预会改变 detector顺序、relation数量和可见性；直接按 index 相减可能监督错误实体，甚至用 checker ID 做隐式对齐。
3. **minor — soft type CE 与 action claim需分开。** type预测准确不等于 action依赖；主结论应由 no/predicted-type action差异决定，CE只作辅助。

## 具体修改动作

1. 把 policy在同一 M 个候选 chunks 上重评分并归一成 categorical，再与 `π*` 做 KL；或改用对连续样本可计算的 set-valued ranking/energy loss。给2-action最小例手算。
2. nuisance consistency改为以部署 detector track/semantic pair 做可审计 matching，或用 permutation-invariant OT/set loss；GT/checker ID只能给 oracle对齐。
3. 报 unmatched mass/visibility变化；不可对齐 token不得被零填后当一致。
4. 同步码本 coverage-regret 与 loss support，防止评测64→128而训练仍固定小库。

## Round 05 验收条件

- [ ] `π*` 与 policy distribution 在同一明确支持上，KL/ranking可手算。
- [ ] nuisance pair token matching为部署可得且置换不变，含 unmatched处理。
- [ ] type CE与action主效应分离，oracle type不进入主结论。
- [ ] 动作库coverage与loss支持同步并有阈值。

