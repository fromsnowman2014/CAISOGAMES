# Feeding Caiso Phase 7: 게임플레이 개선 및 안전성 강화

## 개요 (Overview)

Phase 7은 Phase 6의 비주얼 개편에 이어, **게임플레이 메카닉 개선**, **안전성 강화**, **리더보드 시스템**, **커스터마이징 기능**을 추가합니다.

전문가 분석 결과, 현재 게임은 다음과 같은 핵심 문제가 있습니다:
1. **무제한 스페이스바 스팸**: 딜레이 없이 음식을 연속으로 던질 수 있어 게임이 너무 쉽고 단순함
2. **무서운 화면 깜빡임**: 2-4초마다 검은 화면이 나타나 어린이들이 놀랄 수 있음
3. **스킬 표현 부재**: 모든 던지기가 100% 성공하여 플레이어의 실력 향상을 느낄 수 없음
4. **재플레이 동기 부족**: 최고 점수 기록 및 경쟁 요소 없음
5. **개성 표현 부재**: 플레이어가 게임을 자신만의 스타일로 커스터마이징할 수 없음

---

## 문제 분석 (Problem Analysis)

### 1. 화면 깜빡임 문제 (Critical - Safety Issue)

**현재 상태:**
- **위치**: `src/core/StageManager.js:178-181`
- **동작**: 스테이지 전환 시 전체 화면이 검은색(`rgba(0,0,0,alpha)`)으로 페이드
- **빈도**: 레벨업 시 자동으로 발생 (게임 중 2-4초마다)
- **지속시간**: 1200ms

**코드:**
```javascript
// StageManager.js:178-181
if (this.isTransitioning && this.transitionAlpha > 0) {
    ctx.fillStyle = `rgba(0, 0, 0, ${this.transitionAlpha})`;  // ❌ 검은 화면
    ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);
}
```

**왜 위험한가:**
- 어린이들에게 갑작스러운 어둠은 **공포 반응**을 유발
- 예측할 수 없는 타이밍으로 발생하여 **불안감** 조성
- 게임 컨트롤을 잃은 듯한 **무력감** 발생
- 몰입을 방해하고 **집중력 저하**

**전문가 평가:**
> "9-12세 어린이는 아직 감정 조절 능력이 발달 중입니다. 갑작스러운 전체 화면 검은색 전환은 놀람 반응을 유발하고, 게임에 대한 부정적 감정을 만들 수 있습니다. 특히 '예측할 수 없는' 타이밍이 문제입니다."

### 2. 무제한 음식 던지기 문제 (Gameplay Issue)

**현재 상태:**
- **위치**: `src/core/Game.js:172-192` (`feedCaiso()` 함수)
- **동작**: 스페이스바를 누르면 즉시 음식이 던져짐, 쿨다운 없음
- **결과**: 플레이어가 스페이스바를 연타하여 게임을 너무 쉽게 클리어

**코드:**
```javascript
// Game.js:98-101
handleKeyDown(e) {
    if (e.code === 'Space') {
        e.preventDefault();
        if (this.state === 'menu') this.startGame();
        else if (this.state === 'playing') this.feedCaiso();  // ❌ 제한 없음
    }
    // ...
}
```

**왜 문제인가:**
- **스킬 표현 부재**: 누구나 스페이스바를 빠르게 누르면 이김
- **전략 부재**: 음식 선택이나 타이밍을 고려할 필요 없음
- **지루함**: 반복적인 버튼 연타만 하면 됨
- **콤보 시스템 무의미**: 스팸으로 콤보를 쉽게 유지

**전문가 평가:**
> "현재 게임 루프는 '버튼 연타 → 승리'입니다. 플레이어의 선택이나 스킬이 결과에 영향을 주지 않습니다. 이는 처음엔 재미있지만, 곧 지루해집니다. 마스터리를 느낄 수 없기 때문입니다."

### 3. 100% 성공률 문제 (Depth Issue)

**현재 상태:**
- **위치**: `src/entities/Food.js:20-48`
- **동작**: 던진 음식은 항상 Caiso의 입에 도착 (장애물이 없으면)
- **결과**: 실패가 없어 긴장감 부재

**왜 문제인가:**
- **리스크 없음**: 모든 던지기가 무료이고 안전함
- **보상 없음**: 잘해도 못해도 결과가 같음
- **학습 부재**: 개선할 필요가 없음
- **플로우 상태 불가**: 도전과 실력의 균형이 없음

### 4. 리더보드 부재 (Engagement Issue)

**현재 상태:**
- 게임 종료 시 점수만 표시되고 기록되지 않음
- 다른 플레이어와 비교할 수 없음
- 최고 점수를 갱신하려는 동기 부족

**왜 문제인가:**
- **재플레이 동기 부족**: 한 번 클리어하면 다시 할 이유가 없음
- **사회적 요소 부재**: 친구들과 비교하거나 경쟁할 수 없음
- **성취감 제한**: 기록이 남지 않아 성장을 느끼기 어려움

### 5. 커스터마이징 부재 (Personalization Issue)

