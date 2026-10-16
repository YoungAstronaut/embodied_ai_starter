# CVPR 机器人学习四方向入门资料包

更新时间：2026-08-14

这份资料包围绕四个候选方向组织：几何感知 VLA、4D World Action Model、流式动作与短期意图、JEPA 潜空间世界模型。目标不是把论文堆在一起，而是在一周内完成三件事：建立共同术语；看清每条路线已经解决了什么；形成可以被实验验证的选题假设。

## 目录

1. [`01_geometry_aware_vla/README.md`](01_geometry_aware_vla/README.md)：如何让机器人策略学习 action-relevant geometry，而不是只增加深度输入。
2. [`02_4d_world_action_models/README.md`](02_4d_world_action_models/README.md)：未来几何应该是显式输出、训练监督，还是潜空间状态。
3. [`03_streaming_intent_policy/README.md`](03_streaming_intent_policy/README.md)：如何同时解决 action chunk 延迟与跨 chunk 意图跳变。
4. [`04_jepa_world_models/README.md`](04_jepa_world_models/README.md)：如何从像素生成转向可预测、可规划的潜空间世界状态。
5. [`00_one_week_plan.md`](00_one_week_plan.md)：建议的一周阅读、讨论与原型安排。
6. [`00_direction_comparison.md`](00_direction_comparison.md)：四方向的科研问题、成本、风险和 CVPR 叙事对比。
7. [`00_reading_template.md`](00_reading_template.md)：每篇论文统一使用的阅读记录模板。
8. [`paper_catalog.csv`](paper_catalog.csv)：全部论文的方向、阅读层级、核心机制与本地路径索引。
9. [`references.bib`](references.bib)：资料包论文的统一 BibTeX 条目。
10. [`paper_manifest.json`](paper_manifest.json)：本地 PDF 路径、页数、字节数与解析校验结果。

每个方向目录均包含：

- `README.md`：概念地图、分层学习路线、逐篇阅读顺序与退出标准；
- `paper_notes.md`：核心论文的中文导读与横向比较；
- `resources.md`：论文、代码、项目页与建议检索词；
- `questions.md`：组会讨论问题、选题问题与最小原型建议；
- `papers/`：已下载的核心论文 PDF。

## 推荐使用方式

第一遍不要逐行读公式。先读每个方向的 `README.md`，选两个最感兴趣的方向；然后按标注的“第一层必读”阅读论文的摘要、引言、方法总图和主实验；只有当方向仍然有吸引力时，再阅读第二层与附录。每读完一篇，用统一模板回答：作者定义的失败模式是什么，新增的监督或状态是什么，推理时是否仍需要它，以及动作成功率究竟由哪个模块带来。

## 当前资料边界

- 共收录 18 篇 PDF、460 页，全部已重新打开并完成页数和正文提取校验。
- 2026 年论文大多仍是近期 arXiv 版本，方法、实验表和代码状态可能继续更新；正式立项前应再次检查 arXiv version 与代码仓库。
- 资料包以“入门与确定大方向”为目的，不替代对实验细节、数据协议和基线实现的复核。
