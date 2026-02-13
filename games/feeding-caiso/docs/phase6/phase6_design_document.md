# Feeding Caiso Phase 6: The Hollow Deep (Atmospheric Redesign)

## 1. 개요 (Overview)

기존 "Feeding Caiso" Phase 5는 자연의 하루(Dawn → Void) 테마를 사용하고 있으나, Phase 6에서는 **Hollow Knight**에서 영감을 받은 **어둡고 멜랑콜리하지만 아름다운 지하 세계**로 완전히 전환합니다.

**목표:** 손으로 그린 듯한 2D 아트 스타일, 깊이 있는 분위기, 그리고 곤충(Insect)과 고대 문명을 연상시키는 신비로운 테마를 적용하여 플레이어에게 깊은 몰입감을 제공합니다.

**핵심 변경 사항:**
- 시각 테마 전면 교체 (자연/하루 → 지하 왕국)
- 조명 시스템 완전 재작성 (`src/systems/LightingSystem.js`: 27줄 → 전면 개편)
- 파티클 시스템 신규 구축 (`src/systems/ParticleSystem.js`)
- 패럴랙스 시스템 리팩터링 (`src/utils/ParallaxBackground.js` → `src/systems/ParallaxSystem.js`)
- 오디오 시스템 강화 (크로스페이드, 리버브 추가)
- 스테이지 설정 전면 교체 (`src/config/Stages.js`)

**유지 사항 (Phase 5에서 계승):**
- 핵심 게임 루프: 플레이어가 음식을 Caiso에게 던져 배고픔을 줄이는 메카닉
- 모듈식 ES6 아키텍처 (`core/`, `entities/`, `managers/`, `systems/`, `utils/`, `config/`)
- FeverMode 콤보 시스템 (`src/utils/FeverMode.js`)
- ScreenShake, ImpactFrame 효과 (`src/utils/Juice.js`)
- VirtualJoystick 입력 시스템 (`src/core/Input.js`)
- SquashStretch 애니메이션 (`src/utils/SquashStretch.js`)
- 브라우저 기반 테스트 스위트 (`tests/test-runner.html`)

---

## 2. 디자인 컨셉 (Design Concept)

### 2.1 핵심 키워드

| 키워드 | 설명 | 구현 대상 |
|:---|:---|:---|
| **Hand-Drawn Aesthetic** | 펜화 느낌, 거친 텍스처, 깊이 있는 음영 | 스프라이트, 배경 에셋 |
| **Melancholic Beauty** | 쇠락한 왕국, 잊혀진 지하 세계, 슬프지만 매혹적인 분위기 | 배경, BGM, 컬러 팔레트 |
| **Atmospheric Depth** | 안개, 먼지 입자, 다중 레이어의 패럴랙스 배경 | `ParallaxSystem`, `ParticleSystem` |
| **Insectoid & Organic** | 딱정벌레, 유충, 고치, 균사체 등 자연물 기반의 기괴하면서도 귀여운 디자인 | 캐릭터, 아이템, 장애물 |

### 2.2 컬러 팔레트 (Color Palette)

```
Primary (배경/기본):
  Void Black      #0f0f1b   ← 기본 캔버스 배경 (현재: #0a0a1a in Game.js:432)
  Deep Blue Grey   #2d3436   ← 중경 배경 레이어
  Desaturated Blue #636e72   ← 원경 배경 레이어

Secondary (UI/텍스트):
  Pale Shell White #dfe6e9   ← 주요 텍스트, UI 테두리
  Faded Gold       #b2bec3   ← 유물/고대 느낌의 보조 텍스트

Accent (강조 효과):
  Infection Orange #ff7675   ← 감염 효과, 위험 표시, 데미지
  Soul Blue        #74b9ff   ← 영혼 아이템, 회복, 긍정적 피드백
  Void Purple      #a29bfe   ← Fever Mode, 특수 효과 (현재 로딩 스크린 색상과 연속성)
```

### 2.3 기존 테마와의 매핑

