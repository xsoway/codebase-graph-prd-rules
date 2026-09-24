# 发布前检查记录 — codebase-graph-prd-rules

> 依据 `oss-release-prep` 的 `references/release-checklist.md` 逐项核对。
> 每项的勾选结论均来自实际命令输出、GitHub API/页面证据或文件存在性证据。
> 状态：**已发布**（v1.0.0）。

## A. 版本库状态

- [x] 项目已 `git init` 且已提交 —— 证据：`git log --oneline -1`；最新提交 `2787391 chore: add asset package, Makefile governance, secrets gate, gruvbox-material homepage`
- [x] 明确默认分支 `main`，工作区干净 —— 证据：`git branch -m main`；发布后 `git status -sb` 干净
- [x] 无未提交的敏感文件被跟踪（凭据 / `.env` / 私钥 / 构建产物）—— 证据：`git ls-files | grep -c DS_Store` → `0`；`find . -name '.env*'` → 无

## B. 必备文件

- [x] `README.md`（英文版）存在 —— 根目录，已更新结构树（新增打包/治理文件）
- [x] `README.zh-CN.md`（中文版）存在，切换链接互指正确 —— `README.md:15 → 中文`；`README.zh-CN.md:15 → English`
- [x] `LICENSE` 存在（MIT，版权 xulanzhong，2026）
- [x] `.gitignore` 排除 macOS（`.DS_Store`）/ Python（`__pycache__` 等）/ IDE 产物，且覆盖 `dist/`、`build/`、`*.egg-info`
- [x] `.gitattributes` 统一行尾（`* text=auto eol=lf`）

## C. README 质量

- [x] 结构完整：徽章 + 定位 + 切换链接 + 目录 + 核心概念 + 仓库结构 + 两个 Skill 对比 + 快速开始 + 验证 + 安全边界 + FAQ + 路线图 + 贡献指南 + License + 维护者
- [x] 快速开始里每个命令有依据且可运行 —— 证据：`verify_skill_package.py` 以真实解释器实际运行，两个包均 exit 0，输出 `skill package contract passed: 3 eval cases, prompt, metadata, references`
- [x] 目录树、配置项、功能描述与代码一致 —— 新增发布层文件（pyproject/setup/MANIFEST/Makefile/scripts/src/index.html）已加入 README 结构树
- [x] 双语两版覆盖同一组主题、结构镜像

## D. 敏感信息扫描（发布红线）

- [x] 无真实 API key / token / cookie / 私钥 / 密码 —— 证据：`scripts/check_secrets.py` 以真实解释器运行，对 `.md/.yaml/.yml/.py/.html/.toml` **零命中**，exit 0。覆盖 `sk-proj-*`/`sk-ant-*`/`sk-*`/`ghp_*`/`xox*-*`/`AKIA*`/`authorization: bearer`/`api key`/`secret`/`-----BEGIN …PRIVATE KEY-----`
- [x] `dist/*` wheel 与 sdist 解包扫描 —— **零命中**
- [x] 无个人数据（姓名 / 手机 / 地址 / 身份证 / 浏览器指纹）—— 仅 README 维护者邮箱 `xulanzhong521@gmail.com`，与相邻开源项目一致，属公开元数据
- [x] 无绝对本机路径（`/Users/…`、`/home/…`）—— 零命中；README 仅用相对路径与占位
- [x] `.env`、凭据文件、构建产物、日志文件不被 git 跟踪 —— 无此类文件；`.gitignore` 已覆盖
- [x] 发布记录 `RELEASE_CHECKLIST.md` 在扫描中被显式排除（其本就书写这些模式字样，属文档非泄露），避免红线误伤发布记录本身（外部审查发现并修复）

## E. 可验证性

- [x] 校验命令已运行且通过（真实解释器，非环境 stub）—— 证据：
  - `uv run python scripts/check_secrets.py`（真实 Python 3.10）→ `OK: no secrets or absolute local paths detected`，exit 0
  - 两个 `verify_skill_package.py` → 均 exit 0，`skill package contract passed: 3 eval cases, prompt, metadata, references`
  - `make code-clean`（PY 指向真实解释器）→ exit 0：validate 通过 + check-secrets 通过 + `uv build` 产出 sdist/wheel
