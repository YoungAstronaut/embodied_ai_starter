# Flow Matching 科研入门学习包（机器人版）

更新时间：2026-08-17 初版；**2026-10-13 机器人化改版**（改了什么见文末）

这套材料面向「能读公式、但第一次系统接触 Flow Matching（FM）」的人。主线不是把 FM 当作另一种 diffusion 技巧，而是从概率运输问题出发，理解它为什么能用一次普通的监督回归来训练 Continuous Normalizing Flow（CNF），以及它怎样变成机器人的动作生成器。

## 贯穿全包的一个例子

> **机械臂绕开桌上的水瓶去拿杯子。** 示范里一半从远侧绕，一半从近侧绕。
> 只看「经过瓶子时夹爪的横向偏移 $y$」这一个数：示范是 $\pm1$，$|y|<0.3$ 就算撞瓶。

这个例子小到速度场可以手算出精确解（一个 tanh 公式），但已经包含了机器人 FM 的全部核心现象：

- 为什么不能用回归（平均值会撞瓶）；
- 什么是数据分布、概率路径、速度场；
- 为什么训练标签互相矛盾网络还能学对；
- 多模态从哪来；
- 为什么少步会撞瓶。

所有数字和图都由 `code/robot_1d_intuition.py` 生成，几秒钟就能跑完，不用训练网络。

## 学完后应能回答的六个问题（都能用绕瓶例子回答）

1. 概率路径、样本轨迹、flow map 和速度场分别是什么？在绕瓶例子里各对应什么？
2. 为什么连续性方程能保证「远侧、近侧各占一半」的比例被复现？
3. 原始 FM loss 为什么算不出来？CFM loss 为什么能算、而且梯度等价？
4. 线性路径下，监督信号为什么恰好是 $x_1-x_0$？
5. FM、Rectified Flow、CNF、diffusion、probability-flow ODE 各自处于哪一层？
6. 在机器人中，怎样把一个 action chunk 看成高维样本，从高斯噪声积分成连续动作？为什么 1 步积分会撞瓶？

## 推荐阅读顺序

### 第 0 阶段：先跑例子、建立直觉（约 1.5 小时）

```bash
cd "/Users/youngastronaut/Documents/embodied ai/flow_matching_starter_pack/code"
/Users/youngastronaut/.workbuddy/binaries/python/envs/default/bin/python robot_1d_intuition.py
```

- 然后读 [01_core_concepts.md](01_core_concepts.md) **全文**，对照脚本打印的表和 `figures/` 里的 4 张图。
- 读 [03_diffusion_rectified_flow_comparison.md](03_diffusion_rectified_flow_comparison.md) 的术语表和前三个对比。

### 第 1 阶段：完成公式闭环（约 3–5 小时）

- [02_formula_derivations.md](02_formula_derivations.md)：**先读第 5.5 节**（绕瓶例子的完整手算），再读第 1–7 节的一般推导。每节后面的「🤖 机器人里这是什么」告诉你那个公式在机器人里对应什么。
- `papers/Flow_Matching_2210.02747.pdf`：重点读第 2–4 节。
- `papers/Flow_Matching_Guide_2412.06264.pdf` 的第 2 节 Quick Tour（PDF 第 4–7 页）。
- 运行 `code/toy_flow_matching.py`，看 8-Gaussian 数据怎么从噪声中形成。

### 第 2 阶段：理解设计空间（约 3 小时）

- [03_diffusion_rectified_flow_comparison.md](03_diffusion_rectified_flow_comparison.md) 全文，包括误区 F–H（机器人专用）。
- `papers/Rectified_Flow_2209.03003.pdf`：重点读第 2 节和 reflow。
- `papers/OT_CFM_2302.00482.pdf`：重点读第 3 节及其局限。
- `papers/Stochastic_Interpolants_2303.08797.pdf`：进阶统一视角，不建议首读。

### 第 3 阶段：进入机器人策略（约 3–4 小时）

- [04_robotics_vla_application.md](04_robotics_vla_application.md)：第 2.1 节用绕瓶例子走一遍完整的「看—想—做」循环；**第 11 节是新加的**，讲少步、实时执行（RTC）和 RL 微调。
- 先读 `papers/Diffusion_Policy_2303.04137.pdf`，理解 action chunk 和 receding horizon。
- 再读 `papers/pi0_VLA_Flow_Model_2410.24164.pdf` 第 IV 节，逐项对应到 CFM 公式。
- 最后读 `papers/Streaming_Flow_Policy_2505.21851.pdf`。注意它不是普通的「噪声 action chunk → 干净 action chunk」范式。

