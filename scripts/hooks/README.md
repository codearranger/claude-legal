# Git hooks

Hook scripts that live in the repo (so they are version-controlled and
reviewable) and can be symlinked into `.git/hooks/` to take effect.

## Install

From the repo root:

```bash
ln -sf ../../scripts/hooks/pre-commit .git/hooks/pre-commit
```

A symlink (rather than a copy) means any updates to the hook here are
picked up automatically.

## Hooks

- **`pre-commit`** — runs `scripts/lint-skills.py` on every commit.
  Blocks the commit if any `SKILL.md` has invalid frontmatter
  (missing `name` / `description` / `version`, or `name` not matching
  the containing directory).
