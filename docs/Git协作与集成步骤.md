# Git 协作和最终集成（9 号负责人照此执行）

## A. Day 1：发布统一版本

1. 9 号将完整 UniMind 文件夹上传至一个 GitHub 仓库；第一次提交只包含代码、知识卡、文档和 `.env.example`。
2. **绝对不上传 `.env`、密钥、`.venv`、私有课件、个人图片和大型临时文件**。仓库已有 `.gitignore`。
3. 仓库设为私有或课程组允许范围内访问，邀请其他成员 Collaborator。
4. 约定以 `main` 为可运行分支，学科组禁止直接 push 到 `main`。
5. 10 人按 `README.md` 运行离线网页；至少截取自己的四 Tab 页面作为环境验收。

## B. Day 2：各组独立开发

每组组长使用相应分支（同组成员可从同一分支协作，但避免同时编辑同一行）：

```powershell
git clone 仓库地址
cd UniMind
git switch -c feature/circuit
# 仅编辑 modules/circuit.py 和 knowledge/circuit.json
git add modules/circuit.py knowledge/circuit.json
git commit -m "feat: improve circuit assistant"
git push -u origin feature/circuit
```

其他组依次使用 `feature/math`、`feature/physics`、`feature/programming`。**不要把 `git clone 仓库地址` 原样执行，替换成仓库的实际 HTTPS 地址。**

## C. Day 3：第一次合并

1. 组长在 GitHub 上为自己的分支创建 Pull Request（PR），标题写明模块名。
2. PR 描述必须包括：修改文件、完成的功能、测试案例、失败案例和网页截图。
3. 9 号先阅读差异，再逐个合并，一次只合一个 PR；每次合并后执行：

```powershell
git switch main
git pull origin main
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe app.py
```

4. 打开浏览器测试四个 Tab，尤其测试模电图片上传与计算题回答。
5. 如果某个模块无法合并或运行：让该组在自己的分支修复，不要在 `main` 中直接大改。

## D. Day 4–5：技术集成

- 公共层只有 9 号可以改：`core/llm_client.py`、`core/pipeline.py`、`core/retriever.py`、`app.py`、`modules/_ui.py`。
- 统一 `.env` 中配置真实调用方式，**不把同一个 API Key 发给所有组员**。组员主要用 DEMO_MODE=1 开发，只有 9 号统一进行线上验证。
- 每个学科至少验证 5 个题目；测试计划见 `测试与答辩标准.md`。
- 当接入新功能会影响其他模块时，先建 Issue/提需求，经集成负责人确认后再做。

## E. Day 6–7：冻结、发布与演示

1. D6 上午确定一个可运行的主分支 commit，打标记 `v1.0-demo`，不再临时引入新依赖。
2. 10 号按 README 在另一台 Windows 电脑上全新解压/安装，验证可复现。
3. D7 用本机浏览器做现场演示，提前检查网络和 API 余额；准备经过真实录制的备用视频。
4. 提交：源码、README、组员分工记录、测试报告和演示材料（按老师具体要求）。

## 本地与线上访问区别

`http://127.0.0.1:7860` **只对运行程序的这台电脑可访问**，不等于已在公网部署。团队成员可各自本地运行；现场演示通常一台电脑启动一次服务即可。如确需公网访问，另行选择有 HTTPS、访问权限和密钥保护的部署平台，不能简单将个人 API Key 的网页无认证地暴露出去。
