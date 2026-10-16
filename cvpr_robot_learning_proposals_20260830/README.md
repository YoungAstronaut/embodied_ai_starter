# 具身机器人四方向 Proposal 研究包

更新时间：2026-08-30；文献截止：2026-08-30。

本包基于 `cvpr_robot_learning_starter_pack` 的四条路线，扩展最新直接最近邻并形成 12 个彼此独立的 Proposal。研究包不是题目清单：每份 Proposal 均定义可观察失败、训练/部署信息路径、最强最近邻、公式/伪代码、数据与算力、等预算实验、反向干预、判负阈值与负结果价值。

## 目录

- `literature/search_strategy.md`：检索式、具身筛选规则、入选/排除与 PDF 核验流程。
- `literature/evidence_index.md`：四方向最近邻、版本/代码状态、创新边界。
- `literature/papers/` 与 `paper_text/`：22 篇新增官方 arXiv PDF 与完整提取文本。
- `proposal_index.md`：12 个稳定 ID、不同缺口及被最新邻居否决的旧种子。
- `proposals/<ID_...>/proposal.md`：当前 Proposal revision。
- `proposals/<ID_...>/refinement_log.md`：逐轮评审意见、接受/拒绝、实际改动、分数与未决项。
- `evaluation_rubric.md`、`reviewer_literature_audit.md`、`reviews/`：独立评审 Agent 所有材料（主笔不编辑）。
- `final_certification.md`：独立 Reviewer 的 round_11 最终评分、不可删除科学对象与认证边界。
- `final_recommendations.md`：四方向各3项的定位、最近邻、MVP成本、风险、评分及跨方向启动顺序。

## 完成门槛

每个稳定 ID 至少完成 round_01…round_10，并取得 reviewer 最终 PASS；十五维每维≥4.0、均分≥4.30，创新性/技术正确性/可观测性与泄漏/可证伪性≥4.5，且无 fatal novelty/leakage/falsifiability flaw。round_10 仍未达标则继续迭代。

`validate_pack.py` 只检查结构完整性，不能替代 reviewer 的独立质量证书。

最终状态：**12/12 PASS**。12份proposal均为r10，refinement log均含round_01…round_10十次实际refine，独立review覆盖round_01…round_11。该PASS只表示研究Proposal与预注册实验合同通过设计评审；截至2026-08-30，正式pilot和主实验均尚未执行。

## 证据边界

- 近期 arXiv 版本和代码状态可能快速变化；round_02 与 round_10 必须刷新。
- 本包引用的是作者报告与正文证据，不把 SOTA 摘要宣称当独立复现。
- 仿真 exact-reset 与真机自然配对分开报告；任何未来真值、完整轨迹重建、contact/success 标签只能进入 target/teacher，不得进入部署 action query。
