#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布红线检查：扫描仓库内 .md/.yaml/.yml/.py/.html/.toml 中的敏感信息与绝对本机路径。

由 `make check-secrets` / `make check` 调用。扫描模式自身含 "/Users/" / "sk-…" 等字样，
故跳过本脚本文件本身、verify_skill_package.py，以及发布记录 RELEASE_CHECKLIST.md
（后者本就逐条书写这些模式字样，属"文档"而非"泄露"），避免发布红线误伤发布记录。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# 敏感信息 / 绝对本机路径模式（发布红线）。枚举对齐 RELEASE_CHECKLIST D 节。
# 整体 IGNORECASE：对小写形式（如 /users/）同样命中，更保守、更安全。
PATTERN = re.compile(
    r"sk-proj-[a-zA-Z0-9_-]{12,}|sk-ant-[a-zA-Z0-9_-]{12,}|sk-[a-zA-Z0-9]{24,}|"
    r"ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{8,}|AKIA[0-9A-Z]{16}|"
    r"authorization:\s*bearer\s+[A-Za-z0-9._-]{8,}|bearer\s+[A-Za-z0-9._-]{16,}|"
    r"api[ _-]?key\s*[:=]\s*[A-Za-z0-9._-]{8,}|"
    r"secret\s*[:=]\s*[A-Za-z0-9._-]{8,}|"
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----|"
    r"/users/[a-zA-Z0-9_.-]+|/home/[a-zA-Z0-9_.-]+",
    re.IGNORECASE,
)
EXTS = {".md", ".yaml", ".yml", ".py", ".html", ".toml"}
# 跳过扫描正则定义文件本身 + 发布记录（后者本就书写这些模式字样）。
SKIP_NAMES = {"check_secrets.py", "verify_skill_package.py"}
SKIP_FILES = {"RELEASE_CHECKLIST.md"}


def main() -> int:
    """发布红线扫描：遍历仓库内代码/文档文件，命中敏感内容即返回 1。"""
    hits: list[str] = []

    root = Path(__file__).resolve().parent.parent
    for path in root.rglob("*"):
        if (
            ".git" in path.parts
            or path.suffix not in EXTS
            or path.name in SKIP_NAMES
            or path.name in SKIP_FILES
        ):
            continue
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
        ):
            if PATTERN.search(line):
                hits.append(f"{path.relative_to(root)}:{lineno}: {line.strip()[:120]}")

    if hits:
        print("found sensitive content:", file=sys.stderr)
        for hit in hits:
            print("  " + hit, file=sys.stderr)
        return 1
    print("OK: no secrets or absolute local paths detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())