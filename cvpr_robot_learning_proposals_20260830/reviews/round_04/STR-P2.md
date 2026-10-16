# Round 04 Review — STR-P2

- Proposal-ID: STR-P2
- Reviewed-Revision: r03
- File: `proposals/STR-P2_deadline_anytime_flow/proposal.md`
- Checked: 2026-08-30
- Round focus: 技术正确性与最小反例
- Verdict: **FAIL / REVISE**（双时间轴持续正确；conditional conformal与多k选择的保证表述过强）

## 实际变更核验

r03 已加入latency chance scheduler、256ξ MMD/mode coverage、old suffix age_max=2后的reactive/hold fallback，以及stale/CAS/prefix/timestamp故障注入。R3提出的scheduler/fallback/分布审计均有实质响应。

## 十五维评分

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| D1 问题重要性 | 4.5 | tail latency/陈旧观测重要。 |
| D2 失败模式清晰度 | 4.5 | burst trace与状态机明确。 |
| D3 创新性/最近邻 | 4.0 | multi-exit原语不新，系统组合待证。 |
| D4 机制因果闭环 | 4.5 | exit→scheduler→CAS→execution闭合。 |
| D5 技术正确性 | 3.5 | conformal被写成条件概率下界，且adaptive max-k会破坏单独coverage。 |
| D6 可观测性/泄漏 | 4.5 | 不读future trace。 |
| D7 数据可得性 | 4.0 | trace可采集。 |
| D8 算力/工程 | 4.0 | 状态机/故障测试具体。 |
| D9 可证伪性 | 4.5 | 同对象multi-exit/fixed/one-step强。 |
| D10 基线强度 | 4.5 | RTC/consistency/DMPO/SFP边界正确。 |
| D11 消融充分性 | 4.5 | age 2×2、fallback、teacher、atomic全面。 |
| D12 OOD/真机 | 4.5 | unseen device/burst和真机贴合。 |
| D13 复现性 | 4.0 | trace/schema好；coverage算法需修正。 |
| D14 CVPR 契合度 | 4.5 | 实时视觉机器人系统契合。 |
| D15 风险/负结果 | 4.5 | benchmark/test suite负价值强。 |

平均分：**4.30/5.00**。D3=4.0、D5=3.5、D6=4.5、D9=4.5；round<10且D5未达门槛，R4不通过。

## Top 问题与技术证据

1. **major/technical — conformal不自动给条件概率保证。** 普通split conformal量化的是marginal coverage；正文的`P(T_k≤d|x_runtime)≥.95`条件保证与“lower confidence bound of P”均需更强假设。更正确的操作量是校准quantile `\hat q_{.95,k}(x)≤d`并诚实声明marginal/Mondrian coverage。
2. **major — 从4个k中选最大是adaptive selection。** 即使每个k各自95%覆盖，选择后的deadline miss不一定≤5%；需对所有k做simultaneous calibration/union bound或直接校准selected policy。
3. **major — fallback公平性。** 新增independently trained reactive safety policy可能本身提高success；所有baseline必须共享完全相同age_max/fallback，且额外参数/训练数据计入。
4. **minor — mode coverage定义需冻结。** 动作chunk模式无天然标签，应给clustering/semantic mode匹配算法。

## 具体修改动作

1. 改写为per-k/Mondrian conformal quantile，列交换性、device shift边界；不声称任意x条件保证。
2. 用Bonferroni/step-down simultaneous residual或在calibration replay上直接校准“选最大k”策略的miss rate。
3. 全baseline共享fallback；另报no-fallback系统主结果。
4. mode coverage用固定teacher-side clustering与matching，测试前冻结。

## Round 05 验收条件

- [ ] conformal保证与实际算法一致，不误写conditional P。
- [ ] adaptive k选择后仍有校准miss控制或明确只作经验指标。
- [ ] fallback在全部baseline同预算共享。
- [ ] mode定义/匹配不依赖测试结果。

