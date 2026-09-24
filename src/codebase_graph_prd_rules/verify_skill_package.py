#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2026/09/24 09:10
# @Filename : verify_skill_package.py
# @Author   : Alan_Hsu
"""控制台入口：校验随包分发的两个 skill 包结构契约。

复用仓库根部两个技能自带的 verify_skill_package.py 逻辑，这里做轻量聚合：
对包内 skills/ 下的每个技能目录运行同名校验脚本，任一失败即返回非零。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from codebase_graph_prd_rules import available_skills, skills_dir


def main() -> int:
    base = skills_dir()
    names = available_skills()
    if not names:
        print("no skills bundled in package", file=sys.stderr)
        return 1

    fail = 0
    for name in names:
        script = base / name / "scripts" / "verify_skill_package.py"
        if not script.is_file():
            print(f"missing validator: {script}", file=sys.stderr)
            fail += 1
            continue
        proc = subprocess.run(
            [sys.executable, str(script), str(base / name)],
            capture_output=True,
            text=True,
        )
        print(proc.stdout.strip())
        if proc.returncode != 0:
            print(proc.stderr.strip(), file=sys.stderr)
            fail += 1

    if fail:
        print(f"{fail} skill package(s) failed contract check", file=sys.stderr)
        return 1
    print("all bundled skill packages passed contract check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())