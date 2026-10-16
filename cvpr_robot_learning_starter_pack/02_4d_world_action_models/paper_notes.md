# 核心论文导读：4D World Action Model

## GeoSem-WAM：WAM 的价值可能是表征学习

GeoSem-WAM 先提出一个关键判断：WAM 的主要收益可能不是推理时显式生成未来，而是预测任务在训练期逼迫 backbone 学到 dynamics-aware representation。问题在于 RGB future prediction 更关注外观变化，对空间结构和对象语义约束不足。

- 第一类 rollout-based WAM 强调测试时 imagination，但计算昂贵，且生成质量不等同于控制质量。
- 第二类 RGB-only predictive training 能学习动态，却可能通过表面像素线索完成任务。
- 第三类 direct VLA 推理快，但缺少未来状态监督带来的结构化表征。

方法在 intermediate video-expert token 上挂 DPT-style geometry 和 semantic head，与 RGB/action flow loss 联合训练，部署时删除辅助 head。它直接提示两个后续缺口：pixel-level pseudo-label 噪声与稀缺，以及 heterogeneous losses 的梯度冲突。因此，使用 foundation feature 替代像素标签、只预测 action-relevant structure，或分析多任务冲突，都是比再加一个 dense head 更自然的延伸。

## WAM4D：用 spatial register 做训练期几何 readout

WAM4D 认为显式 dense 4D decoding 会拖慢动作生成，并可能让目标偏向重建而非控制。它用带空间网格的 register token 查询 video representation，通过几何 decoder 预测未来深度，将梯度传回与 action prediction 共享的 latent；部署时移除 register 与 decoder。

- 第一类 2D WAM 缺少遮挡表面、接触和自由空间约束。
- 第二类显式 4D WAM 推理时持续解码 depth/point cloud，延迟高。
- 第三类松散几何融合可能让 future/action token 发生非因果信息泄漏。

除 register 外，应重点阅读 causal mixture attention：video、action 和 geometry token 的可见性才保证训练目标与真实部署一致。论文也承认没有显式长期 object memory，严重遮挡后会发生身份不一致；这是“轻量 4D latent”下一步很具体的缺口。

## GEM-4D：让生成未来具有可执行的点级一致性

GEM-4D 关注另一种失败：视频在感知上真实，但同一物理点跨帧漂移、物体非刚性变形、接触位置变化，使 inverse dynamics 无法恢复可靠动作。因此，它把 dense 4D correspondence supervision 从冻结的几何基础模型蒸馏进 video DiT。

- 第一类通用视频模型优化外观真实性，却不保证相机、深度和物体运动一致。
- 第二类只用 RGB/latent reconstruction 的机器人视频模型可能掩盖细小但致命的 contact drift。
- 第三类固定 inverse dynamics 假设输入 rollout 可跟踪；生成错误会直接传成动作错误。

Geometry-Enhanced Velocity Alignment 在训练时用 parallel geometry branch 约束视频 velocity，推理时保留单流视频模型；Adaptive Inverse Dynamics 再完成目标/末端 grounding、3D tracking、纠错和逆运动学。读实验时必须分开衡量 world model 与 inverse system 的贡献，因为最终 success 是整个系统共同产生的。

## X-WAM：世界生成与动作执行使用不同去噪节奏

X-WAM 试图在单一模型中同时保留高质量 RGB-D future 和实时动作。它从视频 diffusion prior 出发，复制末端若干 DiT block 形成 depth branch，并用 Asynchronous Noise Sampling 让 action 在较少步骤中完成解码，而 world generation 使用完整步骤。

- 第一类 2D unified world model 无法表达未来空间结构。
- 第二类完全同步 denoising 把 action latency 绑定到高保真视频所需步数。
- 第三类训练和推理采用不同 timestep 组合会导致 distribution mismatch。

ANS 的关键不是“两个不同步数”本身，而是训练时从 joint timestep distribution 采样以匹配异步推理。它适合研究多速率预测：高频动作、低频几何状态、按需高质量可视化。但若只复用异步 schedule 而没有新的部分可观测或控制问题，贡献可能偏增量。

## 四篇论文的共同空缺

四篇都把“完整场景几何”作为默认目标，但机器人真正需要的可能是可控部分的未来：目标物体、末端、接触、支撑关系和遮挡后的 identity。一个更清晰的新方向是 action-centric latent 4D state：用 language/action 条件选择少量 persistent object/contact token，训练时预测未来并用于动作，推理时不解码完整深度。

