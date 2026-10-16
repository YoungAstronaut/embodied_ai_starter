# Round 07 Review — WAM-P2

- Proposal-ID: WAM-P2
- Reviewed-Revision: r06
- File: `proposals/WAM-P2_value_of_imagination/proposal.md`
- Checked: 2026-08-30
- Round focus: 数据漏斗、算力账与复现性
- Verdict: **FAIL / REVISE**

## 实际变更核验

r06 已把winner改为五类gate的validation可行集最强者，加入与paired-myopic的closed test、unpaired/CRN×myopic/continuation 2×2、native/adapter与逐模块ledger。R6基线问题已实质响应，actual pilot=0明确。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | 实时计算价值重要。 |
| D2 失败模式清晰度 | 4.5 | harmful/non-myopic compute明确。 |
| D3 创新性/最近邻 | 4.0 | CRN视觉target是核心增量。 |
| D4 机制因果闭环 | 4.5 | target到stop gate闭合。 |
| D5 技术正确性 | 4.0 | 正文仍同时写S8与primary S16。 |
| D6 可观测性/泄漏 | 4.5 | full-path target部署不可见。 |
| D7 数据可得性 | 3.5 | 40M step扩展无吞吐pilot。 |
| D8 算力/工程 | 3.5 | WAM forward与四格训练总账尚未量化。 |
| D9 可证伪性 | 4.5 | 资源/功效失败会降级。 |
| D10 基线强度 | 4.5 | winner+direct myopic足够强。 |
| D11 消融充分性 | 4.5 | target×stopping正交。 |
| D12 OOD/真机 | 4.0 | unseen tasks有，真机只校准。 |
| D13 复现性 | 4.0 | CRN manifest好，但split/seed数矛盾。 |
| D14 CVPR契合度 | 4.5 | WAM实时决策契合。 |
| D15 风险/负结果 | 4.5 | variance-only降级诚实。 |

平均分：**4.23/5.00**。D3/D5/D7/D8/D13未达关键门槛；round<10，不通过。

## 数据/资源攻击面

1. 方法仍写“每个(s,k)用S=8 CRN估值”，下一段primary却用S=16 cross-fit。S8是训练权重、pilot还是旧残留不清，会改变CI与10.24M公式。
2. 10.24M/40.96M env-step与640k/2.56M record算术正确，但未列每branch的WAM expansion forward/latent cache大小；这可能比sim steps更昂贵。
3. 四格共享同rollout shard，不应重复target生成；但四格+五类winner adapter的GPU训练/validation episode成本要相加。当前“A100×天”没有模型数/seed数。
4. split只写train40/test10，缺validation tasks、同task step block定义，以及resource λ/硬件trace是否跨split复用。

## 具体修改动作

1. 全文统一primary S=16；S4/8/32仅bias曲线，写出每个用途和是否共享seed。
2. ledger公式加入`N_epoch×K×WAM expansion states`、每record字段字节、图像引用去重率、每模型×训练seed GPU-hours及validation环境steps。
3. 冻结train/validation/test task列表和step block，resource λ只在validation fit；硬件trace可共享但不能含test outcome。
4. 100-epoch smoke必须输出sim steps/s、WAM states/s、I/O MB/s、cache hit、peak VRAM与推算总wall-clock；只写“将记录”不算验收。

## Round 08 验收条件

需消除S8/S16冲突、补WAM/model-grid总账与三split。R8再审查unseen task/硬件OOD及真机只校准gate是否足以支持控制主张。
