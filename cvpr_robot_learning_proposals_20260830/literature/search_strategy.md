# 具身机器人相邻文献检索与筛选协议

检索截止：2026-08-30；来源优先级：arXiv 官方摘要/PDF > 作者项目页与官方仓库 > 会议开放页面。网页搜索只用于发现候选，方法判断以本地完整 PDF 为准。

## 检索式

- 几何 VLA：`geometry-aware VLA robot manipulation`、`vision geometry action backbone`、`task-relevant geometry contact robot policy`、`VLA geometry uncertainty calibration`。
- 4D WAM：`world action model robotics 4D geometry`、`object-centric WAM occlusion`、`action-controllable world model counterfactual`、`visuo-tactile world model manipulation`。
- 流式/意图：`real-time action chunking flow policy`、`asynchronous VLA latency inpainting`、`dynamic execution horizon action chunk`、`history-conditioned VLA observation aliasing`。
- JEPA：`action-conditioned JEPA robot manipulation`、`JEPA world model physical planning`、`joint-embedding predictive world model invariance`、`JEPA uncertainty multimodal future`。

## 改写后的入选规则

Agentic-RL 技能原规则被改写为具身相关性规则。候选至少满足下列两项才进入主集合：

1. 对机器人策略的可观察失败模式给出机制性定义，而非泛化 VLA 综述；
2. 改变几何/世界状态/时间执行/潜空间预测中的至少一个信息接口；
3. 在 manipulation、physical planning 或动态控制上报告强对照；
4. 能约束本项目某个 Proposal 的创新边界、泄漏审计或可证伪实验。

排除：只有更大模型/更多数据、视觉只是普通输入、仅摘要相关、没有可核查官方来源，或与四方向没有直接机制接口的论文。综述和经典基础论文保留为 supporting，但不作为“最新最近邻”。

## 核验流程

1. 从官方 arXiv 下载 PDF；使用 Codex bundled Python 的 `pypdf` 重新打开并提取全文。
2. 22 篇新增 PDF 均非零页、全文可提取；PDF 与全文分别位于 `papers/` 和 `paper_text/`。
3. 逐篇覆盖摘要、引言、相关工作、方法、主实验、消融、结论/局限；对最近邻额外核对训练/推理可见信息。
4. 代码状态只写“官方仓库/项目页明确、论文承诺、未声明”三类，不把引用了某仓库误写成基于或已开源。

## 候选处理记录

| 候选 | 处理 | 理由 |
|---|---|---|
| VGA 2604.12908 | 入选/几何强最近邻 | 已覆盖原生 3D backbone 直接动作生成，淘汰“换几何 backbone”式提案。 |
| MECo-WAM 2607.05468 | 入选/WAM 强最近邻 | 已覆盖 training-only 4D expert、动作加权关系蒸馏、衰减读掩码与因果可见性。 |
| OA-WAM 2605.06481 | 入选/WAM 强最近邻 | 已覆盖对象 slot、身份地址与未来对象状态；迫使对象记忆 Proposal 处理长遮挡 belief，而非只加 slot。 |
| CoCo 2608.04653 | 入选/WAM 强最近邻 | 已覆盖反事实动作一致性；原 WAM-P3 种子因此被否决并改为隐式物理状态识别。 |
| RTC 2506.07339 / REMAC 2601.20130 | 入选/流式强最近邻 | 分别覆盖测试时异步 inpainting 与训练时 masked chunk 修正。 |
| PACE 2606.00537 / DEHP 2606.11408 | 入选/流式强最近邻 | 已覆盖动态执行 horizon；STR-P2 必须研究 wall-clock deadline 与数值计算预算，而非再选 prefix 长度。 |
| VLA-JEPA 2602.10098 | 入选/JEPA 强最近邻 | 已覆盖 leakage-free future latent prediction 和 action-relevant transition pretraining。 |
| StageWAM 2608.10780v3 | 入选/JEPA/WAM 强最近邻 | 已覆盖 next-stage semantic future；排除“再加阶段 latent”。 |
| DELE-w0.5 2608.22067 | 入选/WAM 强最近邻 | 已覆盖直接未来状态+动作而不生成中间视频；按需想象必须有决策价值检验。 |
| JEPA Safety 2608.17496 | 入选/冲突性边界 | 已覆盖风险头、校准、候选排序与硬 shield；原 JEP-P3 风险校准种子被否决。 |
| ST-VLA 2603.13788 / GeoPredict 2512.16811 | 入选/几何邻居 | 分别覆盖 3D-4D spatial mask 与训练期未来关键点/3D Gaussian。 |
| ViTacWorld 2607.22530 / VT-WM 2602.06001 | 入选/WAM 接触邻居 | 已覆盖显式触觉 world modeling；隐式物理 Proposal 不得把“加触觉”当贡献。 |
| 通用 VLA scaling（Qwen-VLA 等） | 降级 supporting | 能作强通用基线，但没有直接回答四个提案缺口。 |
| 纯导航/纯 HRI 不确定性论文 | 排除主集合 | 可借评测思想，但不直接支持 manipulation 核心主张。 |