**현재 상태:**
- 모든 플레이어가 동일한 비주얼로 플레이
- 자신만의 스타일을 표현할 방법 없음
- 게이지 색상, 파티클 효과가 고정됨

**왜 문제인가:**
- **개성 표현 불가**: "내 게임"이라는 느낌이 없음
- **몰입도 감소**: 커스터마이징은 플레이어 소유감을 높임
- **리워드 시스템 부재**: 성취에 대한 보상으로 스킨을 언락하는 등의 요소 없음

---

## 해결 방안 (Solutions)

### 해결책 1: 화면 깜빡임 완전 제거 ⭐ **최우선**

#### 옵션 A: 반짝이 효과 전환 (추천)

**설명:** 검은색 페이드 대신, 마법같은 반짝이(sparkle) 효과로 스테이지 전환을 표현

**구현:**
```javascript
// StageManager.js:178-181 교체
if (this.isTransitioning && this.transitionAlpha > 0) {
    const progress = this.transitionTimer / this.transitionDuration;

    ctx.save();
    // 중앙에서 퍼져나가는 반짝이 파티클
    for (let i = 0; i < 25; i++) {
        const angle = (i / 25) * Math.PI * 2 + progress * Math.PI * 0.5;
        const distance = progress * 450;
        const x = GAME_CONFIG.WIDTH / 2 + Math.cos(angle) * distance;
        const y = GAME_CONFIG.HEIGHT / 2 + Math.sin(angle) * distance;

        // Soul Blue와 Void Purple 교차
        ctx.fillStyle = i % 2 === 0 ? '#74b9ff' : '#a29bfe';
        ctx.globalAlpha = (1 - progress) * this.transitionAlpha * 0.5;

        const size = 3 + Math.sin(progress * Math.PI * 2 + i) * 2;
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
    }
    ctx.restore();
}
```

**장점:**
- ✅ 어린이들이 좋아하는 "마법" 느낌
- ✅ 화면이 완전히 가려지지 않음
- ✅ 진행 상황을 축하하는 느낌
- ✅ 무섭지 않고 흥미로움

**추가 개선사항:**
- 전환 시간 단축: `1200ms → 600ms` (Line 12)
- 전환 알파 최대값 감소: `1.0 → 0.3`
- 축하 파티클 추가: 스테이지 변경 시 중앙에서 파티클 버스트

---

### 해결책 2: 타이밍 기반 던지기 시스템 도입

#### 핵심 컨셉

**기존:**
```
스페이스 누름 → 음식 던짐 → 100% 성공
```

**신규:**
```
스페이스 누름 → 타이밍 체크 → Perfect/Good/Miss
                        ↓
                Perfect: 보너스 점수, 콤보 유지
                Good: 정상 점수, 콤보 유지
                Miss: 점수 없음, 콤보 끊김, 음식이 Caiso에 도달 못함
```

#### 타이밍 게이지 디자인

**원형 게이지 방식 (추천):**

```
        [Perfect Zone]
           ░░░▓▓▓░░░  ← 초록색 (±12°, Stage 1-2)
         ░░         ░░
        ▒▒           ▒▒ ← 노란색 (Good Zone)
       ▒               ▒
      ▒    ┌───────┐   ▒
     ▒     │       │    ▒
     ▒     │   ●───→   ▒ ← 회전하는 바늘
     ▒     │ Caiso │    ▒
      ▒    └───────┘   ▒
       ▒               ▒
        ▓▓           ▓▓ ← 빨간색 (Miss Zone)
         ▓▓         ▓▓
           ▓▓▓▓▓▓▓▓▓

위치: 화면 하단 중앙, FEED 버튼 위
크기: 반지름 50px
```

**게이지 사양:**
- **위치**: `{ x: GAME_CONFIG.WIDTH / 2, y: GAME_CONFIG.HEIGHT - 100 }`
- **Perfect Zone**: ±8° (초록색), 완벽한 타이밍
- **Good Zone**: ±18° (노란색), 괜찮은 타이밍
- **Miss Zone**: 나머지 (빨간색 배경)
- **회전 속도**: 180°/초 (기본), 난이도에 따라 증가

#### 난이도 조절

**스테이지별 속도 및 윈도우 크기:**

| Stage | Speed Mult | Perfect Window | Good Window | 설명 |
|-------|------------|----------------|-------------|------|
| 1-2 | 1.0x | ±12° (300ms) | ±25° | 튜토리얼, 매우 관대 |
| 3-4 | 1.2x | ±10° (250ms) | ±20° | 편안한 도전 |
| 5-7 | 1.5x | ±8° (200ms) | ±16° | 집중 필요 |
| 8-9 | 2.0x | ±6° (150ms) | ±12° | 숙련 필요 |
| 10 | 2.5x | ±5° (125ms) | ±10° | 전문가 |

#### 피드백 시스템

**시각적 피드백:**

