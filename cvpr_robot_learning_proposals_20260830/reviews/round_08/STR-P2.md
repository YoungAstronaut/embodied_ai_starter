# Round 08 Review — STR-P2

- Proposal-ID: STR-P2
- Reviewed-Revision: r07
- File: `proposals/STR-P2_deadline_anytime_flow/proposal.md`
- Checked: 2026-08-30
- Round focus: OOD、真机外部效度与风险边界
- Verdict: **FAIL / REVISE**

## 实际变更核验

r07 已定义60s trace block/ACF/ESS、open/closed路径、训练账和CUDA-host/10Hz power/CAS计时；R7系统复现缺口解除。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | deadline是硬部署约束。 |
| D2 失败模式清晰度 | 4.5 | jitter/stale/CAS具体。 |
| D3 创新性/最近邻 | 4.0 | multi-cutoff增量待实验。 |
| D4 机制因果闭环 | 4.5 | exit→scheduler→commit闭合。 |
| D5 技术正确性 | 4.5 | chance与两数据路径正确。 |
| D6 可观测性/泄漏 | 4.5 | new device不冒充保证。 |
| D7 数据可得性 | 4.5 | trace/robot协议可采。 |
| D8 算力/工程 | 4.5 | timing/energy合同细。 |
| D9 可证伪性 | 4.5 | frontier/constraints明确。 |
| D10 基线强度 | 4.5 | same wrapper 2×2强。 |
| D11 消融充分性 | 4.5 | exit×scheduler×age充分。 |
| D12 OOD/真机 | 4.5 | unseen trace与6×100真机强。 |
| D13 复现性 | 4.5 | clock/power/ESS完整。 |
| D14 CVPR契合度 | 4.5 | 算法与系统实证兼具。 |
| D15 风险/负结果 | 4.5 | runtime benchmark有独立价值。 |

平均分：**4.47/5.00**。D3=4.0且round<10，不通过。

## OOD/真机攻击面

1. 三硬件应至少一台完全held-out，不在latency quantile calibration中；否则只是per-device calibration，不是device OOD。
2. new device触发fallback合理，但若大多数episode fallback，success不能归因于anytime exits。需设fallback dominance阈值。
3. 6 tasks×100 trial需按trace block×root episode配对，方法顺序随机；网络/GPU负载注入器与真实控制进程隔离，避免人为trace不可复现。
4. deadline miss≤5%、jerk≤1.05×RTC已有硬约束，还需collision/emergency stop等价共享；prefix violation应在线阻止执行而非只事后暂停。

## 修改与R9验收

1. device split冻结train/calibration/test硬件；held-out device只empirical miss，recalibration另表。
2. 报fallback/CAS/stale rejection比例与conditional success；fallback>预设阈值则只保留runtime robustness。
3. 真机root×trace block随机方法，report ESS/CI；共享collision/force/hold safe controller。
4. exit prefix/shape/timestamp checker置于commit前，任何失败原子回退旧suffix/hold并计deadline。

R9应把SFP明确放在跨范式secondary，主叙事只围绕standard chunk flow的完整multi-NFE exits，避免贡献发散。
