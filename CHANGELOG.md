# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed
- Upgraded all agents to latest Gemini models:
  - Text generation: `gemini-3-pro-preview` (code_agent, design_agent, play_agent, sound_agent, image_agent)
  - Image generation: `imagen-4.0-generate-001` (image_agent REST & SDK generators)
  - Fallback text model: `gemini-3-pro-preview` (image_agent REST generator)
- Fixed typo in `games/feeding-caiso/docs/phase3/PHASE3_ANALYSIS_REPORT.md`.
