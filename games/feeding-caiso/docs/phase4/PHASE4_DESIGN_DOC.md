# 🎨 Feeding Caiso Phase 4: Design Document

> **Focus**: Game Feel, Progression, "Hypnotic" Flow
> **Agent**: Design Agent
> **Status**: DRAFT

---

## 1. 🌟 Core Concept: "Neon Kawaii Arcade"

기존의 단순한 "던지기 게임"에서 **"리듬감 있는 아케이드 액션"**으로 진화합니다.
- **Visual Style**: 어두운 네온 배경 + 채도 높은 귀여운 캐릭터 (Cyberpunk meet Kawaii).
- **Core Loop**: Feed -> Combo -> Fever -> Evolve. (기존 유지하되 피드백 강화)

---

## 2. 🎮 Gameplay Mechanics (The "Juice")

### A. Dynamic Feedback (Juice)
게임이 "살아있다"고 느끼게 만드는 요소들입니다.

1.  **Impact Frames (Hit Stop)**:
    -   음식이 Caiso 입에 들어가는 순간, 게임 전체가 `0.05초` 정지. 타격감 극대화.
2.  **Screen Shake**:
    -   Villager가 잡아먹힐 때: 강한 진동 (Red tint).
    -   콤보 10회 이상: 미세한 진동 (Excitement).
3.  **Squash & Stretch 2.0**:
    -   현재보다 과장된 애니메이션. 던질 때 Player 캐릭터가 홀쭉해졌다가 팅겨나가는 탄성 표현.
4.  **Spatial Sound**:
    -   Villager가 화면 왼쪽/오른쪽에서 나타날 때 스테레오 패닝 적용.

### B. Progression & Difficulty
단조로움을 타파하기 위한 "Wave" 시스템 도입.

-   **Wave 1-3**: Tutorial Speed.
-   **Wave 4 (Rush)**: Villager가 2배 속도로 쏟아져 나옴 (Fever 유도).
-   **Wave 5 (Boss)**: "Giant Villager" 등장. (3번 맞춰야 구해짐, 점수 5배).
-   **Infinite Scaling**: 레벨이 오를수록 Villager 속도 증가 + Caiso 배고픔 감소 속도 증가.

### C. Fever Mode Improvements
현재의 Fever Mode는 단순히 "점수 2배"에 가깝습니다. 이를 시각적 축제로 바꿉니다.

-   **Visual**: 배경이 "Neon Grid"로 전환되고 비트가 빨라짐.
-   **Effect**: 
    -   Auto-Magnet: 주변 Villager들이 자동으로 안전지대로 끌려감.
    -   Infinite Ammo: 쿨타임 없이 난사 가능.

---

## 3. 🎭 Narrative & Lore (Context)

> "The Great Hunger is coming..."

-   **Intro Sequence**: 평화로운 네온 시티. 갑자기 Caiso(보라색 괴물)가 배고픔에 눈을 뜹니다.
-   **Character**:
    -   **Chef Pixel**: 플레이어. 전설의 요리사.
    -   **Caiso**: 우주의 포식자지만, 배부르면 귀여운 애완동물.
    -   **Villagers**: 네온 시티 시민들. (다양한 직업군: 경찰, 의사, 펑크족 등 스킨 추가).

---

## 4.  UI/UX Improvements

### In-Game HUD
-   **Dynamic Health Bar**: 배고픔 게이지가 줄어들 때 "덜덜 떨리는" 효과.
-   **Floating Text**: 데미지/회복 숫자가 단순히 위로 올라가는 게 아니라, **포물선을 그리며 튀어오르는** 물리 적용.

### Meta Game
-   **Skin Shop**: 게임 내 재화(Star)로 Caiso 스킨(Robot Caiso, Zombie Caiso) 구매.
-   **Gallery**: 수집한 음식 도감.

---

## 5. 🕹️ Controls (Mobile Optimization)

-   **Virtual Joystick Upgrade**: 현재의 절대 좌표 방식 -> **Floating Joystick** (터치한 곳이 중심이 됨)으로 변경하여 조작 피로도 감소.
-   **Tap to Shoot**: 화면 아무 곳이나 탭하면 발사 (현재는 버튼/조이스틱 분리). **멀티터치** 완벽 지원 필요.
