# Feeding Caiso Phase 6: Technical Specification & Refactoring Plan

이 문서는 "Feeding Caiso" Phase 6 ("The Hollow Deep")의 기술 명세 및 리팩터링 계획입니다.
Hollow Knight 스타일의 대기적(atmospheric) 경험을 구현하기 위한 시스템 변경 사항을 정의합니다.

> **참고 문서:**
> - `design_document.md` — 디자인 컨셉, 에셋 가이드라인, 개발 로드맵
> - `game_scenario.md` — 스테이지별 상세 파라미터 및 게임플레이 규칙

---

## 1. 현재 아키텍처 분석 (Current Architecture)

### 1.1 파일 구조 (20개 JS 파일)

```
games/feeding-caiso/
├── index.html                           # 엔트리 포인트 (type="module" → src/core/Game.js)
├── src/
│   ├── config/
│   │   └── Stages.js                    # 10스테이지 정의 (Phase 5: 자연 테마)
│   ├── core/
│   │   ├── Game.js                      # 메인 루프 (703줄) — 초기화, update, render
│   │   ├── Audio.js                     # AudioManager (22줄) — SoundLibrary 래퍼
│   │   ├── Environment.js               # 풍속/중력/배경색 (33줄)
│   │   ├── Input.js                     # VirtualJoystick (터치/마우스)
│   │   └── StageManager.js              # 스테이지 전환, 장애물 스폰 (115줄)
│   ├── entities/
│   │   ├── Caiso.js                     # 메인 캐릭터 (진화, 표정)
│   │   ├── Food.js                      # 투척 음식 (궤적, 환경 물리)
│   │   ├── Hazard.js                    # 장애물 엔티티
│   │   ├── Player.js                    # 플레이어 컨트롤러
│   │   └── Villager.js                  # NPC (마을 주민)
│   ├── generated/
│   │   └── SoundLibrary.js              # 프로시저럴 사운드 7종 (226줄)
│   ├── managers/
│   │   ├── AssetManager.js              # 이미지 로딩 (18개 에셋)
│   │   └── UIManager.js                 # DOM UI 업데이트
│   ├── systems/
│   │   └── LightingSystem.js            # 단순 오버레이 (27줄) ← 전면 재작성 대상
│   └── utils/
│       ├── Constants.js                 # GAME_CONFIG, FOODS, EVOLUTION_TIERS, FEVER_CONFIG
│       ├── FeverMode.js                 # 피버 게이지, 파티클, 화면 효과 (162줄)
│       ├── Juice.js                     # ScreenShake, ImpactFrame
│       ├── ParallaxBackground.js        # 3레이어 패럴랙스 (53줄) ← 리팩터링 대상
│       └── SquashStretch.js             # 탄성 애니메이션 헬퍼
└── tests/
    └── test-runner.html                 # 브라우저 기반 테스트 (15 suites, 60+ tests)
```

### 1.2 핵심 게임 루프 (Game.js)

```
init()
  ↓
gameLoop(timestamp)
  ├── update(deltaTime)    ← max 50ms cap (Game.js:694)
  │   ├── shake.update()
  │   ├── freeze.update()  ← true이면 나머지 스킵 (임팩트 프레임)
  │   ├── environment.update()
  │   ├── lighting.update()
  │   ├── stageManager.update()
  │   ├── ui.update()
  │   ├── background.update()
  │   ├── [entity updates: caiso, player, fever, villagers, foods, hazards]
  │   ├── [collision detection: food-hazard, food-caiso]
  │   └── [particle & floating text updates]
  └── render()
      └── drawGame()
          ├── environment.drawBackground()   ← 배경색 채우기
          ├── background.draw()              ← 패럴랙스 레이어
          ├── lighting.draw()                ← 오버레이 색상
          ├── fever.draw()                   ← 피버 이펙트 (활성 시)
          ├── [entity draws: villagers, caiso, player, foods, hazards]
          ├── fever.drawGauge()              ← 피버 게이지 (항상)
          ├── [score display, stage name]
          ├── [particles, floating texts]
          ├── joystick.draw()
          └── stageManager.draw()            ← 전환 오버레이 (최상위)
```

### 1.3 모듈별 변경 판정

