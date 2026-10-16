# Round 08 Review — WAM-P3

- Proposal-ID: WAM-P3
- Reviewed-Revision: r07
- File: `proposals/WAM-P3_hidden_physics_belief/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已冻结Ncandidate16×belief16×noise4×H16，补50k physics/nuisance cells、200-state nested K1024及model-grid calls；R7可行性P0解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 隐动力学适应重要。 |
| D2 失败模式清晰度 | 4.5 | t0/t2与nuisance分层明确。 |
| D3 创新性/最近邻 | 4.0 | predictive belief增量待实证。 |
| D4 机制因果闭环 | 4.5 | residual→belief→CVaR闭合。 |
| D5 技术正确性 | 4.5 | sample/资源/因果边界一致。 |
| D6 可观测性/泄漏 | 4.5 | physics标签仅评测。 |
| D7 数据可得性 | 4.0 | cell与split可生成。 |
| D8 算力/工程 | 4.0 | 大但已闭合。 |
| D9 可证伪性 | 4.5 | t0/shift/oracle判负强。 |
| D10 基线强度 | 4.5 | deploy-equal adapters充分。 |
| D11 消融充分性 | 4.5 | representation×belief完整。 |
| D12 OOD/真机 | 4.5 | held-out physics与4×120真机较强。 |
| D13 复现性 | 4.5 | bins/particles/seed nesting清楚。 |
| D14 CVPR契合度 | 4.5 | 视觉适应控制强。 |
| D15 风险/负结果 | 4.5 | 可辨识边界有价值。 |

平均分：**4.40/5.00**。D3=4.0且round<10，不通过。

## OOD/真机攻击面

1. held-out physics interval必须与可见外观独立；摩擦表面、软硬海绵会改变纹理/形变，t0识别可能来自视觉线索。需全交叉或外观配对。
2. 4 tasks×120“paired trials”需说明pair是同root/同action在不同物性，还是方法配对；物理条件不可无限reset，block/drift需建模。
3. 真机mass/friction labels只评测合理，但接触位置/force marker、tactile oracle和model RGB必须隔离。主动probe不能混入passive t2 primary。
4. CVaR planner缺安全fallback；错误belief在重物/低摩擦上可能选危险候选。

## 修改与R9验收

1. 做physics×appearance全交叉；t0按appearance stratum检验，若t0可预测则只称visually conditioned dynamics，不称hidden。
2. 真机按root object/trajectory/physics block随机方法顺序，记录温度、磨损、表面漂移；paired bootstrap以root为单位。
3. marker/force/θ全部独立logger，仅oracle表；passive与probe分表。
4. 共享force/workspace/collision guard，报告unsafe candidate reject、fallback和conditional regret；安全层主导则降为system-ID diagnostic。

R9需要将“functional predictive equivalence、非物理参数识别”置于摘要显著位置，这是最重要的审稿防线。
