# 核心论文导读：几何感知 VLA

## VGGT：几何 teacher 或 backbone 从哪里来

VGGT 的核心问题是，传统 3D 重建往往把匹配、相机估计、深度和优化拆成多个阶段，复杂且依赖后处理。它尝试用一个前馈 Transformer 从一张到数百张图像直接恢复 camera、depth、point map 和 point track，并将中间特征作为可迁移的几何 backbone。

- 第一类是传统 SfM/BA 管线：几何约束清晰，但迭代优化成本高，组件复杂。
- 第二类是 DUSt3R/MASt3R 式 pairwise 模型：学习能力强，但扩展到多视图仍需配对、融合或优化。
- 第三类是任务专用网络：每个 3D 输出单独设计，难形成共享的几何基础表征。

VGGT 用 frame-wise 与 global attention 交替聚合多视图信息，再由不同 head 解码相机、深度、point map 和 track。对机器人方向而言，最重要的不是把全部输出接入策略，而是把它作为统一 teacher，比较哪一层、哪一种几何表征最能预测动作相关状态。其边界是极端旋转、大幅非刚性运动、全景/鱼眼输入，以及多帧时显存增长。

## VGGT-Ω：将重建模型扩展为 scene-token 基础表征

VGGT-Ω 追问的不是如何再增加一个三维输出，而是前馈重建能否像视觉基础模型一样随数据和参数规模稳定提升。原始 VGGT 已经统一了多视图几何任务，但全局注意力、多个高分辨率 dense heads 和稀缺的三维标注限制了训练规模；同时，原有 register tokens 在推理后被丢弃，尚未成为可供下游任务直接复用的场景表示。

- 第一类瓶颈来自架构：所有 patch 跨帧做 global attention，多个 DPT head 又保存高分辨率激活，导致训练显存随视图和任务增加。VGGT-Ω 用16个 per-frame scene tokens 承担跨帧信息瓶颈，以 register attention 替换25%的 global attention，并将高分辨率卷积改成轻量 MLP + pixel shuffle。
- 第二类瓶颈来自监督：point map、depth 和 tracking 多头虽然互相促进，却为每个任务维持昂贵 decoder。VGGT-Ω 只直接输出 camera、depth 和 confidence，但继续使用 camera、depth、反投影 point 与 patch matching loss，让多任务监督保留在训练目标中而不保留冗余输出头。
- 第三类瓶颈来自数据：静态三维数据难以覆盖真实视频中的物体运动。作者用 VLM 预筛选、动态区域屏蔽、多匹配器、VGGT 初始化、COLMAP/MVS 和监督式几何过滤构建静态/动态伪标签，并用 teacher-student 协议利用无标签视频。论文报告约400万有监督序列和1800万无标签视频，但动态像素的真实深度仍主要依赖规模较小的合成数据。

架构、目标和数据三条改动共同服务于 scaling：训练显存约降至 VGGT 的30%，模型从2亿扩展到100亿参数，静态与动态六个 benchmark 均随规模提升。最值得机器人方向注意的是，register 不再被丢弃；冻结 VGGT-Ω 后把 scene tokens 拼接到 OpenVLA-OFT 输入，在 LIBERO 上平均成功率由97.1%提高到98.5%。这已经覆盖“通用几何 token 直接增强 VLA”的基础命题，因此后续工作不能只做 frozen token concatenation，而需要验证 task-conditioned selection、object/contact-centric state、动作后的在线更新或几何不确定性如何改变控制决策。边界上，它仍不显式预测物体轨迹或 canonical 4D 状态，自监督收益较小，25% register attention 仍需保留多数 full global attention，而且 VLA 证据目前主要来自单一高饱和 benchmark。

## Spatial Forcing：用隐式对齐替代显式 3D 输入

Spatial Forcing 认为 VLA 的空间能力弱，根源在于其视觉 backbone 主要在 2D 图文数据上预训练；直接输入点云或深度又受到传感器噪声、硬件差异和历史数据缺少深度的限制。因此它选择在 VLA 中间层对齐外部 3D foundation model 的特征。