### 第 4 阶段：变成自己的研究问题（约 1 天）

- [05_paper_notes.md](05_paper_notes.md)：横向看八篇论文各自解决哪一层问题。
- [06_exercises_and_experiments.md](06_exercises_and_experiments.md)：公式习题，加上新增的机器人习题 6–8（附答案），以及最小实验。

### 学完之后

转到新包 `../flow_matching/`。它讲少步方法的数学（flow map 统一视角、MeanFlow 推导），以及一个包含 Shortcut / MeanFlow / OT / Reflow 的 32 维 action-chunk 实验台。新包写得更紧凑，**建议在这个包读顺之后再看**。

## 文件说明

| 文件 | 用途 |
|---|---|
| `01_core_concepts.md` | **（重写）** 直觉、四个核心对象、CFM、最小闭环、少步为什么撞瓶，全程用绕瓶例子 |
| `02_formula_derivations.md` | 连续性方程、FM/CFM、Gaussian/linear path 的完整推导；**新增第 5.5 节手算例子和每节的机器人解释** |
| `03_diffusion_rectified_flow_comparison.md` | 与 diffusion、Rectified Flow、OT-CFM 的关系和常见误区；**新增机器人例子与误区 F–H** |
| `04_robotics_vla_application.md` | action chunk CFM、π0、Streaming Flow Policy、部署问题；**新增 2.1 节完整循环、第 11 节少步 / RTC / RL** |
| `05_paper_notes.md` | 八篇论文的定位、贡献、弱点和阅读问题（未改） |
| `06_exercises_and_experiments.md` | 一周计划、习题、最小实验、可证伪研究假设；**新增机器人习题 6–8，修正了运行命令** |
| `code/robot_1d_intuition.py` | **（新）** 绕瓶例子：解析速度场、所有数字表、4 张图 |
| `code/toy_flow_matching.py` | 纯 PyTorch 二维 FM 最小实验，可切换 Euler/Heun |
| `figures/` | **（新）** 数据分布、概率路径、速度场、步数与碰撞，共 4 张图 |
| `requirements.txt` | 最小实验依赖（PyTorch、Matplotlib） |
| `paper_catalog.csv` / `references.bib` / `paper_manifest.json` | 论文目录、BibTeX、本地 PDF 校验信息 |
| `papers/` | 本地保存的 8 篇论文 PDF |

## 一句话总纲

给定易采样的源分布 $p_0$（随机动作草稿）和数据分布 $p_1$（专家示范），先人为规定一条从 $p_0$ 到 $p_1$ 的概率路径，再用可采样的条件路径（每次只看一条示范）构造速度监督，训练神经网络去近似边缘速度场；推理时从 $p_0$ 抽一份草稿，解神经 ODE 把它改成一个像示范的动作。

## 版本与边界

- PDF 均保存为本地副本；网页可能继续更新，以 `paper_manifest.json` 中记录的 arXiv 版本为准。
- 本包以连续欧氏空间 FM 为核心。离散 Flow Matching、Riemannian FM、Schrödinger bridge 只作为进阶入口。
- 机器人部分强调行为克隆 / 条件生成，不把 FM 本身等同于规划、RL 或世界模型。
- 绕瓶例子是一维、理想化的（示范是精确的 ±1）。它用来建立直觉，结论的数量级不能直接推到真实机器人上。

## Markdown 公式兼容性

全部笔记统一使用 `$...$` 表示行内公式、`$$...$$` 表示独立公式。若编辑器仍显示源码，请在 Markdown Preview 设置中启用 KaTeX/MathJax 数学渲染；普通源码编辑视图不会主动排版公式。

## 2026-10-13 改版记录

- 修改前的完整备份在 `../flow_matching_starter_pack_backup_20261013/`。
- `01` 全文重写：原有概念全部保留，每个概念都配上绕瓶例子和可复现的数字。
- `02`、`03`、`04`、`06` 只做增补（「🤖」块、新小节），原有推导和正文没有删。
- 修正了几处排版问题：Windows 绝对路径、`ẋ_t=u_t$X_t$`、两处 `qquad` 缺反斜杠、`(#)` push-forward 记号。
