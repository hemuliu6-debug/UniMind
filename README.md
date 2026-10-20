## Windows 快速开始

### 首次安装

1. 安装 64 位 Python 3.13。
2. 将项目解压到本地文件夹。
3. 双击 setup_windows.bat，等待依赖安装和离线测试完成。
4. 双击 start_windows.bat，启动网页。
5. 如果浏览器没有自动打开，访问 http://127.0.0.1:7860 。

使用期间保持终端窗口打开，按 Ctrl+C 停止服务。

### 配置文件

首次安装时，脚本会将 .env.example 复制为 .env。
如果 .env 已存在，脚本会保留已有配置。

默认使用离线演示模式，无须 API Key。
离线模式用于验证交互和检索流程，不生成真实 AI 解答。

### 分享项目

分享源代码和 .env.example。
不要打包 .venv、.venv-old、venv、.env 和 Python 缓存目录。
每台电脑应自行运行安装脚本，创建本机虚拟环境。

如果提示虚拟环境引用的 Python 不存在，
将 .venv 重命名为一个尚不存在的备份目录名，
然后重新运行 setup_windows.bat。

# UniMind｜多学科生成式 AI 学习助手

> 大二生成式人工智能课程黑客松 · 10 人 / 7 天 · Python 3.13 + Gradio 6 + DeepSeek（可选）

本仓库是**可以直接运行与分发**的统一网页 App 项目骨架：一个入口 `app.py`，四个学科模块，各自有问答逻辑与本地小知识库，公共层负责 RAG 检索和 API 调用。**默认离线演示**，没有 API Key 也能搭建、调试 UI；离线回答只是流程占位，不是真正的模型推理。

## 0. 目录说明

```text
UniMind/
├── app.py                     # 唯一网页入口（9 号负责）
├── modules/
│   ├── circuit.py              # 1、2 号：模拟电路
│   ├── math_subject.py         # 3、4 号：高等数学
│   ├── physics.py              # 5、6 号：大学物理
│   ├── programming.py          # 7、8 号：Python 编程
│   └── _ui.py                  # 公共 Gradio 组件（9 号负责）
├── knowledge/
│   ├── circuit.json            # 对应学科的知识库
│   ├── math.json
│   ├── physics.json
│   └── programming.json
├── core/
│   ├── pipeline.py             # RAG 主流程：检索 → 生成
│   ├── retriever.py            # 关键词检索（不是向量检索）
│   └── llm_client.py           # 唯一 DeepSeek API 调用文件
├── docs/
│   ├── 团队分工与7天计划.md
│   ├── 模块接口规范.md
│   ├── Git协作与集成步骤.md
│   ├── 测试与答辩标准.md
│   └── 学科任务书/               # 四份可以直接发给组员的任务书
├── tests/test_project.py       # 不联网、不调用付费 API 的单元测试
├── .env.example                # 可复制为 .env（只存在本机）
├── requirements.txt
├── setup_windows.bat           # Windows 初始安装
└── start_windows.bat           # Windows 启动
```

## 1. Windows：快速启动（**队友优先看这里**）

前置：安装 **Python 3.13**（和负责人保持一致），联网安装软件包；不需要每位队友都有 API Key。

1. 下载项目 ZIP 并解压，进入解压后的根目录（应看到 `app.py`、`requirements.txt`）。
2. **双击 `setup_windows.bat`**：自动建立 `.venv`、安装依赖、创建 `.env`，并运行离线测试。首次可能耗时几分钟。
3. **双击 `start_windows.bat`**：启动 UniMind 网页。不要关掉黑色终端窗口。
4. 浏览器打开 `http://127.0.0.1:7860`（若终端显示其他端口，以终端为准）。
5. 四个学科 Tab 均可输入问题；页面顶部注明“离线演示模式”。这是正常现象。

**命令行替代方式（适合已使用 Mini LabMate 的同学）：**

```powershell
cd 你的项目文件夹路径
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe app.py
```

> `.env` 已存在时无需再次复制，以免覆盖密钥。`start_windows.bat` 会从项目根目录加载 `.env`。

## 2. 真实 AI 模式（仅负责人、测试人员必要时启用）

1. 在本机打开 `.env`，把 `DEMO_MODE=1` 改成 `DEMO_MODE=0`。
2. 在 `DEEPSEEK_API_KEY=` 后写入自己有效的 DeepSeek API Key；不要上传 `.env`，更不要把密钥发在群里。
3. 运行 `start_windows.bat`；只有点击“AI 解答”才会发起云端请求和产生可能的费用。
4. 模型名默认 `deepseek-flash`，接口基址默认 `https://api.deepseek.com`；如果厂商接口有更新，以官方文档为准。

**安全与成本：** 在线时上传的图片、提问与检索到的资料会发送给模型提供方；不要上传含隐私、版权受限或商业保密信息的材料。模型可能回答错误，学术推导与实际电气操作都需人工验证。演示后可恢复 `DEMO_MODE=1`。不要开启公开分享链接或未经认证地暴露带付费密钥的服务。

## 3. 给四个学科组的最短说明

- 模电：仅修改 `modules/circuit.py` 与 `knowledge/circuit.json`。
- 高数：仅修改 `modules/math_subject.py` 与 `knowledge/math.json`。
- 物理：仅修改 `modules/physics.py` 与 `knowledge/physics.json`。
- 编程：仅修改 `modules/programming.py` 与 `knowledge/programming.json`。
- 所有组都保持 `answer(question, image=None) -> str` 与 `build_tab() -> None` 不变。**不得调用 `demo.launch()`，不得在模块中粘贴自己的 API Key。**
- 若要修改 `app.py`、`core/` 或 `modules/_ui.py`，向 9 号负责人提交需求，由其统一修改。

详见 `docs/模块接口规范.md` 和 `docs/学科任务书/`。

## 4. 验收和答辩

先在离线模式运行：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

所有测试通过后，再按 `docs/测试与答辩标准.md` 中的样本测试在线效果；不要把离线模拟回答误当成 AI 生成或准确率评估。第 3 天必须将四个模块集成到同一页面，第 5 天冻结主体功能，第 7 天演示。

## 5. 特色、限制与后续扩展

- 当前已有四学科页面、共用 API、模拟电路的图片输入、学科提示词、JSON 知识检索、来源列表。
- 检索方法是**关键词匹配**，不是向量检索；更严格地讲是一个轻量的“检索增强生成”教学原型。后续可换 TF-IDF / Embedding 检索，但必须先让 MVP 稳定。
- 目前四个模块是单轮问答；多轮会话、公式渲染优化、用户账户等都属于选做项。
- 编程组**只分析代码，不执行用户代码**；电路组不提供危险的高压实操指令。

项目技术参考：
- Gradio Blocks：https://www.gradio.app/docs/gradio/blocks
- DeepSeek OpenAI 兼容 API：https://api-docs.deepseek.com/
- DeepSeek 图片输入：https://api-docs.deepseek.com/guides/vision/
