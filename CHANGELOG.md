# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed
- Upgraded agents to use Gemini 3 models (`gemini-3-pro-preview`):
  - `agents/code_agent/utils/llm.py`
  - `agents/design_agent/utils/llm.py`
  - `agents/image_agent/config.yaml`
  - `agents/image_agent/image_generator/generators/gemini_generator.py`
  - `agents/play_agent/utils/llm.py`
  - `agents/sound_agent/config.yaml`
- Fixed typo in `games/feeding-caiso/docs/phase3/PHASE3_ANALYSIS_REPORT.md`.