| Phase 5 (현재 `Stages.js`) | Phase 6 (The Hollow Deep) |
|:---|:---|
| Stage 1: Morning Dew (Dawn) | Stage 1: 잊혀진 교차로 (The Forgotten Crossroads) |
| Stage 2: Sunlit Bloom (Morning) | Stage 2: 녹색 거리 (Greenpath) |
| Stage 3: Whispering Breeze (Noon) | Stage 3: 곰팡이 황무지 (Fungal Wastes) |
| Stage 4: Golden Harvest (Afternoon) | Stage 4: 눈물의 도시 (City of Tears) |
| Stage 5: Crimson Sunset (Sunset) | Stage 5: 수정 봉우리 (Crystal Peak) |
| Stage 6: Twilight Grove (Dusk) | Stage 6: 깊은 둥지 (Deepnest) |
| Stage 7: Moonlit Lake (Night) | Stage 7: 왕국의 끝자락 (Kingdom's Edge) |
| Stage 8: Starry Expanse (Midnight) | Stage 8: 심연 (The Abyss) |
| Stage 9: Aurora Borealis (Deep Night) | Stage 9: 백색 궁전 (White Palace) |
| Stage 10: Cosmic Dawn (Void) | Stage 10: 광휘 (The Radiance) |

---

## 3. 에셋 생성 가이드라인 (Asset Generation Guidelines)

CAISOGAMES 프로젝트는 Vercel 프록시를 통한 AI 이미지 생성 파이프라인을 사용합니다 (CLAUDE.md 참조).

### 3.1 이미지 에셋 생성

**생성 도구:** `scripts/generate_asset.py` (Vercel → Gemini API 프록시)

```bash
# 환경 설정
export VERCEL_APP_URL=https://caisogames.vercel.app

# 캐릭터 스프라이트 생성
python scripts/generate_asset.py sprite \
  "hand-drawn 2D game art, Hollow Knight style, cute but slightly creepy little bug creature, white mask, black body, cloak, dark atmospheric, cel shaded but moody, sketch lines" \
  caiso_hollow_idle \
  --size 256x256

# 배경 생성
python scripts/generate_asset.py background \
  "underground cave system, ancient ruins, blue mist, Hollow Knight style, dark monochrome with blue ambient light, hand-drawn 2D, stalactites" \
  bg_crossroads \
  --size 960x854

# 아이템 생성
python scripts/generate_asset.py sprite \
  "glowing soul orb, ethereal blue light, Hollow Knight style, hand-drawn, simple but luminous" \
  item_soul_orb \
  --size 64x64
```

### 3.2 프롬프트 스타일 가이드

모든 이미지 생성 프롬프트에 반드시 포함할 키워드:

| 카테고리 | 필수 키워드 | 비고 |
|:---|:---|:---|
| **스타일** | `hand-drawn 2D game art`, `Hollow Knight style` | 기본 스타일 |
| **분위기** | `dark atmospheric`, `cel shaded but moody`, `sketch lines` | 톤 통일 |
| **캐릭터** | `gothic insect fantasy`, `white mask`, `dark body` | Caiso 테마 |
| **배경** | `underground`, `ancient ruins`, `blue ambient light` | 환경 테마 |

### 3.3 에셋 저장 위치

모든 Phase 6 에셋은 게임 전용 에셋 폴더에 저장합니다:

```
games/feeding-caiso/assets/
├── sprites/
│   ├── caiso/           # Caiso 표정별 스프라이트 (256x256)
│   │   ├── caiso_idle.png
│   │   ├── caiso_hungry.png
│   │   ├── caiso_happy.png
│   │   └── caiso_sad.png
│   ├── player/          # 플레이어 스프라이트 (128x160)
│   │   └── player_throwing.png
│   └── villagers/       # 마을 주민 (64x64)
│       ├── villager_normal.png
│       └── villager_scared.png
├── items/               # 음식/아이템 (64x64)
│   ├── item_soul_orb.png         # ← apple 대체
│   ├── item_geo_cluster.png      # ← burger 대체
│   ├── item_pale_ore.png         # ← pizza 대체
│   ├── item_kings_idol.png       # ← dorito 대체
│   ├── item_lifeblood.png        # ← watermelon 대체
│   └── item_void_egg.png         # ← dynamite 대체
├── backgrounds/         # 배경 레이어 (960xH, 단계별)
│   ├── bg_far.png       # 원경 레이어 (speed: 0.1)
│   ├── bg_mid.png       # 중경 레이어 (speed: 0.3)
│   └── bg_near.png      # 근경 레이어 (speed: 0.6)
└── ui/
    ├── title_background.png
    └── ui_button_feed.png
```

### 3.4 사운드 에셋

현재 사운드는 `src/generated/SoundLibrary.js`에서 Web Audio API로 프로시저럴 생성됩니다.
Phase 6에서는 기존 7종 사운드를 Hollow Knight 톤으로 재조정합니다:

| 사운드 키 | 현재 스타일 | Phase 6 목표 스타일 |
|:---|:---|:---|
| `throw` | Zen whoosh | 동굴 울림이 있는 날카로운 소리 |
| `eat` | Ethereal chime | 영혼 흡수 효과음 (리버브) |
| `combo` | Bell sequence | 수정 공명 사운드 |
| `fever` | Wind gust | 공허의 폭발 (저음 진동) |
| `gameover` | Soft descent | 가면 깨지는 소리 |
| `levelup` | Ascending tones | 벤치 세이브 느낌의 따뜻한 멜로디 |

---

## 4. 게임플레이 리디자인 (Gameplay Redesign)

### 4.1 핵심 메카닉 유지 (Core Loop Preserved)

Phase 6는 **시각/청각적 전면 개편**이며, 핵심 게임플레이는 유지합니다:

```
[플레이어] → 음식 던지기 → [Caiso 먹기] → 배고픔 감소 → 승리 조건
     ↑                                         |
  조이스틱 이동                            콤보/피버 시스템
```

**변경되는 요소:**
- 음식 아이템 → 영혼/룬/유물 (시각적 리스킨)
- 마을 주민 → 하충(Husks) 또는 작은 곤충 생명체
- 장애물 → 감염체, 포자, 톱날 등 (스테이지별)
- 배고픔 → "공허(Void)" 게이지
- 체력(마을 주민 수) → "가면(Masks)" 개수

### 4.2 진화 시스템 리스킨

현재 `Constants.js`의 `EVOLUTION_TIERS`를 재해석합니다:

| 현재 | Phase 6 | 레벨 | 스케일 |
|:---|:---|:---|:---|
| Baby Caiso | Grub (유충) | 1 | 0.8 |
| Teen Caiso | Husk (번데기) | 3 | 1.0 |
| Adult Caiso | Knight (기사) | 6 | 1.2 |
| King Caiso | Shade Lord (공허의 군주) | 10 | 1.5 |

### 4.3 Fever Mode 리스킨

현재 `FeverMode.js`의 시각 효과를 Hollow Knight 테마로 변경:
- 화면 플래시 색상: `#ff006e` → `#74b9ff` (Soul Blue)
- 파티클 색상: 현재 5색 → `['#74b9ff', '#a29bfe', '#dfe6e9', '#636e72', '#0f0f1b']`
- 게이지 그래디언트: 오렌지 계열 → 블루 계열

---

## 5. 개발 로드맵 (Development Roadmap)

### Step 1: 스테이지 설정 교체 (Config Migration)
- **대상 파일:** `src/config/Stages.js`
- **작업:** 10개 스테이지 정의를 Hollow Knight 테마로 전면 교체
- **세부 사항:** `game_scenario.md`의 스테이지별 파라미터를 코드에 반영
- **의존성:** 없음

### Step 2: 조명 시스템 재작성 (Lighting System Rewrite)
- **대상 파일:** `src/systems/LightingSystem.js` (현재 27줄 → 예상 200줄+)
- **작업:** 2D 다이내믹 라이팅 (Radial Gradient, Vignette, globalCompositeOperation)
- **의존성:** Step 1 (스테이지별 조명 파라미터)

### Step 3: 패럴랙스 시스템 리팩터링 (Parallax System Upgrade)
- **대상:** `src/utils/ParallaxBackground.js` → `src/systems/ParallaxSystem.js`로 이전
- **작업:** 스테이지별 다른 배경 레이어 로딩, 레이어 수 확장 (3 → 4-5)
- **의존성:** Step 1

### Step 4: 파티클 시스템 신규 구축 (Particle System)
- **대상:** `src/systems/ParticleSystem.js` (신규)
- **작업:** 오브젝트 풀링, 다양한 이미터 타입 (먼지, 포자, 비, 재)
- **참고:** 현재 `Game.js:325-336`과 `FeverMode.js`의 인라인 파티클 로직 통합
- **의존성:** 없음

### Step 5: 에셋 생성 및 교체 (Asset Swap)
- **대상:** `assets/` 디렉터리 전체
- **작업:** Phase 5 에셋 백업 후 Phase 6 에셋으로 교체
- **참고:** `AssetManager.js`의 에셋 키는 유지, 이미지 파일만 교체
- **의존성:** Step 1 (어떤 에셋이 필요한지 확정 후)

### Step 6: 오디오 강화 (Audio Enhancement)
- **대상:** `src/core/Audio.js`, `src/generated/SoundLibrary.js`
- **작업:** BGM 크로스페이드, ConvolverNode 리버브, SFX 리디자인
- **의존성:** Step 1

### Step 7: Game.js 통합 및 테스트 (Integration)
- **대상:** `src/core/Game.js` (현재 703줄)
- **작업:** 새 시스템들을 update/render 사이클에 통합
- **의존성:** Step 2, 3, 4, 5, 6 모두

---

## 6. 기술적 제약 사항 (Technical Constraints)

| 항목 | 제약 | 근거 |
|:---|:---|:---|
| **캔버스 크기** | 480 x 854 (고정) | `GAME_CONFIG.WIDTH/HEIGHT` |
| **목표 프레임율** | 60 FPS | deltaTime 50ms 제한 (`Game.js:694`) |
| **임포트 경로** | 반드시 상대 경로 사용 | `/src/...` 절대 경로는 허브에서 로딩 실패 |
| **에셋 로딩** | 비동기, graceful degradation | `AssetManager` fallback 패턴 유지 |
| **입력 지연** | 최소화 (타이트한 조작감 최우선) | 터치/마우스 즉시 반응 |
| **번들링** | 없음 (ES6 모듈 직접 로드) | `index.html`의 `type="module"` |

---

*이 문서는 Phase 6 개발의 디자인 기준이며, `game_scenario.md`(스테이지 상세)와 `technical_specification.md`(구현 명세)와 함께 참조합니다.*
