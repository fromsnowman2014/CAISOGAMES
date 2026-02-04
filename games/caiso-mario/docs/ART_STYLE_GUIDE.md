# Caiso Mario - Art Style Guide

## 1. 비주얼 컨셉: "Illuminated Strategy"

### 1.1 핵심 아트 디렉션
게임의 시각적 테마는 **"살아 움직이는 입체 동화책"**과 **"고급스러운 체스 세트"**의 조화입니다.

- **조명**: 키아로스쿠로(Chiaroscuro) 명암대비 기법
- **텍스처**: 낡은 종이 + 매끄러운 대리석 대비
- **색상**: 따뜻한 갈색/금색 + 차가운 흑백 체스판

### 1.2 컬러 팔레트
```
Primary Colors:
- #2D1810 (Dark Mahogany) - 책장, 어두운 영역
- #8B4513 (Saddle Brown) - 나무 질감
- #DAA520 (Goldenrod) - 마법, 하이라이트
- #FFFAF0 (Floral White) - 밝은 페이지

Chess Colors:
- #1A1A1A (Jet Black) - 검은 체스 타일/적
- #F5F5F5 (White Smoke) - 흰 체스 타일
- #4A4A4A (Dim Gray) - 돌 질감

Accent Colors:
- #8B0000 (Dark Red) - 데미지, 위험
- #228B22 (Forest Green) - 체력, 안전
- #4169E1 (Royal Blue) - 마법 효과
- #9400D3 (Dark Violet) - Caiso, 부패
```

---

## 2. 캐릭터 디자인

### 2.1 주인공: Jay Oh

**외형 특징:**
- 11세 소년, 아시아계
- 동그란 검은 안경
- 헐렁한 연두색 니트 조끼
- 흰색 셔츠, 짧은 갈색 바지
- 낡은 가죽 책가방 (등에 멤)
- 헝클어진 검은 머리카락

**스프라이트 크기:** 32x48 픽셀 (타일 32px 기준)

**애니메이션 상태:**
| 상태 | 프레임 수 | 설명 |
|------|----------|------|
| idle | 4 | 숨쉬기 + 눈 깜빡임 |
| run | 8 | 달리기 사이클 |
| jump | 2 | 점프 상승 |
| fall | 2 | 낙하 |
| attack | 4 | 무기 휘두르기 |
| hurt | 2 | 피격 |
| victory | 6 | 스테이지 클리어 |

### 2.2 무기 디자인

**Wooden Pawn (기본 무기)**
- 크기: 16x24 픽셀
- 재질: 따뜻한 나무 질감
- 발광: 은은한 황금빛 아우라
- 특징: 단순한 폰 형태, 둥근 머리

**Stone Knight (1단계)**
- 크기: 20x28 픽셀
- 재질: 회색 돌, 룬 문자 새김
- 발광: 푸른 마법 문양
- 특징: 말 머리 형상, 갑옷 디테일

**Crystal Bishop (2단계)**
- 크기: 18x32 픽셀
- 재질: 투명한 보라색 수정
- 발광: 내부에서 퍼지는 빛
- 특징: 뾰족한 모자, 지팡이 형태

**Marble Rook (3단계)**
- 크기: 24x28 픽셀
- 재질: 흰 대리석, 금 장식
- 발광: 강렬한 황금빛
- 특징: 성벽/탑 형태, 무거운 느낌

---

## 3. 적 캐릭터 디자인

### 3.1 The Unlettered (기본 적)
모든 기본 적은 "얼굴 없는 체스 기물"로 표현됩니다.
- 눈 대신 빛나는 균열
- 고대 룬 문자가 몸체에 새겨짐
- 어두운 돌/금속 질감

**Stone Pawn**
- 크기: 24x32 픽셀
- 색상: 어두운 회색 돌
- 특징: 단순한 원통 형태, 균열에서 붉은 빛

**Jumping Knight**
- 크기: 32x40 픽셀
- 색상: 검은 철, 녹슨 갑옷
- 특징: 말 머리, 뿔처럼 솟은 귀
- 애니메이션: 점프 준비 시 웅크림

**Sniper Bishop**
- 크기: 28x44 픽셀
- 색상: 찢어진 보라색 로브
- 특징: 뾰족한 모자, 지팡이에서 빛 발산
- 애니메이션: 조준 시 빛나는 선 표시

**Charging Rook**
- 크기: 36x36 픽셀
- 색상: 검은 대리석, 금 테두리
- 특징: 성벽 형태, 돌진 시 불꽃 이펙트
- 애니메이션: 돌진 전 "CHECK!" 표시

### 3.2 Caiso (최종 보스)

**외형:**
- 거대한 그림자 괴물 (화면의 1/3 차지)
- 비정상적으로 큰 입 (부서진 체스판과 책 소용돌이)
- 체스 시계 형태의 눈 (째깍째깍 움직임)
- 몸체는 불분명한 그림자, 촉수처럼 퍼짐

