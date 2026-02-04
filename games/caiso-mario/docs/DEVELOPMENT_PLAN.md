# Caiso Mario - 개발 계획서 (Development Plan)

## 1. 프로젝트 개요

### 1.1 게임 정보
- **게임명**: Caiso Mario - Chess Platformer
- **장르**: 2D 플랫포머 + 전략
- **타겟**: 8-14세 어린이
- **플랫폼**: 웹 브라우저 (HTML5 Canvas)

### 1.2 메인 페이지 통합
이 게임은 CAISOGAMES 플랫폼의 **두 번째 게임**으로 등록됩니다.

```
메인 페이지 (index.html) 수정 사항:
├── Featured Game: Feeding Caiso (기존 유지)
├── Game Grid:
│   ├── Slot 1: Feeding Caiso ✓
│   ├── Slot 2: Caiso Mario ★ (신규 추가)
│   ├── Slot 3: Coming Soon
│   └── Slots 4-6: Empty
```

**통합 작업 체크리스트:**
- [ ] 메인 페이지에 Caiso Mario 카드 추가
- [ ] 게임 썸네일 SVG/이미지 생성
- [ ] 링크 연결: `/games/caiso-mario/`
- [ ] Coming Soon을 Slot 3으로 이동

---

## 2. 이미지 생성 전략 (Image Generation Strategy)

### 2.1 image_generator 사용 정책

#### 환경 설정
```bash
# 개발 환경 설정 (Claude Code에서)
export VERCEL_APP_URL=https://caisogames.vercel.app
export USE_MOCK_GENERATOR=false  # 실제 생성 사용

# 테스트/디버깅 시
export USE_MOCK_GENERATOR=true   # 플레이스홀더 사용
```

#### 생성 우선순위
| 순위 | 에셋 유형 | 파일 수 | 중요도 |
|------|----------|---------|--------|
| 1 | 주인공 스프라이트 | 20+ | 필수 |
| 2 | 적 스프라이트 | 16+ | 필수 |
| 3 | 타일/플랫폼 | 8+ | 필수 |
| 4 | 배경 레이어 | 4+ | 높음 |
| 5 | UI 요소 | 10+ | 높음 |
| 6 | 이펙트/파티클 | 8+ | 중간 |
| 7 | 보스 (Caiso) | 8+ | 필수 |

### 2.2 디버깅 정책 (Debugging Policy)

#### 이미지 생성 실패 시 대응 절차

```
[이미지 생성 시도]
        │
        ▼
   ┌─────────┐
   │ 성공?   │──Yes──▶ 에셋 저장 & 계속
   └─────────┘
        │ No
        ▼
┌──────────────────┐
│ 오류 유형 확인   │
└──────────────────┘
        │
   ┌────┴────┬─────────┬─────────┐
   ▼         ▼         ▼         ▼
[403/네트워크] [429/속도제한] [400/프롬프트] [500/서버]
   │         │         │         │
   ▼         ▼         ▼         ▼
Vercel 확인  대기 후   프롬프트   API 상태
& 재배포    재시도    수정       확인
```

#### 오류별 해결 방법

**1. 403 Forbidden (네트워크 차단)**
```bash
# 증상: Claude Code 환경에서 직접 API 호출 불가
# 해결: Vercel 프록시 사용 확인
echo $VERCEL_APP_URL  # URL 설정 확인

# Vercel 배포 상태 확인
curl -I https://caisogames.vercel.app/api/generate-image

# 재배포 필요 시
git push origin claude/ready-CjaAA
# Vercel에서 자동 배포 대기
```

**2. 429 Rate Limit (속도 제한)**
```python
# 증상: 너무 많은 요청으로 일시 차단
# 해결: 지수 백오프 적용
import asyncio

async def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await service.generate(prompt)
        except RateLimitError:
            wait_time = 2 ** attempt * 10  # 10s, 20s, 40s
            print(f"Rate limited. Waiting {wait_time}s...")
            await asyncio.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

**3. 400 Bad Request (프롬프트 문제)**
```
# 증상: 프롬프트가 필터링되거나 형식 오류
# 해결: 프롬프트 단순화 및 안전한 표현 사용

