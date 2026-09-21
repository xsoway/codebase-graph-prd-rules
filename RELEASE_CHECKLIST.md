# 发布前检查记录 — codebase-graph-prd-rules

> 依据 `oss-release-prep` 的 `references/release-checklist.md` 逐项核对。
> 每项的勾选结论均来自实际命令输出或文件存在性证据。

## A. 版本库状态

- [x] 项目已 `git init` 且已提交 —— 证据：`git log --oneline -1` → `22f3161 chore: init repo with bilingual README, MIT license, and two business-rule skills`
- [x] 明确默认分支 `main`，工作区干净 —— 证据：`git branch -m main`；`git status -sb` → `## main`
- [x] 无未提交的敏感文件被跟踪（凭据 / `.env` / 私钥 / 构建产物）—— 证据：`git ls-files | grep -c DS_Store` → `0`；`find . -name '.env*'` → 无

## B. 必备文件

- [x] `README.md`（英文版）存在 —— 根目录，12.5KB
- [x] `README.zh-CN.md`（中文版）存在，切换链接互指正确 —— 证据：`README.md:15 → <a href="./README.zh-CN.md">中文</a>`；`README.zh-CN.md:15 → <a href="./README.md">English</a>`
- [x] `LICENSE` 存在（MIT，版权 xulanzhong，2026）
- [x] `.gitignore` 排除 macOS（`.DS_Store`）/ Python（`__pycache__` 等）/ IDE 产物
- [x] `.gitattributes` 统一行尾（`* text=auto eol=lf`）

## C. README 质量

- [x] 结构：居中徽章 + 定位 + 切换链接 + 目录 + 核心概念 + 仓库结构 + 两个 Skill 对比 + 快速开始 + 验证 + 安全边界 + FAQ + 路线图 + 贡献指南 + License + 维护者（参照 `references/readme-style.md` 详尽版）
- [x] 快速开始里每个命令有依据且可运行 —— 证据：`verify_skill_package.py` 已实际运行，两个包均 exit 0，输出 `skill package contract passed: 3 eval cases, prompt, metadata, references`
- [x] 目录树、配置项、功能描述与代码一致 —— 两个 Skill 的 prompts / references / evals / agents / scripts 均经逐文件读取核对，README 结构树与实际目录逐一对应
- [x] 双语两版覆盖同一组主题、结构镜像

## D. 敏感信息扫描（发布红线）

- [x] 无真实 API key / token / cookie / 私钥 / 密码 —— 证据：对全部 `.md` / `.yaml` 跑正则扫描，`sk-…`/`sk-proj-`/`sk-ant-`/`ghp_`/`xox…`/`AKIA…`/`authorization:`/`api key`/`secret`/`BEGIN … PRIVATE KEY` **零命中**（唯一匹配是 `verify_skill_package.py` 校验脚本自身的扫描正则定义，非真实凭据）
- [x] 无模型默认凭据 / 高熵占位疑似值 —— 零命中
- [x] 无个人数据（姓名 / 手机 / 地址 / 身份证 / 浏览器指纹）—— `[\w.+-]+@[\w.-]+\.\w{2,}` 扫描仅命中 README 维护者邮箱 `xulanzhong521@gmail.com`，该邮箱是项目公开维护者联系方式，与相邻开源项目 `skill-spec` 完全一致，属公开元数据而非泄露的个人数据
- [x] 无绝对本机路径（`/Users/…`、`/home/…`）—— 零命中；README 仅使用相对路径与代码位置占位（如 `src/...:line`）
- [x] `.env`、凭据文件、构建产物、日志文件不被 git 跟踪 —— 无此类文件；`.gitignore` 已覆盖
- [x] 示例、测试、README 代码块无真实用户数据或密钥 —— 已核对 `examples/` 两个示例仅说明结构，不含业务事实

## E. 可验证性

- [x] 校验命令已运行且通过 —— 证据：两个 `verify_skill_package.py` 均 exit 0
  - `python3 codebase-graph-business-rules/scripts/verify_skill_package.py codebase-graph-business-rules` → exit 0
  - `python3 codebase-graph-module-rules/scripts/verify_skill_package.py codebase-graph-module-rules` → exit 0
- [ ] 未运行行为级 eval（`run`）—— 原因：需在指定引擎/数据下消耗模型资源，未在本检查中执行；README 已明示静态校验 ≠ 项目已被分析
- [x] 依赖、运行环境已说明 —— README「快速开始」注明 Python 3.9+、仅标准库、无第三方依赖

## F. 发布动作授权（绝不默认执行）

- [ ] `git push` / 创建远程仓库（`gh repo create`）—— **未执行**，未获授权
- [x] 已给出用户可复制的命令（见下方「未执行的发布动作」）

---

## 未执行的发布动作

用户显式要求发布到 GitHub 后，运行：

```bash
cd /Users/xulanzhong/Desktop/my-ai-workspace/code_project/src/github-repos/codebase-graph-prd-rules
gh repo create <owner>/codebase-graph-prd-rules --public --source=. --push
```

或将本地 `main` 推送到已有远程：

```bash
git remote add origin <remote-url>
git push -u origin main
```

---

## 遗留风险 / 说明

- 根级 `status-beta` 徽章为本次发布采用的保守标记；如项目定位为生产可用，可改为 `stable`。
- 未执行行为级 eval（`run`），属于发布后可选回归项，不影响包结构可发布性。
- 维护者邮箱为公开项目联系方式，符合 oss-release-prep 的维护者约定（参照 skill-spec）。