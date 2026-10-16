# Flow Matching 重拾包（2026-10 重整版）

> **2026-10-13 更新：先读旧包。** 旧包 `../flow_matching_starter_pack/` 已经按绕瓶例子改成了机器人版，基础概念从那里入门更顺。这个包改作**进阶**：少步方法的数学和 32 维 action-chunk 实验台。
>
> 定位：给「以前学过、现在要重新捡起来、并且准备拿它做机器人研究」的自己。
> 新包补了旧包缺的三块：**少步方法**（Consistency / Shortcut / MeanFlow）、**执行层**（RTC 两代）、**RL 微调**。另外加了一个能跑、并且已经跑过的实验台。

## 重拾路线（约 1–2 周，每天 1–2 小时）

| 天 | 读 | 做 | 验收 |
|---|---|---|---|
| 1 | `01_一页纸复习.md` 第 1–4 节；对照旧包 `02_formula_derivations.md` 第 5–7 节 | 闭卷推一遍 CFM 梯度等价 | `01` 第 8 节自测题 1–4 |
| 2 | `01` 第 5–8 节；Guide（`../flow_matching_starter_pack/papers/Flow_Matching_Guide_2412.06264.pdf`）的 Quick Tour | 跑 `python fm_lab.py basics`，对着 `04` 第 1 节看懂每个数 | 能解释「为什么 Heun 1 步比 Euler 2 步差」 |
| 3 | `02_设计空间.md` 第 1–3 节；Rectified Flow 第 2 节、OT-CFM 第 3 节 | `python fm_lab.py coupling` | 能解释 OT/Reflow 为什么会在模式之间留下「桥」 |
| 4–5 | `02` 第 4 节；Shortcut（2410.12557）和 MeanFlow（2505.13447）原文 | `python fm_lab.py fewstep`；`python check_meanflow_identity.py`；**自己推一遍正向约定的 MeanFlow 恒等式** | `01` 第 8 节自测题 6–7 |
| 6 | `03_机器人中的FM.md` 第 1–2 节；π0 第 IV 节 | `python fm_lab.py action` 和 `action_raw` | 能说清 1 步 FM 为什么会撞墙，以及归一化为什么要紧 |
| 7–8 | `03` 第 3 节；RTC（旧研究包 `literature/papers/RTC_2506.07339.pdf`）；training-time RTC（2512.05964，需要下载） | `04` 第 7 节练习 1 | 写出 NFE 与引导效果关系的一张表 |
| 9–10 | `03` 第 5 节；DPPO、ReinFlow 原文 | 读 DPPO 或 ReinFlow 的开源代码 | 能说清两者各自的「似然从哪来」 |

做完以后回到 `../01_研究方向梳理.md`，开始阶段 1。

## 文件

| 文件 | 内容 |
|---|---|
| `01_一页纸复习.md` | 四个对象、连续性方程、CFM、线性路径、**参数化换算表**、**1 步 Euler 落在均值的命题**、自测清单 |
| `02_设计空间.md` | 五个旋钮；少步失败的两个原因；OT/Reflow；**用 flow map 统一 Consistency / Shortcut / MeanFlow**（含正向约定下的 MeanFlow 推导） |
| `03_机器人中的FM.md` | action chunk 复习、三个工程细节、少步策略、**RTC 两代**（含 ΠGDM 引导公式）、SFP、**RL 微调**（DPPO / ReinFlow）、读论文提问清单 |
| `04_实验记录.md` | 5 个实验的实测数字与解读、**3 个实现陷阱**、局限、下一步练习 |
| `code/fm_lab.py` | 单文件实验台：FM / OT-CFM / Reflow / Shortcut / MeanFlow，加 2D 和 action-chunk 两个 toy |
| `code/check_meanflow_identity.py` | 用高斯解析解检验 MeanFlow 恒等式（符号、切向量） |
| `code/results/` | 已经跑出来的指标 JSON 和图 |

## 运行

```bash
cd "/Users/youngastronaut/Documents/embodied ai/flow_matching/code"
PY=/Users/youngastronaut/.workbuddy/binaries/python/envs/default/bin/python   # 已装好 torch / scipy / matplotlib
$PY fm_lab.py basics            # 约 20s
$PY fm_lab.py all               # 全部实验，M5 Pro CPU 约 10.5 分钟
$PY check_meanflow_identity.py  # 应输出 PASS
```

换一台机器的话：`pip install -r code/requirements.txt`。

## 旧包的已知问题（没有改动旧包，只在这里记录）

- **Windows 绝对路径** `D:\opd\survey_agent\output\...`：出现在 `README.md` 第 79 行、`06_exercises_and_experiments.md` 第 110–120 行，以及入门包的 `paper_manifest.json`。在 Mac 上直接复制运行会失败。
- **公式排版残缺**（不影响理解）：
  - `02_formula_derivations.md` 第 69 行的 `ẋ_t=u_t$X_t$` 应为 $\dot X_t=u_t(X_t)$；
  - 第 278 行和 `03_*.md` 第 48 行的 `qquad` 缺反斜杠；
  - 第 19 行的 `(#)` 是 push-forward 记号 $\#$。
- **覆盖缺口**：没有少步方法（Consistency / Shortcut / MeanFlow）、没有 training-time RTC、没有 RL 微调。新包已经补上。