| 모듈 | 현재 상태 | Phase 6 액션 | 우선순위 |
|:---|:---|:---|:---|
| `config/Stages.js` | Phase 5 테마 | **전면 교체** — Hollow Knight 10스테이지 | P0 |
| `systems/LightingSystem.js` | 27줄, 단순 오버레이 | **전면 재작성** — 다이내믹 라이팅 | P0 |
| `utils/ParallaxBackground.js` | 53줄, 3레이어 고정 | **리팩터링** → `systems/ParallaxSystem.js` | P1 |
| `systems/ParticleSystem.js` | 존재하지 않음 | **신규 작성** — 오브젝트 풀링 파티클 | P1 |
| `core/Audio.js` | 22줄, 기본 재생 | **확장** — 크로스페이드, 리버브 | P2 |
| `core/Game.js` | 703줄 | **수정** — 새 시스템 통합 | P1 |
| `core/StageManager.js` | 115줄 | **수정** — 확장된 스테이지 설정 지원 | P1 |
| `core/Environment.js` | 33줄 | **수정** — 풍향 교대, 추가 물리 | P2 |
| `managers/AssetManager.js` | 18개 에셋 | **수정** — Phase 6 에셋 목록 교체 | P1 |
| `utils/Constants.js` | FOODS, EVOLUTION_TIERS | **수정** — 이름/에셋키 리스킨 | P2 |
| `utils/FeverMode.js` | 162줄 | **수정** — 색상/이펙트 테마 변경 | P2 |
| `entities/*` | 안정 | **수정 최소화** — 에셋 키만 변경 | P3 |

---

## 2. 핵심 제약 사항 (Critical Constraints)

구현 시 반드시 준수해야 하는 규칙입니다.

### 2.1 임포트 경로

```javascript
// ✅ 올바른 사용 (상대 경로)
import { STAGES } from '../config/Stages.js';
import { LightingSystem } from '../systems/LightingSystem.js';

// ❌ 절대 사용 금지 (절대 경로 — 허브에서 로딩 실패)
import { STAGES } from '/src/config/Stages.js';
```

> **근거:** CAISOGAMES 허브(`index.html`)가 루트에서 서빙하므로 절대 경로는 `games/feeding-caiso/src/...`가 아닌 `/src/...`로 해석되어 404 발생.

### 2.2 캔버스 설정

```javascript
// Constants.js에서 정의
GAME_CONFIG.WIDTH  = 480;   // 고정
GAME_CONFIG.HEIGHT = 854;   // 고정

// 주요 Y 좌표
GAME_CONFIG.CAISO_Y         = 180;  // Caiso 위치
GAME_CONFIG.PLAYER_Y        = 700;  // 플레이어 위치
GAME_CONFIG.VILLAGER_SPAWN_Y = 620; // 마을 주민 스폰 위치
GAME_CONFIG.HUD_HEIGHT      = 80;   // HUD 영역
GAME_CONFIG.CONTROL_HEIGHT  = 180;  // 조작 영역
```

### 2.3 성능 제약

| 항목 | 제한 | 비고 |
|:---|:---|:---|
| 프레임율 목표 | 60 FPS | deltaTime 50ms cap |
| 최대 파티클 수 | 500개 (풀 크기) | 오브젝트 풀링 필수 |
| 최대 장애물 수 | 20개 동시 | `hazards` 배열 크기 제한 |
| 에셋 로딩 | 비동기, 실패 시 fallback | 그림 로드 실패해도 게임 진행 |
| 번들링 | 없음 | ES6 모듈 직접 로드 |

---

## 3. 시스템 구현 명세 (System Specifications)

### 3.1 스테이지 설정 구조 (`src/config/Stages.js`)

현재 스테이지 설정을 확장하여 Phase 6 요소를 지원합니다.