| 결과 | 화면 효과 | 파티클 | 게이지 애니메이션 |
|------|-----------|--------|------------------|
| **Perfect** | 하얀 플래시 (0.1초, 30% 불투명) | 15개 파란/흰색 파티클 | 펄스 (1.0→1.2→1.0) |
| **Good** | 노란 글로우 | 8개 노란 파티클 | 미세한 노란 빛 |
| **Miss** | 빨간 테두리 플래ش | 회색 파티클 | 가로 흔들림 (6px) |

---

### 해결책 3: 리더보드 시스템 ⭐ **신규 기능**

#### 디자인 철학

**Hollow Knight 테마에 맞는 모던하고 대기적인 리더보드:**
- 고대 유물에 새겨진 기록처럼 보이게
- Soul Blue와 Void Purple 컬러 팔레트 사용
- 글래스모피즘 스타일로 현대적이면서도 게임 분위기 유지

#### UI 디자인

**리더보드 화면 구조:**

```
┌─────────────────────────────────────┐
│     HALL OF SOULS                   │  ← 타이틀 (Fredoka One)
│     ═══════════════                 │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 👑 1. KNIGHT    12,850 pts  │   │  ← 1위 (금색 글로우)
│  │    Perfect: 45  Stage: 10   │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 🥈 2. SHADE     11,200 pts  │   │  ← 2위 (은색)
│  │    Perfect: 38  Stage: 9    │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 🥉 3. VESSEL     9,750 pts  │   │  ← 3위 (동색)
│  │    Perfect: 32  Stage: 8    │   │
│  └─────────────────────────────┘   │
│                                     │
│  ...                                │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 📍 10. YOU       8,540 pts  │   │  ← 플레이어 (강조)
│  │     Perfect: 28  Stage: 7   │   │
│  └─────────────────────────────┘   │
│                                     │
│     [PLAY AGAIN]  [BACK TO HUB]    │
└─────────────────────────────────────┘
```

**비주얼 스타일:**
```javascript
const LEADERBOARD_STYLE = {
    // 배경
    background: 'linear-gradient(180deg, #0f0f1b 0%, #1a1a2e 100%)',

    // 제목
    title: {
        font: 'bold 32px Fredoka One',
        color: '#dfe6e9',
        shadowColor: 'rgba(116, 185, 255, 0.6)',
        shadowBlur: 20
    },

    // 엔트리 카드 (글래스모피즘)
    entryCard: {
        background: 'rgba(15, 15, 27, 0.6)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(116, 185, 255, 0.3)',
        borderRadius: 12,
        padding: '12px 16px',
        shadow: '0 4px 12px rgba(0, 0, 0, 0.3)'
    },

    // 랭크별 색상
    ranks: {
        1: { emoji: '👑', color: '#ffd700', glow: 'rgba(255, 215, 0, 0.4)' },
        2: { emoji: '🥈', color: '#c0c0c0', glow: 'rgba(192, 192, 192, 0.3)' },
        3: { emoji: '🥉', color: '#cd7f32', glow: 'rgba(205, 127, 50, 0.3)' },
        other: { emoji: '', color: '#b2bec3', glow: null }
    },

    // 현재 플레이어 강조
    currentPlayer: {
        background: 'rgba(116, 185, 255, 0.15)',
        border: '2px solid #74b9ff',
        glow: '0 0 15px rgba(116, 185, 255, 0.5)',
        emoji: '📍'
    }
};
```

#### 이름 입력 모달

**게임 종료 시 나타나는 이름 입력 화면:**

```
┌─────────────────────────────────────┐
│                                     │
│         🏆 NEW HIGH SCORE! 🏆       │
│                                     │
│           Score: 12,850             │
│                                     │
│   ┌───────────────────────────┐    │
│   │ Enter your name:          │    │
│   │                           │    │
│   │  ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂        │    │  ← 입력 필드
│   │  K N I G H T ▊            │    │
│   │  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔        │    │
│   │                           │    │
│   │  Max 12 characters        │    │
│   └───────────────────────────┘    │
│                                     │
│         [SUBMIT]  [SKIP]            │
│                                     │
└─────────────────────────────────────┘
```

**입력 스타일:**
```javascript
const NAME_INPUT_STYLE = {
    // 모달 배경
    overlay: 'rgba(0, 0, 0, 0.8)',

    // 모달 박스
    modal: {
        background: 'linear-gradient(135deg, #0f0f1b, #1a1a2e)',
        border: '2px solid rgba(116, 185, 255, 0.5)',
        borderRadius: 16,
        width: 360,
        padding: 24,
        shadow: '0 10px 40px rgba(0, 0, 0, 0.6)'
    },

    // 입력 필드
    input: {
        background: 'rgba(15, 15, 27, 0.8)',
        border: '2px solid rgba(116, 185, 255, 0.4)',
        borderFocus: '2px solid #74b9ff',
        borderRadius: 8,
        color: '#dfe6e9',
        font: 'bold 24px Fredoka One',
        textAlign: 'center',
        padding: '12px 16px',
        letterSpacing: '2px',
        caretColor: '#74b9ff'
    },

    // 버튼
    button: {
        background: 'linear-gradient(135deg, #74b9ff, #a29bfe)',
        color: '#dfe6e9',
        font: 'bold 18px Fredoka One',
        padding: '10px 24px',
        borderRadius: 8,
        hover: 'linear-gradient(135deg, #5fa8ff, #8d7fe6)',
        shadow: '0 4px 12px rgba(116, 185, 255, 0.3)'
    }
};
```