**색상:**
- 주 색상: 깊은 보라/검정
- 입 내부: 붉은 소용돌이
- 눈: 빛나는 노란색 시계

---

## 4. 배경 디자인

### 4.1 The Infinite Scriptorium

**Layer 1 - 전경 (상호작용 가능)**
- 튀어나온 책들 (발판)
- 체스판 바닥 타일
- 흔들리는 촛불

**Layer 2 - 중경**
- 거대한 책장들 (수직으로 솟음)
- 떠다니는 책들
- 사다리, 계단

**Layer 3 - 후경**
- 끝없이 뻗은 책장 실루엣
- 높은 창문에서 들어오는 빛줄기
- 먼지 입자 파티클

**특수 효과:**
- 갓레이 (God Rays): 황금빛 빛줄기
- 먼지 파티클: 천천히 떠다니는 입자
- 책 플러터: 책장에서 펄럭이는 페이지

### 4.2 환경 기믹 디자인

**Sliding Shelf**
- 책장에서 튀어나오는 거대한 책
- 표지에 제목 (장식용)
- 일정 주기로 들어갔다 나옴

**Chess Timer Platform**
- 흑백 체스 타일 발판
- 위에 디지털 카운트다운 표시
- 0이 되면 붉게 변하며 사라짐

**Checkered Floor Hazard**
- 체스판 패턴 바닥
- 번갈아 가며 투명해지는 타일
- 타이밍 맞춰 이동해야 함

---

## 5. UI 디자인

### 5.1 HUD
```
┌────────────────────────────────────────┐
│ [♥][♥][♥]    SCORE: 00000    [🏆]x3  │
│ [무기 아이콘]                STAGE 1-1 │
└────────────────────────────────────────┘
```

- HP: 하트 아이콘 (빨간색, 빈 하트는 회색)
- 무기: 현재 장착 무기 썸네일
- 점수: 픽셀 폰트 숫자
- 코인/수집품: 황금 아이콘

### 5.2 메뉴 스타일
- 배경: 펼쳐진 고서적 페이지
- 버튼: 양피지 느낌의 둥근 사각형
- 폰트: 고딕/세리프 스타일 픽셀 폰트
- 선택 효과: 황금빛 글로우

---

## 6. AI 이미지 생성 프롬프트

### 6.1 주인공 스프라이트
```
"2D pixel art game character sprite sheet of an 11-year-old Asian boy
named Jay. He wears round black glasses, a loose mint-green knit vest
over a white shirt, brown shorts, and carries a worn leather satchel.
His black hair is messy. He holds a glowing golden chess pawn weapon.
Style: 16-bit retro pixel art, limited color palette, transparent
background. Views: idle, running, jumping, attacking, hurt.
Resolution: 32x48 pixels per frame."
```

### 6.2 적 스프라이트
```
"2D pixel art enemy sprite sheet: A living stone chess Pawn with no
face, only glowing red cracks. Ancient runes are carved on its body.
Dark gray stone texture. Style: 16-bit retro pixel art, menacing but
cartoonish, transparent background. Include: idle (2 frames), walking
(4 frames), hurt (1 frame). Size: 24x32 pixels."
```

### 6.3 배경
```
"2D platformer game background: The Infinite Scriptorium. Massive
wooden bookshelves stretching vertically into darkness. Giant hardcover
books protrude to form platforms. Polished black and white marble
chessboard floor. Golden god rays streaming from high windows. Dusty
atmosphere with floating particles. Style: detailed pixel art,
parallax-ready layers, warm brown and gold colors with cool black/white
chess elements. Resolution: 1280x720."
```

### 6.4 보스 (Caiso)
```
"2D game boss concept art: Caiso, a colossal shadow monster. Dominant
feature is an enormous cavernous mouth filled with swirling broken
chess pieces and torn book pages. Eyes resemble ticking mechanical
chess clocks with glowing yellow hands. Body is made of writhing
shadows with tentacle-like extensions. Style: dark fantasy pixel art,
terrifying but stylized. Colors: deep purple, black shadows, red
glowing mouth, yellow clock eyes. Size: Large, occupies 1/3 of screen."
```

---

## 7. 이펙트 & 파티클

### 7.1 공격 이펙트
- **무기 스윙**: 반원형 흔적, 황금빛
- **피격**: 별 모양 스파크, 흰색
- **치명타**: 큰 폭발 이펙트, 금+빨강

### 7.2 환경 이펙트
- **먼지**: 작은 원형 입자, 천천히 부유
- **빛줄기**: 대각선 그라데이션, 반투명
- **마법**: 빛나는 룬 문자, 파란색

### 7.3 UI 이펙트
- **데미지**: 화면 흔들림 + 빨간 플래시
- **레벨업**: 황금빛 광선 폭발
- **수집**: 작은 별 파티클 상승
