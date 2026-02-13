# Feeding Caiso Phase 6: The Hollow Deep - 10-Stage Scenario

이 문서는 "Feeding Caiso" Phase 6의 게임 시나리오 및 레벨 디자인 문서입니다.
Hollow Knight에서 영감을 받은 10단계 스테이지 구성을 통해 시각적 아름다움과 점진적인 난이도 상승을 정의합니다.

> **참고 문서:**
> - `design_document.md` — 전체 디자인 컨셉 및 아트 방향
> - `technical_specification.md` — 구현 명세 및 리팩터링 계획

---

## 0. 핵심 메카닉 (Core Mechanics)

Phase 5에서 검증된 핵심 게임 루프를 유지하되, 시각/청각 테마만 전면 교체합니다.

### 0.1 플레이어 액션

| 요소 | Phase 5 (현재) | Phase 6 (리스킨) |
|:---|:---|:---|
| **플레이어** | 마을 주민 (Player) | 작은 곤충 기사 (Little Ghost) |
| **입력** | VirtualJoystick (터치/마우스 드래그) + 피드 버튼 | 동일 (변경 없음) |
| **액션** | 음식을 Caiso에게 던짐 | 영혼/룬을 공허 존재에게 투척 |
| **목표** | 배고픔(Hunger) 0%로 줄여 승리 | 공허(Void) 게이지 0%로 줄여 정화 |
| **실패 조건** | 마을 주민이 모두 먹히면 게임 오버 | 가면(Masks)이 모두 깨지면 게임 오버 |

### 0.2 기존 시스템 매핑

| 게임 시스템 | 소스 파일 | Phase 6 변경 |
|:---|:---|:---|
| 콤보/피버 | `src/utils/FeverMode.js` | 색상/이펙트만 변경 (Soul Blue 테마) |
| 화면 흔들림 | `src/utils/Juice.js` (ScreenShake) | 유지 |
| 임팩트 프레임 | `src/utils/Juice.js` (ImpactFrame) | 유지 |
| 진화 단계 | `src/utils/Constants.js` (EVOLUTION_TIERS) | Grub → Husk → Knight → Shade Lord |
| 스테이지 전환 | `src/core/StageManager.js` | 페이드 효과 유지, 설정값 교체 |
| 환경 물리 | `src/core/Environment.js` | 풍속/중력값 스테이지별 재조정 |

### 0.3 아이템 매핑

현재 `Constants.js`의 `FOODS` 구조를 유지하되 이름/에셋만 교체합니다:

| 키 | Phase 5 | Phase 6 | 배고픔 감소 | 해금 레벨 |
|:---|:---|:---|:---|:---|
| `apple` | Apple | Soul Orb (영혼 구슬) | 8 | 1 |
| `burger` | Burger | Geo Cluster (지오 뭉치) | 15 | 2 |
| `pizza` | Pizza | Pale Ore (창백한 광석) | 22 | 3 |
| `dorito` | Dorito | King's Idol (왕의 우상) | 12 | 4 |
| `watermelon` | Watermelon | Lifeblood (생명혈) | 30 | 5 |
| `dynamite` | Dynamite | Void Egg (공허의 알) | 40 | 7 |

---

## Stage 1: 잊혀진 교차로 (The Forgotten Crossroads)
> *"오래된 왕국의 입구. 차가운 바람만이 불어옵니다."*

### 비주얼 (Visual)
- **배경색:** `#1a1a2e` (어두운 남색)
- **패럴랙스 원경:** 거대한 동굴 천장, 희미한 종유석 실루엣
- **패럴랙스 중경:** 무너진 고대 기둥, 풍화된 도로
- **패럴랙스 근경:** 깨진 석재 바닥, 이끼 자국
- **파티클:** 회색 먼지가 천천히 부유 (`DustEmitter`, density: low)
- **조명:** 전체적으로 어둡지만 플레이어 주변에 은은한 원형 광원
  - `ambientLight`: 0.3
  - `playerLightRadius`: 150
  - `playerLightColor`: `rgba(116, 185, 255, 0.4)` (Soul Blue)