#### 데이터 저장 (LocalStorage)

**리더보드 데이터 구조:**
```javascript
// LocalStorage 키: 'feedingCaiso_leaderboard'
{
    version: 1,
    entries: [
        {
            id: 'uuid-1',
            name: 'KNIGHT',
            score: 12850,
            level: 25,
            stage: 10,
            perfectCount: 45,
            maxCombo: 18,
            evolution: 'Shade Lord',
            timestamp: 1708000000000,
            timePlayed: 245000  // ms
        },
        // ... 최대 50개 엔트리
    ]
}
```

**저장 및 불러오기:**
```javascript
// src/managers/LeaderboardManager.js
export class LeaderboardManager {
    constructor() {
        this.maxEntries = 50;
        this.storageKey = 'feedingCaiso_leaderboard';
        this.entries = this.load();
    }

    load() {
        try {
            const data = localStorage.getItem(this.storageKey);
            if (!data) return [];
            const parsed = JSON.parse(data);
            return parsed.entries || [];
        } catch (err) {
            console.error('Failed to load leaderboard:', err);
            return [];
        }
    }

    save() {
        try {
            const data = {
                version: 1,
                entries: this.entries.slice(0, this.maxEntries)
            };
            localStorage.setItem(this.storageKey, JSON.stringify(data));
        } catch (err) {
            console.error('Failed to save leaderboard:', err);
        }
    }

    addEntry(entry) {
        // UUID 생성
        entry.id = this.generateUUID();

        // 엔트리 추가
        this.entries.push(entry);

        // 점수 순으로 정렬
        this.entries.sort((a, b) => b.score - a.score);

        // 최대 개수 제한
        this.entries = this.entries.slice(0, this.maxEntries);

        // 저장
        this.save();

        // 랭크 반환 (1부터 시작)
        return this.entries.findIndex(e => e.id === entry.id) + 1;
    }

    getRank(score) {
        // 이 점수가 몇 위인지 반환
        const higherScores = this.entries.filter(e => e.score > score).length;
        return higherScores + 1;
    }

    isNewHighScore(score) {
        if (this.entries.length < this.maxEntries) return true;
        return score > this.entries[this.entries.length - 1].score;
    }

    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
}
```

---

### 해결책 4: 커스터마이징 시스템 ⭐ **신규 기능**

#### 디자인 철학

**Phase 6 Hollow Knight 테마에 완벽히 통합:**
- 모든 커스터마이징 옵션이 게임 세계관 내에서 의미를 가짐
- "영혼의 색상", "가면 스타일" 등 테마에 맞는 용어 사용
- 언락 조건이 게임 진행과 자연스럽게 연결

#### 커스터마이징 카테고리

**1. 타이밍 게이지 스킨 (Gauge Themes)**

```javascript
const GAUGE_THEMES = {
    // 기본 (처음부터 사용 가능)
    soul: {
        name: 'Soul Essence',
        nameKo: '영혼의 정수',
        colors: {
            perfect: '#74b9ff',    // Soul Blue
            good: '#ffd93d',       // Bright Yellow
            miss: '#636e72',       // Dark Gray
            needle: '#dfe6e9',     // Pale White
            glow: '#74b9ff'
        },
        unlock: 'default'
    },

    // 언락 가능 테마들
    void: {
        name: 'Void Abyss',
        nameKo: '공허의 심연',
        colors: {
            perfect: '#a29bfe',    // Void Purple
            good: '#6c5ce7',       // Deep Purple
            miss: '#2d3436',       // Void Black
            needle: '#dfe6e9',
            glow: '#a29bfe'
        },
        unlock: 'reach_stage_8'
    },

    infection: {
        name: 'Radiant Infection',
        nameKo: '광휘의 감염',
        colors: {
            perfect: '#ff9500',    // Infection Orange
            good: '#ffd93d',
            miss: '#ff7675',       // Red
            needle: '#fff',
            glow: '#ff9500'
        },
        unlock: 'reach_stage_10'
    },

    crystal: {
        name: 'Crystal Resonance',
        nameKo: '수정의 울림',
        colors: {
            perfect: '#e694ff',    // Crystal Pink
            good: '#74b9ff',
            miss: '#b2bec3',
            needle: '#fff',
            glow: '#e694ff'
        },
        unlock: 'perfect_streak_10'
    },

    greenpath: {
        name: 'Greenpath Bloom',
        nameKo: '녹색 거리의 꽃',
        colors: {
            perfect: '#00b894',    // Green
            good: '#55efc4',
            miss: '#2d3436',
            needle: '#dfe6e9',
            glow: '#00b894'
        },
        unlock: 'reach_stage_3'
    },

    pale: {
        name: 'Pale King\'s Legacy',
        nameKo: '창백한 왕의 유산',
        colors: {
            perfect: '#dfe6e9',    // Pure White
            good: '#b2bec3',
            miss: '#636e72',
            needle: '#fff',
            glow: '#dfe6e9'
        },
        unlock: 'reach_stage_9'
    }
};
```

