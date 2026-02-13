# Feeding Caiso Phase 6: Modern Ethereal Redesign (Visual Overhaul)

## 1. 개요 (Overview)
기존의 "Feeding Caiso"는 귀여운 보라색 몬스터와 캐주얼한 그래픽을 중심으로 했으나, Phase 6에서는 완전히 새로운 시각적 정체성을 확립합니다.
**목표:** 성인도 즐길 수 있는 모던하고 세련된 그래픽, 차갑지만 무섭지 않은 신비로운 분위기, 그리고 정적인 이미지보다는 동적인 애니메이션 효과가 주가 되는 게임으로 탈바꿈합니다.

## 2. 디자인 컨셉 (Design Concept)

### 2.1 핵심 키워드
- **Modern (현대적인):** 미니멀리즘, 깔끔한 선, 세련된 UI.
- **Cold but Not Scary (차갑지만 무섭지 않은):** 얼음, 수정, 유리, 네온 블루/화이트 톤. 공포감이 아닌 신비로움과 평온함을 강조.
- **Animation-Heavy (애니메이션 중심):** 정지된 스프라이트 대신 파티클, 쉐이더, 빛 번짐(Bloom), 유동적인 움직임 강조.
- **Abstract & Ethereal (추상적 & 천상적):** 구체적인 생명체보다는 기하학적 형태나 반투명한 에너지체 형상.

### 2.2 컬러 팔레트 (Color Palette)
- **Primary:** Deep Navy (#0a0e17), Ice Blue (#a0e9ff), Neon Cyan (#00f3ff).
- **Secondary:** Silver/White (#ffffff with opacity), Violet Mist (#bd93f9).
- **Accent:** Energy Glow (Hot Pink or Bright Yellow - minimal usage).

## 3. 에이전트 활용 가이드라인 (Agent Usage Guidelines)

본 프로젝트는 `./agents` 내의 AI 에이전트들을 적극 활용하여 개발합니다.

### 3.1 DesignAgent (기획 및 디자인)
- **역할:** 전체적인 분위기 설정 및 세부 디자인 명세 작성.
- **활용법:**
  - 현대적인 UI/UX 레퍼런스 분석 요청.
  - 컬러 팔레트 구체화 및 헥사코드 생성.
  - 추상적인 캐릭터("Caiso")의 형태 아이디어 도출.

### 3.2 ImageAgent (에셋 생성)
- **역할:** 게임 내 사용할 그래픽 리소스 생성 (배경, 캐릭터, 아이템).
- **프롬프트 가이드:**
  - *Style:* "Minimalist digital art, glowing neon edges, glassmorphism, ethereal, cold color palette."
  - *Character:* "Abstract geometric floating entity, glowing core, translucent shell, soft blue light."
  - *Background:* "Deep space or underwater abyss, minimal geometric parallax layers, cool gradient."
- **명령 예시:** `python -m agents image_agent --prompt "minimalist glowing blue geometric crystal character, vector style, dark background" --output "assets/sprites/caiso.png"`

### 3.3 SoundAgent (사운드 디자인)
- **역할:** 시각적 변화에 맞는 오디오 경험 제공.
- **스타일:** Ambient, Glassy textures, Deep bass drones, Wind chimes via Web Audio API (Phase 5의 절차적 생성 강화).
- **명령 예시:** `python -m agents sound_agent --theme "ethereal ice cave" --type "bgm"`

### 3.4 CodeAgent (구현 및 애니메이션)
- **역할:** 에셋 적용 및 고급 애니메이션 효과(쉐이더, 파티클) 구현.
- **주요 작업:**
  - Canvas API/WebGL을 이용한 파티클 시스템 구현 (눈내림, 에너지 입자).
  - 동적 조명 효과 (Glow effects).
  - 물리 기반의 부드러운 움직임 (Lerp, Spring physics).

## 4. 개발 로드맵 (Development Roadmap)

### Step 1: 리소스 정리 (Cleanup) - [완료]
- 기존 `assets` 폴더를 백업(`assets_backup_phase5`)으로 이동 및 초기화.

### Step 2: 비주얼 프로토타이핑 (Visual Prototyping)
- **목표:** 새로운 Caiso 캐릭터와 배경 스타일 확정.
- **Action:** `ImageAgent`를 사용하여 3-4가지 스타일 시안 생성 후 결정.

### Step 3: 코어 그래픽 시스템 구축 (Core Graphic System)
- **목표:** 정적인 이미지 대신 코드로 그려지는 효과 구현.
- **Action:**
  - `ParticleSystem.js` 개발: 마우스 인터랙션, 배경 부유물.
  - `PostProcessing.js`: Bloom 효과, 색수차(Chromatic Aberration) 등 모던한 필터 적용.

### Step 4: UI/UX 리뉴얼 (Modern UI)
- **목표:** 기존 픽셀 폰트 제거, 고해상도 벡터 느낌의 UI.
- **Action:** Glassmorphism(유리 질감) UI 패널 구현, 미니멀한 아이콘.

### Step 5: 애니메이션 통합 (Animation Integration)
- **목표:** 캐릭터의 상태(배고픔, 기쁨)를 형상/색상 변화로 표현.
- **Action:** 단순히 이미지를 교체하는 것이 아니라, 쉐이더나 오퍼시티, 스케일 변화로 감정 표현.

## 5. 기술적 고려사항 (Technical Considerations)
- **Performance:** 다량의 파티클과 효과 사용 시 프레임 드랍 주의 (Object Pooling 사용).
- **Responsive:** 고해상도 디스플레이(Retina) 대응.
- **Accessibility:** 명도 대비 유지 (너무 어둡거나 눈부시지 않도록).

---
*이 문서는 Phase 6 개발의 기준이 되며, 모든 변경사항은 이 문서의 철학(Frozen Modernity)을 따라야 합니다.*
