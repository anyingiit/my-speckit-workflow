#!/usr/bin/env python3
"""Check that the README pair stays consistent (spec 001, FR-009).

Checks, as defined in specs/001-readme-workflow-prompt/contracts/readme-layout.md:

  layout               Each README has one prompt region with one version label and one
                       ```text block.
  prompt-identical     The prompt block in README.zh-CN.md is identical to the one in README.md.
  translation-current  The translation-of marker in README.zh-CN.md matches README.md's digest.
  version-matches      Both version labels equal the highest released version in CHANGELOG.md.

Usage:
  python3 tools/check_readme.py                       run all checks
  python3 tools/check_readme.py --update-digest       refresh the translation marker, then check
  python3 tools/check_readme.py --print-prompt FILE   print the prompt block of FILE

Standard library only. Run from the repository root, or pass --root.
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

EN = "README.md"
ZH = "README.zh-CN.md"
CHANGELOG = "CHANGELOG.md"

START = "<!-- workflow-prompt:start -->"
END = "<!-- workflow-prompt:end -->"
LABEL_PATTERNS = {
    EN: re.compile(r"^\*\*Workflow version\*\*: v(\d+\.\d+\.\d+)$"),
    ZH: re.compile(r"^\*\*工作流版本\*\*：v(\d+\.\d+\.\d+)$"),
}
MARKER = re.compile(r"^<!-- translation-of: README\.md sha256:([0-9a-f]{16}) -->$")
RELEASE_HEADING = re.compile(r"^## \[(\d+)\.(\d+)\.(\d+)\] - \d{4}-\d{2}-\d{2}\s*$")


class LayoutError(Exception):
    """The prompt region of a README does not follow the layout contract."""


class Region:
    """The parts of a README's prompt region that the checks compare."""

    def __init__(self, prompt, prompt_line, version):
        self.prompt = prompt
        self.prompt_line = prompt_line
        self.version = version


def read_text(path):
    """Read a file as UTF-8 with line endings normalised to \\n."""
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")


def extract_region(text, name):
    """Return the Region of a README, or raise LayoutError explaining what is wrong."""
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if line.strip() == START]
    ends = [i for i, line in enumerate(lines) if line.strip() == END]
    if len(starts) != 1 or len(ends) != 1:
        raise LayoutError(
            f"expected exactly one {START} and one {END}, "
            f"found {len(starts)} and {len(ends)}"
        )
    start, end = starts[0], ends[0]
    if end < start:
        raise LayoutError(f"{END} comes before {START}")
    body = lines[start + 1:end]

    pattern = LABEL_PATTERNS.get(name, LABEL_PATTERNS[EN])
    labels = [(i, pattern.match(line.strip())) for i, line in enumerate(body)]
    labels = [(i, m) for i, m in labels if m]
    if len(labels) != 1:
        raise LayoutError(
            f"expected exactly one version label matching {pattern.pattern!r} inside the "
            f"prompt region, found {len(labels)}"
        )
    version = labels[0][1].group(1)

    fences = [i for i, line in enumerate(body) if line.startswith("```")]
    if len(fences) != 2 or body[fences[0]] != "```text" or body[fences[1]] != "```":
        raise LayoutError(
            "expected exactly one ```text fenced block inside the prompt region"
        )
    first, last = fences
    prompt_lines = body[first + 1:last]
    prompt = "\n".join(prompt_lines) + "\n" if prompt_lines else ""
    return Region(prompt, start + 1 + first + 2, version)


class Report:
    """Collects failures as '<check>: <file>: <message>' lines."""

    def __init__(self):
        self.failures = []

    def fail(self, check, name, message):
        self.failures.append(f"{check}: {name}: {message}")


def load_regions(root, report):
    regions = {}
    for name in (EN, ZH):
        try:
            regions[name] = extract_region(read_text(root / name), name)
        except LayoutError as error:
            report.fail("layout", name, str(error))
    return regions


def readme_digest(root):
    """First 16 hex digits of SHA-256 over the raw bytes of README.md."""
    return hashlib.sha256((root / EN).read_bytes()).hexdigest()[:16]


def marker_line(digest):
    return f"<!-- translation-of: {EN} sha256:{digest} -->"


