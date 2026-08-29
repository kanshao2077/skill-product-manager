#!/usr/bin/env python3
"""Validate the portable, minimum structure of an Agent Skill package.

The validator deliberately uses only Python's standard library.  Run it with
the skill directory as the sole argument; when omitted, it validates the skill
that contains this script.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOP_LEVEL_KEY_PATTERN = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]*(.*))?$")
INLINE_LINK_PATTERN = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^)\n]+)\)")
REFERENCE_LINK_PATTERN = re.compile(
    r"(?m)^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*(<[^>\n]+>|\S+)"
)
SCANNED_TEXT_SUFFIXES = {
    ".md",
    ".markdown",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".py",
    ".sh",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".jsx",
}
UNFINISHED_PATTERNS = (
    re.compile(r"\[(?:TO" + r"DO|TBD|PLACEHOLDER)(?::[^\]]*)?\]", re.IGNORECASE),
    re.compile(r"(?:^|\s)(?:TO" + r"DO|TBD|FIXME)\s*:", re.IGNORECASE),
    re.compile(r"\{\{\s*(?:TO" + r"DO|TBD|PLACEHOLDER)[^}]*\}\}", re.IGNORECASE),
    re.compile(
        r"<\s*(?:TO" + r"DO|TBD|PLACEHOLDER|YOUR[-_ A-Z0-9]+)\s*>",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:your (?:skill )?(?:name|description|content) here|"
        r"replace (?:this|me)|fill (?:this )?in)\b",
        re.IGNORECASE,
    ),
    re.compile(r"(?:待填写|待补充|请在此(?:填写|补充)|占位内容)"),
)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def passed(self, message: str) -> None:
        print(f"[PASS] {message}")

    def warn(self, message: str) -> None:
        self.warnings.append(message)
        print(f"[WARN] {message}")

    def fail(self, message: str) -> None:
        self.errors.append(message)
        print(f"[FAIL] {message}")

    def finish(self) -> int:
        print()
        print(
            "Summary: "
            f"{len(self.errors)} error(s), {len(self.warnings)} warning(s)"
        )
        if self.errors:
            print("INVALID: fix the errors above and run validation again.")
            return 1
        print("VALID: no blocking problems found.")
        return 0


def _remove_yaml_comment(value: str) -> str:
    """Remove an unquoted YAML comment from a simple scalar."""
    quote: str | None = None
    escaped = False
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if character == "\\" and quote == '"':
            escaped = True
            continue
        if character in {"'", '"'}:
            if quote is None:
                quote = character
            elif quote == character:
                quote = None
            continue
        if character == "#" and quote is None and (
            index == 0 or value[index - 1].isspace()
        ):
            return value[:index].rstrip()
    return value.rstrip()


def _decode_scalar(raw_value: str, key: str, report: Report) -> str:
    value = _remove_yaml_comment(raw_value.strip())
    if not value:
        return ""
    if value[0] == "'":
        if len(value) < 2 or value[-1] != "'":
            report.fail(f"SKILL.md frontmatter has an unterminated quote for {key!r}")
            return ""
        return value[1:-1].replace("''", "'")
    if value[0] == '"':
        if len(value) < 2 or value[-1] != '"':
            report.fail(f"SKILL.md frontmatter has an unterminated quote for {key!r}")
            return ""
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError as exc:
            report.fail(f"SKILL.md frontmatter has an invalid quoted {key!r}: {exc.msg}")
            return ""
        return decoded if isinstance(decoded, str) else str(decoded)
    return value


def parse_frontmatter(skill_file: Path, report: Report) -> dict[str, str]:
    try:
        text = skill_file.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        report.fail(f"cannot read SKILL.md as UTF-8: {exc}")
        return {}

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        report.fail("SKILL.md must start with YAML frontmatter delimited by ---")
        return {}

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() in {"---", "..."}),
        None,
    )
    if closing_index is None:
        report.fail("SKILL.md frontmatter has no closing --- delimiter")
        return {}

    frontmatter_lines = lines[1:closing_index]
    values: dict[str, str] = {}
    seen_keys: set[str] = set()
    index = 0
    while index < len(frontmatter_lines):
        line = frontmatter_lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line[:1].isspace():
            index += 1
            continue
        match = TOP_LEVEL_KEY_PATTERN.match(line)
        if not match:
            report.fail(f"invalid top-level frontmatter line: {line!r}")
            index += 1
            continue

        key, raw_value = match.group(1), (match.group(2) or "")
        if key in seen_keys:
            report.fail(f"SKILL.md frontmatter repeats the key {key!r}")
        seen_keys.add(key)

        block_match = re.fullmatch(r"[>|][+-]?", raw_value.strip())
        if block_match:
            block_lines: list[str] = []
            index += 1
            while index < len(frontmatter_lines):
                continuation = frontmatter_lines[index]
                if continuation and not continuation[:1].isspace():
                    break
                block_lines.append(continuation.strip())
                index += 1
            separator = " " if raw_value.strip().startswith(">") else "\n"
            values[key] = separator.join(block_lines).strip()
            continue

        values[key] = _decode_scalar(raw_value, key, report)
        index += 1

    return values


def validate_frontmatter(skill_dir: Path, skill_file: Path, report: Report) -> None:
    values = parse_frontmatter(skill_file, report)
    name = values.get("name", "").strip()
    description = values.get("description", "").strip()

    if not name:
        report.fail("SKILL.md frontmatter must contain a non-empty name")
    elif len(name) > 64:
        report.fail("frontmatter name must be at most 64 characters")
    elif not NAME_PATTERN.fullmatch(name):
        report.fail(
            "frontmatter name must use lowercase letters, digits, and single hyphens only"
        )
    elif name != skill_dir.name:
        report.fail(
            f"directory name {skill_dir.name!r} must exactly match frontmatter name {name!r}"
        )
    else:
        report.passed(f"frontmatter name is valid and matches {skill_dir.name!r}")

    if not description:
        report.fail("SKILL.md frontmatter must contain a non-empty description")
    elif len(description) > 1024:
        report.fail("frontmatter description must be at most 1024 characters")
    elif any(ord(character) < 32 and character not in "\n\t" for character in description):
        report.fail("frontmatter description contains a control character")
    else:
        report.passed("frontmatter description is present and basically valid")


def _walk_files(skill_dir: Path):
    for path in skill_dir.rglob("*"):
        if any(part.startswith(".") for part in path.relative_to(skill_dir).parts):
            continue
        if path.is_file():
            yield path


def validate_unfinished_markers(skill_dir: Path, validator_path: Path, report: Report) -> None:
    findings: list[str] = []
    for path in _walk_files(skill_dir):
        if path.resolve() == validator_path.resolve() or path.suffix.lower() not in SCANNED_TEXT_SUFFIXES:
            continue
        try:
            if path.stat().st_size > 2_000_000:
                report.warn(f"skipped unfinished-marker scan for large file: {path.relative_to(skill_dir)}")
                continue
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            report.fail(f"cannot scan {path.relative_to(skill_dir)} for unfinished markers: {exc}")
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any(pattern.search(line) for pattern in UNFINISHED_PATTERNS):
                findings.append(f"{path.relative_to(skill_dir)}:{line_number}")

    if findings:
        for finding in findings:
            report.fail(f"unfinished marker found at {finding}")
    else:
        report.passed("no unfinished scaffold markers found in text files")


def _link_destination(raw_destination: str) -> str:
    destination = raw_destination.strip()
    if destination.startswith("<") and destination.endswith(">"):
        return destination[1:-1].strip()
    # Markdown paths containing spaces must use angle brackets.  Anything after
    # the first whitespace-delimited token is an optional link title.
    return destination.split(maxsplit=1)[0]


def _is_external_or_anchor(destination: str) -> bool:
    if not destination or destination.startswith("#") or destination.startswith("//"):
        return True
    split = urlsplit(destination)
    return bool(split.scheme)


def validate_markdown_links(skill_dir: Path, report: Report) -> None:
    missing: set[tuple[Path, str]] = set()
    outside: set[tuple[Path, str]] = set()
    absolute: set[tuple[Path, str]] = set()
    markdown_files = [path for path in _walk_files(skill_dir) if path.suffix.lower() in {".md", ".markdown"}]
    root = skill_dir.resolve()

    for markdown_file in markdown_files:
        try:
            text = markdown_file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            report.fail(f"cannot read Markdown file {markdown_file.relative_to(skill_dir)}: {exc}")
            continue
        raw_destinations = [match.group(1) for match in INLINE_LINK_PATTERN.finditer(text)]
        raw_destinations.extend(match.group(1) for match in REFERENCE_LINK_PATTERN.finditer(text))

        for raw_destination in raw_destinations:
            destination = _link_destination(raw_destination)
            if _is_external_or_anchor(destination):
                continue
            decoded_path = unquote(urlsplit(destination).path)
            if not decoded_path:
                continue
            source_label = markdown_file.relative_to(skill_dir)
            if Path(decoded_path).is_absolute():
                absolute.add((source_label, destination))
                continue
            target = (markdown_file.parent / decoded_path).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                outside.add((source_label, destination))
                continue
            if not target.exists():
                missing.add((source_label, destination))

    for source, destination in sorted(outside, key=lambda item: (str(item[0]), item[1])):
        report.fail(f"relative Markdown link escapes the skill directory: {source} -> {destination}")
    for source, destination in sorted(missing, key=lambda item: (str(item[0]), item[1])):
        report.fail(f"relative Markdown link target does not exist: {source} -> {destination}")
    for source, destination in sorted(absolute, key=lambda item: (str(item[0]), item[1])):
        report.warn(f"absolute Markdown link is not portable and was not checked: {source} -> {destination}")
    if not outside and not missing:
        report.passed("all in-package relative Markdown links resolve")


def validate_scripts(skill_dir: Path, report: Report) -> None:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        report.passed("scripts/ is absent (scripts are optional)")
        return
    if not scripts_dir.is_dir():
        report.fail("scripts exists but is not a directory")
        return

    script_files = [path for path in scripts_dir.rglob("*") if path.is_file()]
    unreadable: list[Path] = []
    for script_file in script_files:
        try:
            if not os.access(script_file, os.R_OK):
                raise PermissionError("read permission is not available")
            with script_file.open("rb") as handle:
                handle.read(1)
        except OSError:
            unreadable.append(script_file.relative_to(skill_dir))

    if unreadable:
        for script_file in unreadable:
            report.fail(f"script is not readable: {script_file}")
    else:
        report.passed(f"all {len(script_files)} file(s) under scripts/ are readable")


def validate_skill(skill_dir: Path) -> int:
    report = Report()
    skill_dir = skill_dir.expanduser().resolve()
    print(f"Validating skill: {skill_dir}")

    if not skill_dir.exists():
        report.fail("target skill directory does not exist")
        return report.finish()
    if not skill_dir.is_dir():
        report.fail("target exists but is not a directory")
        return report.finish()
    report.passed("target skill directory exists")

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        report.fail("root SKILL.md is missing")
        return report.finish()
    report.passed("root SKILL.md exists")

    discovered_skill_files = sorted(skill_dir.rglob("SKILL.md"))
    if len(discovered_skill_files) > 1:
        extras = ", ".join(str(path.relative_to(skill_dir)) for path in discovered_skill_files[1:])
        report.fail(f"multiple exact SKILL.md files found; nested candidates: {extras}")
    else:
        report.passed("exactly one SKILL.md was found recursively")

    validate_frontmatter(skill_dir, skill_file, report)
    validate_unfinished_markers(skill_dir, Path(__file__), report)
    validate_markdown_links(skill_dir, report)
    validate_scripts(skill_dir, report)

    readme = skill_dir / "README.md"
    if readme.is_file():
        report.passed("optional README.md exists")
    else:
        report.warn("README.md is absent (optional for validation)")
    return report.finish()


def main() -> int:
    default_skill_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Validate the basic structure and portability of an Agent Skill."
    )
    parser.add_argument(
        "skill_dir",
        nargs="?",
        type=Path,
        default=default_skill_dir,
        help="skill directory to validate (default: the skill containing this script)",
    )
    arguments = parser.parse_args()
    return validate_skill(arguments.skill_dir)


if __name__ == "__main__":
    sys.exit(main())
