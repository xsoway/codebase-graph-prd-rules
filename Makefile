# 项目监管入口：`make code-clean` 一键清理 / 校验，`make check` 只读检查。
# 目标：代码清洁（make-code-clean）与知识图谱（code-review-graph 见 scripts/ 与 .codex 配置）。

PY ?= python3
UV ?= uv

.PHONY: help validate build-dist check format check-secrets code-clean clean

help:
	@echo "usage:"
	@echo "  make validate       运行两个 skill 包结构校验"
	@echo "  make build-dist     用 uv build 产出 sdist + wheel 到 dist/"
	@echo "  make check          只读检查：校验 + 敏感信息/绝对路径扫描"
	@echo "  make format         （无格式化工具时提示并跳过）"
	@echo "  make code-clean     check + build-dist + 清理缓存"
	@echo "  make clean          移除 dist/ build/ 与 __pycache__"

# 运行两个 skill 自带的包结构校验脚本（exit 0 = 通过）。
validate:
	"$(PY)" codebase-graph-business-rules/scripts/verify_skill_package.py codebase-graph-business-rules
	"$(PY)" codebase-graph-module-rules/scripts/verify_skill_package.py codebase-graph-module-rules
	@echo "OK: all skill packages passed contract check"

# uv build 产出可分发的 sdist + wheel 到 dist/。
build-dist:
	$(UV) build
# 敏感信息 / 绝对本机路径扫描（发布红线）。命中即失败；见 scripts/check_secrets.py。
check-secrets:
	"$(PY)" scripts/check_secrets.py
check: validate check-secrets
	@echo "OK: check passed"

# 占位：本项目为纯 skill/Markdown 资产，暂无格式化工具；有则在此接入。
format:
	@echo "info: no formatter configured for this Markdown/YAML skill repo; skipping"
	@echo "  (consider prettier for .md/.yaml if desired)"

# 发布前一键清理 + 校验 + 构建产物。
code-clean: clean check build-dist
	@echo "OK: repository clean and release artifacts built"

clean:
	rm -rf dist build src/*.egg-info
	find . -type d -name __pycache__ -not -path "./.git/*" -prune -exec rm -rf {} + 2>/dev/null || true
	@echo "OK: cleaned build artifacts and caches"