**2. 파티클 이펙트 (Particle Effects)**

```javascript
const PARTICLE_EFFECTS = {
    // 기본
    souls: {
        name: 'Soul Orbs',
        nameKo: '영혼 구슬',
        shape: 'circle',
        colors: ['#74b9ff', '#a29bfe', '#dfe6e9'],
        size: [3, 8],
        trail: false,
        unlock: 'default'
    },

    fireflies: {
        name: 'Lumaflies',
        nameKo: '빛나는 파리',
        shape: 'circle',
        colors: ['#ffd93d', '#ff9500'],
        size: [2, 5],
        trail: true,
        glow: true,
        unlock: 'combo_50'
    },

    crystals: {
        name: 'Crystal Shards',
        nameKo: '수정 파편',
        shape: 'diamond',
        colors: ['#e694ff', '#a29bfe'],
        size: [4, 10],
        sparkle: true,
        unlock: 'reach_stage_5'
    },

    infection: {
        name: 'Infection Spores',
        nameKo: '감염 포자',
        shape: 'circle',
        colors: ['#ff9500', '#ff7675'],
        size: [2, 6],
        pulse: true,
        unlock: 'reach_stage_10'
    },

    void: {
        name: 'Void Essence',
        nameKo: '공허의 정수',
        shape: 'circle',
        colors: ['#2d3436', '#636e72', '#0f0f1b'],
        size: [3, 9],
        fade: 'slow',
        unlock: 'evolution_4'
    },

    petals: {
        name: 'White Petals',
        nameKo: '하얀 꽃잎',
        shape: 'petal',
        colors: ['#dfe6e9', '#b2bec3'],
        size: [4, 8],
        rotation: true,
        unlock: 'reach_stage_9'
    }
};
```

**3. 승리 애니메이션 (Victory Animations)**

```javascript
const VICTORY_ANIMATIONS = {
    default: {
        name: 'Soul Ascension',
        nameKo: '영혼의 상승',
        effect: 'particles_rise',
        color: '#74b9ff',
        unlock: 'default'
    },

    radiance: {
        name: 'Radiant Burst',
        nameKo: '광휘의 폭발',
        effect: 'explosion',
        color: '#ff9500',
        unlock: 'victory_stage_10'
    },

    voidHeart: {
        name: 'Void Heart',
        nameKo: '공허의 심장',
        effect: 'spiral_black',
        color: '#0f0f1b',
        unlock: 'evolution_4'
    }
};
```

#### 커스터마이징 UI

**설정 화면 레이아웃:**

```
┌─────────────────────────────────────┐
│   [←] CUSTOMIZATION                 │
│                                     │
│   ┌─ Timing Gauge Theme ─────┐    │
│   │                           │    │
│   │  [●] Soul Essence         │    │  ← 선택됨
│   │  [ ] Void Abyss    🔒     │    │  ← 잠김
│   │  [ ] Crystal       🔒     │    │
│   │  [ ] Infection     🔒     │    │
│   └───────────────────────────┘    │
│                                     │
│   ┌─ Particle Effects ───────┐    │
│   │                           │    │
│   │  [●] Soul Orbs            │    │
│   │  [ ] Lumaflies     🔒     │    │
│   │  [ ] Crystals      🔒     │    │
│   └───────────────────────────┘    │
│                                     │
│   ┌─ Victory Animation ──────┐    │
│   │                           │    │
│   │  [●] Soul Ascension       │    │
│   │  [ ] Radiant Burst 🔒     │    │
│   └───────────────────────────┘    │
│                                     │
│   ┌─ Preview ──────────────────┐   │
│   │                            │   │
│   │      [실시간 미리보기]      │   │  ← 선택한 테마로 게이지 표시
│   │                            │   │
│   └────────────────────────────┘   │
│                                     │
│         [SAVE]  [RESET]             │
└─────────────────────────────────────┘
```

**언락 툴팁:**
```
┌──────────────────────────┐
│ 🔒 Void Abyss            │
│                          │
│ Reach Stage 8 to unlock  │
│ Progress: Stage 5 / 8    │
│                          │
│ ░░░░░░░░░░▓▓▓▓▓▓         │  ← 진행 바
│         62%              │
└──────────────────────────┘
```

#### 언락 조건

