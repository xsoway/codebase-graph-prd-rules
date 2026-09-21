<p align="center">
  <img src="https://img.shields.io/badge/codebase--graph--prd--rules-1.0.0-blue" alt="codebase-graph-prd-rules 版本">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="许可证">
  <img src="https://img.shields.io/badge/status-beta-yellow" alt="状态">
  <img src="https://img.shields.io/badge/python-3.9+-informational" alt="Python 版本">
</p>

<h1 align="center">codebase-graph-prd-rules</h1>

<p align="center">
  <strong>把代码整理成可追溯的业务规则</strong>
</p>

<p align="center">
  <a href="./README.md">English</a>
</p>

<p align="center">
  <b>先建图谱 · 源码确认 · 非开发者可读 · 可评测</b>
</p>

---

## 目录

- [这是什么](#这是什么)
- [为什么需要](#为什么需要)
- [核心概念](#核心概念)
- [仓库结构](#仓库结构)
- [两个 Skill](#两个-skill)
- [快速开始](#快速开始)
- [验证](#验证)
- [安全边界](#安全边界)
- [常见问题 FAQ](#常见问题-faq)
- [路线图](#路线图)
- [贡献指南](#贡献指南)
- [许可证](#许可证)
- [维护者](#维护者)

---

## 这是什么

`codebase-graph-prd-rules` 是一组互补的 AI 代理 **Skill**，把项目源码整理成供非开发者（产品、运营、QA）阅读的、**可追溯的详细业务规则文档**。

两个 Skill 共享同一方法论与证据边界——先建 **Graphify** 代码图谱，用图谱定位入口与调用链路，再逐条用真实源码、SQL/XML 与配置确认规则。**图谱负责导航，源码负责确认**。两者都不改动业务系统——只分析和写文档。

两个 Skill 覆盖不同粒度：

- **`codebase-graph-business-rules`** —— *全项目*业务规则。扫描整个项目、建图，产出一份集成文档：模块地图、入口、实体/状态、数据与配置、端到端链路、逐模块规则表、测试范围与追溯索引。
- **`codebase-graph-module-rules`** —— *单模块*深挖。给定功能描述或模块名，追溯一个模块的规则、排序/限额/状态/流程，产出测试导向的专项文档。

---

## 为什么需要

| 常规做法（反例） | 本项目 |
|---|---|
| 规则只存在开发者脑中或零散注释里 | 成文、可源码验证的规则文档 |
| 排序被含糊地叫成“优先级” | 拆分资格过滤 vs 排序键 vs 后置过滤/终止 |
| 无证据，无法核查 | 每条规则带 `src/...:line` 来源 |
| 图谱推断边被当成事实 | 图谱只作导航；源码确认事实 |
| 静态检查通过被说成已验证 | 静态与运行行为分开、如实报告 |
| 模块多条链路在末尾重复追加 | 同一模块的分支合并到同一节 |

它解决 **5 个工程痛点**：

1. **可追溯** — 每条规则记录来源文件+行号，便于审计与变更。
2. **非开发者可读** — 表格与 Mermaid 图解释业务含义，而不是堆类名。
3. **证据诚实分层** — EXTRACTED / INFERRED / 源码确认分开报告。
4. **测试就绪** — 每条关键规则映射到可执行的 P0/P1 测试断言矩阵。
5. **安全** — 拒绝未授权的生产动作、绝不输出凭据。

---

## 核心概念

### 1. 图谱导航，源码确认

图谱负责定位入口与候选链路（`触发 → 编排 → 决策 → 存储/日志 → 外部结果`）。每条规则再用源码、SQL/XML、配置确认——**INFERRED 图谱边只是线索，不是事实**。

### 2. 三层规则

业务规则分为三层，绝不混为一谈：

- **资格过滤** —— 候选是否具备进入资格？
- **候选排序** —— 谁先处理（字段、方向、null 规则、并列行为）？
- **运行时控制** —— 限额、去重、并发、发送、失败回滚。

排序必须写明字段、方向、null/空值规则、并列行为、后置过滤与最终终止条件——以实际比较器或 SQL `ORDER BY` 为准，而非假设。

### 3. 证据等级

| 等级 | 可写结论 | 不可写结论 |
|---|---|---|
| 源码/SQL/配置已复核 | 当前实现的条件、顺序、字段、调用与副作用 | 外部系统最终结果 |
| 图谱 EXTRACTED | 可作为定位和关系线索 | 未读实现的业务规则 |
| 图谱 INFERRED | 标为待源码确认的候选关系 | 已确认调用或业务合同 |
| 注释/日志/字段名 | 补充意图或待确认项 | 独立事实 |
| 运行结果 | 该环境和输入下的观测 | 未覆盖场景的普遍保证 |

### 4. 只分析，不执行

两个 Skill 只分析和写文档。未经显式授权，拒绝调用真实下游服务、发送真实线索、改动数据或运行生产行为——并如实报告哪些*未执行*。

---

## 仓库结构

```text
codebase-graph-prd-rules/
├── README.md                        # 本说明（英文）
├── README.zh-CN.md                  # 本说明（中文）
├── LICENSE                          # MIT
├── .gitignore                       # 排除 macOS/Python/IDE 产物
├── .gitattributes                   # * text=auto eol=lf
├── codebase-graph-business-rules/   # 全项目业务规则 Skill
│   ├── SKILL.md                     # 激活入口
│   ├── prompts/codebase-graph-business-rules.md
│   ├── agents/openai.yaml           # 发现元数据
│   ├── references/
│   │   ├── graphify-and-evidence.md # 建图顺序 + 语义提取 + 证据等级
│   │   └── document-contract.md     # 文档与测试契约
│   ├── evals/eval.yaml + cases/     # 3 个回归用例
│   ├── examples/project-rules-example.md
│   └── scripts/verify_skill_package.py
└── codebase-graph-module-rules/     # 单模块规则 Skill
    ├── SKILL.md                     # 激活入口
    ├── prompts/codebase-graph-module-rules.md
    ├── agents/openai.yaml           # 发现元数据
    ├── references/
    │   ├── module-discovery.md      # 术语→候选→链路检索
    │   └── module-document-contract.md
    ├── evals/eval.yaml + cases/     # 3 个回归用例
    ├── examples/module-rules-example.md
    └── scripts/verify_skill_package.py
```

每个 Skill 都是自包含包：激活入口、完整执行规范、发现元数据、三个 eval 用例、示例与可执行的包校验器。

---

## 两个 Skill

| | `codebase-graph-business-rules` | `codebase-graph-module-rules` |
|---|---|---|
| **范围** | 全项目 | 单个功能 / 模块 |
| **输入** | 项目根 + 源码范围 | 功能描述 / 模块名 |
| **输出** | 集成文档：模块地图、实体/状态、数据与配置、链路、逐模块规则、测试范围、追溯索引 | 专项文档：边界、关系、规则/排序/限额、测试矩阵 |
| **合并规则** | 同一模块跨入口/异常/定时链路合并到一节 | 同一模块主/支链路合并到一节 |
| **适用** | “梳理全项目 / 全量功能 / PRD 基线” | “梳理某个模块 / 某条规则” |

选择规则：一个明确边界的模块用 `codebase-graph-module-rules`；无单模块边界的全项目扫描用 `codebase-graph-business-rules`。

---

## 快速开始

**环境要求**：校验器需要 Python 3.9+（仅标准库，无第三方依赖）。需要一个可分析的源码项目；语义图谱提取可选地需要配置 LLM 凭据。

### 1. 让代理能加载该 Skill

把需要的 Skill 目录（如 `codebase-graph-business-rules/`）复制到代理的 skill 路径，或按本地路径 Skill 引用。

### 2. 校验一个 Skill 包

对 Skill 目录运行内置包校验器：

```bash
python3 codebase-graph-business-rules/scripts/verify_skill_package.py codebase-graph-business-rules
# → skill package contract passed: 3 eval cases, prompt, metadata, references

python3 codebase-graph-module-rules/scripts/verify_skill_package.py codebase-graph-module-rules
# → skill package contract passed: 3 eval cases, prompt, metadata, references
```

校验器检查：必需工件存在、`SKILL.md` 前置 `name` 与目录一致、`agents/openai.yaml` 的 `metadata.key` 一致、任何 `.md`/`.yaml` 无凭据类内容。

### 3. 使用该 Skill

向代理提出请求，例如：

```text
"请扫描项目代码，先建 Graphify 图谱，再按模块输出业务规则、来源、流程图和测试范围。"
"请针对线索包和排序规则，先建 Graphify 图谱，再输出详细业务规则、流程图、来源和测试点。"
```

两个 Skill 默认在项目本地 `docs/` 输出 Markdown 文档；明确要求时附加 CSV/JSON 规则账本。

---

## 验证

每个 Skill 带 `evals/` 下的 3 用例回归契约：

| 用例 | 文件 | 验证什么 |
|---|---|---|
| 成功路径 | `basic-success.yaml` | 完整请求产出图谱 + 规则 + 来源 + 测试 |
| 信息缺失 | `edge-incomplete-input.yaml` | 缺少输入必须暴露缺口/“待确认”，而非猜 |
| 范围/风险边界 | `edge-scope-boundary.yaml` | 越界请求（如发送真实线索）被拒绝 |

静态包校验（`verify_skill_package.py`）证明*结构与安全*；它**不代表**任何项目已被分析。

---

## 安全边界

- **无凭据**：不输出、不持久化任何 API key、token、cookie 或私钥。
- **无个人数据 / 绝对本机路径**（`/Users/…`、`/home/…`）在任一产物中。
- **无未授权外部动作**：未经显式授权，绝不调用真实下游服务或改动数据。
- **凭据（用于语义提取时）只存在于进程环境中**——绝不写入源码、文档、Skill、shell 配置或输出。
- **无伪造运行结论**：未运行的集成/数据库/调度/生产行为，如实报告为未执行。

---

## 常见问题 FAQ

**Q: 该用哪个 Skill？**
一个边界明确的模块用 `codebase-graph-module-rules`；无单模块边界的全项目扫描用 `codebase-graph-business-rules`。

**Q: 需要 LLM 凭据吗？**
不需要。语义提取仅在显式提供凭据时才执行；无凭据时退化为结构图谱+源码复核，并报告该限制。

**Q: 这些 Skill 会改我的代码吗？**
不会。两个 Skill 只分析和写文档。改动业务代码、数据或外部系统需要你另行显式授权。

**Q: 文档长什么样？**
Markdown + 表格 + Mermaid 流程/状态图，业务含义优先而非堆类名，并带 `src/main/.../Service.java:120` 这类可定位来源。

**Q: 能把规则导出 CSV/JSON 吗？**
可以，明确要求时在 Markdown 主稿之外附加导出。

---

## 路线图

- [x] 全项目业务规则 Skill（含证据分层）
- [x] 单模块深挖 Skill（含排序/限额/测试矩阵）
- [x] 每个 Skill 三类 eval 契约
- [x] 可执行的包校验器 + 凭据扫描
- [ ] CI 工作流：每次 push/PR 运行校验器
- [ ] 将两个 Skill 发布到 Skill 注册表
- [ ] `examples/` 下补充更多真实项目示例

---

## 贡献指南

- 为任何新建或实质修改的 Skill 维护三类 eval case。
- 提交前运行两个 `scripts/verify_skill_package.py` 校验器。
- 保持 `SKILL.md` 前置 `name` 与 `agents/openai.yaml` 的 `metadata.key` 与目录名一致。
- 绝不引入真实凭据或绝对本机路径。
- 区分静态校验与真实模型行为——只有包校验通过绝不宣称项目已被分析。

---

## 许可证

[MIT](./LICENSE)

## 维护者

[xulanzhong](https://github.com/xulanzhong) · <xulanzhong521@gmail.com>