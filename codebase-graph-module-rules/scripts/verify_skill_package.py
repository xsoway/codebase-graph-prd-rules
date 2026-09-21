#!/usr/bin/env python3
"""Validate this standalone skill's required package contract."""
from __future__ import annotations
import re
import sys
from pathlib import Path

REQUIRED = ("SKILL.md", "prompts/codebase-graph-module-rules.md", "agents/openai.yaml", "evals/eval.yaml", "evals/cases/basic-success.yaml", "evals/cases/edge-incomplete-input.yaml", "evals/cases/edge-scope-boundary.yaml", "references/module-discovery.md", "references/module-document-contract.md")
NAME = "codebase-graph-module-rules"

def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) == 2 else ".").resolve()
    missing = [item for item in REQUIRED if not (root / item).is_file()]
    if missing:
        print("missing: " + ", ".join(missing), file=sys.stderr); return 1
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    meta = (root / "agents/openai.yaml").read_text(encoding="utf-8")
    if f"name: {NAME}" not in skill or f'key: "{NAME}"' not in meta:
        print("skill name and metadata key differ", file=sys.stderr); return 1
    corpus = "\n".join(p.read_text(encoding="utf-8") for p in root.rglob("*")
                       if p.is_file() and p.suffix in {".md", ".yaml"})
    if re.search(r"(?i)(sk-[a-z0-9_-]{12,}|authorization:|api[_ -]?key\s*[:=])", corpus):
        print("credential-like content found", file=sys.stderr); return 1
    print("skill package contract passed: 3 eval cases, prompt, metadata, references")
    return 0

if __name__ == "__main__": raise SystemExit(main())