**진행 기반 언락:**
```javascript
const UNLOCK_CONDITIONS = {
    // 스테이지 도달
    reach_stage_3: {
        check: (game) => game.stageManager.currentStageIndex >= 2,
        description: 'Reach Stage 3',
        descriptionKo: 'Stage 3 도달'
    },
    reach_stage_5: {
        check: (game) => game.stageManager.currentStageIndex >= 4,
        description: 'Reach Stage 5',
        descriptionKo: 'Stage 5 도달'
    },
    reach_stage_8: {
        check: (game) => game.stageManager.currentStageIndex >= 7,
        description: 'Reach Stage 8',
        descriptionKo: 'Stage 8 도달'
    },
    reach_stage_9: {
        check: (game) => game.stageManager.currentStageIndex >= 8,
        description: 'Reach Stage 9 (White Palace)',
        descriptionKo: 'Stage 9 도달 (백색 궁전)'
    },
    reach_stage_10: {
        check: (game) => game.stageManager.currentStageIndex >= 9,
        description: 'Reach Stage 10 (Radiance)',
        descriptionKo: 'Stage 10 도달 (광휘)'
    },

    // 승리 조건
    victory_stage_10: {
        check: (saves) => saves.highestStageVictory >= 10,
        description: 'Win the game by reaching Stage 10',
        descriptionKo: 'Stage 10까지 도달하여 승리'
    },

    // 진화 조건
    evolution_4: {
        check: (game) => game.caiso.evolutionTier >= 3,  // Shade Lord
        description: 'Evolve Caiso to Shade Lord',
        descriptionKo: 'Caiso를 Shade Lord로 진화'
    },

    // 스킬 기반
    perfect_streak_10: {
        check: (game) => game.maxPerfectStreak >= 10,
        description: 'Achieve 10 Perfect hits in a row',
        descriptionKo: '10회 연속 Perfect 달성'
    },
    combo_50: {
        check: (game) => game.maxCombo >= 50,
        description: 'Reach 50x combo',
        descriptionKo: '50 콤보 달성'
    }
};
```

#### 데이터 저장

**커스터마이징 설정 저장:**
```javascript
// LocalStorage 키: 'feedingCaiso_customization'
{
    version: 1,
    selected: {
        gaugeTheme: 'soul',
        particleEffect: 'souls',
        victoryAnimation: 'default'
    },
    unlocked: [
        'soul',           // 기본
        'souls',          // 기본
        'default',        // 기본
        'greenpath',      // 언락됨
        'fireflies'       // 언락됨
    ],
    progress: {
        maxStage: 5,
        maxCombo: 35,
        maxPerfectStreak: 7,
        evolutionTier: 2,
        highestStageVictory: 5
    }
}
```

---

## 구현 로드맵 (Implementation Roadmap)

### Phase 7.1: 안전성 패치 (최우선) ⚠️

**목표:** 어린이 안전을 위해 화면 깜빡임 즉시 제거

**작업:**
1. ✅ `StageManager.js:179` 수정
   - `rgba(0,0,0,alpha)` → 반짝이 효과
2. ✅ `StageManager.js:12` 수정
   - `transitionDuration: 1200` → `600`
3. ✅ 최대 불투명도 제한
   - `transitionAlpha` 최대값 0.3으로 제한
4. ✅ 테스트: 어린이와 함께 플레이하여 불안감 확인

**예상 소요 시간:** 1-2시간

**파일:**
- `src/core/StageManager.js` (10줄 수정)

---

### Phase 7.2: 스페이스바 제한 (버그 수정)

**목표:** 한 번 누르면 한 개만 던지도록 수정

**작업:**
1. ✅ `Game.js`에 `spacePressed` 상태 추가
2. ✅ `keyup` 이벤트 리스너 추가
3. ✅ `feedCaiso()` 중복 호출 방지 로직
4. ✅ 터치 버튼도 동일하게 적용

**예상 소요 시간:** 30분

**파일:**
- `src/core/Game.js` (15줄 추가)

---

### Phase 7.3: 타이밍 시스템 MVP (핵심 기능)

**목표:** 타이밍 게이지 기본 기능 구현

**작업:**
1. ✅ `src/utils/TimingGauge.js` 신규 생성
   - 원형 게이지 렌더링
   - 회전하는 바늘 애니메이션
   - 타이밍 윈도우 체크 메서드
2. ✅ `Game.js`에 통합
   - `this.timingGauge` 인스턴스 생성
   - `feedCaiso()` 수정: 타이밍 체크 추가
   - 화면 하단에 게이지 렌더링
3. ✅ 3가지 결과 처리
   - Perfect/Good/Miss 판정
   - 간단한 색상 플래시 피드백
   - 음식 궤적 변경 (Miss 시 짧게)

**예상 소요 시간:** 4-6시간

**파일:**
- `src/utils/TimingGauge.js` (신규, ~200줄)
- `src/core/Game.js` (50줄 수정)
- `src/entities/Food.js` (20줄 수정)

---

### Phase 7.4: 리더보드 시스템 구현 ⭐

**목표:** 점수 기록 및 순위 시스템 구축

**작업:**
1. ✅ `src/managers/LeaderboardManager.js` 신규 생성
   - LocalStorage 저장/불러오기
   - 엔트리 추가 및 정렬
   - 랭크 계산
2. ✅ 이름 입력 모달 UI
   - 게임 종료 시 표시
   - 입력 필드 및 검증
   - Hollow Knight 테마 디자인