### 게임플레이 (Difficulty: Very Easy)

| 파라미터 | 값 | 비고 |
|:---|:---|:---|
| `duration` | 60000ms | 60초 |
| `windX` | 0 | 바람 없음 |
| `gravityY` | 1.0 | 표준 중력 |
| `hazards` | `[]` | 장애물 없음 |
| `itemSpeedMult` | 1.0 | 기본 아이템 속도 |
| `overlayColor` | `rgba(15, 15, 27, 0.3)` | 가벼운 어둠 |

### 목표
- 조작감 익히기. Caiso의 부드러운 관성 이동 체험.
- Soul Orb(apple) 아이템만 등장.

---

## Stage 2: 녹색 거리 (Greenpath)
> *"이끼와 잎사귀가 가득한 생명의 흔적이나, 어딘가 독성을 품고 있습니다."*

### 비주얼 (Visual)
- **배경색:** `#1a3a2e` (짙은 녹색)
- **패럴랙스 원경:** 거대한 잎사귀 실루엣, 덩굴
- **패럴랙스 중경:** 이끼 낀 기둥, 수액이 흐르는 벽
- **파티클:** 나뭇잎과 포자가 흩날림 (`SporeEmitter`, density: low-medium)
- **조명:**
  - `ambientLight`: 0.35
  - `playerLightRadius`: 140
  - `accentLightColor`: `rgba(46, 204, 113, 0.2)` (녹색 환경광)
- **사운드:** 풀벌레 소리와 물 흐르는 소리 (앰비언스 레이어 추가)

### 게임플레이 (Difficulty: Easy)

| 파라미터 | 값 | 비고 |
|:---|:---|:---|
| `duration` | 60000ms | |
| `windX` | 0.5 | 약한 미풍 |
| `gravityY` | 1.0 | |
| `hazards` | `["acid_drop"]` | 산성 물방울: 닿으면 0.5초 스턴 |
| `itemSpeedMult` | 1.1 | 약간 빨라진 아이템 |
| `overlayColor` | `rgba(20, 60, 40, 0.25)` | 녹색 틴트 |

### 특수 요소
- **산성 물방울 (Acid Drop):** Hazard 엔티티. 연두색 반투명 구슬로, 음식에 닿으면 음식 파괴. 스폰 간격: `max(1500, 3000 - level * 100)ms`

---

## Stage 3: 곰팡이 황무지 (Fungal Wastes)
> *"포자가 시야를 가립니다. 통통 튀는 버섯들이 가득합니다."*

### 비주얼 (Visual)
- **배경색:** `#2d1b4e` (탁한 보라색)
- **패럴랙스 원경:** 기이하게 생긴 거대 버섯 실루엣
- **패럴랙스 중경:** 발광하는 작은 버섯들, 균사체
- **파티클:** 시야를 살짝 가리는 짙은 포자 구름 (`SporeEmitter`, density: high)
  - 파티클 크기: 8-20px, 알파: 0.3-0.6
  - 효과: 아이템 시인성 감소 (전략적 난이도 요소)
- **조명:**
  - `ambientLight`: 0.25
  - 버섯에서 나오는 고정 광원 2-3개 (보라색 빛)

### 게임플레이 (Difficulty: Normal)

| 파라미터 | 값 | 비고 |
|:---|:---|:---|
| `duration` | 60000ms | |
| `windX` | 0 | |
| `gravityY` | 0.9 | 포자로 인한 약간 낮은 중력 |
| `hazards` | `["exploding_spore"]` | 폭발 포자: 먹으면 화면 흔들림 |
| `itemSpeedMult` | 1.2 | |
| `overlayColor` | `rgba(50, 20, 80, 0.35)` | 보라색 안개 |

### 특수 요소
- **폭발 포자 (Exploding Spore):** 먹으면 `ScreenShake.trigger(12, 300)`, 점수 패널티 -50.
- **포자 구름 (Spore Cloud):** 파티클 시스템으로 구현. 시야를 부분적으로 가림.

---

