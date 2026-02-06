# 🧪 Feeding Caiso Phase 4: Test Plan (QA Strategy)

> **Focus**: Quality Assurance, UX Verification
> **Agent**: Play Agent
> **Status**: DRAFT

---

## 1. 🎯 Testing Objectives

Phase 4의 목표인 "Polished Arcade Experience"를 검증하기 위해 다음 항목을 집중 테스트합니다.

1.  **Mobile Usability**: 터치 반응속도, 멀티터치, 화면 비율 대응.
2.  **Game Balance**: 난이도 곡선이 적절한가? (너무 쉽거나 불합리하게 어렵지 않은가)
3.  **Performance**: 저사양 기기에서 60 FPS 유지 여부 (Particle stress test).
4.  **Audio Sync**: 사운드가 액션과 정확히 일치하는가.

---

## 2. 🤖 Automated Testing (Play Agent)

`Playwright`를 이용한 자동화 스크립트로 회귀 테스트(Regression Test)를 수행합니다.

### Test Case 1: Core Loop Stability
-   **Action**: 30초 동안 랜덤 위치에 Food 발사.
-   **Expected Result**:
    -   Crash 없음.
    -   Caiso 상태가 `Eat` <-> `Hungry` 정상 전환.
    -   Villager가 사라질 때 `VillagerCount` 감소 확인.

### Test Case 2: Fever Mode Trigger
-   **Action**: `combo` 변수를 강제로 주입하거나 빠르게 맞춰서 Fever 게이지 충전.
-   **Expected Result**:
    -   Fever 진입 시 시각/청각 효과(파티클, 사운드) 발생 로그 확인.
    -   Villager 감소 속도 변화 확인.

### Test Case 3: Mobile Touch Emulation
-   **Action**: Playwright의 Mobile Emulation(`iPhone 12`) 모드로 실행.
-   **Check**: 조이스틱 영역과 발사 버튼 영역이 겹치지 않는지 좌표 검증.

---

## 3. 🖐 Manual Testing Checklist (Human Review)

| Category | Item | Criteria |
|----------|------|----------|
| **Visual** | Neon Glow | 과도한 Bloom이 게임플레이를 방해하지 않는가? |
| **Visual** | Text Visibility | 배경과 텍스트의 명암비가 4.5:1 이상인가? |
| **Control** | Input Lag | 터치 후 발사까지 100ms 이내 반응하는가? |
| **Control** | Joystick | 손가락이 화면 밖으로 나갔을 때 조이스틱이 튀지 않는가? |
| **Audio** | Loop | BGM 반복 지점에서 튐(Pop) 현상이 없는가? |
| **Audio** | Volume | SFX가 BGM에 묻히지 않는가? |

---

## 4. 📈 Performance Design Targets

-   **Frame Rate**: Stable 60 FPS on mid-range devices (e.g., iPhone 8+, Galaxy S10+).
-   **Load Time**: < 3 seconds (Initial load).
-   **Memory**: < 100MB Heap usage.
-   **Draw Calls**: < 50 per frame (Sprite batching 필수).

---

## 5. 🐛 Bug Reporting Protocol

Play Agent가 시뮬레이션 중 발견한 이슈는 다음 포맷으로 자동 리포트됩니다:

```markdown
### ⚠️ Issue Detected
- **Type**: Frame Drop / Logic Error / Collision Failure
- **Timestamp**: 12.5s
- **Context**: Fever Mode + 50 Particles + 20 Villagers
- **Log Snippet**: `Warning: Long frame execution (32ms)`
```