3. ✅ 리더보드 화면
   - 상위 10개 엔트리 표시
   - 현재 플레이어 강조
   - 순위별 아이콘 및 색상
4. ✅ Game.js 통합
   - 게임 종료 시 리더보드 체크
   - 하이스코어 시 이름 입력 프롬프트

**예상 소요 시간:** 6-8시간

**파일:**
- `src/managers/LeaderboardManager.js` (신규, ~250줄)
- `src/screens/NameInputScreen.js` (신규, ~180줄)
- `src/screens/LeaderboardScreen.js` (신규, ~220줄)
- `src/core/Game.js` (통합, 40줄 추가)

---

### Phase 7.5: 커스터마이징 시스템 구현 ⭐

**목표:** 게이지, 파티클, 애니메이션 커스터마이징

**작업:**
1. ✅ `src/managers/CustomizationManager.js` 신규 생성
   - 테마 데이터 관리
   - 언락 조건 체크
   - LocalStorage 저장/불러오기
2. ✅ 커스터마이징 화면 UI
   - 카테고리별 옵션 표시
   - 실시간 미리보기
   - 언락 진행 상황
3. ✅ TimingGauge에 테마 적용
   - 색상 변경 시스템
   - 테마별 시각 효과
4. ✅ ParticleSystem에 이펙트 적용
   - 파티클 모양/색상 변경
   - 특수 효과 (글로우, 궤적 등)
5. ✅ 승리 화면 애니메이션
   - 테마별 다른 효과

**예상 소요 시간:** 8-10시간

**파일:**
- `src/managers/CustomizationManager.js` (신규, ~300줄)
- `src/screens/CustomizationScreen.js` (신규, ~280줄)
- `src/utils/TimingGauge.js` (테마 지원, 50줄 추가)
- `src/systems/ParticleSystem.js` (이펙트 지원, 60줄 추가)
- `src/core/Game.js` (통합, 30줄 추가)

---

### Phase 7.6: 피드백 시스템 (Juice)

**목표:** 타이밍 결과에 대한 만족스러운 피드백 추가

**작업:**
1. ✅ 시각 효과
   - Perfect: 화면 플래시, 파티클 버스트, 게이지 펄스
   - Good: 노란 글로우
   - Miss: 빨간 테두리, 흔들림
2. ✅ 오디오 효과
   - `SoundLibrary.js`에 3가지 사운드 추가
3. ✅ 텍스트 표시

**예상 소요 시간:** 3-4시간

**파일:**
- `src/utils/TimingGauge.js` (50줄 추가)
- `src/generated/SoundLibrary.js` (30줄 추가)

---

### Phase 7.7: 테스트 및 조정

**목표:** 실제 플레이 테스트 및 밸런스 조정

**작업:**
1. ✅ 내부 테스트
2. ✅ 사용자 테스트 (어린이 5-7명)
3. ✅ 밸런스 조정

**예상 소요 시간:** 4-6시간

---

## 상세 구현 가이드

### LeaderboardManager.js 구조

```javascript
// src/managers/LeaderboardManager.js
export class LeaderboardManager {
    constructor() {
        this.maxEntries = 50;
        this.storageKey = 'feedingCaiso_leaderboard';
        this.entries = this.load();
    }

    load() {
        try {
            const data = localStorage.getItem(this.storageKey);
            if (!data) return [];
            const parsed = JSON.parse(data);
            return parsed.entries || [];
        } catch (err) {
            console.error('Failed to load leaderboard:', err);
            return [];
        }
    }

    save() {
        try {
            const data = {
                version: 1,
                entries: this.entries.slice(0, this.maxEntries)
            };
            localStorage.setItem(this.storageKey, JSON.stringify(data));
        } catch (err) {
            console.error('Failed to save leaderboard:', err);
        }
    }

    addEntry(entry) {
        entry.id = this.generateUUID();
        this.entries.push(entry);
        this.entries.sort((a, b) => b.score - a.score);
        this.entries = this.entries.slice(0, this.maxEntries);
        this.save();
        return this.entries.findIndex(e => e.id === entry.id) + 1;
    }

    getRank(score) {
        const higherScores = this.entries.filter(e => e.score > score).length;
        return higherScores + 1;
    }

    isNewHighScore(score) {
        if (this.entries.length < this.maxEntries) return true;
        return score > this.entries[this.entries.length - 1].score;
    }

    getTopEntries(count = 10) {
        return this.entries.slice(0, count);
    }

    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
}
```

### CustomizationManager.js 구조