```javascript
// Phase 6 스테이지 설정 스키마
export const STAGES = [
    {
        // === 기본 (Phase 5 호환) ===
        name: "The Forgotten Crossroads",        // 표시 이름
        nameKo: "잊혀진 교차로",                    // 한국어 이름
        theme: "crossroads",                      // 테마 식별자
        duration: 60000,                          // ms 단위 (현재: 60 → 유지)

        // === 배경 ===
        backgroundColor: "#1a1a2e",               // 기본 캔버스 배경색
        atmosphere: {
            overlayColor: "rgba(15, 15, 27, 0.3)",
            windX: 0,
            gravityY: 1.0
        },

        // === Phase 6 확장 필드 ===
        lighting: {
            ambientLight: 0.3,                    // 0.0(완전 암흑) ~ 1.0(완전 밝음)
            playerLightRadius: 150,               // 플레이어 광원 반경 (px)
            playerLightColor: "rgba(116, 185, 255, 0.4)",
            fixedLights: [],                      // [{x, y, radius, color}]
            bloom: false,                         // 블룸 효과
            vignette: true                        // 비네팅 효과
        },

        parallax: {
            layers: [
                { key: "bg_crossroads_far",  speed: 0.1, y: 0,   height: 854 },
                { key: "bg_crossroads_mid",  speed: 0.3, y: 200, height: 400 },
                { key: "bg_crossroads_near", speed: 0.6, y: 500, height: 354 }
            ]
        },

        particles: {
            emitters: [
                { type: "dust", density: "low", color: "#636e72", sizeRange: [2, 5] }
            ]
        },

        gameplay: {
            hazards: [],                          // Hazard 타입 목록
            itemSpeedMult: 1.0,                   // 아이템 속도 배율
            scoreMultiplier: 1.0,                 // 점수 배율
            slipperyFloor: false,                 // 미끄러운 바닥
            visibilityRadius: null,               // null = 무제한, 숫자 = px
            windDirection: "static"               // "static" | "alternating"
        },

        audio: {
            bgmKey: "bgm_crossroads",             // BGM 식별자
            ambience: ["drip", "wind_light"],      // 앰비언스 레이어
            reverbLevel: 0.3                       // 리버브 강도
        }
    },
    // ... Stage 2-10
];
```

### 3.2 조명 시스템 (`src/systems/LightingSystem.js`)

**현재 상태 (27줄):**
```javascript
// 현재: 단순 overlayColor fillRect만 수행
draw(ctx) {
    ctx.fillStyle = this.overlayColor;
    ctx.fillRect(0, 0, width, height);
}
```

**Phase 6 목표 구현:**

```javascript
export class LightingSystem {
    constructor(game) {
        this.game = game;
        this.ambientLight = 0.3;
        this.playerLightRadius = 150;
        this.playerLightColor = "rgba(116, 185, 255, 0.4)";
        this.fixedLights = [];
        this.vignette = true;
        this.bloom = false;

        // 오프스크린 캔버스 (성능 최적화)
        this.lightCanvas = document.createElement('canvas');
        this.lightCtx = this.lightCanvas.getContext('2d');
    }

    setAtmosphere(config) {
        // config.lighting 객체에서 모든 조명 파라미터 로드
    }

    update(deltaTime) {
        // 조명 펄스/깜빡임 애니메이션
        // 블룸 효과 타이머
    }

    draw(ctx) {
        const { WIDTH, HEIGHT } = GAME_CONFIG;
        const lc = this.lightCanvas;
        const lctx = this.lightCtx;

        lc.width = WIDTH;
        lc.height = HEIGHT;

        // 1단계: 어둠 기본 레이어 생성
        lctx.fillStyle = `rgba(0, 0, 0, ${1 - this.ambientLight})`;
        lctx.fillRect(0, 0, WIDTH, HEIGHT);

        // 2단계: 광원 위치에 원형 그래디언트로 "구멍" 뚫기
        lctx.globalCompositeOperation = 'destination-out';
        this._drawLight(lctx, playerX, playerY, this.playerLightRadius, this.playerLightColor);
        this.fixedLights.forEach(light => {
            this._drawLight(lctx, light.x, light.y, light.radius, light.color);
        });
        lctx.globalCompositeOperation = 'source-over';

        // 3단계: 어둠 레이어를 게임 캔버스에 합성
        ctx.drawImage(lc, 0, 0);

        // 4단계: 비네팅 (선택적)
        if (this.vignette) {
            this._drawVignette(ctx, WIDTH, HEIGHT);
        }
    }

    _drawLight(ctx, x, y, radius, color) {
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
        gradient.addColorStop(0, 'rgba(0, 0, 0, 1)');
        gradient.addColorStop(0.7, 'rgba(0, 0, 0, 0.5)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
    }

    _drawVignette(ctx, w, h) {
        const gradient = ctx.createRadialGradient(w/2, h/2, w*0.3, w/2, h/2, w*0.8);
        gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.4)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, w, h);
    }
}
```

**핵심 기법:**
- `globalCompositeOperation = 'destination-out'`: 어둠 레이어에서 광원 위치를 "지움"
- 오프스크린 캔버스: 메인 캔버스 상태 오염 방지, 성능 최적화
- Stage 6(Deepnest) 시야 제한: `ambientLight = 0.05`, `playerLightRadius = 100`으로 극적 효과

### 3.3 패럴랙스 시스템 (`src/systems/ParallaxSystem.js`)

현재 `utils/ParallaxBackground.js`를 `systems/`로 이전하고 확장합니다.

**현재 → Phase 6 변경:**

