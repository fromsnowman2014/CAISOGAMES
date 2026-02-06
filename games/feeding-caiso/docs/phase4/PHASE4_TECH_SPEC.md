# 🛠️ Feeding Caiso Phase 4: Technical Specification

> **Focus**: Refactoring, Architecture, Optimization
> **Agent**: Code Agent
> **Status**: DRAFT

---

## 1. 🏗️ Architecture Refactoring

현재 `index.html` 단일 파일 구조에서 **ES Modules (ESM) 기반의 모듈형 구조**로 전환합니다.
(배포 시 Bundler 사용 없이 Native ESM 사용 예정 - Modern Browser Only)

### Directory Structure
```
games/feeding-caiso/
├── index.html          # Entry Point (Bootstrap only)
├── src/
│   ├── core/
│   │   ├── Game.js     # Main Loop, Initialization
│   │   ├── Input.js    # Virtual Joystick, Touch handling
│   │   └── Audio.js    # Web Audio API wrapper
│   ├── entities/
│   │   ├── Entity.js   # Base class
│   │   ├── Caiso.js    # Boss logic
│   │   ├── Player.js   # Player logic
│   │   └── Villager.js # Enemy logic
│   ├── managers/
│   │   ├── AssetManager.js # Scale/Load assets
│   │   ├── PoolManager.js  # Object Pooling (Bullets, Particles)
│   │   └── UIManager.js    # Canvas UI rendering
│   └── utils/
│       ├── MathUtils.js
│       └── StateMachine.js
└── assets/             # Images, Sounds
```

---

## 2. ⚡ Performance Optimization Strategy

code_agent의 분석 결과(`docs/feeding-caiso_code_review.md` - 가정)에 따른 최적화 포인트:

1.  **Object Pooling (Object Reuse)**:
    -   *Current*: `new FlyingFood()`, `new Particle()` 매 프레임 생성/삭제 -> GC Spike 유발.
    -   *Phase 4*: `FoodPool`, `ParticlePool` 구현. 미리 100개 생성 후 `active` 플래그로 재사용.
    -   *Benefit*: 모바일 환경에서 프레임 드랍(Stuttering) 제거.

2.  **Sprite Batching (Optimization)**:
    -   동일한 텍스처(예: 파티클)는 한 번의 `drawImage` 호출이 아닌, Offscreen Canvas 등을 활용하거나 렌더링 순서를 최적화. (Canvas API 한계 내 최적화)

3.  **Variable Timestep (Game Loop)**:
    -   현재 `deltaTime`을 단순 적용 중.
    -   *Phase 4*: `FixedUpdate(logic)`와 `Update(render)` 분리하여 저사양 기기에서도 물리학(충돌 감지)이 뚫리지 않도록 보정.

---

## 3. 🧩 State Management (FSM)

현재 `this.state = 'playing'` 문자열 비교 방식을 **State Pattern**으로 변경.

```javascript
// State Machine Concept
class GameState {
    enter() {}
    update(dt) {}
    exit() {}
}

class MenuState extends GameState { ... }
class PlayState extends GameState { ... }
class FeverState extends GameState { ... } // Feve를 별도 상태 또는 Sub-state로 관리
class GameOverState extends GameState { ... }
```
-   **Benefit**: 상태별 로직(Input 처리, 렌더링)을 명확히 분리하여 스파게티 코드 방지.

---

## 4. 📱 Mobile Specifics

1.  **Touch Areas**:
    -   `touchstart` 이벤트를 `passive: false`로 설정하여 스크롤/줌 방지 (이미 적용됨, 강화 필요).
    -   "Notch" 대응: `viewport-fit=cover` 메타 태그 대응 및 Safe Area 패딩 처리.
2.  **Floating Joystick**:
    -   고정 위치 조이스틱 대신, 화면 왼쪽 절반 어디든 터치하면 그곳이 조이스틱 중심이 되는 로직 구현.

---

## 5. 🔊 Audio System Upgrade

-   **Browser Policy**: "User Interaction" 없으면 오디오 재생 불가 문제 완벽 대응.
    -   *Solution*: 첫 터치("Tap to Start") 시 `AudioContext`를 Resume하고 0 volume buffer를 재생하여 잠금 해제.
-   **Audio Sprite**: 다수의 짧은 효과음을 하나의 파일로 합쳐 로딩 속도 및 요청 수 최적화.