```javascript
// src/managers/CustomizationManager.js
import { GAUGE_THEMES, PARTICLE_EFFECTS, VICTORY_ANIMATIONS, UNLOCK_CONDITIONS } from '../config/Customization.js';

export class CustomizationManager {
    constructor() {
        this.storageKey = 'feedingCaiso_customization';
        this.data = this.load();
    }

    load() {
        try {
            const data = localStorage.getItem(this.storageKey);
            if (!data) return this.getDefaultData();
            return JSON.parse(data);
        } catch (err) {
            console.error('Failed to load customization:', err);
            return this.getDefaultData();
        }
    }

    getDefaultData() {
        return {
            version: 1,
            selected: {
                gaugeTheme: 'soul',
                particleEffect: 'souls',
                victoryAnimation: 'default'
            },
            unlocked: ['soul', 'souls', 'default'],
            progress: {
                maxStage: 0,
                maxCombo: 0,
                maxPerfectStreak: 0,
                evolutionTier: 0,
                highestStageVictory: 0
            }
        };
    }

    save() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.data));
        } catch (err) {
            console.error('Failed to save customization:', err);
        }
    }

    updateProgress(game) {
        let changed = false;

        if (game.stageManager.currentStageIndex > this.data.progress.maxStage) {
            this.data.progress.maxStage = game.stageManager.currentStageIndex;
            changed = true;
        }
        if (game.maxCombo > this.data.progress.maxCombo) {
            this.data.progress.maxCombo = game.maxCombo;
            changed = true;
        }
        if (game.maxPerfectStreak > this.data.progress.maxPerfectStreak) {
            this.data.progress.maxPerfectStreak = game.maxPerfectStreak;
            changed = true;
        }
        if (game.caiso.evolutionTier > this.data.progress.evolutionTier) {
            this.data.progress.evolutionTier = game.caiso.evolutionTier;
            changed = true;
        }

        if (changed) {
            this.checkUnlocks(game);
            this.save();
        }
    }

    checkUnlocks(game) {
        // 모든 테마/효과의 언락 조건 체크
        const allItems = [
            ...Object.entries(GAUGE_THEMES),
            ...Object.entries(PARTICLE_EFFECTS),
            ...Object.entries(VICTORY_ANIMATIONS)
        ];

        allItems.forEach(([key, item]) => {
            if (this.data.unlocked.includes(key)) return;  // 이미 언락됨

            const condition = UNLOCK_CONDITIONS[item.unlock];
            if (!condition) return;

            if (condition.check(game, this.data.progress)) {
                this.unlock(key);
            }
        });
    }

    unlock(itemKey) {
        if (!this.data.unlocked.includes(itemKey)) {
            this.data.unlocked.push(itemKey);
            this.save();
            return true;  // 새로 언락됨
        }
        return false;
    }

    isUnlocked(itemKey) {
        return this.data.unlocked.includes(itemKey);
    }

    select(category, itemKey) {
        if (!this.isUnlocked(itemKey)) return false;
        this.data.selected[category] = itemKey;
        this.save();
        return true;
    }

    getSelected(category) {
        return this.data.selected[category];
    }

    getUnlockProgress(unlockCondition) {
        const condition = UNLOCK_CONDITIONS[unlockCondition];
        if (!condition) return { current: 0, required: 0, percent: 0 };

        // 진행률 계산 (조건별 구현 필요)
        return condition.getProgress(this.data.progress);
    }
}
```

---

## 예상 효과

### 게임플레이 개선
- ✅ **스킬 표현**: 플레이어의 실력이 결과에 영향을 미침
- ✅ **재미 증가**: Perfect를 맞추는 만족감
- ✅ **반복성**: 더 나은 기록을 위해 다시 플레이
- ✅ **난이도 곡선**: 점진적으로 어려워지는 도전

### 안전성 강화
- ✅ **공포 제거**: 검은 화면 깜빡임 완전 제거
- ✅ **부드러운 전환**: 자연스럽고 예쁜 스테이지 전환
- ✅ **긍정적 경험**: 어린이들이 안심하고 플레이

### 사회적 요소
- ✅ **경쟁 동기**: 리더보드에서 친구들과 순위 경쟁
- ✅ **성취 기록**: 최고 점수가 영구히 저장됨
- ✅ **자랑할 거리**: 이름과 함께 기록되어 공유 가능

### 개인화
- ✅ **소유감**: "내 스타일"로 커스터마이징
- ✅ **언락 동기**: 새 테마를 얻기 위해 도전
- ✅ **표현**: 개성을 게임에 반영

### 교육적 가치
- ✅ **타이밍 훈련**: 손과 눈의 협응력 향상
- ✅ **집중력**: 타이밍에 집중하는 연습
- ✅ **성취감**: 점진적 난이도로 성장 경험

---

## 다음 단계 (Phase 8 이후)

Phase 7 완료 후 고려할 수 있는 추가 개선:

1. **온라인 리더보드**: Firebase 연동하여 글로벌 순위
2. **멀티플레이어 모드**: 친구와 함께 타이밍 맞추기
3. **일일 도전**: 매일 바뀌는 특별 조건
4. **모바일 최적화**: 터치 입력 정밀도 향상
5. **더 많은 음식**: 각각 다른 타이밍 효과
6. **보스 스테이지**: 특별한 타이밍 패턴
7. **업적 시스템**: 특정 조건 달성 시 배지 획득
8. **공유 기능**: 리더보드 스크린샷 공유

---

**작성일**: 2026-02-14
**버전**: Phase 7 v1.0
**작성자**: UX Researcher + Play Agent 분석 기반
