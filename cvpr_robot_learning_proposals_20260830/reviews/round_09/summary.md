# Round 09 Summary — 论文叙事与审稿攻击面

- Review date: 2026-08-30
- Input revisions: 12/12 r08，`Responds-To-Review: round_08`
- Refinement logs: 12/12 含 `## round_08 / r08`
- Individual reviews: 12/12，均含十五维评分、模拟审稿攻击与R10验收
- Policy: round<10，全部 **FAIL / REVISE**
- Score range: 4.30–4.50

## 汇总

| ID | 平均分 | D3 | R9最危险审稿攻击 | 建议论文定位 |
|---|---:|---:|---|---|
| GEO-P1 | 4.30 | 4.0 | checker自洽；VGA+Cofact组合 | Geometry Counterfactual Ranking |
| GEO-P2 | 4.43 | 4.5 | engineered ontology；ContactGuard已覆盖 | Action-Conditioned Contact Transition Fields |
| GEO-P3 | 4.33 | 4.0 | 三分支不实用；oracle repair/stop收益 | When Should Geometry Be Rejected? |
| WAM-P1 | 4.40 | 4.0 | JPDA+WAM；不可观察identity | Occlusion-ID calibrated benchmark |
| WAM-P2 | 4.40 | 4.5 | VOC旧；大量oracle rollouts | Paired Continuation-Value Targets |
| WAM-P3 | 4.43 | 4.5 | PEARL/RMA已做；physics可见 | Functional Predictive Beliefs |
| STR-P1 | 4.43 | 4.5 | BOCPD旧；RMRT tube手调 | Reset-Worthiness from Change+Value |
| STR-P2 | 4.50 | 4.5 | consistency multi-exit已有；像系统工程 | Deadline-Valid Complete-Chunk Exits |
| STR-P3 | 4.40 | 4.5 | synthetic自洽；1B steps | Counterfactual-Alias benchmark |
| JEP-P1 | 4.30 | 4.0 | Action-Bisim已覆盖；canonicalizer贡献 | ActMetric-3D benchmark |
| JEP-P2 | 4.40 | 4.5 | NRI+rich labels；图/slot/JEPA旧 | Ordered Contact Transactions |
| JEP-P3 | 4.40 | 4.5 | ANOVA旧；JEPA branding | ExoManip factorial benchmark |

## R9跨Proposal结论

1. **标题必须跟最不可删除的贡献走。** GEO-P1/GEO-P3/WAM-P1/JEP-P1首先是benchmark/reliability/metric；JEP-P2/JEP-P3不应把slots或JEPA写成不可删除的标题核心。
2. **先承认最近邻覆盖。** “pseudometric、JPDA、VOC、change point、functional ANOVA、graph/slot/JEPA本身不新”要出现在摘要/related work前半，而非局限段。
3. **最危险基线必须在主表第一组。** label-equal VGA/ContactGuard/regret router、L11 JPDA、paired myopic、standard multi-exit、Action-Bisim adapter、NRI×typed、non-JEPA same objective都不能藏附录。
4. **部署图只画可见量。** checker/GT repair/Q/e/physics/marker/logger用虚线独立target branch；禁止视觉上连进student/controller。
5. **结果条件化标题不是软弱，而是科学合同。** 每份都要准备method与benchmark/diagnostic/runtime两个版本；关键机制持平时实际删标题/摘要claim。
6. **合成数据攻击要用独立evaluator回应。** checker、repair、pair-Q、factorial e若同时定义数据和评测，会被判self-fulfilling；independent reward/checkpoint/simulator/real semantic audit需进入正文。

## Round 10最终压力测试验收

1. proposal正文必须含：唯一主命题、明确not-claim、primary、最危险baseline、三条reviewer attacks、claim ladder、降级标题。
2. 再扫全篇禁词/残留：被废弃seed、过强causal/mediation/zero-shot/guarantee/real-world verification、旧primary、错误资源量不得复发。
3. 对每份重算15维；PASS硬门槛保持：每维≥4.0、均分≥4.30、D3/D5/D6/D9≥4.5、无fatal，且轮次≥10。
4. D3=4.0的GEO-P1/GEO-P3/WAM-P1/JEP-P1不能靠措辞自动升分：必须把benchmark/protocol本身的独特、可复用科学对象与最近邻字段差异写成不可删除贡献。
5. final压力测试从三种反事实结果出发：strong baseline持平、control secondary<3pp、OOD/真机失败；逐一验证剩余论文仍不虚假。
6. 只有12/12全部过门槛才写`final_certification.md`；任何一份未过继续round_11。
