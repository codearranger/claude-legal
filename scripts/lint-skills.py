#!/usr/bin/env python3
"""
Lint SKILL.md files across all plugins in the marketplace.

Checks each SKILL.md under `plugins/*/skills/*/SKILL.md`:

  - File begins with YAML frontmatter delimited by --- lines
  - Frontmatter declares required keys: name, description, version
  - Frontmatter `name` equals the containing directory name
    (the plugin runtime uses the directory as the skill ID; a mismatch
    means the skill won't load under its declared name)

Usage:
    python3 scripts/lint-skills.py [root]

`root` defaults to `plugins`. Exit code 0 if every skill passes,
1 if any skill fails, 2 on script error.

Pre-commit hook (optional):

    #!/usr/bin/env bash
    exec python3 scripts/lint-skills.py
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_KEYS = {"name", "description", "version"}

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
# Top-level keys sit at column 0 followed by a colon.
TOP_KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:", re.MULTILINE)
NAME_VALUE_RE = re.compile(r"^name\s*:\s*(.+?)\s*$", re.MULTILINE)


@dataclass
class Skill:
    path: Path
    dir_name: str
    frontmatter: str | None
    keys: set[str]
    name_value: str | None


def parse(path: Path) -> Skill:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return Skill(path, path.parent.name, None, set(), None)
    fm = m.group(1)
    keys = set(TOP_KEY_RE.findall(fm))
    name_match = NAME_VALUE_RE.search(fm)
    return Skill(
        path=path,
        dir_name=path.parent.name,
        frontmatter=fm,
        keys=keys,
        name_value=name_match.group(1).strip() if name_match else None,
    )


def check(skill: Skill) -> list[str]:
    errors: list[str] = []
    if skill.frontmatter is None:
        errors.append("missing YAML frontmatter (no --- delimiters at top)")
        return errors
    for key in sorted(REQUIRED_KEYS - skill.keys):
        errors.append(f"missing required key: {key}")
    if skill.name_value and skill.name_value != skill.dir_name:
        errors.append(
            f"name '{skill.name_value}' does not match directory '{skill.dir_name}'"
        )
    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path("plugins")
    if not root.exists():
        print(f"Root not found: {root}", file=sys.stderr)
        return 2

    skill_files = sorted(root.rglob("skills/*/SKILL.md"))
    if not skill_files:
        print(f"No SKILL.md files found under {root}", file=sys.stderr)
        return 2

    cwd = Path.cwd()
    failures = 0
    for path in skill_files:
        try:
            rel = path.resolve().relative_to(cwd.resolve())
        except ValueError:
            rel = path
        errors = check(parse(path))
        if errors:
            failures += 1
            print(f"[FAIL] {rel}")
            for err in errors:
                print(f"    - {err}")
        else:
            print(f"[PASS] {rel}")

    print("-" * 60)
    print(f"{len(skill_files)} skills checked; {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
