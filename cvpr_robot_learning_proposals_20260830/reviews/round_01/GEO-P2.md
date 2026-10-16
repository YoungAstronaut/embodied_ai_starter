# Round 01 Review — GEO-P2

- Proposal-ID: GEO-P2
- Reviewed-Revision: r00
- File: `proposals/GEO-P2_contact_transition/proposal.md`
- Checked: 2026-08-30
- Round focus: 问题、失败模式、科学命题与最小反例
- Verdict: **FAIL / FATAL-IN-r00**（下一接触转移未条件化于候选动作，当前方法图不成立）

## 文件变更核验

首轮核对确认 r00 已把一般 contact-aware 表述收缩为 mode/time/normal 的局部场，列出无触觉主结果、触觉 oracle、可见性表、接触阶段终点和判负阈值；交接所述内容存在。

## 十五维评分

| 维度 | 分数 | 文件内证据与评审理由 |
|---|---:|---|
| D1 问题重要性 | 4.0 | 接触时刻/模式错误是精细操作核心失败；仍缺不同失败在基线上的发生率。 |
| D2 失败模式清晰度 | 3.5 | 穿透/滑脱/错误支撑清楚，但 `C_t(p)` 的空间域、事件粒度和 mode 互斥性未定义。 |
| D3 创新性/最近邻 | 4.0 | 与几何预测、视触觉 WM、contact intention 有明确区分；ContactWorld/TouchWorld 的字段级重叠待 R2。 |
| D4 机制因果闭环 | 3.5 | contact latent 删除/置换连接 success；“时刻/法向是中介”的方向干预尚未设计。 |
| D5 技术正确性 | 2.5 | 预测未来 contact 必须依赖将执行的候选 action，当前 head 输入未含候选动作；action expert 又读取该场，形成未定义循环。 |
| D6 可观测性/泄漏 | 4.0 | 未来 contact/位姿只作 target、触觉默认不部署；canonical object frame 的在线 pose 来源未列。 |
| D7 数据可得性 | 3.5 | 仿真标签字段可生成并有真机 audit；跨引擎法向/mode 定义和许可证/导出脚本缺失。 |
| D8 算力/工程 | 3.5 | 两档预算合理；真机 300 trials 与标签同步工作量未计入，pose/canonicalization 失败回退缺失。 |
| D9 可证伪性 | 4.0 | 有成功、timing、latent intervention 判负；技术图未闭合使阈值暂不能执行。 |
| D10 基线强度 | 4.0 | dense depth、GeoPredict/MECo、contact binary、触觉 oracle 与 random aux 齐全。 |
| D11 消融充分性 | 4.0 | mode/time/normal/frame/staging/FLOPs 完整；缺候选 action conditioning 与 teacher-noise 正交消融。 |
| D12 OOD/真机 | 4.0 | 两引擎、pose noise、三真机任务；未明确物体材质/摩擦 OOD 与 trial power。 |
| D13 复现性 | 3.0 | 有标签列表和统计框架，无 contact ontology、单位/坐标、时间离散、版本和脚本契约。 |
| D14 CVPR 契合度 | 4.0 | 局部几何/接触表示学习是核心，视觉贡献清楚。 |
| D15 风险/负结果 | 4.0 | 处理仿真标签理想化与 pose noise，并保留可辨识性边界产出。 |

平均分：**3.70/5.00**。关键门槛：D3=4.0、D5=2.5、D6=4.0、D9=4.0。当前存在可修复但致命的技术缺口。

## Top 问题

1. **fatal-in-r00 — 动作条件缺失**：同一视觉状态下不同候选动作产生不同接触位置/时刻/模式；不输入候选 action 的场不是 transition model。action head 读取无动作条件的未来场又无法解决该歧义。
2. **major — ontology 未定义**：`approach` 不是接触拓扑，`stick/slide` 可能随时间切换；`p_contact` 与空间点 `p`、`τ_contact` 的概率/回归语义不清。
3. **major — 部署 canonical frame 可能成为隐藏 oracle**：object pose/instance mask 的来源、误差与漏检回退未写；GT pose 若进入部署则 D6 直接失败。

## 最近邻冲突与证据缺口

- [ContactWorld 2606.13877](https://arxiv.org/abs/2606.13877)、[TouchWorld 2607.07287](https://arxiv.org/abs/2607.07287)、[ViTacWorld 2607.22530](https://arxiv.org/abs/2607.22530) 已覆盖 contact/force/tactile world prediction；R2 必须列字段、传感器、预测对象和 policy 使用方式。
- [Where to Touch 2601.10930](https://arxiv.org/abs/2601.10930) 已把 contact intention 接到规划；差异不能只写“结构化 MPC vs latent policy”。
- [GeoPredict 2512.16811](https://arxiv.org/abs/2512.16811) 的未来关键点/3D Gaussian 是否已隐含接触时间，需要正文级任务/消融对比。

## 必须修改的动作

1. 选择并画清一个无循环技术图：`candidate action -> contact-transition predictor -> candidate scoring/planning`，或联合生成 `p(a,C|o)` 并给出可训练分解；列出 train/deploy token。
2. 给出 contact event ontology：坐标、单位、H、时间离散、mode 转移图、同时多接触、无接触 censoring 和 ground-truth 提取算法。
3. 将机制测试改为定向干预：保持动作只错 contact time/normal/mode，测 success 方向；加入 oracle field 与 deliberately wrong field。
4. 将 canonical frame 拆成 GT-pose oracle、部署 detector/GFM、pose-noise 和 failure fallback，主结果不得使用 GT pose。

## Round 02 验收条件

- [ ] 下一 contact field 明确条件化候选 action，且 action 与 field 不形成循环。
- [ ] ontology/label extractor 可按伪代码二元实现，覆盖多接触和无接触。
- [ ] 部署 frame 不用 GT pose，信息表列出 detector/pose 的时间戳和失败回退。
- [ ] 最近邻表逐项覆盖 ContactWorld、TouchWorld、ViTacWorld、Where-to-Touch、GeoPredict。
- [ ] refinement log 记录 fatal 缺口如何消除并升为 r01。