## Stage 4: 눈물의 도시 (City of Tears)
> *"끝없이 비가 내리는 슬픈 도시. 우산이 필요해 보입니다."*

### 비주얼 (Visual)
- **배경색:** `#1a2a4a` (깊은 청색)
- **패럴랙스 원경:** 웅장하지만 쓸쓸한 푸른색 건축물 실루엣
- **패럴랙스 중경:** 창문에서 새어 나오는 노란 불빛 (고정 광원)
- **효과:** 화면 전체에 빗줄기 (`RainEmitter`, density: very high)
  - 빗방울: 1-2px 너비, 15-25px 길이, 알파 0.3-0.5
  - 각도: 약 10도 기울어짐
- **조명:**
  - `ambientLight`: 0.3
  - 창문 고정 광원 3-4개 (따뜻한 황색)
- **사운드:** 빗소리 앰비언스 (지속적, 리버브 강함)

### 게임플레이 (Difficulty: Normal+)

| 파라미터 | 값 | 비고 |
|:---|:---|:---|
| `duration` | 60000ms | |
| `windX` | 1.0 | 비바람 |
| `gravityY` | 1.1 | 빗물 무게로 약간 높은 중력 |
| `hazards` | `["rain_gust"]` | 돌풍: 아이템 궤적 랜덤 변동 |
| `itemSpeedMult` | 1.3 | 가속도 불규칙 |
| `overlayColor` | `rgba(20, 40, 80, 0.4)` | 깊은 청색 |
| `slipperyFloor` | `true` | 바닥 미끄러짐 (플레이어 관성 1.5배) |

