# 🎮 Feeding Caiso Phase 4: "Fever & Polish" Master Plan

> **Objective**: Transform `Feeding Caiso` from a functional prototype into a polished, mobile-ready arcade game with "Juicy" game feel, coherent aesthetics, and robust code architecture.
> **Target Audience**: Casual Mobile Gamers (10-30m sessions)
> **Key Metric**: Retention (Replayability) & Visual Satisfaction

---

## 1. 🎯 Analysis & Improvement Targets

| Category | Current State | Target State (Phase 4) | Responsible Agent |
|----------|---------------|------------------------|-------------------|
| **Graphics** | 혼합된 에셋 (기본 도형 + 일부 스프라이트). 스타일 불일치. | **"Neon Kawaii"**: 통일된 색감, 글로우 효과, 고해상도 일관된 스프라이트. | `Image Agent` |
| **Gameplay** | 단순 반복. 피드백(Juice) 부족. 난이도 곡선이 단순함. | **"Juicy Arcade"**: 타격감(Screen Shake), 시각적 피드백 강화, 다이나믹한 난이도 조절. | `Design Agent` |
| **Audio** | 기본 Oscillator 사운드. 배경음악 부재. | **"Adaptive Audio"**: 상황에 따라 변하는 BGM, 풍부한 SFX (타격, 피버, UI). | `Sound Agent` |
| **Code** | 단일 파일(`index.html`)에 1800라인 집중. 유지보수 어려움. | **"Modular Architecture"**: 클래스 분리, 상태 관리 패턴 도입, 성능 최적화. | `Code Agent` |
| **QA/UX** | 기본 터치 지원. 일부 UI 겹침. | **"Polished UX"**: 완벽한 모바일 대응, 튜토리얼, 버그 없는 경험. | `Play Agent` |

---

## 2. 🗓️ Execution Roadmap

### Step 1: Design & Asset Production (The Visual Upgrade)
- **Goal**: 교체 가능한 모든 그래픽/오디오 에셋을 확정하고 생성.
- **Actions**:
  1. `Design Agent`: "Neon Kawaii" 스타일 가이드 확정 및 상세 기획서 작성.
  2. `Image Agent`: 배경(Parallax), 캐릭터(5단계 진화), 아이템, UI 에셋 일괄 생성.
  3. **Crucial**: "Pixel Art" 대신 "Vector/Cell Shaded" 스타일로 변경하여 현대적인 느낌 부여 고려.

### Step 2: Core Gameplay Loop "Juice" Up (The Feel)
- **Goal**: 조작감과 피드백을 극대화.
- **Actions**:
  1. **Squash & Stretch**: 현재 구현을 더 과장되게 튜닝.
  2. **Particles**: 피버 모드, 먹기, 레벨업 시 파티클 폭발 효과 강화.
  3. **Screen Shake**: 데미지 입거나 피버 발동 시 화면 흔들림 추가.
  4. **Hit Stop**: 중요한 순간(레벨업)에 0.1초 멈춤 효과로 임팩트 강화.

### Step 3: Technical Refactoring (The Foundation)
- **Goal**: 안정적이고 확장 가능한 코드베이스 구축.
- **Actions**:
  1. `Code Agent`: `index.html`을 `src/` 디렉토리로 분리 (ES Modules 도입 검토).
  2. **Performance**: 객체 풀링(Object Pooling) 도입으로 가비지 컬렉션 최소화 (Code Agent 리포트 반영).
  3. **State Management**: 게임 상태(Menu -> Play -> Fever -> Over)를 명확한 FSM(Create State Machine)으로 리팩토링.

### Step 4: Audio Immersion (The Vibe)
- **Goal**: 청각적 피드백으로 몰입감 증대.
- **Actions**:
  1. `Sound Agent`: Web Audio API Oscillator 대신 생성된 고품질 MP3/WAV 에셋 사용.
  2. **Adaptive BGM**: 일반 상태 vs 피버 상태 BGM 크로스페이드 구현.

---

## 3. 📂 Documentation Structure

본 폴더(`docs/phase4/`)에 저장될 상세 계획 문서:

1. `PHASE4_DESIGN_DOC.md`: 상세 기획서 (밸런스, 피버 역학, UI/UX 플로우)
2. `PHASE4_TECH_SPEC.md`: 기술 명세서 (아키텍처, 리팩토링, 성능 최적화)
3. `PHASE4_ASSET_LIST.md`: 필요한 이미지/사운드 프롬프트 리스트
4. `PHASE4_TEST_PLAN.md`: QA 시나리오 및 테스트 케이스

---

## 🚀 "Best Target" Definition

**"Hypnotic Arcade Action"**
- 플레이어가 무념무상으로 몰입할 수 있는 **"최면적인 아케이드 액션"**을 지향합니다.
- 시각(Neon Colors), 청각(Beat-synced Audio), 촉각(Visual Feedback)의 일체감을 목표로 합니다.