# 피해야 할 표현:
- 폭력적인 묘사
- 특정 브랜드/캐릭터 언급 (Mario, Nintendo 등)
- 너무 복잡한 다중 요청

# 권장 형식:
"2D pixel art game sprite, [주제], [스타일], transparent background"
```

**4. Mock 모드 폴백**
```bash
# 실제 생성이 계속 실패할 경우
export USE_MOCK_GENERATOR=true

# 플레이스홀더로 개발 진행 후
# 나중에 실제 이미지로 교체
```

### 2.3 에셋 파일 관리

```
games/caiso-mario/assets/
├── sprites/
│   ├── player/
│   │   ├── jay_idle_01.png
│   │   ├── jay_idle_02.png
│   │   ├── jay_run_01.png ~ jay_run_08.png
│   │   ├── jay_jump_01.png
│   │   ├── jay_fall_01.png
│   │   └── jay_attack_01.png ~ jay_attack_04.png
│   ├── enemies/
│   │   ├── pawn_idle_01.png ~ pawn_walk_04.png
│   │   ├── knight_idle_01.png ~ knight_jump_04.png
│   │   ├── bishop_idle_01.png ~ bishop_aim_03.png
│   │   └── rook_idle_01.png ~ rook_charge_06.png
│   ├── weapons/
│   │   ├── pawn_weapon.png
│   │   ├── knight_weapon.png
│   │   ├── bishop_weapon.png
│   │   └── rook_weapon.png
│   └── effects/
│       ├── hit_spark.png
│       ├── dust_cloud.png
│       └── magic_glow.png
├── backgrounds/
│   ├── scriptorium_far.png
│   ├── scriptorium_mid.png
│   └── scriptorium_near.png
├── tiles/
│   ├── ground_wood.png
│   ├── platform_book.png
│   ├── chess_white.png
│   └── chess_black.png
└── ui/
    ├── heart_full.png
    ├── heart_empty.png
    ├── coin.png
    └── button_*.png
```

---

## 3. 상세 이미지 생성 프롬프트

### 3.1 주인공 (Jay Oh) 스프라이트

#### 기본 캐릭터 시트
```
Prompt: "2D pixel art character sprite sheet of an 11-year-old Asian boy game character. He wears round black-framed glasses, a loose light green knit vest over a white collared shirt, brown knee-length shorts, and brown leather shoes. His black hair is slightly messy. He carries a small worn leather backpack. Art style: 16-bit retro SNES era, clean pixels, limited color palette of 16 colors maximum. The character should look determined but friendly. Include front-facing idle pose. Transparent background. Resolution: 32x48 pixels."

파일명: jay_idle_base.png
크기: 32x48 픽셀
```

#### Idle 애니메이션 (4 프레임)
```
Frame 1: "...idle pose, standing straight, arms at sides..."
Frame 2: "...idle pose, slight breathing motion, chest raised..."
Frame 3: "...idle pose, eyes blinking..."
Frame 4: "...idle pose, returning to neutral..."
```

#### Run 애니메이션 (8 프레임)
```
Prompt Template:
"2D pixel art running animation frame [N] of 8 for the same boy character (green vest, glasses, backpack). Frame [N]: [동작 설명]. Maintain consistent character proportions and style. Transparent background. 32x48 pixels."

Frame 1: "right leg forward, left arm forward, body leaning"
Frame 2: "right leg planted, pushing off, left leg rising"
Frame 3: "airborne moment, both legs tucked"
Frame 4: "left leg reaching forward, right arm forward"
Frame 5: "left leg planted, pushing off"
Frame 6: "right leg swinging forward"
Frame 7: "right foot about to land"
Frame 8: "transition back to frame 1"
```

#### Jump 애니메이션 (2 프레임)
```
Jump Rising:
"2D pixel art jump pose, boy character (green vest, glasses) in upward jump motion. Arms raised above head, legs slightly bent, looking upward with determined expression. Dynamic pose showing upward momentum. Transparent background. 32x48 pixels."