| 항목 | 현재 (`ParallaxBackground.js`) | Phase 6 (`ParallaxSystem.js`) |
|:---|:---|:---|
| 위치 | `src/utils/` | `src/systems/` |
| 레이어 수 | 3 (고정) | 스테이지별 동적 (2-5) |
| 레이어 정의 | 하드코딩 (clouds, city, ground) | `Stages.js`의 `parallax.layers` 설정 |
| 배경 에셋 | 3개 고정 | 스테이지별 교체 (최대 30개) |
| fallback | 단색 사각형 | 그래디언트 fallback |
| 스크롤 입력 | `playerVelocityX`만 | `playerVelocityX` + 자동 스크롤 옵션 |

```javascript
export class ParallaxSystem {
    constructor(game) {
        this.game = game;
        this.layers = [];
    }

    /**
     * 스테이지 전환 시 호출
     * @param {Object} parallaxConfig - Stages.js의 parallax 설정
     */
    loadStageConfig(parallaxConfig) {
        this.layers = parallaxConfig.layers.map(layerDef => ({
            key: layerDef.key,
            speed: layerDef.speed,
            y: layerDef.y,
            height: layerDef.height,
            offset: 0,
            autoScroll: layerDef.autoScroll || 0  // 자동 스크롤 속도 (px/s)
        }));
    }

    update(playerVelocityX, deltaTime) {
        this.layers.forEach(layer => {
            // 플레이어 움직임 기반 스크롤
            layer.offset -= playerVelocityX * layer.speed * deltaTime * 0.02;
            // 자동 스크롤 (배경 움직임)
            layer.offset -= layer.autoScroll * deltaTime * 0.001;
            // 래핑
            const img = this.game.assets.get(layer.key);
            const width = img ? img.width : GAME_CONFIG.WIDTH * 2;
            if (Math.abs(layer.offset) > width) layer.offset = 0;
        });
    }

    draw(ctx) {
        this.layers.forEach(layer => {
            const img = this.game.assets.get(layer.key);
            if (img) {
                const w = img.width;
                ctx.drawImage(img, layer.offset, layer.y, w, layer.height);
                ctx.drawImage(img, layer.offset + w, layer.y, w, layer.height);
                ctx.drawImage(img, layer.offset - w, layer.y, w, layer.height);
            } else {
                this._drawFallback(ctx, layer);
            }
        });
    }

    _drawFallback(ctx, layer) {
        // 스테이지 테마 기반 그래디언트 fallback
        ctx.fillStyle = 'rgba(15, 15, 27, 0.3)';
        ctx.fillRect(0, layer.y, GAME_CONFIG.WIDTH, layer.height);
    }
}
```

**마이그레이션 단계:**
1. `ParallaxSystem.js`를 `src/systems/`에 생성
2. `Game.js`의 임포트를 `ParallaxBackground` → `ParallaxSystem`으로 변경
3. `StageManager.loadStage()`에서 `parallaxSystem.loadStageConfig()` 호출 추가
4. `utils/ParallaxBackground.js` 삭제

### 3.4 파티클 시스템 (`src/systems/ParticleSystem.js`)

**신규 시스템.** 현재 코드에서 파티클은 두 곳에서 인라인으로 관리됩니다:
- `Game.js:325-336` — `addParticles()` (단순 원형 파티클)
- `Game.js:412-418` — update 루프 (중력, 수명 감소)
- `FeverMode.js:27-66` — 피버 전용 파티클

이들을 통합하고, 환경 파티클(먼지, 포자, 비, 재)을 추가합니다.