def check_prompt_identical(regions, report):
    """L2: the Chinese README's prompt block equals the English one."""
    if EN not in regions or ZH not in regions:
        return
    en_lines = regions[EN].prompt.split("\n")
    zh_lines = regions[ZH].prompt.split("\n")
    if en_lines == zh_lines:
        return
    for index in range(max(len(en_lines), len(zh_lines))):
        en_line = en_lines[index] if index < len(en_lines) else None
        zh_line = zh_lines[index] if index < len(zh_lines) else None
        if en_line != zh_line:
            report.fail(
                "prompt-identical",
                ZH,
                f"prompt block differs from {EN} at prompt line {index + 1} "
                f"(file line {regions[ZH].prompt_line + index}); copy the block from {EN}",
            )
            return


def check_translation_current(root, report):
    """L3: the translation-of marker matches the current README.md digest."""
    actual = readme_digest(root)
    markers = [
        MARKER.match(line.strip())
        for line in read_text(root / ZH).split("\n")
        if line.strip().startswith("<!-- translation-of:")
    ]
    if len(markers) != 1 or markers[0] is None:
        report.fail(
            "translation-current",
            ZH,
            f"expected one marker '{marker_line('<16 hex>')}', found {len(markers)} "
            "(or a malformed one); add it, then run --update-digest",
        )
        return
    recorded = markers[0].group(1)
    if recorded != actual:
        report.fail(
            "translation-current",
            ZH,
            f"marker sha256:{recorded} != {EN} sha256:{actual}; update the translation, "
            "then run --update-digest",
        )


def update_digest(root):
    """Rewrite the translation-of marker line in README.zh-CN.md; touch nothing else."""
    path = root / ZH
    raw = path.read_bytes().decode("utf-8")
    new_marker = marker_line(readme_digest(root))
    lines = raw.split("\n")
    for index, line in enumerate(lines):
        if line.strip().startswith("<!-- translation-of:"):
            ending = "\r" if line.endswith("\r") else ""
            lines[index] = new_marker + ending
            break
    else:
        print(f"translation-current: {ZH}: no translation-of marker to update", file=sys.stderr)
        return
    path.write_bytes("\n".join(lines).encode("utf-8"))


def latest_release(changelog_text):
    """Return the highest released X.Y.Z in a Keep a Changelog file, or None."""
    versions = [
        tuple(int(part) for part in match.groups())
        for match in map(RELEASE_HEADING.match, changelog_text.split("\n"))
        if match
    ]
    if not versions:
        return None
    return ".".join(str(part) for part in max(versions))


def check_version(root, regions, report):
    """L4: both labels equal the highest released version in CHANGELOG.md."""
    latest = latest_release(read_text(root / CHANGELOG))
    if latest is None:
        report.fail(
            "version-matches",
            CHANGELOG,
            "no released version found; add a '## [X.Y.Z] - YYYY-MM-DD' heading",
        )
        return
    for name, region in regions.items():
        if region.version != latest:
            report.fail(
                "version-matches",
                name,
                f"label v{region.version} != {CHANGELOG} latest release {latest}",
            )


def run_checks(root):
    """Run every check; return (report, workflow version or None)."""
    report = Report()
    regions = load_regions(root, report)
    check_prompt_identical(regions, report)
    check_translation_current(root, report)
    check_version(root, regions, report)
    version = regions[EN].version if EN in regions else None
    return report, version


def print_prompt(root, name):
    path = root / name
    if not path.is_file():
        print(f"missing file: {path}", file=sys.stderr)
        return 2
    try:
        region = extract_region(read_text(path), name)
    except LayoutError as error:
        print(f"layout: {name}: {error}", file=sys.stderr)
        return 1
    sys.stdout.write(region.prompt)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check README consistency (FR-009).")
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument(
        "--update-digest",
        action="store_true",
        help=f"rewrite the translation-of marker in {ZH} from the current {EN}, then check",
    )
    parser.add_argument(
        "--print-prompt", metavar="FILE", help="print the prompt block of FILE and exit"
    )
    args = parser.parse_args(argv)
    root = Path(args.root)

    if args.print_prompt:
        return print_prompt(root, args.print_prompt)

    missing = [name for name in (EN, ZH, CHANGELOG) if not (root / name).is_file()]
    if missing:
        for name in missing:
            print(f"missing file: {root / name}", file=sys.stderr)
        return 2

    if args.update_digest:
        update_digest(root)

    report, version = run_checks(root)
    if report.failures:
        for line in report.failures:
            print(line, file=sys.stderr)
        return 1
    print(f"README checks passed (workflow version {version}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
