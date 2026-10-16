# Round 02 Review — STR-P2

- Proposal-ID: STR-P2
- Reviewed-Revision: r01
- File: `proposals/STR-P2_deadline_anytime_flow/proposal.md`
- Checked: 2026-08-30
- Round focus: 最近邻、冲突性工作与创新边界
- Verdict: **FAIL / FATAL-IN-r01**（SFP physical-time streaming 与 chunk-flow NFE multi-exit 语义混合）

## 实际变更核验

r01 确实新增burst trace、shared-noise multi-cutoff teacher、mean+tail+energy、age 2×2、SFP go/no-go和runtime schema。但独立通读本地 SFP v2 正文后发现更深冲突：SFP 的ODE时间 `t` 沿**物理动作轨迹**前进，Algorithm 2每个积分步立即执行当前动作；Proposal却把1/2/4/8称为生成同一“完整chunk”的NFE exits并原子提交。两者不是同一状态语义。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | deadline与stale observation真实。 |
| D2 失败模式清晰度 | 4.0 | burst反例清楚，但建立在混合生成语义上。 |
| D3 创新性/最近邻 | 3.5 | deadline calibration可能有增量；当前既不像SFP也未与标准multi-exit flow明确区分。 |
| D4 机制因果闭环 | 3.5 | age/cutoff→atomic chunk→success；cutoff对象不一致破坏闭环。 |
| D5 技术正确性 | 3.0 | shared-teacher chunk exit与SFP action-time integration不能同时成立。 |
| D6 可观测性/泄漏 | 4.5 | clock/age/future-latency边界仍清楚。 |
| D7 数据可得性 | 3.5 | traces可得；checkpoint/teacher family不兼容。 |
| D8 算力/工程 | 4.0 | runtime overhead与schema较好。 |
| D9 可证伪性 | 4.0 | go/no-go和Pareto明确，但需先选择技术对象。 |
| D10 基线强度 | 4.5 | SFP/RTC/DMPO/multi-exit均列；比较语义尚未对齐。 |
| D11 消融充分性 | 4.5 | age2×2/teacher/cutoff/runtime全面。 |
| D12 OOD/真机 | 4.5 | unseen bursts/devices与真机日志强。 |
| D13 复现性 | 3.5 | runtime schema增强；核心tensor/时间轴不明确。 |
| D14 CVPR 契合度 | 3.5 | 若退为scheduler/benchmark，算法新意弱。 |
| D15 风险/负结果 | 4.5 | 主动设置SFP overlap go/no-go。 |

平均分：**3.93/5.00**。D3=3.5、D5=3.0、D6=4.5、D9=4.0；当前 fatal 未解除。

## 证据冲突

- [Streaming Flow Policy 2505.21851v2](https://arxiv.org/abs/2505.21851) 正文 Eq.1–5/Algorithm 2：flow time就是action trajectory time，有限差分顺序产生并执行动作；它匹配每个物理时间的marginal，而非对同一完整chunk做1/2/4/8 denoising exits。
- [RTC 2506.07339v2](https://arxiv.org/abs/2506.07339) 才是生成完整future chunk并冻结/修补prefix的异步范式。
- 因此当前“使用π0.5/SFP checkpoint”“每cutoff完整chunk”“NFE”“atomic commit”至少有一项必须放弃或重定义。

## 必须修改的动作

1. 二选一：A) 标准chunk flow/diffusion的multi-NFE exits，保留atomic chunk但不称SFP中间态；B) 真SFP physical-time action streaming，研究deadline下next-action availability而不是完整chunk exits。
2. 为选定方案画两个时间轴：生成积分/NFE与物理控制/action horizon；给每个tensor shape和commit单位。
3. 若选A，强邻居应转为multi-exit/consistency distillation/DMPO+RTC；SFP只作不同范式对照。若选B，删除同teacher完整chunk/MMD措辞并重设安全prefix。
4. 重新构造burst反例以匹配所选语义；不得用SFP无法输出的对象攻击SFP。

## Round 03 验收条件

- [ ] 唯一生成语义被选定，NFE time与physical action time不再混用。
- [ ] checkpoint/model family与公式兼容。
- [ ] 最近邻表按同一输出对象和时间轴公平比较。
- [ ] burst反例与部署runtime state machine可逐步模拟；日志记录fatal修复。