```javascript
export class ParticleSystem {
    constructor(game) {
        this.game = game;
        this.pool = [];           // 오브젝트 풀 (비활성 파티클)
        this.active = [];         // 활성 파티클
        this.emitters = [];       // 활성 이미터
        this.maxParticles = 500;  // 성능 제한

        // 풀 초기화
        for (let i = 0; i < this.maxParticles; i++) {
            this.pool.push(this._createParticle());
        }
    }

    _createParticle() {
        return {
            x: 0, y: 0, vx: 0, vy: 0,
            size: 0, color: '#fff', alpha: 1,
            life: 0, maxLife: 0,
            gravity: 0.35,       // 기본 중력
            active: false
        };
    }

    /**
     * 풀에서 파티클 하나를 가져와 활성화
     */
    spawn(x, y, config) {
        if (this.active.length >= this.maxParticles) return null;

        const p = this.pool.pop();
        if (!p) return null;

        Object.assign(p, {
            x, y,
            vx: config.vx || (Math.random() - 0.5) * 14,
            vy: config.vy || (Math.random() - 0.5) * 14 - 5,
            size: config.size || Math.random() * 10 + 4,
            color: config.color || '#fff',
            alpha: 1,
            life: config.life || 35 + Math.random() * 20,
            maxLife: config.life || 55,
            gravity: config.gravity ?? 0.35,
            active: true
        });

        this.active.push(p);
        return p;
    }

    /**
     * 한번에 여러 파티클 발사 (Game.js addParticles 대체)
     */
    burst(x, y, color, count) {
        for (let i = 0; i < count; i++) {
            this.spawn(x, y, { color });
        }
    }

    /**
     * 지속적 이미터 추가 (스테이지별 환경 파티클)
     */
    addEmitter(emitterConfig) {
        this.emitters.push({
            type: emitterConfig.type,        // "dust" | "spore" | "rain" | "ash" | "void"
            density: emitterConfig.density,  // "low" | "medium" | "high" | "very_high" | "extreme"
            color: emitterConfig.color,
            sizeRange: emitterConfig.sizeRange || [2, 5],
            timer: 0,
            active: true
        });
    }

    clearEmitters() {
        this.emitters = [];
    }

    update(deltaTime) {
        // 이미터에서 파티클 생성
        this.emitters.forEach(emitter => {
            if (!emitter.active) return;
            emitter.timer += deltaTime;
            const interval = this._getEmitterInterval(emitter.density);
            while (emitter.timer >= interval) {
                emitter.timer -= interval;
                this._emitParticle(emitter);
            }
        });

        // 활성 파티클 업데이트
        for (let i = this.active.length - 1; i >= 0; i--) {
            const p = this.active[i];
            p.x += p.vx;
            p.y += p.vy;
            p.vy += p.gravity;
            p.life--;
            p.alpha = p.life / p.maxLife;

            if (p.life <= 0) {
                p.active = false;
                this.active.splice(i, 1);
                this.pool.push(p);  // 풀로 반환
            }
        }
    }

    draw(ctx) {
        this.active.forEach(p => {
            ctx.globalAlpha = p.alpha;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.globalAlpha = 1;
    }

    _getEmitterInterval(density) {
        const intervals = {
            low: 200,       // 5/sec
            medium: 80,     // 12.5/sec
            high: 40,       // 25/sec
            very_high: 16,  // 60/sec
            extreme: 8      // 125/sec
        };
        return intervals[density] || 80;
    }

    _emitParticle(emitter) {
        const W = GAME_CONFIG.WIDTH;
        const H = GAME_CONFIG.HEIGHT;
        const [minSize, maxSize] = emitter.sizeRange;
        const size = minSize + Math.random() * (maxSize - minSize);

        const configs = {
            dust: {
                x: Math.random() * W, y: Math.random() * H,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.3,
                gravity: 0, life: 200 + Math.random() * 100
            },
            spore: {
                x: Math.random() * W, y: -10,
                vx: (Math.random() - 0.5) * 1,
                vy: 0.3 + Math.random() * 0.5,
                gravity: 0.01, life: 300
            },
            rain: {
                x: Math.random() * W, y: -10,
                vx: 0.5, // 풍향 영향
                vy: 8 + Math.random() * 4,
                gravity: 0, life: 80
            },
            ash: {
                x: Math.random() * W, y: -10,
                vx: (Math.random() - 0.5) * 2, // 풍향 영향
                vy: 0.5 + Math.random() * 1,
                gravity: 0, life: 400
            },
            void: {
                x: Math.random() * W, y: H + 10,
                vx: (Math.random() - 0.5) * 0.5,
                vy: -(1 + Math.random() * 2), // 위로 상승
                gravity: -0.01, life: 300
            }
        };

        const cfg = configs[emitter.type] || configs.dust;
        this.spawn(cfg.x, cfg.y, {
            ...cfg,
            color: emitter.color,
            size
        });
    }
}
```

### 3.5 오디오 시스템 확장 (`src/core/Audio.js`)

**현재 상태 (22줄):**
- `AudioManager`: `AudioContext` + `SoundLibrary[key]()` 호출
- BGM 없음, SFX만 7종

**Phase 6 확장:**