- [x] 资产包可验证 —— 证据：
  - `uv build` → `dist/codebase_graph_prd_rules-1.0.0.tar.gz` + `.whl`
  - wheel 装入临时 venv（真实解释器）：`import codebase_graph_prd_rules` 正常、`__version__==1.0.0`、`available_skills()` 返回 2 个 skill、`verify-skill-package` 控制台入口 exit 0
  - sdist 干净重建 → 安装后 `verify-skill-package` 同样通过（rebuild-from-sdist 成立）
- [x] 主页中英切换在无头 Chromium 本地验证 —— 默认中文、切英文/切回正常、同一时刻仅一种语言可见
- [x] 依赖、运行环境已说明 —— README「快速开始」注明 Python 3.9+、仅标准库、无第三方依赖
- [ ] 未运行行为级 eval（`run`）—— 原因：需在指定引擎/数据下消耗模型资源；README 已明示静态校验 ≠ 项目已被分析（发布后可选回归项）

## F. 发布动作（本次已执行并授权）

- [x] `git push` 到 `origin/main` —— 证据：`git push origin main` → `f4c4ac3..2787391 main -> main`
- [x] About 描述 / topics / website 已配置 —— 证据：`gh repo view --json description,repositoryTopics,homepageUrl`：
  - description：`Two source-verified AI-agent skills that turn project code into traceable business-rule documents (whole-project + single-module). Graph-guided, evidence-graded, evaluation-backed.`
  - topics（8）：`agent, ai, code-graph, graphify, llm, persona, self-memory, skill`（覆盖要求的 ai/llm/skill/persona/self-memory）
  - homepage：`https://xsoway.github.io/codebase-graph-prd-rules/`
- [x] GitHub Pages 已启用并构建成功 —— 证据：`gh api .../pages` → `status: built`，URL 返回 HTTP 200，服务主页（含中英切换按钮）
- [x] GitHub Discussions 已启用 —— 证据：`has_discussions: true`；默认分类 Annoucements / General / Ideas / Polls / Q&A / Show and tell
- [x] Release `v1.0.0` 已创建并附带两个资产 —— 证据：`gh release view v1.0.0 --json assets` → `[.whl, .tar.gz]`，states `uploaded`
- [x] 资产下载 URL 可达 —— 证据：`releases/latest/download/…whl` 与 `.tar.gz` 均 HTTP 200

## G. 外部审查（团队外 reviewer）

- [x] 已派发独立 reviewer 审查本次全量改动（Reviewer 子代理），结论：打包正确、无回归、接口为纯新增、版本一致
- [x] 发现的 1 个 High 级阻塞问题已修复并复验证：
  - 问题：`check_secrets.py` 的裸 `sk-proj-|sk-ant-` 模式命中发布记录自身的文档字样 → 红线扫描恒 exit 1，反向阻塞发布
  - 修复：(1) 显式排除 `RELEASE_CHECKLIST.md`；(2) 模式改为高熵/带前缀形式并补齐 `xox*-`、`authorization: bearer`、`api key`、`secret`、PEM 私钥，整体 IGNORECASE
  - 复验证：真实解释器运行 → `OK: no secrets...` exit 0；`make code-clean` exit 0
- [x] 其余发现（README 结构树未含新文件、主页 wheel 链接为发布后有效）均已处理/确认

---

## 遗留风险 / 说明

- 根级 `status-beta` 徽章为本次发布的保守标记；如项目定位生产可用可改 `stable`。
- 未执行行为级 eval（`run`），发布后可选回归项，不影响包结构可发布性。
- 主页 wheel 安装链接依赖 `releases/latest`；若未来发布更名 wheel 需同步更新 `index.html` 与 release notes。
- GitHub Pages 根分支部署会公开全部仓库文件（repo 本就公开），skill 目录页面化可浏览，属预期。