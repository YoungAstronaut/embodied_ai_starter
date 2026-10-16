# 文献证据索引与创新边界

所有链接均指向官方 arXiv、作者项目页或官方代码；版本以下载 PDF 首页为准。`本地 PDF` 指 `literature/papers/`，starter 论文仍位于原资料包。

## 方向一：几何感知 VLA

| 工作 | 版本/状态 | 已覆盖机制 | 对 Proposal 的约束 |
|---|---|---|---|
| [VGGT](https://arxiv.org/abs/2503.11651) / [VGGT-Ω](https://arxiv.org/abs/2605.15195) | starter 本地 PDF；官方代码可用 | 通用多视图几何与可复用 scene tokens | GEO-P1 必须证明动作因果相关性，不能只拼 scene token。 |
| [VGA](https://arxiv.org/abs/2604.12908) | v2；本地 PDF；论文给项目页 | 原生 3D world backbone + progressive volumetric modulation | GEO-P1/GEO-P2 不能声称“几何 backbone 做动作”本身新。 |
| [MECo-WAM](https://arxiv.org/abs/2607.05468) | v1；[项目页](https://meco-wam.github.io/) | action-aware temporal geometric distillation | GEO-P1 必须用反事实中介证明选出的几何真的改变决策。 |
| [ST-VLA](https://arxiv.org/abs/2603.13788) | 本地 PDF；论文给项目页 | 任务相关 3D-4D mask 与长时规划接口 | GEO-P1 不得只用语言生成 spatial mask。 |
| [GeoPredict](https://arxiv.org/abs/2512.16811) | 本地 PDF | 未来机械臂关键点与 3D Gaussian 训练监督 | GEO-P2 必须预测接触拓扑转移，而非一般未来几何。 |
| [UAOR](https://arxiv.org/abs/2602.18020) | 本地 PDF；[项目页](https://uaor.jiabingyang.cn/) | action entropy 触发 observation reinjection | GEO-P3 必须校准几何证据可靠度，而非通用 action entropy 门控。 |
| [Confidence Calibration in VLA](https://arxiv.org/abs/2507.17383) | 官方 arXiv | VLA 成功置信度基线与 Platt scaling | GEO-P3 的主要终点应是几何误差条件下的选择性风险，而非总体 confidence。 |

## 方向二：4D World Action Models

| 工作 | 版本/状态 | 已覆盖机制 | 对 Proposal 的约束 |
|---|---|---|---|
| GeoSem-WAM / WAM4D / GEM-4D / X-WAM | starter 本地 PDF | training-only 几何、register depth、显式 rollout+IDM、异步联合生成 | 三个 WAM Proposal 必须分别处理身份 belief、想象价值、隐藏物理参数。 |
| [MECo-WAM](https://arxiv.org/abs/2607.05468) | v1；本地全文 | 4D expert 与无推理开销蒸馏 | 不能再提“训练期 action-centric 4D loss”。 |
| [OA-WAM](https://arxiv.org/abs/2605.06481) | v1；本地全文 | identity address + time-varying content object slots | WAM-P1 聚焦完全遮挡下的多假设 belief、重现关联与身份校准。 |
| [DELE-w0.5](https://arxiv.org/abs/2608.22067) | v1；本地全文 | 直接预测未来状态和动作，去掉中间视频 | WAM-P2 要证明“何时想象”具有净决策价值，而非只降计算。 |
| [CoCo](https://arxiv.org/abs/2608.04653) | v1；本地全文 | 动作/空间反事实一致性与 controllability 指标 | 反事实动作响应已被覆盖，不能作为 WAM-P3 主张。 |
| [VT-WM](https://arxiv.org/abs/2602.06001) / [ViTacWorld](https://arxiv.org/abs/2607.22530) | 本地全文；后者有[项目页](https://vitacworld.github.io/) | 显式视触觉未来预测、触觉数据扩增与策略评估 | WAM-P3 用部署可得 proprio/视觉残差推断 hidden physics，并把触觉作为 oracle/上界。 |
| [Robot-Factored WM](https://arxiv.org/abs/2607.22535) | 本地全文 | 把控制器与机器人渲染从场景响应中分解 | WAM-P3 必须控制 action realization，避免把控制误差当物体物性。 |
| [EVA](https://arxiv.org/abs/2603.17808) | 本地全文 | IDM reward 对视频可执行性做 RL 对齐 | WAM-P2 的价值信号须与生成质量分离并做 IDM/策略公平对照。 |

## 方向三：Streaming + Intent

| 工作 | 版本/状态 | 已覆盖机制 | 对 Proposal 的约束 |
|---|---|---|---|
| Streaming Flow Policy / IntentVLA | starter 本地 PDF | 可执行 flow trajectory；历史短期 intent 与 AliasBench | STR-P1 需同时测稳定性和突变恢复，STR-P3 需做配对反事实历史。 |
| [RTC](https://arxiv.org/abs/2506.07339) | v2；本地全文；官方代码/项目材料见论文 | 异步生成、冻结必执行前缀、soft-mask inpainting | STR-P2 不能把异步执行或前缀 inpainting 当贡献。 |
| [REMAC](https://arxiv.org/abs/2601.20130) | ICLR 2026；本地全文 | masked action chunk、self-conditioned curriculum、prefix-preserved sampling | STR-P2 必须独立于 intra/inter-chunk consistency 训练。 |
| [PACE](https://arxiv.org/abs/2606.00537) | v2；本地全文 | 从速度谷训练自由地选择 execution horizon | STR-P1 的事件不能只定义为低速 phase boundary。 |
| [DEHP](https://arxiv.org/abs/2606.11408) | v1；[项目页](https://dehp-chunking.github.io/) | PPO 学习动态执行 horizon | STR-P2 不再学习 prefix 长度，改为 deadline 下 NFE/观测龄/计算调度。 |
| [DMPO](https://arxiv.org/abs/2601.20701) | 本地全文 | 一步 MeanFlow 与 RL 微调 | STR-P2 必须在同一硬件 wall-clock 下与一步/两步策略比较质量-延迟 Pareto。 |

## 方向四：JEPA 世界模型

| 工作 | 版本/状态 | 已覆盖机制 | 对 Proposal 的约束 |
|---|---|---|---|
| V-JEPA / V-JEPA 2 / V-JEPA 2.1 / LeJEPA | starter 本地 PDF；官方 Meta/作者仓库 | latent prediction、action-conditioned planning、dense features、防塌缩 | 不把“action-conditioned JEPA”当创新。 |
| [VLA-JEPA](https://arxiv.org/abs/2602.10098) | v2；[官方代码](https://github.com/ginwind/VLA-JEPA/) | leakage-free future latent target 与 action-relevant transition pretraining | JEP-P1 必须有 same-state alternative-action 干预和 action-equivalence 判据。 |
| [StageWAM](https://arxiv.org/abs/2608.10780) | v3；本地全文 | next-stage semantic future + short WAM | 不再做 coarse/fine stage latent 拼接。 |
| [JEPA-WM study](https://arxiv.org/abs/2512.24497) | v3/TMLR；[官方代码](https://github.com/facebookresearch/jepa-wms) | 多步 loss、proprio、encoder、planner 的系统比较；指出确定性均值问题 | JEP-P3 直接以多模态未来和外生动态为缺口。 |
| [Invariant JEPA-WM](https://arxiv.org/abs/2602.18639) | v1；本地全文 | bisimulation 去 slow-feature，当前只验证简单导航 | JEP-P1/JEP-P3 必须超越静态背景不变性，验证 manipulation 干预。 |
| [JEPA Safety](https://arxiv.org/abs/2608.17496) | v1；本地全文 | 风险/进度头、校准、候选排序、deterministic shield | 风险校准 Proposal 被排除；也不能暗示 JEPA 本身提供安全保证。 |

## 证据边界

- 2026 年多数为近期 arXiv；引用时保留版本号，round_10 再刷新。
- 本索引记录作者报告，不把摘要中 SOTA 声明当独立复现结论。
- 真正复现实验前还需逐仓库核查许可证、commit、checkpoint 与数据协议；未明确者在 Proposal 中按风险处理。