```javascript
export class AudioManager {
    constructor() {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        this.masterVolume = 0.5;
        this.enabled = true;

        // Phase 6 추가
        this.masterGain = this.ctx.createGain();
        this.masterGain.gain.value = this.masterVolume;
        this.masterGain.connect(this.ctx.destination);

        // 리버브 (ConvolverNode)
        this.convolver = null;       // 리버브 노드
        this.reverbLevel = 0;        // 0.0 ~ 1.0
        this.reverbGain = this.ctx.createGain();
        this.reverbGain.connect(this.masterGain);

        // BGM 크로스페이드
        this.currentBgm = null;      // { source, gain }
        this.nextBgm = null;
        this.crossfadeDuration = 2000; // ms
    }

    /**
     * 리버브 임펄스 응답 생성 (프로시저럴)
     */
    async initReverb() {
        const sampleRate = this.ctx.sampleRate;
        const length = sampleRate * 2; // 2초 리버브
        const buffer = this.ctx.createBuffer(2, length, sampleRate);

        for (let ch = 0; ch < 2; ch++) {
            const data = buffer.getChannelData(ch);
            for (let i = 0; i < length; i++) {
                data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, 2);
            }
        }

        this.convolver = this.ctx.createConvolver();
        this.convolver.buffer = buffer;
        this.convolver.connect(this.reverbGain);
    }

    setReverbLevel(level) {
        this.reverbLevel = level;
        this.reverbGain.gain.value = level;
    }

    /**
     * SFX 재생 (기존 호환 + 리버브 옵션)
     */
    play(key) {
        if (!this.enabled) return;
        if (this.ctx.state === 'suspended') this.ctx.resume();

        if (SoundLibrary[key]) {
            SoundLibrary[key](this.ctx, this.masterVolume);
            // 리버브가 활성화된 경우 리버브 채널에도 동시 전송
        }
    }

    /**
     * BGM 크로스페이드 전환
     * @param {string} bgmKey - 새 BGM 키
     */
    crossfadeBgm(bgmKey) {
        // 현재 BGM 페이드 아웃
        if (this.currentBgm) {
            const fadeOut = this.currentBgm.gain;
            fadeOut.gain.linearRampToValueAtTime(
                0, this.ctx.currentTime + this.crossfadeDuration / 1000
            );
        }
        // 새 BGM 페이드 인
        // (구체적 BGM 로딩/생성 로직은 SoundLibrary 확장에 의존)
    }
}
```

**BGM 전략:**
- Phase 6의 BGM은 `SoundLibrary.js`에 프로시저럴 생성 함수로 추가하거나, 외부 오디오 파일을 `AudioBuffer`로 로드
- 각 스테이지의 `audio.bgmKey`로 식별

---

## 4. Game.js 통합 계획

### 4.1 임포트 변경

```javascript
// 제거
import { ParallaxBackground } from '../utils/ParallaxBackground.js';

// 추가
import { ParallaxSystem } from '../systems/ParallaxSystem.js';
import { ParticleSystem } from '../systems/ParticleSystem.js';
```

### 4.2 초기화 변경 (constructor)

```javascript
// 기존
this.background = null;  // → init()에서 new ParallaxBackground(this.assets)
this.particles = [];     // → 인라인 파티클 배열

// 변경
this.parallax = new ParallaxSystem(this);
this.particleSystem = new ParticleSystem(this);
```

### 4.3 update() 변경

```javascript
update(deltaTime) {
    // ... (기존 코드 유지)

    // 변경: background.update → parallax.update
    this.parallax.update(this.player.vx * bgSpeedMult, deltaTime);

    // 추가: 파티클 시스템 업데이트
    this.particleSystem.update(deltaTime);

    // 제거: 인라인 파티클 업데이트 (Game.js:412-418)
    // this.particles = this.particles.filter(p => { ... });
}
```

### 4.4 drawGame() 변경

```javascript
drawGame() {
    ctx.save();
    this.shake.apply(ctx);

    // 변경: 렌더 순서
    this.environment.drawBackground(ctx);    // 1. 배경색
    this.parallax.draw(ctx);                 // 2. 패럴랙스 레이어
    this.particleSystem.draw(ctx);           // 3. 환경 파티클 (조명 전)
    this.lighting.draw(ctx);                 // 4. 조명/어둠 오버레이

    // ... (엔티티 렌더 — 기존과 동일)

    // 변경: 인라인 파티클 → 파티클 시스템으로 이미 처리됨
    // (이펙트 파티클은 별도 레이어로 조명 위에 그려야 할 수 있음)

    this.stageManager.draw(ctx);             // 최상위: 전환 오버레이
    ctx.restore();
}
```

### 4.5 addParticles() 변경

```javascript
// 기존 (Game.js:325-336)
addParticles(x, y, color, count) {
    for (let i = 0; i < count; i++) {
        this.particles.push({ x, y, vx: ..., vy: ..., color, size: ..., life: ... });
    }
}

// 변경: ParticleSystem 위임
addParticles(x, y, color, count) {
    this.particleSystem.burst(x, y, color, count);
}
```

