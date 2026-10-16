# 方向二：几何增强的 4D World Action Model

World Action Model 将未来观测预测和机器人动作建模放到同一训练框架中。这里最重要的分歧不是“2D 还是 4D”，而是未来世界在控制中扮演什么角色：推理时显式想象未来、训练时作为辅助监督，还是仅以紧凑 latent state 存在。

## 三种范式

1. **训练期 structured supervision，推理期直接出动作**：GeoSem-WAM 和 WAM4D。几何/语义分支负责塑造 representation，部署时移除。
2. **显式生成未来，再提取动作**：GEM-4D。未来视频必须保持点级 correspondence，随后由 inverse dynamics 恢复动作。
3. **统一生成世界与动作，但异步控制成本**：X-WAM 同时生成 RGB-D 和动作，动作少步解码、视频完整去噪。

## 分层阅读路线

### 第一层：建立争论

1. **GeoSem-WAM**：先读它对“为什么 WAM 有效”的判断，再看 future RGB、geometry、semantic 三种监督和 training-only DPT head。
2. **WAM4D**：重点看 spatial register、future-depth readout、causal mixture attention，以及为何推理时可以删除几何分支。
3. **GEM-4D**：重点看 Geometry-Enhanced Velocity Alignment、4D correspondence teacher 和 Adaptive Inverse Dynamics。理解“视频好看”与“视频能转成动作”的差别。
4. **X-WAM**：重点看 RGB-D branch、Asynchronous Noise Sampling 的训练/推理分布，以及动作延迟与视频质量如何分离。

## 横向比较维度

- 预测对象：RGB、depth、semantic mask、point map、correspondence 或 latent feature。
- 几何来源：真实传感器标签、伪标签、冻结 GFM、训练中并行 geometry model。
- 推理接口：observation-to-action、future rollout-to-action、joint denoising。
- 因果性：future token 是否泄漏给 action token；训练与推理 attention mask 是否一致。
- 计算：训练额外分支、推理去噪步数、控制频率、显存和视频生成是否必需。
- 评价：动作成功、几何一致性、生成质量、OOD 稳健性是否同时报告。

## 读完应能回答

- 如果推理时不生成未来，模型还能否被称为 world model？其价值来自哪里？
- dense depth 与 4D correspondence 分别约束什么失败？
- 显式 future rollout 对动作成功有独立贡献吗？
- 训练期 auxiliary head 的增益是否只是多任务正则化？
- 为什么 action/video/geometry 的 attention visibility 必须严格因果？
- 如何公平比较 inference-free WAM 与 rollout-based WAM？

## 入门实践

不要从训练视频 DiT 开始。先在同一组离线 robot feature 上训练三个小型 future predictor：RGB latent、depth latent、GFM feature。保持 backbone、参数量和 action head 相同，比较 future prediction、action retrieval 和 OOD action success。这个小实验能提前判断“完整几何输出”是否真的比“几何 feature prediction”有价值。

## 退出标准

能够画出四篇论文的训练图和推理图，并明确指出哪些分支只用于训练、哪些输出参与动作恢复、哪些 attention 存在因果泄漏风险，就达到了入门标准。

