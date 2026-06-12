#!/usr/bin/env python3
"""
Lint SKILL.md files across all plugins in the marketplace.

Checks each SKILL.md under `plugins/*/skills/*/SKILL.md`:

  1. File begins with YAML frontmatter delimited by --- lines
  2. Frontmatter declares required keys: name, description, version
  3. Frontmatter `name` equals the containing directory name
     (the plugin runtime uses the directory as the skill ID; a mismatch
     means the skill won't load under its declared name)
  4. Description length: decoded description scalar must not exceed 1024
     characters (the runtime truncates longer values, silently breaking
     trigger matching)
  5. Semver format: `version:` must match ^\\d+\\.\\d+\\.\\d+$
  6. Cross-plugin skill-name uniqueness: no two skills across all plugins
     may share a name (a federal plugin and a state plugin can be
     co-installed; duplicate names cause the second to shadow the first)
  7. Symlink integrity: every symlink anywhere under plugins/ must resolve
     to an existing path inside the repo
  8. Marketplace agreement: every plugin listed in
     .claude-plugin/marketplace.json must have a source directory under
     plugins/, every directory under plugins/ must appear in the manifest,
     every plugins/<p>/.claude-plugin/plugin.json must exist, be valid
     JSON, declare name and version, and have name == directory name
  9. Broken reference paths (WARN, not FAIL): explicit relative paths of
     the form (../../references/foo.md) or `../../references/foo.md`
     found in SKILL.md bodies are resolved against the skill directory;
     missing targets produce a WARNING line (does not affect exit code)

Usage:
    python3 scripts/lint-skills.py [root]

`root` defaults to `plugins/` inside the repo that contains this script.
Exit code 0 if every skill passes, 1 if any skill fails, 2 on script error.

Pre-commit hook (optional):

    #!/usr/bin/env bash
    exec python3 scripts/lint-skills.py
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo / path helpers
# ---------------------------------------------------------------------------

# Resolve repo root from the script's own location so the pre-commit hook
# works regardless of the working directory it is invoked from.
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent


def _plugins_root(argv: list[str]) -> Path:
    """Return the plugins root: argv[1] if given, else <repo_root>/plugins."""
    if len(argv) > 1:
        return Path(argv[1])
    return _REPO_ROOT / "plugins"


def _marketplace_path() -> Path:
    return _REPO_ROOT / ".claude-plugin" / "marketplace.json"


# ---------------------------------------------------------------------------
# Regex constants
# ---------------------------------------------------------------------------

REQUIRED_KEYS = {"name", "description", "version"}

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
# Top-level YAML keys sit at column 0 followed by a colon.
TOP_KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:", re.MULTILINE)
NAME_VALUE_RE = re.compile(r"^name\s*:\s*(.+?)\s*$", re.MULTILINE)
VERSION_VALUE_RE = re.compile(r"^version\s*:\s*(.+?)\s*$", re.MULTILINE)
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

# Description block: everything from `description:` to the next top-level key or end.
DESC_BLOCK_RE = re.compile(
    r"^description\s*:\s*(.*?)(?=^[A-Za-z][A-Za-z0-9_-]*\s*:|\Z)",
    re.MULTILINE | re.DOTALL,
)

# Reference-path patterns in SKILL.md bodies (check 9).
# Parenthetical Markdown link target: (../../references/foo.md)
REF_PAREN_RE = re.compile(
    r"\(((?:\.\./)+references/[A-Za-z0-9._/-]+\.(?:md|py|json))\)"
)
# Bare backtick: `../../references/foo.md`
REF_BACK_RE = re.compile(
    r"`((?:\.\./)+references/[A-Za-z0-9._/-]+\.(?:md|py|json))`"
)


# ---------------------------------------------------------------------------
# Description decoding
# ---------------------------------------------------------------------------

def _decode_description(raw: str) -> str:
    """Return the human-readable scalar from a raw YAML description block.

    Handles:
    - Folded block scalar (>): strip indicator, join non-blank lines with spaces.
    - Literal block scalar (|): strip indicator, join lines with spaces.
    - Inline scalar: return as-is after stripping.
    """
    raw = raw.strip()
    if not raw:
        return ""
    if raw[0] in (">", "|"):
        lines = raw.split("\n")[1:]  # drop the block-scalar indicator line
        decoded = " ".join(line.strip() for line in lines if line.strip())
        return decoded.strip()
    return raw


# ---------------------------------------------------------------------------
# Per-skill dataclass and parser
# ---------------------------------------------------------------------------

@dataclass
class Skill:
    path: Path
    dir_name: str
    frontmatter: str | None
    keys: set[str]
    name_value: str | None
    version_value: str | None
    description_decoded: str | None  # None if frontmatter missing


def parse(path: Path) -> Skill:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return Skill(path, path.parent.name, None, set(), None, None, None)
    fm = m.group(1)
    keys = set(TOP_KEY_RE.findall(fm))

    name_match = NAME_VALUE_RE.search(fm)
    version_match = VERSION_VALUE_RE.search(fm)
    desc_match = DESC_BLOCK_RE.search(fm)

    description_decoded = (
        _decode_description(desc_match.group(1)) if desc_match else None
    )

    return Skill(
        path=path,
        dir_name=path.parent.name,
        frontmatter=fm,
        keys=keys,
        name_value=name_match.group(1).strip() if name_match else None,
        version_value=version_match.group(1).strip() if version_match else None,
        description_decoded=description_decoded,
    )


# ---------------------------------------------------------------------------
# Per-skill checks (returns list of error strings)
# ---------------------------------------------------------------------------

DESC_MAX_CHARS = 1024


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

    # Check 4: description length
    if skill.description_decoded is not None:
        dlen = len(skill.description_decoded)
        if dlen > DESC_MAX_CHARS:
            errors.append(
                f"description too long: {dlen} chars (max {DESC_MAX_CHARS})"
            )

    # Check 5: semver version
    if skill.version_value is not None:
        if not SEMVER_RE.match(skill.version_value):
            errors.append(
                f"version '{skill.version_value}' is not semver (expected N.N.N)"
            )

    return errors


# ---------------------------------------------------------------------------
# Check 9: broken reference paths (warnings, collected per skill)
# ---------------------------------------------------------------------------

def check_reference_paths(skill: Skill) -> list[str]:
    """Return WARNING strings for broken relative reference paths in the body."""
    warnings: list[str] = []
    try:
        body = skill.path.read_text(encoding="utf-8")
    except OSError:
        return warnings

    skill_dir = skill.path.parent
    seen: set[str] = set()

    for pat in (REF_PAREN_RE, REF_BACK_RE):
        for m in pat.finditer(body):
            rel_path = m.group(1)
            if rel_path in seen:
                continue
            seen.add(rel_path)
            target = (skill_dir / rel_path).resolve()
            if not target.exists():
                warnings.append(
                    f"WARNING: broken reference path '{rel_path}' in {skill.path}"
                )

    return warnings


# ---------------------------------------------------------------------------
# Check 6: cross-plugin skill-name uniqueness
# ---------------------------------------------------------------------------

def check_name_uniqueness(skills: list[Skill]) -> list[str]:
    """Return error strings for any skill names that appear in more than one plugin."""
    from collections import defaultdict

    name_to_paths: dict[str, list[Path]] = defaultdict(list)
    for skill in skills:
        if skill.name_value:
            name_to_paths[skill.name_value].append(skill.path)

    errors: list[str] = []
    for name, paths in sorted(name_to_paths.items()):
        if len(paths) > 1:
            locs = ", ".join(str(p) for p in sorted(paths))
            errors.append(f"duplicate skill name '{name}' in: {locs}")
    return errors


# ---------------------------------------------------------------------------
# Check 7: symlink integrity
# ---------------------------------------------------------------------------

def check_symlinks(plugins_root: Path) -> list[str]:
    """Return error strings for any broken symlinks under plugins_root."""
    errors: list[str] = []
    repo_root = _REPO_ROOT.resolve()

    for path in plugins_root.rglob("*"):
        if not path.is_symlink():
            continue
        resolved = path.resolve()
        if not resolved.exists():
            errors.append(
                f"broken symlink: {path} -> {path.readlink()} (target does not exist)"
            )
        else:
            # Verify the target lives inside the repo
            try:
                resolved.relative_to(repo_root)
            except ValueError:
                errors.append(
                    f"symlink escapes repo: {path} -> {resolved}"
                )
    return errors


# ---------------------------------------------------------------------------
# Check 8: marketplace agreement
# ---------------------------------------------------------------------------

def check_marketplace(plugins_root: Path) -> list[str]:
    """Return error strings for marketplace.json / plugin.json inconsistencies."""
    errors: list[str] = []
    mfest_path = _marketplace_path()

    # Parse marketplace.json
    try:
        mfest_text = mfest_path.read_text(encoding="utf-8")
    except OSError:
        errors.append(f"cannot read marketplace manifest: {mfest_path}")
        return errors

    try:
        mfest = json.loads(mfest_text)
    except json.JSONDecodeError as exc:
        errors.append(f"marketplace.json is invalid JSON: {exc}")
        return errors

    listed_plugins: list[dict] = mfest.get("plugins", [])
    if not isinstance(listed_plugins, list):
        errors.append("marketplace.json: 'plugins' is not an array")
        return errors

    # Build set of plugin names declared in the manifest, and verify source dirs
    manifest_names: set[str] = set()
    for entry in listed_plugins:
        pname = entry.get("name", "")
        source = entry.get("source", "")
        manifest_names.add(pname)

        # Resolve source relative to repo root
        if source.startswith("./"):
            source_path = _REPO_ROOT / source[2:]
        else:
            source_path = _REPO_ROOT / source

        if not source_path.exists():
            errors.append(
                f"marketplace.json: plugin '{pname}' source '{source}' does not exist"
            )

    # Every directory under plugins_root must be listed
    if plugins_root.exists():
        for entry in sorted(plugins_root.iterdir()):
            if not entry.is_dir():
                continue
            if entry.is_symlink():
                continue
            dname = entry.name
            if dname not in manifest_names:
                errors.append(
                    f"plugin directory '{dname}' is not listed in marketplace.json"
                )

    # Check each plugin's plugin.json
    for entry in sorted(plugins_root.iterdir()):
        if not entry.is_dir() or entry.is_symlink():
            continue
        pj_path = entry / ".claude-plugin" / "plugin.json"
        if not pj_path.exists():
            errors.append(f"plugin '{entry.name}': missing .claude-plugin/plugin.json")
            continue

        try:
            pj_text = pj_path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"plugin '{entry.name}': cannot read plugin.json: {exc}")
            continue

        try:
            pj = json.loads(pj_text)
        except json.JSONDecodeError as exc:
            errors.append(f"plugin '{entry.name}': plugin.json is invalid JSON: {exc}")
            continue

        if "name" not in pj:
            errors.append(f"plugin '{entry.name}': plugin.json missing 'name' field")
        elif pj["name"] != entry.name:
            errors.append(
                f"plugin '{entry.name}': plugin.json name '{pj['name']}'"
                f" does not match directory name"
            )

        if "version" not in pj:
            errors.append(f"plugin '{entry.name}': plugin.json missing 'version' field")

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    plugins_root = _plugins_root(argv)
    if not plugins_root.exists():
        print(f"Root not found: {plugins_root}", file=sys.stderr)
        return 2

    skill_files = sorted(plugins_root.rglob("skills/*/SKILL.md"))
    if not skill_files:
        print(f"No SKILL.md files found under {plugins_root}", file=sys.stderr)
        return 2

    cwd = Path.cwd()
    all_skills: list[Skill] = []
    per_skill_errors: dict[Path, list[str]] = {}
    all_warnings: list[str] = []

    # --- Per-skill checks (1-5) ---
    for path in skill_files:
        skill = parse(path)
        all_skills.append(skill)
        per_skill_errors[path] = check(skill)

    # --- Check 6: cross-plugin uniqueness (runs after collecting all skills) ---
    uniqueness_errors = check_name_uniqueness(all_skills)

    # --- Check 7: symlink integrity ---
    symlink_errors = check_symlinks(plugins_root)

    # --- Check 8: marketplace agreement ---
    marketplace_errors = check_marketplace(plugins_root)

    # --- Check 9: broken reference paths (warnings per skill) ---
    for skill in all_skills:
        all_warnings.extend(check_reference_paths(skill))

    # --- Emit per-skill results ---
    failures = 0
    for path in skill_files:
        try:
            rel = path.resolve().relative_to(cwd.resolve())
        except ValueError:
            rel = path
        errors = per_skill_errors[path]
        if errors:
            failures += 1
            print(f"[FAIL] {rel}")
            for err in errors:
                print(f"    - {err}")
        else:
            print(f"[PASS] {rel}")

    # --- Emit global check results ---
    if uniqueness_errors:
        failures += 1
        print("[FAIL] cross-plugin skill-name uniqueness")
        for err in uniqueness_errors:
            print(f"    - {err}")

    if symlink_errors:
        failures += 1
        print("[FAIL] symlink integrity")
        for err in symlink_errors:
            print(f"    - {err}")

    if marketplace_errors:
        failures += 1
        print("[FAIL] marketplace agreement")
        for err in marketplace_errors:
            print(f"    - {err}")

    # --- Emit warnings ---
    for w in all_warnings:
        print(w)

    # --- Summary ---
    print("-" * 60)
    warn_note = f"; {len(all_warnings)} reference-path warning(s)" if all_warnings else ""
    print(
        f"{len(skill_files)} skills checked; {failures} failure group(s){warn_note}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
