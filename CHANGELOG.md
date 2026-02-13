# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- `agents/shared/` module: centralized constants, base LLM service, and pipeline runner
  - `constants.py`: Single source of truth for model versions (`GEMINI_TEXT_MODEL`, `IMAGEN_MODEL`)
  - `llm.py`: Shared `LLMService` base class (zero-dependency, urllib-based)
  - `pipeline.py`: `AgentPipeline` for composing agent analyses sequentially
- `agents/__main__.py`: Top-level CLI to run agent pipelines (`python -m agents <game> [--agents ...]`)
- `agents/code_agent/__main__.py`: CLI entry point (`python -m agents.code_agent`)
- `agents/play_agent/__main__.py`: CLI entry point (`python -m agents.play_agent`)
- `agents/sound_agent/utils/llm.py`: Own LLM service (removes cross-dependency on design_agent)
- `games/feeding-caiso`: Procedural Sound Library (Web Audio API) with Zen/Ethereal theme
- `games/feeding-caiso`: Stage transition system with fade effects and hazard spawning
- Health check (`do_GET`) for `/api/analyze-code` endpoint
- Vercel routes for `/api/analyze-code` and `/api/generate-sound` (were missing, causing 404s)

### Changed
- Upgraded all agents to latest Gemini models:
  - Text generation: `gemini-3-pro-preview` (all agents + API endpoints)
  - Image generation: `imagen-4.0-generate-001` (image_agent REST & SDK generators)
- Refactored all agent LLM services to extend `agents.shared.llm.LLMService`:
  - Each agent retains its own mock responses and temperature settings
  - Eliminated 4 copies of duplicated HTTP client code
- `agents/__init__.py` now exports all 4 agents: DesignAgent, CodeAgent, SoundAgent, PlayAgent
- `agents/sound_agent/agent.py`: Imports from own `utils.llm` instead of `design_agent.utils.llm`
- `games/feeding-caiso/src/core/StageManager.js`: Enhanced stage loading logic
- `games/feeding-caiso/src/generated/SoundLibrary.js`: Complete rewrite for Phase 5 audio (Zen/Ethereal)

### Fixed
- `api/generate_sound.py`: Removed duplicate code (lines 281-536 were a second httpx-based implementation)
- `api/analyze_code.py`: Updated model from `gemini-1.5-flash` to `gemini-3-pro-preview`
- `api/generate_sound.py`: Updated models from `gemini-1.5-pro`/`gemini-1.5-flash` to `gemini-3-pro-preview`
- `agents/design_agent/config.yaml`: Fixed model from `claude-3-5-sonnet-20240620` to `gemini-3-pro-preview`
- `agents/design_agent/agent.py`: Fixed fallback model from `gemini-1.5-flash` to `gemini-3-pro-preview`
- `agents/image_agent/image_generator/generators/gemini_generator.py`: Fixed metadata `imagen-3.0` to `imagen-4.0-generate-001`
- `vercel.json`: Added missing routes for analyze-code and generate-sound endpoints
