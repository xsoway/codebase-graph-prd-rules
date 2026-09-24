#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2026/09/24 09:05
# @Filename : __init__.py
# @Author   : Alan_Hsu
"""codebase-graph-prd-rules —— 两个 source-verified 图化业务规则 Skill 的资产包。

本包不包含可导入的业务代码，而是把两个独立 Skill（全项目 / 单模块）以包数据的形式
随 sdist/wheel 一同分发，便于 agent 或用户通过 pip/uv 安装后拿到完整技能目录。
"""
from __future__ import annotations

from pathlib import Path

__version__ = "1.0.0"

# 包内技能目录（构建时由 setup.py 从仓库根复制而来）。
_SKILLS_SUBDIR = "skills"


def skills_dir() -> Path:
    """返回包含两个技能目录的路径（`<pkg>/skills`）。"""
    return Path(__file__).resolve().parent / _SKILLS_SUBDIR


def available_skills() -> list[str]:
    """列出随包分发的技能目录名。"""
    base = skills_dir()
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir())


__all__ = ["skills_dir", "available_skills", "__version__"]