### 특수 요소
- **미끄러운 바닥:** `Player.js`의 마찰계수를 스테이지 설정으로 조정. 관성이 증가하여 정밀 조작 난이도 상승.
- **귀족의 유물 (Noble's Relic):** 저확률(10%) 고득점 아이템. 기존 아이템의 3배 점수.

---

## Stage 5: 수정 봉우리 (Crystal Peak)
> *"노래하는 수정들이 가득한 광산. 아름답지만 날카롭습니다."*

### 비주얼 (Visual)
- **배경색:** `#2a1a3a` (밝은 보라-분홍 암석)
- **패럴랙스 원경:** 거대한 수정 클러스터 실루엣
- **패럴랙스 중경:** 빛을 반사하는 작은 수정들 (반짝임 효과)
- **파티클:** 수정 가루가 반짝이며 부유 (`DustEmitter` + sparkle 변형)
- **조명:**
  - `ambientLight`: 0.4 (수정 반사로 밝은 편)
  - 간헐적 블룸 효과: 수정이 번쩍이며 전체 밝기 일시적 증가
  - 수정 색상: `rgba(230, 150, 255, 0.5)` (분홍-보라)
- **사운드:** 맑은 종소리와 기계적인 윙윙거리는 소리

### 게임플레이 (Difficulty: Hard)

| 파라미터 | 값 | 비고 |
|:---|:---|:---|
| `duration` | 60000ms | |
| `windX` | 0 | |
| `gravityY` | 1.0 | |
| `hazards` | `["crystal_beam"]` | 레이저 빔: 1초 예고 후 발사 |
| `itemSpeedMult` | 1.4 | |
| `overlayColor` | `rgba(50, 30, 70, 0.2)` | 연한 보라색 |

### 특수 요소
- **레이저 빔 (Crystal Beam):** 화면 상단에서 수직 또는 사선으로 발사. 발사 전 1초간 얇은 빨간 경고선 표시. 음식이 빔에 닿으면 파괴.
- **수정 조각 (Crystal Shard):** 특수 아이템. 바닥에 닿으면 파편이 튀며 사라짐 (시간 제한 아이템).

---

## Stage 6: 깊은 둥지 (Deepnest)
> *"빛이 닿지 않는 거미들의 굴. 바스락거리는 소리가 들립니다."*

### 비주얼 (Visual)
- **배경색:** `#0a0a0f` (거의 완전한 검정)
- **패럴랙스:** 최소한의 실루엣만 (거미줄 텍스처)
- **파티클:** 없음 (극도의 정적)
- **조명:** **핵심 기믹 — 시야 제한**
  - `ambientLight`: 0.05 (거의 암흑)
  - `playerLightRadius`: 100 (축소된 광원)
  - `playerLightColor`: `rgba(255, 200, 150, 0.6)` (랜턴 색)
  - 플레이어 광원 범위 밖: 완전한 검정 (아이템 실루엣만 보임)
- **사운드:** 바스락거리는 소리, 곤충 울음, 긴장감 있는 저음

### 게임플레이 (Difficulty: Hard+)

| 파라미터 | 값 | 비고 |
|:---|:---|:---|
| `duration` | 60000ms | |
| `windX` | 0 | |
| `gravityY` | 1.0 | |
| `hazards` | `["mimic"]` | 가짜 아이템: 먹으면 데미지 |
| `itemSpeedMult` | 1.3 | |
| `overlayColor` | `rgba(0, 0, 0, 0.85)` | 극도의 어둠 |
| `visibilityRadius` | 100 | 시야 제한 반경 (px) |

### 특수 요소
- **시야 제한:** `LightingSystem`에서 `globalCompositeOperation = 'destination-in'`으로 원형 마스크 적용. 광원 밖의 모든 것은 보이지 않음.
- **가짜 아이템 (Mimic):** 정상 아이템과 동일한 외형. 먹으면 데미지 (가면 -1) + `ScreenShake.trigger(15, 400)`. 구별법: 광원 범위 안에서 미세한 떨림.

---

## Stage 7: 왕국의 끝자락 (Kingdom's Edge)
> *"재가 눈처럼 내리는 세상의 끝. 바람이 거셉니다."*

### 비주얼 (Visual)
- **배경색:** `#1a1a20` (창백한 회색 계열)
- **패럴랙스 원경:** 거대한 고대 생물의 사체 실루엣
- **패럴랙스 중경:** 절벽, 뼈 구조물
- **파티클:** 하얀 재(Ash)가 끊임없이 휘날림 (`AshEmitter`, density: very high)
  - 재 파티클: 3-6px, 흰색/밝은 회색, 측풍에 영향받음
- **조명:**
  - `ambientLight`: 0.35
  - 하늘에서 내려오는 약한 백색 광원 (상부 그래디언트)
- **사운드:** 바람 소리 (지속적), 먼 곳의 울림

### 게임플레이 (Difficulty: Very Hard)

| 파라미터 | 값 | 비고 |
|:---|:---|:---|
| `duration` | 60000ms | |
| `windX` | 3.0 | **강한 측풍** |
| `gravityY` | 0.9 | 재가 날려 약간 가벼움 |
| `hazards` | `["ash_gust"]` | 돌풍: 주기적으로 방향 전환 |
| `itemSpeedMult` | 1.5 | |
| `overlayColor` | `rgba(30, 30, 35, 0.3)` | 회색 톤 |
| `windDirection` | `alternating` | 5초마다 풍향 전환 |

### 특수 요소
- **교차 풍향:** `Environment.js`에서 5초 주기로 `windX`를 +3.0 ↔ -3.0 교대. 아이템과 플레이어 모두 영향받음.
- **재 파티클:** 풍향에 따라 이동 방향 변경. 시각적으로 풍향 예고.

---

## Stage 8: 심연 (The Abyss)
> *"공허가 당신을 부릅니다. 그림자가 춤을 춥니다."*

### 비주얼 (Visual)
- **배경색:** `#050508` (칠흑)
- **패럴랙스:** 거의 보이지 않음. 바닥에서 검은 촉수들이 일렁이는 애니메이션
- **파티클:** 검은 입자가 아래에서 위로 상승 (`VoidEmitter`, 역중력)
- **조명:**
  - `ambientLight`: 0.1
  - `playerLightRadius`: 120
  - 검은 촉수에서 나오는 역광(보라색)
- **사운드:** 소름 끼치는 정적. 가끔 저음 진동.

### 게임플레이 (Difficulty: Nightmare)

| 파라미터 | 값 | 비고 |
|:---|:---|:---|
| `duration` | 60000ms | |
| `windX` | 0 | |
| `gravityY` | 0.7 | 낮은 중력 (부유감) |
| `hazards` | `["void_tendril", "void_rising"]` | 촉수 + 상승하는 공허 |
| `itemSpeedMult` | 1.4 | |
| `overlayColor` | `rgba(5, 0, 15, 0.7)` | 깊은 보라색 어둠 |

### 특수 요소
- **상승하는 공허 (Void Rising):** 바닥에서 검은 물결이 천천히 차오름 (60초 중 마지막 20초에 활성화). 화면 하단 20%를 채우며, 닿으면 지속 데미지.
- **공허 촉수 (Void Tendril):** 하단에서 무작위 위치로 올라오는 검은 촉수. 음식을 가로채 파괴.

---

## Stage 9: 백색 궁전 (White Palace)
> *"고통스러운 순백의 왕실. 모든 것이 날카롭습니다."*

### 비주얼 (Visual)
- **배경색:** `#e8e8f0` (눈이 시린 흰색)
- **패럴랙스 원경:** 정교한 백색 기계 장치 실루엣
- **패럴랙스 중경:** 톱니바퀴, 회전하는 기어들
- **파티클:** 백색 먼지, 기계 불꽃 (`SparkEmitter`, density: medium)
- **조명:**
  - `ambientLight`: 0.8 (매우 밝음 — 이전 스테이지와 극적 대비)
  - 과도한 밝기로 인한 눈부심 효과 (Bloom)
  - 플레이어 그림자 효과 추가
- **사운드:** 톱니바퀴 돌아가는 소리, 금속성 울림

### 게임플레이 (Difficulty: Insane)

| 파라미터 | 값 | 비고 |
|:---|:---|:---|
| `duration` | 60000ms | |
| `windX` | 0 | |
| `gravityY` | 1.0 | |
| `hazards` | `["buzzsaw"]` | 회전 톱날: 화면을 가로지름 |
| `itemSpeedMult` | 1.6 | 매우 빠른 아이템 |
| `overlayColor` | `rgba(240, 240, 250, 0.1)` | 밝은 오버레이 |
| `scoreMultiplier` | 2.0 | 점수 2배 보상 |

### 특수 요소
- **회전 톱날 (Buzzsaw):** 화면 좌→우 또는 우→좌로 수평 이동하는 원형 톱날. 이동 속도: 3px/frame. 음식과 Hazard 모두에 적용. 예고: 진입 측면에 1초간 경고 표시.
- **점수 배율:** 이 스테이지에서 모든 점수 획득에 2배 적용 (`scoreMultiplier` in stage config).

---

## Stage 10: 광휘 (The Radiance)
> *"잊혀진 빛, 혹은 감염의 근원. 꿈의 끝."*

### 비주얼 (Visual)
- **배경색:** `#3a2000` → 점진적으로 `#ff9500`으로 밝아짐
- **패럴랙스:** 강렬한 주황-황금색 구름이 일렁임
- **파티클:** 감염 입자가 비처럼 쏟아짐 (`InfectionEmitter`, density: extreme)
  - 주황색 발광 파티클, 크기: 4-12px
- **조명:**
  - `ambientLight`: 0.5 → 스테이지 진행에 따라 0.9까지 증가
  - 태양 같은 중앙 후광 효과 (Radial Gradient, 화면 중앙 상부)
  - 화면 전체가 일렁이는 열기 효과 (사인파 왜곡)
- **사운드:** 웅장한 오르간 사운드, 감염 맥박 소리

### 게임플레이 (Difficulty: God)

| 파라미터 | 값 | 비고 |
|:---|:---|:---|
| `duration` | 90000ms | **90초** (최종 스테이지 연장) |
| `windX` | `random(-2, 2)` | 무작위 풍향 |
| `gravityY` | 0.5 | 매우 낮은 중력 (몽환적) |
| `hazards` | `["infection_rain", "light_beam"]` | 감염비 + 빛 기둥 |
| `itemSpeedMult` | 1.8 | |
| `overlayColor` | `rgba(255, 150, 0, 0.15)` | 황금색 |
| `scoreMultiplier` | 3.0 | 점수 3배 |

### 특수 요소
- **감염비 (Infection Rain):** 탄막 슈팅(Bullet Hell) 스타일. 주황색 감염 구체가 화면 상단에서 대량 낙하. 음식에 닿으면 파괴.
- **빛 기둥 (Light Beam):** 화면 상부에서 내려오는 황금색 수직 빔. 2초 간격, 1초 예고. 닿으면 데미지.
- **클리어 조건:** 60초 동안 생존하며 공허 게이지 0% 달성. 또는 90초 경과 시 남은 공허 게이지 기반 점수 산정.
- **엔딩 연출:** 성공 시 Caiso가 나비 날개(Monarch Wings)를 펼치며 화면 위로 비상. 파티클 폭발 + 페이드 아웃.

---

## 스테이지 전환 규칙 (Stage Transition Rules)

### 전환 트리거

현재 `StageManager.js:87`에서 레벨 기반으로 전환합니다:

```
game.level > currentStageIndex + 1  →  nextStage() 호출
```

레벨업 조건 (`Constants.js`):
- `HUNGER_PER_LEVEL`: 4 (배고픔 4% 감소당 1레벨)
- 총 배고픔: 100% → 25레벨까지 가능
- 10스테이지 기준: 레벨 1-10에서 각 스테이지 진입

### 전환 연출

현재 구현 (`StageManager.js:60-84`):
1. 1.2초 트랜지션 (`transitionDuration: 1200ms`)
2. 전반 0.5: 검은색으로 페이드 아웃
3. 중간점(0.5-0.55): 새 스테이지 로드
4. 후반 0.5: 검은색에서 페이드 인

**Phase 6 개선:**
- BGM 크로스페이드: 전환 시작 시점부터 새 스테이지 BGM 페이드 인
- 스테이지 이름 표시: 페이드 인 후 2초간 "Stage N: 스테이지 이름" 텍스트 표시
- 스테이지별 전환 색상: 검정 → 스테이지 테마 색상으로 변경 가능

---

## 난이도 곡선 요약 (Difficulty Curve Summary)

```
난이도 ──────────────────────────────────────────────────▶

  God     │                                          ██ S10
  Insane  │                                     ██ S9
  Nmr     │                                ██ S8
  V.Hard  │                           ██ S7
  Hard+   │                      ██ S6
  Hard    │                 ██ S5
  Norm+   │            ██ S4
  Normal  │       ██ S3
  Easy    │  ██ S2
  V.Easy  │█ S1
          └────────────────────────────────────────────────
           S1   S2   S3   S4   S5   S6   S7   S8   S9  S10
```

| 스테이지 | 핵심 난이도 요소 | 시야 | 물리 변동 |
|:---|:---|:---|:---|
| S1 | 없음 (튜토리얼) | 전체 | 표준 |
| S2 | Acid Drop | 전체 | 약한 바람 |
| S3 | 포자 시야 방해 | 감소 | 약간 낮은 중력 |
| S4 | 비, 미끄러운 바닥 | 전체 | 강한 바람, 높은 중력 |
| S5 | 레이저 빔 | 전체 | 표준 |
| S6 | **시야 제한**, 미믹 | **극소** | 표준 |
| S7 | **강한 교차 풍향** | 재 방해 | 바람 3.0, 낮은 중력 |
| S8 | 상승하는 공허, 촉수 | 어둠 | 매우 낮은 중력 |
| S9 | **회전 톱날** (속도 최대) | 전체 (밝음) | 표준 |
| S10 | **탄막, 빛 기둥** (종합) | 감염 입자 방해 | 무작위 풍향, 최저 중력 |

---

*각 스테이지 파라미터는 `src/config/Stages.js`에 정의되며, 플레이테스팅을 통해 밸런스 조정합니다.*
*스테이지 설정의 전체 구조는 `technical_specification.md` Section 3.1을 참조합니다.*
