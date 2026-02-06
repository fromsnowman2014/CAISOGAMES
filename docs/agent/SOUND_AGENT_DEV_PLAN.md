# Sound Agent Development Plan

## Overview

**역할**: 게임에 적합한 사운드 효과와 배경 음악 생성/적용

**Score Weight**: 15점 (총 100점 중)

---

## Core Features

| Feature | Description | Implementation |
|---------|-------------|----------------|
| `audit_sounds()` | 현재 게임의 사운드 상태 분석 | Parse HTML/JS for audio elements |
| `define_sound_requirements()` | 필요한 사운드 목록 생성 | LLM-based analysis |
| `generate_procedural_sfx()` | Web Audio API 코드 생성 | Generate JS code snippets |
| `generate_bgm_code()` | Tone.js 배경음악 코드 | Generate Tone.js patterns |
| `integrate_sounds()` | 게임 코드에 사운드 통합 | Code injection |

---

## Sound Categories

| Category | Examples | Priority |
|----------|----------|----------|
| 🔊 UI | 버튼 클릭, 메뉴 전환, 선택 | High |
| 💥 Gameplay | 충돌, 점프, 아이템 획득, 공격 | High |
| 🎵 BGM | 메인 메뉴, 인게임, 게임오버 | Medium |
| 📣 Feedback | 성공, 실패, 콤보, 레벨업 | Medium |

---

## Folder Structure

```
agents/sound_agent/
├── __init__.py           # Package init
├── __main__.py           # CLI entry point
├── agent.py              # Core SoundAgent class
├── config.yaml           # Configuration
├── README.md             # Documentation
├── prompts/              # LLM prompts
│   ├── audit_sounds.txt
│   ├── define_requirements.txt
│   └── generate_sfx.txt
├── generators/           # Sound generators
│   ├── __init__.py
│   ├── web_audio.py      # Web Audio API generator
│   └── tone_js.py        # Tone.js BGM generator
├── templates/            # Output templates
│   └── sound_integration.js
└── utils/
    └── llm.py            # LLM client (reuse from design_agent)
```

---

## Implementation Approach

### Phase 1: Analysis
1. Parse game HTML/JS for existing audio elements
2. Identify game events that need sounds
3. Generate sound requirement list via LLM

### Phase 2: Generation
1. Generate Web Audio API code snippets for SFX
2. Generate Tone.js patterns for BGM
3. Create integration code template

### Phase 3: Output
1. Generate `{game}_sound_audit.md` report
2. Generate ready-to-use JS code files
3. Provide integration instructions

---

## Prompts

### 1. Audit Sounds Prompt
```
Analyze this game code and identify:
1. Existing audio/sound implementations
2. Game events that need sounds
3. Missing sound categories
```

### 2. Define Requirements Prompt
```
Based on this game, define sound requirements:
- List specific SFX needed with descriptions
- Suggest BGM style and tempo
- Prioritize by importance
```

### 3. Generate SFX Prompt
```
Generate Web Audio API JavaScript code for:
Sound: {sound_name}
Description: {description}
Duration: {duration}ms
```

---

## Verification Plan

1. **Run against `feeding-caiso`**
2. **Check output**: `feeding-caiso_sound_audit.md`
3. **Verify JS code**: Generated Web Audio snippets are valid
4. **Mock mode**: Works without API key
