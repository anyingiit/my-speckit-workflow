"""Unit tests for tools/check_readme.py.

Every test writes its own README.md, README.zh-CN.md and CHANGELOG.md into a temporary
directory and runs the checker against it with --root, so nothing depends on the real files.
"""

import contextlib
import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_readme  # noqa: E402

PROMPT = "/goal 测试。\n\n0. 第一步“引号”（括号），完成\n1. /speckit-plan\n"

EN_README = f"""# My Spec-Kit Workflow

**English** · [简体中文](README.zh-CN.md)

## Usage

<!-- workflow-prompt:start -->
**Workflow version**: v1.0.0

```text
{PROMPT}```
<!-- workflow-prompt:end -->
"""

ZH_README_TEMPLATE = f"""# My Spec-Kit Workflow

[English](README.md) · **简体中文**

> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。

{{marker}}

## 使用

<!-- workflow-prompt:start -->
**工作流版本**：v1.0.0

```text
{PROMPT}```
<!-- workflow-prompt:end -->
"""

CHANGELOG = """# Changelog

## [Unreleased]

## [1.0.0] - 2026-09-23

### Added

- First release.
"""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def marker_for(en_text: str) -> str:
    return f"<!-- translation-of: README.md sha256:{digest(en_text.encode('utf-8'))} -->"


