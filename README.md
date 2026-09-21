<p align="center">
  <img src="https://img.shields.io/badge/codebase--graph--prd--rules-1.0.0-blue" alt="codebase-graph-prd-rules version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/status-beta-yellow" alt="status">
  <img src="https://img.shields.io/badge/python-3.9+-informational" alt="python version">
</p>

<h1 align="center">codebase-graph-prd-rules</h1>

<p align="center">
  <strong>Turn code into traceable business rules</strong>
</p>

<p align="center">
  <a href="./README.zh-CN.md">中文</a>
</p>

<p align="center">
  <b>Graphify first · Source-verified · Non-developer readable · Evaluable</b>
</p>

---

## Table of Contents

- [What is it](#what-is-it)
- [Why do we need it](#why-do-we-need-it)
- [Core concepts](#core-concepts)
- [Repository structure](#repository-structure)
- [The two skills](#the-two-skills)
- [Quick start](#quick-start)
- [Verification](#verification)
- [Safety boundary](#safety-boundary)
- [FAQ](#faq)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Maintainer](#maintainer)

---

## What is it

`codebase-graph-prd-rules` is a set of two complementary AI-agent **skills** that turn project source code into detailed, source-traceable **business-rule documents** for non-developers (product, operations, and QA teams).

Both skills share the same methodology and evidence boundary — build a **Graphify** code graph first, use it to locate entry points and call chains, then confirm every rule against the actual source, SQL/XML, and configuration. The graph navigates; the source confirms. Neither skill modifies the business system — analyze and document only.

The two skills cover different granularity:

- **`codebase-graph-business-rules`** — *whole-project* business rules. Scan an entire project, build the graph, and produce a full integration document: module map, entries, entities/state, data & config, end-to-end flows, per-module rule tables, test scope, and a traceability index.
- **`codebase-graph-module-rules`** — *single-module* deep dive. Given a feature description or module name, trace one module's rules, sorting/limits/status/flows, and produce a specialized test-focused document.

---

## Why do we need it

| Common approach (anti-pattern) | This project |
|---|---|
| Rules live only in developer heads or scattered comments | Codified, source-verified rule documents |
| Sorting described as vague "priority" | Sorting broken into filter vs sort key vs post-filter/termination |
| No evidence — claims can't be checked | Every rule carries `src/...:line` sources |
| Graph IR edges mistaken for facts | Graph is *navigation only*; source confirms facts |
| Static doc passes claimed as verified behavior | Static vs runtime clearly separated and reported |
| Mixed module flows appended at the end | Same module's branches merged into one section |

It solves **5 pain points**:

1. **Traceability** — every rule records a source file + line for auditing and changes.
2. **Non-developer readability** — tables and Mermaid diagrams explain business meaning, not class names.
3. **Honest evidence levels** — EXTRACTED vs INFERRED vs source-verified are reported separately.
4. **Test-ready** — each key rule maps to an executable P0/P1 test assertion matrix.
5. **Safety** — the skills refuse unauthorized production actions and never emit credentials.

---

## Core concepts

### 1. Graphify navigates, source confirms

The graph finds entry points and candidate call chains (`trigger → orchestration → decision → storage/log → external result`). Every rule is then confirmed against source, SQL/XML, and configuration — **an INFERRED graph edge is only a lead, never a fact**.

### 2. Three-layer rules

Business rules are separated into three layers, never conflated:

- **Qualification filter** — is a candidate even eligible?
- **Candidate sorting** — who is processed first (fields, direction, null rules, tie-breaks)?
- **Runtime control** — limits, de-duplication, concurrency, sending, failure rollback.

For sorting, the document must state the fields, direction, null/empty rules, tie behavior, post-filter, and final termination — per the actual comparator or SQL `ORDER BY`, not assumptions.

### 3. Evidence levels

| Level | What may be written | What may NOT |
|---|---|---|
| Source/SQL/config reviewed | Current conditions, order, fields, calls, side effects | External system final results |
| Graph EXTRACTED | Location and relationship leads | Unread business rules |
| Graph INFERRED | Candidate relationships awaiting source confirmation | Confirmed calls or business contracts |
| Comments/logs/field names | Supplemental intent or open items | Standalone facts |
| Runtime result | Observed behavior in that environment/input | Universal guarantees beyond the covered cases |

### 4. Analyze, never act

Both skills analyze and write documents only. They refuse to call real downstream services, send real leads, mutate data, or run production behavior without explicit authorization — and they report what was *not* executed.

---

## Repository structure

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

Each skill is a self-contained package: activation entry, full execution spec, discovery metadata, three eval cases, examples, and an executable package validator.

---

## The two skills

| | `codebase-graph-business-rules` | `codebase-graph-module-rules` |
|---|---|---|
| **Scope** | Whole project | One feature / module |
| **Input** | Project root + source scope | Feature description / module name |
| **Output** | Full integration doc: module map, entity/state, data & config, flows, per-module rules, test scope, traceability index | Specialized module doc: boundary, relationships, rules/sorting/limits, test matrix |
| **Merge rule** | Same module across entry/exception/timer flows merged into one section | All main/branch chains of a module merged into one section |
| **Use when** | "梳理全项目 / 全量功能 / PRD 基线" | "梳理某个模块 / 某条规则" |

The choice rule: use `codebase-graph-module-rules` for one clearly bounded module and `codebase-graph-business-rules` for a whole-project scan with no single-module boundary.

---

## Quick start

**Environment**: Python 3.9+ for the validator (stdlib only, no third-party dependency). You need a project whose source can be analyzed, and optionally a configured LLM credential for semantic graph extraction.

### 1. Place the skill where your agent can load it

Copy the desired skill directory (e.g. `codebase-graph-business-rules/`) into your agent's skill path, or reference it as a local-path skill.

### 2. Verify a skill package

Run the built-in package validator against a skill directory:

```bash
python3 codebase-graph-business-rules/scripts/verify_skill_package.py codebase-graph-business-rules
# → skill package contract passed: 3 eval cases, prompt, metadata, references

python3 codebase-graph-module-rules/scripts/verify_skill_package.py codebase-graph-module-rules
# → skill package contract passed: 3 eval cases, prompt, metadata, references
```

The validator checks: required artifacts exist, `SKILL.md` front-matter `name` matches the directory, `agents/openai.yaml` `metadata.key` matches, and no credential-like content appears in any `.md`/`.yaml`.

### 3. Use the skill

Give your agent a request. Examples:

```text
"请扫描项目代码，先建 Graphify 图谱，再按模块输出业务规则、来源、流程图和测试范围。"
"请针对线索包和排序规则，先建 Graphify 图谱，再输出详细业务规则、流程图、来源和测试点。"
```

Both skills output a Markdown document in the project's local `docs/` (default), with optional CSV/JSON rule ledgers on explicit request.

---

## Verification

Every skill carries a 3-case eval contract under `evals/`:

| Case | File | Verifies |
|---|---|---|
| Success path | `basic-success.yaml` | A complete request produces a graph + rules + sources + tests |
| Incomplete input | `edge-incomplete-input.yaml` | Missing input must surface gaps/"待确认", not guess |
| Scope/risk boundary | `edge-scope-boundary.yaml` | Out-of-scope requests (e.g. sending a real lead) are refused |

Static package validation (`verify_skill_package.py`) proves *structure and safety*; it is **not** a claim that any project has been analyzed.

---

## Safety boundary

- **No credentials**: no API keys, tokens, cookies, or private keys are emitted or persisted.
- **No personal data / absolute local paths** (`/Users/…`, `/home/…`) in any artifact.
- **No unauthorized external action**: skills never call real downstream services or mutate data without explicit authorization.
- **Credentials, when used for semantic extraction, exist only in the process environment** — never in source, docs, skill files, shell config, or output.
- **No fabricated runtime claims**: unrun integration/database/scheduling/production behavior is reported as not executed.

---

## FAQ

**Q: Which skill should I use?**
Use `codebase-graph-module-rules` for one bounded module/feature; use `codebase-graph-business-rules` for a whole-project scan with no single-module boundary.

**Q: Do I need an LLM credential?**
No. Semantic extraction only runs when you explicitly provide a credential. Without one, the skills fall back to structural graph + source review and report that limitation.

**Q: Do these skills modify my code?**
No. Both skills analyze and write documents only. Modifying business code, data, or external systems requires your explicit separate authorization.

**Q: What do the docs look like?**
Markdown with tables and Mermaid flow/state diagrams, business-meaning-first rather than class-name-heavy, with sourcable references like `src/main/.../Service.java:120`.

**Q: Can I get the rules in CSV/JSON?**
Yes, on explicit request, in addition to the Markdown primary deliverable.

---

## Roadmap

- [x] Whole-project business-rule skill with evidence levels
- [x] Single-module deep-dive skill with sorting/limits/test matrix
- [x] Three-case eval contract per skill
- [x] Executable package validator + credential scan
- [ ] CI workflow running validators on every push/PR
- [ ] Publish both skills to a skill registry
- [ ] More real-project examples under `examples/`

---

## Contributing

- Keep the three eval cases up to date for any new or substantially modified skill.
- Before committing, run both `scripts/verify_skill_package.py` validators.
- Keep `SKILL.md` front-matter `name` and `agents/openai.yaml` `metadata.key` matching the directory name.
- Never introduce real credentials or absolute local paths.
- Separate static validation from real model behavior — never claim a project was analyzed when only a package check passed.

---

## License

[MIT](./LICENSE)

## Maintainer

[xulanzhong](https://github.com/xulanzhong) · <xulanzhong521@gmail.com>