### 4.6 StageManager.loadStage() 변경

```javascript
loadStage(index) {
    const config = STAGES[index];

    // 기존
    this.game.environment.setAtmosphere(config);
    this.game.lighting.setAtmosphere(config.atmosphere);

    // 추가
    this.game.lighting.setAtmosphere(config.lighting);       // 확장된 조명 설정
    this.game.parallax.loadStageConfig(config.parallax);     // 스테이지별 패럴랙스
    this.game.particleSystem.clearEmitters();                 // 이전 스테이지 이미터 제거
    config.particles.emitters.forEach(e => {
        this.game.particleSystem.addEmitter(e);              // 새 이미터 등록
    });
    this.game.audio.crossfadeBgm(config.audio.bgmKey);      // BGM 크로스페이드
    this.game.audio.setReverbLevel(config.audio.reverbLevel); // 리버브 설정
}
```

---

## 5. 에셋 매니저 변경 (`src/managers/AssetManager.js`)

### 5.1 현재 에셋 목록 (18개)

```
caiso_idle, caiso_hungry, caiso_happy, caiso_sad     (4) - 스프라이트
player_idle                                           (1) - 플레이어
villager_normal, villager_scared                      (2) - NPC
food_apple ~ food_dynamite                            (6) - 아이템
title_background, bg_sky, bg_clouds, bg_city, bg_ground (5) - 배경/UI
```

### 5.2 Phase 6 에셋 목록 (예상 38개+)

```
=== 캐릭터 (7) ===
caiso_idle, caiso_hungry, caiso_happy, caiso_sad     # 리스킨 (Hollow Knight 스타일)
player_idle                                           # 작은 곤충 기사
villager_normal, villager_scared                      # Husks

=== 아이템 (6) ===
food_apple ~ food_dynamite                            # 키 유지, 이미지만 교체

=== 배경 - 스테이지별 (최대 30) ===
bg_crossroads_far, bg_crossroads_mid, bg_crossroads_near     # Stage 1
bg_greenpath_far, bg_greenpath_mid, bg_greenpath_near        # Stage 2
bg_fungal_far, bg_fungal_mid, bg_fungal_near                 # Stage 3
# ... (Stage 4-10)

=== UI (2+) ===
title_background
ui_button_feed
```

### 5.3 단계적 에셋 로딩 전략

전체 에셋을 한번에 로드하면 초기 로딩이 길어지므로, 단계적 로딩을 고려합니다:

1. **초기 로드:** 캐릭터(7) + 아이템(6) + UI(2) + Stage 1 배경(3) = **18개** (현재와 동일)
2. **지연 로드:** Stage 2-10 배경은 스테이지 진입 1단계 전에 비동기 프리로드
3. **fallback:** 에셋 미로드 시 `ParallaxSystem._drawFallback()` 사용

```javascript
// AssetManager 확장
async preloadStageAssets(stageIndex) {
    const config = STAGES[stageIndex];
    if (!config || !config.parallax) return;

    const promises = config.parallax.layers.map(layer => {
        if (this.assets[layer.key]) return Promise.resolve(); // 이미 로드됨
        return this._loadImage(layer.key, `assets/backgrounds/${layer.key}.png`);
    });

    await Promise.all(promises);
}
```

---

## 6. 디렉터리 구조 변경 요약

```
games/feeding-caiso/src/
├── config/
│   └── Stages.js              # [전면 교체] Hollow Knight 10스테이지
├── core/
│   ├── Game.js                # [수정] 새 시스템 통합
│   ├── Audio.js               # [확장] 크로스페이드, 리버브
│   ├── Environment.js         # [수정] 풍향 교대 로직
│   ├── Input.js               # [유지]
│   └── StageManager.js        # [수정] 확장된 설정 지원
├── entities/
│   ├── Caiso.js               # [수정 최소] 에셋 키 유지
│   ├── Food.js                # [유지]
│   ├── Hazard.js              # [수정] 새 장애물 타입 추가
│   ├── Player.js              # [수정 최소] 미끄러운 바닥 지원
│   └── Villager.js            # [유지]
├── generated/
│   └── SoundLibrary.js        # [수정] Hollow Knight 톤 SFX + BGM 추가
├── managers/
│   ├── AssetManager.js        # [수정] 스테이지별 에셋 목록 + 지연 로딩
│   └── UIManager.js           # [수정 최소] 색상 테마 변경
├── systems/
│   ├── LightingSystem.js      # [전면 재작성] 다이내믹 라이팅
│   ├── ParallaxSystem.js      # [신규] 스테이지별 동적 패럴랙스
│   └── ParticleSystem.js      # [신규] 오브젝트 풀링 파티클 + 이미터
└── utils/
    ├── Constants.js            # [수정] 아이템/진화 이름 리스킨
    ├── FeverMode.js            # [수정] 색상/이펙트 테마 변경
    ├── Juice.js                # [유지]
    ├── ParallaxBackground.js   # [삭제] → systems/ParallaxSystem.js로 이전
    └── SquashStretch.js        # [유지]
```

