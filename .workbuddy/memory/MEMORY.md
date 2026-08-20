# 项目长期记忆（AI 大模型学习）

## 用户档案
- 工业 Qt 工程师，C++ 桌面端背景，有工程化/系统集成经验。
- 转行目标：AI 大模型应用开发。
- 差异化方向：工业 AI + 本地端侧部署（llama.cpp/GGUF 量化）、Qt 客户端 + 本地 LLM + RAG + MCP。
- 有两台电脑，希望跨设备继续学习（工作区需手动同步，见下）。

## 已定学习路线（v2.1 · 博学谷 2026 大纲为主 + 尚硅谷精选补充）
- 主线 7 大模块约 31 周：①开发入门(Python+聊天机器人+FastAPI服务化) ②语言进阶(OOP/MySQL/Pandas，含开窗函数/数据可视化) + **模块2补充·工程基础(Linux/Shell+Docker，第10周)** ③智能体平台(Coze/Dify) ④核心技术(ML/DL+PyTorch+Transformer) ⑤RAG应用(工业手册全栈，增强 MinerU/OCR+RAGAS+Graph RAG) ⑥智能体高级(ReAct/LangGraph/MCP，含 NL2SQL 案例) ⑦微调部署(LoRA/QLoRA+量化+vLLM+llama.cpp)。
- 2026-08-18 v2.0→v2.1 精选补充依据：尚硅谷《人工智能大模型课程大纲&项目手册》(82页PDF，10阶段/24项目)，已提取全文存 .workbuddy/tmp/pdf_text.txt。
- 赠送专题选修：Vibe Coding、算法、蒸馏、强化学习（深化为 RLHF 三阶段+DPO/GRPO 案例）、CV/多模态、OpenClaw（+Harness Engineering 了解）。
- 差异化保留：模块5场景=工业设备手册（对标尚硅谷「掌柜智库」）、模块6里程碑=Qt封装MCP、模块7增补llama.cpp/GGUF端侧量化。

## 协作约定
- 用户希望 AI 陪伴式"带着学"：定计划、讲解、布置练习、检查答疑。
- 学习节奏：工作日每天下班后 1–2 小时；主线约 7 个月（30 周）。
- **学习模式：项目先行**（2026-08-10 定）——跳过顺序学基础，直接做里程碑项目，Python 基础穿插补；用户能读懂 Python 但不擅长写，讲解代码要逐行注释 + C++ 视角对照。
- 学习成果/进度文档统一放在本工作区根目录（学习计划.md、学习进度.md、各阶段课程讲义），便于多电脑同步继续。
- **讲义同步纪律（2026-08-18 定）**：每次教学新内容（新知识点/演示/练习/坑）必须同步写入对应讲义 .md，演示脚本/图片也存讲义目录；不能只存在对话里或 .workbuddy/tmp。
- 微调需 GPU：优先 Colab/Kaggle 免费 T4；无 GPU 可用小模型 CPU 慢跑。
- 当前进度：**模块 2 · 语言进阶完成 ✅（2026-08-18）**——第 9 课 MySQL（含开窗函数）✅、第 10 课 PyMySQL ✅、第 11 课 Numpy/Pandas + 数据可视化（Matplotlib/Seaborn）✅；下一步：模块 2 补充·工程基础（第 10 周 Linux/Shell+Docker）→ 模块 3 智能体平台（Coze/Dify）。里程碑 1 已于 2026-08-11 完成。
- **本地模型：qwen3.5:4b**（用户自选并已安装，曾用 deepseek-r1:1.5b；Qwen 若开思考模式也可能输出思考过程）。
- **实现偏好：接口调用倾向用官方 ollama SDK**（client.chat），而非裸 requests（用户 2026-08-11 采用）。
- **Python 环境约定（2026-08-18 确认）：用户所有 AI 项目统一用 conda aipy 环境（D:\miniconda3\envs\aipy，python.exe 即 /d/miniconda3/envs/aipy/python.exe；已含 numpy 2.4.6/pandas 3.0.5/pymysql 2.2.8/sqlalchemy 2.0.51 等）。** 需要给用户装包时优先装到 aipy；WorkBuddy 侧验证代码用自带隔离 venv（C:\Users\YueLi\.workbuddy\binaries\python\envs\default），两边互不污染。

## 工作区与记忆机制
- 工作区路径随电脑不同：另一台电脑为 F:\WorkBuddy\AI大模型学习 / Agent-study；本机（2026-08-13 起）为 C:\Users\YueLi\Desktop\Agent-study。不跨设备自动同步，靠网盘/Git 手动同步整个工作区文件夹。
- 本地记忆：用户级 C:\Users\YueLi\.workbuddy\；项目级 .workbuddy\memory\。
- MySQL 环境（本机 2026-08-14 实测）：Docker Desktop + 容器 ai-mysql（mysql:latest 26.7.0，宿主机端口 **13306**→容器内 3306，root 密码 root123456；另有用户 ai/ai123456、默认库 ai_demo）。注意：本机无 mysql 客户端，操作需 `docker exec -it ai-mysql mysql -u root -p`；PyMySQL 连接端口用 13306。另一台电脑的 MySQL 配置可能不同（如 8.4/3306），同步记忆时注意区分。
