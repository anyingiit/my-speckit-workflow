<!-- Source: Keep a Changelog 1.1.0 (MIT) — https://keepachangelog.com/en/1.1.0/ -->
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-09-23

### Added

- The Spec Kit `/goal` workflow prompt, version 1.0.0, in the README's "Usage" section, with a
  four-step overview of the whole workflow, so readers can see the complete workflow and copy the
  prompt with one click.
- Prerequisites in the README's "Getting Started" section: Spec Kit 1.0.6, Claude Code as the
  verified agent, and an existing feature spec, so readers know what the prompt needs before they
  run it.
- `README.zh-CN.md`, a Simplified Chinese translation of the README with the same untranslated
  prompt, as required by the constitution's English-first documentation principle.
- Community files from Chef's Pick OSS Starter v1.2.1 (align mode, 2026-09-23): modules M01–M09,
  M11 and M12 accepted; optional modules M13–M16 declined by the author; M10 ships no files.
- The project constitution, which governs how this workflow is documented and versioned.
- `tools/check_readme.py` and CI checks that fail when the two READMEs' prompts differ, the
  Chinese translation is out of date, or the README version disagrees with this changelog.
- `.gitignore` rules for Python bytecode (`__pycache__/`, `*.pyc`), which the checker and its
  tests create when they run.

[Unreleased]: https://github.com/anyingiit/my-speckit-workflow/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/anyingiit/my-speckit-workflow/releases/tag/v1.0.0