**파일 변경 요약:**
- **전면 교체/재작성:** 2개 (`Stages.js`, `LightingSystem.js`)
- **신규:** 2개 (`ParallaxSystem.js`, `ParticleSystem.js`)
- **확장:** 2개 (`Audio.js`, `AssetManager.js`)
- **수정:** 6개 (`Game.js`, `StageManager.js`, `Environment.js`, `Constants.js`, `FeverMode.js`, `Hazard.js`)
- **삭제:** 1개 (`ParallaxBackground.js`)
- **유지:** 7개 (`Input.js`, `Caiso.js`, `Food.js`, `Player.js`, `Villager.js`, `Juice.js`, `SquashStretch.js`)

---

## 7. 테스트 전략

### 7.1 기존 테스트 (`tests/test-runner.html`)

현재 15개 테스트 스위트, 60+ 테스트가 존재합니다. Phase 6 변경 후:

- **깨질 가능성이 높은 테스트:** `Stages.js` 참조 테스트, `LightingSystem` 테스트
- **안전한 테스트:** 엔티티 로직, 콤보/피버, 충돌 감지

### 7.2 Phase 6 테스트 추가 항목

| 테스트 대상 | 검증 내용 |
|:---|:---|
| `ParticleSystem` | 오브젝트 풀 정상 작동, 풀 소진 시 graceful 처리 |
| `LightingSystem` | `setAtmosphere()` 파라미터 반영, 오프스크린 캔버스 생성 |
| `ParallaxSystem` | `loadStageConfig()` 레이어 동적 생성, 래핑 동작 |
| `Stages.js` | 10개 스테이지 모두 필수 필드 존재 확인 (스키마 검증) |
| `AudioManager` | 리버브 초기화, 크로스페이드 타이밍 |

### 7.3 성능 테스트

```
Stage 10 (최악 케이스) 시뮬레이션:
- 파티클: extreme density (125/sec) → 최대 500개 동시 활성
- 장애물: infection_rain + light_beam → 최대 20개
- 조명: 높은 ambientLight + 중앙 후광 + 비네팅
- 목표: 60 FPS 유지 (mid-range 기기 기준)
```

---

## 8. 구현 순서 (Implementation Order)

Phase 6 구현은 다음 순서로 진행합니다. 각 단계는 독립적으로 테스트 가능해야 합니다.

```
Phase 6-1: 기반 시스템 (Foundation)
  ├── [6-1a] Stages.js 전면 교체 (스테이지 설정)
  ├── [6-1b] LightingSystem.js 재작성
  ├── [6-1c] ParticleSystem.js 신규 작성
  └── [6-1d] ParallaxSystem.js 리팩터링

Phase 6-2: 통합 (Integration)
  ├── [6-2a] Game.js 수정 (새 시스템 연결)
  ├── [6-2b] StageManager.js 수정 (확장된 설정 로딩)
  └── [6-2c] Environment.js 수정 (풍향 교대)

Phase 6-3: 콘텐츠 (Content)
  ├── [6-3a] 에셋 생성 (Stage 1-3 우선)
  ├── [6-3b] Constants.js 리스킨 (아이템/진화 이름)
  ├── [6-3c] FeverMode.js 테마 변경
  ├── [6-3d] Hazard.js 새 장애물 타입
  └── [6-3e] AssetManager.js 에셋 목록 업데이트

Phase 6-4: 오디오 (Audio)
  ├── [6-4a] Audio.js 확장 (리버브, 크로스페이드)
  └── [6-4b] SoundLibrary.js 사운드 리디자인

Phase 6-5: 폴리싱 (Polish)
  ├── [6-5a] 테스트 스위트 업데이트
  ├── [6-5b] 성능 최적화
  └── [6-5c] 밸런스 튜닝
```

---

*이 기술 명세는 Phase 6 엔지니어링의 청사진입니다. 모든 코드 변경은 상대 경로 임포트를 사용하고, 기존 테스트 호환성을 유지합니다.*