Jump Falling:
"2D pixel art falling pose, same character descending. Arms spread for balance, legs dangling, looking downward. Showing downward momentum. Transparent background. 32x48 pixels."
```

#### Attack 애니메이션 (4 프레임)
```
Prompt Template:
"2D pixel art attack animation frame [N] for boy character (green vest, glasses). He swings a glowing golden chess pawn weapon. Frame [N]: [동작]. The pawn weapon glows with magical golden aura. Transparent background. 40x48 pixels (wider for weapon swing)."

Frame 1: "wind-up pose, weapon pulled back behind shoulder"
Frame 2: "mid-swing, weapon at head level, motion blur effect"
Frame 3: "full extension, weapon pointing forward, golden arc trail"
Frame 4: "follow-through, weapon lowering, particles dispersing"
```

### 3.2 적 캐릭터 스프라이트

#### Stone Pawn (기본 적)
```
Prompt: "2D pixel art enemy sprite: A living stone chess Pawn piece as a game enemy. The pawn is made of dark gray cracked stone with ancient glowing red runes carved into its surface. It has no face - only two glowing red cracks where eyes would be. Small floating stone debris around it. Menacing but cartoonish style. Art style: 16-bit pixel art, limited palette. Transparent background. Size: 24x32 pixels."

파일명: pawn_idle_01.png
변형: pawn_walk_01~04.png, pawn_hurt.png
```

#### Jumping Knight (점프 적)
```
Prompt: "2D pixel art enemy sprite: A dark chess Knight piece come to life. Horse-head shaped with metallic black armor texture. Glowing orange eyes in the horse head. Pointed ears like horns. Body is segmented dark metal with rust spots. Crouching pose ready to jump. Intimidating but stylized game enemy look. Art style: 16-bit pixel art. Transparent background. Size: 32x40 pixels."

변형:
- knight_idle_01.png (기본)
- knight_charge_01~03.png (점프 준비)
- knight_jump_01~04.png (공중)
- knight_land_01.png (착지)
- knight_stun_01.png (기절)
```

#### Sniper Bishop (원거리 적)
```
Prompt: "2D pixel art enemy sprite: A sinister chess Bishop piece as a magic-casting enemy. Tall pointed hat/top, body wrapped in tattered purple and black robes. No visible face under the hood - only a glowing purple slit. Holds a golden staff with a glowing crystal orb at top. Mystical and threatening appearance. Art style: 16-bit pixel art. Transparent background. Size: 28x44 pixels."

변형:
- bishop_idle_01~02.png (부유하는 애니메이션)
- bishop_aim_01~03.png (조준 중, 빛나는 효과 증가)
- bishop_shoot_01.png (발사)
- bishop_retreat_01~02.png (후퇴)
```

#### Charging Rook (돌진 적)
```
Prompt: "2D pixel art enemy sprite: A massive chess Rook piece as a heavy enemy. Castle tower shape made of polished black marble with gold decorative trim. Crenellated top (battlements). A large glowing red window in the center acts as its 'eye'. Heavy and solid appearance. Small cracks with red glow. Art style: 16-bit pixel art. Transparent background. Size: 36x36 pixels."

변형:
- rook_idle_01~02.png (대기)
- rook_warning_01.png ("CHECK!" 텍스트 포함)
- rook_charge_01~06.png (돌진, 불꽃 효과)
- rook_wall_hit_01.png (벽 충돌)
- rook_stun_01~02.png (기절, 별 이펙트)
```

### 3.3 보스: Caiso

```
Prompt: "2D pixel art boss character: Caiso, a massive shadow monster boss. Dominant feature is an enormous gaping mouth filled with swirling broken chess pieces and torn book pages. The mouth takes up most of its body. Two mechanical chess clock faces serve as eyes above the mouth, with ticking hands and glowing yellow numbers. Body is made of writhing dark purple and black shadows with tentacle-like extensions reaching outward. Terrifying but stylized for a children's game. Art style: detailed 16-bit pixel art. Size: 192x160 pixels (large boss). Dark purple, black, red glow from mouth, yellow clock eyes."