class CheckerTestCase(unittest.TestCase):
    """Builds a fixture that satisfies invariants L1-L4; tests change only what they exercise."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.write_fixture()

    def tearDown(self):
        self._tmp.cleanup()

    def write_fixture(self, en=EN_README, zh=None, changelog=CHANGELOG):
        if zh is None:
            zh = ZH_README_TEMPLATE.format(marker=marker_for(en))
        self.write("README.md", en)
        self.write("README.zh-CN.md", zh)
        self.write("CHANGELOG.md", changelog)

    def write(self, name, text, newline="\n"):
        (self.root / name).write_bytes(text.replace("\n", newline).encode("utf-8"))

    def read(self, name):
        return (self.root / name).read_text(encoding="utf-8")

    def replace_in(self, name, old, new):
        text = self.read(name)
        self.assertIn(old, text)
        self.write(name, text.replace(old, new, 1))

    def run_checker(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = check_readme.main(["--root", str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def failures(self, err, check):
        return [line for line in err.splitlines() if line.startswith(f"{check}: ")]


class LayoutTests(CheckerTestCase):
    def test_valid_fixture_passes(self):
        code, out, err = self.run_checker()
        self.assertEqual(self.failures(err, "layout"), [])
        self.assertEqual(code, 0, err)
        self.assertIn("README checks passed (workflow version 1.0.0).", out)

    def test_missing_end_marker_fails_layout(self):
        self.replace_in("README.md", "<!-- workflow-prompt:end -->", "")
        code, _, err = self.run_checker()
        self.assertEqual(code, 1)
        self.assertTrue(
            any(line.startswith("layout: README.md:") for line in err.splitlines()), err
        )

    def test_two_start_markers_fail_layout(self):
        self.replace_in(
            "README.md",
            "<!-- workflow-prompt:start -->",
            "<!-- workflow-prompt:start -->\n<!-- workflow-prompt:start -->",
        )
        code, _, err = self.run_checker()
        self.assertEqual(code, 1)
        self.assertTrue(self.failures(err, "layout"), err)

    def test_region_without_text_fence_fails_layout(self):
        self.replace_in("README.md", "```text\n", "```sh\n")
        code, _, err = self.run_checker()
        self.assertEqual(code, 1)
        self.assertTrue(self.failures(err, "layout"), err)

    def test_region_without_version_label_fails_layout(self):
        self.replace_in("README.md", "**Workflow version**: v1.0.0\n", "")
        code, _, err = self.run_checker()
        self.assertEqual(code, 1)
        self.assertTrue(
            any(line.startswith("layout: README.md:") for line in err.splitlines()), err
        )

    def test_missing_readme_exits_2(self):
        (self.root / "README.md").unlink()
        code, _, err = self.run_checker()
        self.assertEqual(code, 2)
        self.assertIn("README.md", err)

    def test_print_prompt_outputs_block_exactly(self):
        self.write("README.md", EN_README, newline="\r\n")
        code, out, _ = self.run_checker("--print-prompt", "README.md")
        self.assertEqual(code, 0)
        self.assertEqual(out, PROMPT)


class VersionMatchesTests(CheckerTestCase):
    def test_matching_labels_and_changelog_pass(self):
        code, _, err = self.run_checker()
        self.assertEqual(self.failures(err, "version-matches"), [])
        self.assertEqual(code, 0, err)

    def test_unreleased_heading_is_ignored(self):
        self.write_fixture(
            changelog=CHANGELOG.replace("## [Unreleased]\n", "## [Unreleased]\n\n- Pending.\n")
        )
        code, _, err = self.run_checker()
        self.assertEqual(code, 0, err)

    def test_versions_compare_numerically(self):
        en = EN_README.replace("v1.0.0", "v1.10.0")
        zh = ZH_README_TEMPLATE.format(marker=marker_for(en)).replace("v1.0.0", "v1.10.0")
        changelog = CHANGELOG.replace(
            "## [1.0.0] - 2026-09-23",
            "## [1.9.0] - 2026-09-24\n\n## [1.10.0] - 2026-09-25\n\n## [1.0.0] - 2026-09-23",
        )
        self.write_fixture(en=en, zh=zh, changelog=changelog)
        code, _, err = self.run_checker()
        self.assertEqual(self.failures(err, "version-matches"), [])
        self.assertEqual(code, 0, err)

    def test_label_newer_than_changelog_fails(self):
        en = EN_README.replace("v1.0.0", "v1.0.1")
        self.write_fixture(en=en)
        code, _, err = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn(
            "version-matches: README.md: label v1.0.1 != CHANGELOG.md latest release 1.0.0",
            err.splitlines(),
        )

    def test_chinese_label_mismatch_names_chinese_file(self):
        self.replace_in("README.zh-CN.md", "**工作流版本**：v1.0.0", "**工作流版本**：v0.9.0")
        code, _, err = self.run_checker()
        self.assertEqual(code, 1)
        self.assertTrue(
            any(
                line.startswith("version-matches: README.zh-CN.md:")
                for line in err.splitlines()
            ),
            err,
        )

    def test_changelog_without_release_fails(self):
        self.write_fixture(changelog="# Changelog\n\n## [Unreleased]\n")
        code, _, err = self.run_checker()
        self.assertEqual(code, 1)
        self.assertTrue(self.failures(err, "version-matches"), err)


class PromptIdenticalTests(CheckerTestCase):
    def test_identical_blocks_pass(self):
        code, _, err = self.run_checker()
        self.assertEqual(self.failures(err, "prompt-identical"), [])
        self.assertEqual(code, 0, err)

    def test_changed_character_in_chinese_block_fails(self):
        self.replace_in("README.zh-CN.md", "第一步“引号”", "第一步\"引号\"")
        code, _, err = self.run_checker()
        self.assertEqual(code, 1)
        lines = [
            line
            for line in err.splitlines()
            if line.startswith("prompt-identical: README.zh-CN.md:")
        ]
        self.assertEqual(len(lines), 1, err)
        self.assertIn("line 3", lines[0])

    def test_crlf_line_endings_still_match(self):
        zh = ZH_README_TEMPLATE.format(marker=marker_for(EN_README))
        self.write("README.zh-CN.md", zh, newline="\r\n")
        code, _, err = self.run_checker()
        self.assertEqual(self.failures(err, "prompt-identical"), [])
        self.assertEqual(code, 0, err)


class TranslationCurrentTests(CheckerTestCase):
    def test_current_marker_passes(self):
        code, _, err = self.run_checker()
        self.assertEqual(self.failures(err, "translation-current"), [])
        self.assertEqual(code, 0, err)

    def test_stale_marker_fails(self):
        self.replace_in("README.md", "## Usage", "## Usage\n\nOne more sentence.")
        code, _, err = self.run_checker()
        self.assertEqual(code, 1)
        lines = self.failures(err, "translation-current")
        self.assertEqual(len(lines), 1, err)
        self.assertTrue(lines[0].startswith("translation-current: README.zh-CN.md:"), err)

    def test_missing_marker_fails(self):
        self.write_fixture(zh=ZH_README_TEMPLATE.format(marker=""))
        code, _, err = self.run_checker()
        self.assertEqual(code, 1)
        self.assertTrue(
            any(
                line.startswith("translation-current: README.zh-CN.md:")
                for line in err.splitlines()
            ),
            err,
        )

    def test_update_digest_rewrites_only_the_marker(self):
        self.replace_in("README.md", "## Usage", "## Usage\n\nOne more sentence.")
        en_before = (self.root / "README.md").read_bytes()
        zh_before = self.read("README.zh-CN.md")

        code, _, err = self.run_checker("--update-digest")

        self.assertEqual(code, 0, err)
        self.assertEqual((self.root / "README.md").read_bytes(), en_before)
        zh_after = self.read("README.zh-CN.md")
        changed = [
            (old, new)
            for old, new in zip(zh_before.splitlines(), zh_after.splitlines())
            if old != new
        ]
        self.assertEqual(len(changed), 1)
        self.assertEqual(changed[0][1], marker_for(en_before.decode("utf-8")))
        self.assertEqual(self.run_checker()[0], 0)


if __name__ == "__main__":
    unittest.main()