- 第一类是纯 2D VLA：具备语义，但空间精度主要依赖动作监督自行涌现。
- 第二类是显式 RGB-D/point-cloud VLA：信息直接，但训练和部署依赖传感器与数据格式。
- 第三类是先估深度再送入策略：会把深度估计误差和场景偏差传递给动作模型。

其方法用投影和特征对齐把空间 teacher 的中间表示压入 VLA，部署时无需额外 3D 输入。阅读时应重点质疑：对齐的是通用几何还是任务相关几何；teacher 与 student 的 patch/视角如何对应；提升是否主要来自正则化和额外监督，而非真正的空间理解。

## Geometric Action Model：将 GFM 直接改造成动作基模

GAM 进一步批评“语义 backbone + 外接几何模块”的松散组合：它认为感知、未来预测和动作解码应该共享几何基础表征。方法在 GFM 中间层切开网络，浅层编码当前观测，插入 language/proprioception/action-history 条件的 causal future predictor，再让预测 token 通过 GFM 后半部分传播和解码未来几何与动作。

- 第一类 VLA 继承语义和语言能力，但 3D 接触结构隐式。
- 第二类视频 WAM 具备时间预测，却常停留在 RGB 或 2D latent。
- 第三类外挂 GFM 的策略只把几何当补充输入，未把 GFM 的结构变成时间和动作建模的共同底座。

GAM 的价值在于提出“geometry-first policy backbone”，但也抬高了后续工作的门槛。简单复刻“GFM + future predictor”新意不足；更好的切口是 task-conditioned token routing、contact-centric prediction、跨 embodiment 的 canonical geometry，或验证 GFM 哪些层真正携带可控动态。

## GEAR-VLA：统一动作、空间与 embodiment 表征

GEAR-VLA 把现实泛化失败拆成三个 representation gap：低层轨迹 token 缺少动作语义；3D 路径与 VLM 语义不对齐；不同机器人之间的状态动作空间不统一。它相应引入 coarse-to-fine action learning、semantic-aligned 3D integration 和 embodiment canonicalization。

- 第一类 action-token VLA 把连续轨迹量化，却可能只学到轨迹模仿。
- 第二类 3D VLA 引入空间特征，但与原有语义表征可能互相干扰。
- 第三类多 embodiment 策略直接混合不同机器人坐标与控制接口，使共享表示承担不必要差异。

这篇适合作为系统化参考，而不适合作为最小起点。阅读 ablation 时要分别检查三条主张，尤其关注 gradient decoupling、冻结 2D 语义通路，以及 cross-embodiment 增益是否来自 canonicalization。

## GuidedVLA：让 action attention 学习指定因素

GuidedVLA 关注端到端策略对视觉捷径的依赖。其核心判断是 action decoder 不是不可分解的整体，不同 attention heads 可以被辅助信号专门化为 object grounding、spatial geometry 和 temporal skill logic。

- 第一类端到端 VLA 只依靠动作损失，task-relevant factor 需要隐式涌现。
- 第二类 post-hoc attention 可视化只能解释模型，不能保证模型使用正确因素。
- 第三类全局 feature alignment 强制所有 token 携带同类信息，可能缺少任务条件选择。

它提供了“action-relevant geometry”最直接的接口：不是对齐所有 patch，而是用任务和功能拆分决定哪些 head 关注哪些因素。其局限是 specialized signal 的人工定义与标注成本，以及 attention specialization 是否能跨 backbone、任务与 embodiment 稳定迁移。

## Vision Transformers Need Registers：理解 register，但不要误读

这篇论文发现 ViT 会把低信息背景 patch 复用为内部计算存储，形成高范数 token 与不平滑 feature map。加入少量额外 register token 后，内部计算有了专门承载位置，dense feature 和 attention map 更干净。

它对本方向的启发是“额外 token 可以成为结构化信息通道”，但原始 register 本身不带空间网格、未来状态或深度监督。WAM4D 的 spatial register 是在这一基础思想上赋予了空间布局和几何 readout 任务，不能把两者的贡献混写。
