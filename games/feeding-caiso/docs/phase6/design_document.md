# Feeding Caiso Phase 6: The Hollow Deep (Atmospheric Redesign)

## 1. 개요 (Overview)
기존의 "Feeding Caiso"는 모던하고 이세시적인 분위기를 지향했으나, Phase 6에서는 **Hollow Knight**에서 영감을 받은 **어둡고 멜랑콜리하지만 아름다운 지하 세계**로 재탄생합니다.
**목표:** 손으로 그린 듯한 2D 아트 스타일, 깊이 있는 분위기, 그리고 벌레(Insect)와 고대 문명을 연상시키는 신비로운 테마를 적용하여 플레이어에게 깊은 몰입감을 선사합니다.

## 2. 디자인 컨셉 (Design Concept)

### 2.1 핵심 키워드
- **Hand-Drawn Aesthetic (손으로 그린 듯한 미학):** 펜화 느낌, 거친 텍스처, 깊이 있는 음영.
- **Melancholic Beauty (우울한 아름다움):** 쇠락한 왕국, 잊혀진 지하 세계, 슬프지만 매혹적인 분위기.
- **Atmospheric Depth (대기감과 깊이):** 안개, 먼지 입자, 다중 레이어의 파럴랙스(Parallax) 배경.
- **Insectoid & Organic (곤충형 & 유기적):** 딱정벌레, 유충, 고치, 균사체 등 자연물 기반의 기괴하면서도 귀여운 캐릭터 디자인.

### 2.2 컬러 팔레트 (Color Palette)
- **Primary:** Void Black (#0f0f1b), Deep Blue Grey (#2d3436), Desaturated Blue (#636e72).
- **Secondary:** Pale Shell White (#dfe6e9), Faded Gold (#b2bec3 - relic feel).
- **Accent:** Infection Orange (#ff7675) or Soul Blue (#74b9ff) - 빛나는 효과에 사용.

## 3. 에이전트 활용 가이드라인 (Agent Usage Guidelines)

본 프로젝트는 `./agents` 내의 AI 에이전트들을 적극 활용하여 할로우 나이트 풍의 에셋과 코드를 생성합니다.

### 3.1 DesignAgent (기획 및 월드빌딩)
- **역할:** "Feeding Caiso"의 세계관을 '잊혀진 지하 왕국'으로 재해석.
- **활용법:**
  - Caiso를 '굶주린 고대 유충' 혹은 '공허의 존재'로 설정.
  - 먹이 아이템을 '영혼(Soul)'이나 '고대의 룬'으로 변경.

### 3.2 ImageAgent (아트워크 생성)
- **역할:** 손으로 그린 느낌의 스프라이트와 배경 생성.
- **프롬프트 가이드:**
  - *Style:* "Hand-drawn 2D game art, Hollow Knight style, dark atmospheric, cel shaded but moody, sketch lines, gothic insect fantasy."
  - *Character (Caiso):* "Cute but slightly creepy little bug knight or void creature, white mask, black body, cloak, simple vector but hand-drawn feel."
  - *Background:* "Underground cave system, ancient ruins, blue mist, platforms, Stalactites, dark monochrome with blue ambient light."
- **명령 예시:** `python -m agents image_agent --prompt "hand-drawn style 2d cute bug character with skull mask, hollow knight vibe, dynamic pose" --output "assets/sprites/caiso_knight.png"`

### 3.3 SoundAgent (오디오 및 앰비언스)
- **역할:** 공허하고 울림이 있는 사운드스케이프 조성.
- **스타일:**
  - *BGM:* Solo piano with heavy reverb, melancholic cello, minimal orchestral.
  - *SFX:* Echoing footsteps, insect chittering, breaking glass/crystal sounds, sword slashes (nail sound).
- **명령 예시:** `python -m agents sound_agent --theme "melancholic underground ruin" --type "bgm"`

### 3.4 CodeAgent (이펙트 및 연출)
- **역할:** 2D 조명, 파티클, 카메라 연출 구현.
- **주요 작업:**
  - **Parallax Scrolling:** 다중 배경 레이어로 깊이감 표현.
  - **Dynamic Lighting:** 플레이어 주변을 밝히는 랜턴 효과 (Vignette & Radial Gradient).
  - **Impact Frames:** 피격/식사 시 화면 멈춤 및 흔들림 (Screen Shake) 강조.
  - **Particle System:** 공기 중에 떠다니는 먼지, 포자(Spores), 영혼 입자.

## 4. 개발 로드맵 (Development Roadmap)

### Step 1: 아트 스타일 정립 (Art Direction)
- **목표:** '할로우 나이트' 스타일의 Caiso 캐릭터와 기본 타일셋 확정.
- **Action:**
  - Caiso: 가면을 쓴 작은 벌레 형태.
  - Food: 영혼 구슬(Soul Orb) 또는 지오(Geo) 형태.

### Step 2: 배경 및 조명 시스템 (Environment & Lighting)
- **목표:** 2D 캔버스에 깊이감 있는 조명 구현.
- **Action:**
  - 배경을 근경, 중경, 원경으로 분리하여 파럴랙스 적용.
  - 전체적으로 어둡게 처리하고 캐릭터와 아이템에만 빛(Glow) 효과 부여.

### Step 3: 캐릭터 애니메이션 (Fluid Movement)
- **목표:** 프레임 단위의 애니메이션보다는(혹은 스파인 느낌의) 부드럽고 탄력 있는 움직임.
- **Action:**
  - 점프 시 스쿼시 앤 스트레치(Squash & Stretch).
  - 망토 휘날림 효과 (Sine wave 활용 가능).

### Step 4: UI/UX (Organic UI)
- **목표:** 게임 화면에 녹아드는 다이제틱(Diegetic) UI.
- **Action:**
  - 체력바를 '가면' 개수로 표시.
  - 점수는 '지오(화폐)' 카운터처럼 표시.
  - 폰트: 펜 글씨체 혹은 고대 비석 느낌의 세리프 폰트.

### Step 5: 사운드 통합 (Audio Immersion)
- **목표:** 시각적 분위기를 청각적으로 완성.
- **Action:** 동굴 울림 효과(Reverb)를 웹 오디오 API로 구현.

## 5. 기술적 고려사항 (Technical Considerations)
- **2D Lighting:** `globalCompositeOperation`을 활용한 마스킹 기법으로 어둠 속의 빛 구현.
- **Asset Size:** 손그림 스타일 텍스처의 용량 최적화 (Sprite Sheet 활용).
- **Input Lag:** 타이트한 조작감을 위해 입력 반응 속도 최우선.

---
*이 문서는 Phase 6 개발의 기준이 되며, 'Hollow Knight'의 심미적 기준을 철저히 따릅니다.*