변형:
- caiso_idle_01~04.png (입에서 소용돌이)
- caiso_roar_01~03.png (포효, 입 더 크게)
- caiso_attack_01~04.png (촉수 공격)
- caiso_summon_01~02.png (하수인 소환)
- caiso_hurt_01.png (피격)
- caiso_defeat_01~04.png (패배 애니메이션)
```

### 3.4 타일셋 & 배경

#### 지형 타일
```
Wood Bookshelf Ground:
"2D pixel art game tile: Wooden bookshelf surface viewed from side as ground platform. Dark mahogany wood texture with visible grain. Small decorative carvings on front edge. Seamless tileable horizontally. Art style: 16-bit pixel art. Size: 32x32 pixels."

Book Platform:
"2D pixel art game tile: A large closed hardcover book lying flat as a platform. Deep red leather cover with gold embossed decorations on spine. Yellowed page edges visible. Seamless for horizontal tiling. Art style: 16-bit pixel art. Size: 32x16 pixels."

Chess Tile White:
"2D pixel art game tile: White marble chess board square. Polished surface with subtle veining. Slight 3D depth effect with darker edges. Art style: 16-bit pixel art. Size: 32x32 pixels."

Chess Tile Black:
"2D pixel art game tile: Black marble chess board square. Polished obsidian-like surface. Subtle reflection. Slight 3D depth with lighter edge highlights. Art style: 16-bit pixel art. Size: 32x32 pixels."
```

#### 패럴랙스 배경
```
Far Background (Layer 3):
"2D pixel art game background layer: Infinite library far background. Silhouettes of massive bookshelves fading into darkness. Warm golden light rays streaming from unseen high windows. Dusty atmospheric perspective. Very low detail, mostly shapes and mood. Art style: 16-bit pixel art. Size: 960x540 pixels. Colors: deep browns, warm golds, soft shadows."

Mid Background (Layer 2):
"2D pixel art game background layer: Library middle ground. Medium-detail wooden bookshelves with visible books. Floating dust particles catching light. Ladders and walkways visible. Some books slightly protruding. Art style: 16-bit pixel art. Size: 1280x540 pixels (wider for parallax). Colors: rich browns, burgundy books, gold accents."

Near Background (Layer 1):
"2D pixel art game background layer: Library foreground decorative elements. Detailed bookshelf edges, candle sconces with flickering flames, hanging chains, decorative scrollwork. Will appear closest to player. Art style: 16-bit pixel art. Size: 1920x540 pixels (widest for parallax). Colors: dark wood, warm flame colors, metallic gold."
```

### 3.5 UI 요소

```
Heart Full:
"2D pixel art UI icon: Red heart health indicator, full/complete. Glossy cartoon style with highlight. Clear silhouette. Art style: 16-bit pixel art. Transparent background. Size: 20x20 pixels."

Heart Empty:
"2D pixel art UI icon: Empty heart health indicator outline. Gray/dark outline only, hollow inside. Matches full heart shape exactly. Art style: 16-bit pixel art. Transparent background. Size: 20x20 pixels."

Coin:
"2D pixel art UI icon: Golden coin collectible. Circular with embossed dollar sign or star. Shiny with highlight. Art style: 16-bit pixel art. Transparent background. Size: 16x16 pixels."

