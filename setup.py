#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2026/09/24 09:00
# @Filename : setup.py
# @Author   : Alan_Hsu
"""构建脚本：把仓库根部的两个 skill 目录作为包数据打进 sdist/wheel。

设计要点：
- 仓库根部 codebase-graph-business-rules/、codebase-graph-module-rules/ 是技能的**唯一事实来源**，
  不提交重复副本；本脚本在构建时把它们复制到构建目录的包内 skills/ 下。
- 这样 `uv build` 能产出真正的 sdist + wheel，用户可 pip/uv 安装后获得两份完整技能。
"""
from __future__ import annotations

import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py

ROOT = Path(__file__).parent.resolve()
SKILL_DIRS = ("codebase-graph-business-rules", "codebase-graph-module-rules")
SHARE_FILES = ("README.md", "README.zh-CN.md", "LICENSE")


class BuildSkills(build_py):
    """build_py 子类：构建时把根部 skill 目录与共享文档复制进包内。"""

    def run(self) -> None:
        super().run()
        pkg_dir = Path(self.build_lib) / "codebase_graph_prd_rules"
        skills_dest = pkg_dir / "skills"
        skills_dest.mkdir(parents=True, exist_ok=True)
        for skill in SKILL_DIRS:
            src = ROOT / skill
            dest = skills_dest / skill
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            # 复制前清理可能残留的字节码/缓存
            for cache in dest.rglob("__pycache__"):
                shutil.rmtree(cache, ignore_errors=True)
        for name in SHARE_FILES:
            shutil.copy2(ROOT / name, pkg_dir / name)
        # 供运行时定位技能目录。
        (pkg_dir / "_asset_manifest.txt").write_text(
            "\n".join(["skills/" + s for s in SKILL_DIRS] + list(SHARE_FILES)) + "\n",
            encoding="utf-8",
        )


setup(cmdclass={"build_py": BuildSkills})