Weapon Icon - Pawn:
"2D pixel art UI icon: Small chess pawn piece icon for UI weapon display. Golden wood color with magical glow aura. Simple but recognizable. Art style: 16-bit pixel art. Transparent background. Size: 24x24 pixels."
```

### 3.6 이펙트 스프라이트

```
Hit Spark:
"2D pixel art effect sprite: Impact spark effect for weapon hits. Star-burst shape with white center fading to yellow then orange edges. 4-point star with smaller particles. Art style: 16-bit pixel art. Transparent background. Size: 32x32 pixels."

Dust Cloud:
"2D pixel art effect sprite: Small dust puff for landing/running. Soft beige/brown circular cloud shape. Semi-transparent edges. Art style: 16-bit pixel art. Transparent background. Size: 24x16 pixels."

Magic Projectile:
"2D pixel art effect sprite: Purple magic orb projectile. Glowing purple sphere with darker core, lighter edges. Small trailing particles. Magical energy crackling effect. Art style: 16-bit pixel art. Transparent background. Size: 16x16 pixels."
```

---

## 4. 개발 단계 (Development Phases)

### Phase 1: 기반 구축 ✓
- [x] 문서 작성 (PRD, 기술 설계, 아트 가이드)
- [x] 게임 폴더 구조 생성
- [x] 기본 게임 엔진 구현 (물리, 충돌)
- [x] 프로시저럴 스프라이트로 프로토타입

### Phase 2: 에셋 생성 (현재)
- [ ] image_generator 연결 테스트
- [ ] 주인공 스프라이트 생성 (20개)
- [ ] 적 스프라이트 생성 (16개)
- [ ] 타일셋 생성 (8개)
- [ ] 배경 생성 (4개)
- [ ] UI 요소 생성 (10개)

### Phase 3: 게임 통합
- [ ] 생성된 에셋을 게임에 적용
- [ ] 애니메이션 시스템 연결
- [ ] 레벨 디자인 확장 (3개 월드)
- [ ] 보스전 구현

### Phase 4: 폴리싱
- [ ] 사운드 이펙트 추가
- [ ] 파티클 시스템 개선
- [ ] 게임 밸런스 조정
- [ ] 버그 수정

### Phase 5: 통합 & 배포
- [ ] 메인 페이지에 게임 카드 추가
- [ ] 반응형 디자인 테스트
- [ ] 모바일 터치 컨트롤 최적화
- [ ] 최종 테스트 & 커밋

---

## 5. 품질 기준 (Quality Standards)

### 5.1 성능 목표
- 60 FPS 유지 (중급 사양 기준)
- 초기 로딩 2초 이내
- 에셋 총 용량 5MB 이하

### 5.2 게임플레이 목표
- 스테이지당 플레이 시간: 2-3분
- 첫 플레이 완주율: 60% 이상
- 조작 반응 지연: 16ms 이하 (1프레임)

### 5.3 그래픽 품질
- 일관된 16-bit 픽셀 아트 스타일
- 모든 스프라이트 투명 배경
- 색상 팔레트 통일성 유지
- 애니메이션 부드러움 (최소 4프레임/동작)

---

## 6. 리스크 관리

| 리스크 | 확률 | 영향 | 대응 방안 |
|--------|------|------|-----------|
| API 생성 실패 | 중 | 높음 | Mock 모드 사용, 수동 에셋 제작 |
| 스타일 불일치 | 높음 | 중 | 프롬프트 반복 조정, 후처리 |
| 성능 저하 | 낮음 | 중 | 에셋 최적화, 로딩 분할 |
| 모바일 호환성 | 중 | 중 | 터치 컨트롤 별도 테스트 |

---

## 7. 일정 (Timeline)

| 주차 | 목표 | 산출물 |
|------|------|--------|
| Week 1 | 문서화 + 프로토타입 | 기본 게임 동작 |
| Week 2 | 에셋 생성 | 모든 스프라이트/타일 |
| Week 3 | 레벨 구축 | 3개 월드, 보스전 |
| Week 4 | 폴리싱 + 배포 | 최종 버전 |

---

*문서 버전: 1.0*
*최종 수정: 2026-02-04*
