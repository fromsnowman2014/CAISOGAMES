# Caiso Mario - 이미지 생성 가이드 (Image Generation Guide)

## 1. 개요

이 문서는 Caiso Mario 게임의 모든 그래픽 에셋을 image_generator를 사용하여 생성하기 위한 상세 가이드입니다.

### 1.1 생성 도구
```bash
# CLI 명령어
python scripts/generate_asset.py [type] "[prompt]" [name] [options]

# 타입: sprite, background, image
# 옵션: --size WxH, --style [pixel_art|cartoon|realistic]
```

### 1.2 Python API
```python
from image_generator import ImageGeneratorService
import asyncio

async def generate_sprite(prompt, name, size=(64, 64)):
    service = ImageGeneratorService()
    print(f"Generator: {service.generator_type}")

    image = await service.generate(
        prompt=prompt,
        width=512,  # 고해상도로 생성
        height=512,
        style='pixel_art'
    )

    # 저장
    output_path = f"games/caiso-mario/assets/sprites/{name}.png"
    image.save(output_path)
    print(f"Saved: {output_path}")

    return output_path

# 실행
asyncio.run(generate_sprite("pixel art hero", "player_idle"))
```

---

## 2. 캐릭터 스프라이트

### 2.1 주인공: Jay Oh

#### 기본 정보
| 속성 | 값 |
|------|-----|
| 스프라이트 크기 | 32x48 픽셀 |
| 색상 수 | 16색 이하 |
| 스타일 | 16-bit SNES 레트로 |
| 배경 | 투명 |

#### 프롬프트 템플릿
```
베이스 설명:
"11-year-old Asian boy, round black glasses, light green knit vest over white shirt, brown shorts, worn leather backpack, messy black hair"

스타일 설명:
"16-bit pixel art style, limited color palette, clean pixels, no anti-aliasing, transparent background"
```

#### 상세 프롬프트

**Idle (대기) - 4프레임**
```bash
# Frame 1: 기본 서있기
python scripts/generate_asset.py sprite \
  "2D pixel art game character, 11-year-old Asian boy standing idle, round black glasses, light green knit vest over white shirt, brown shorts, leather backpack, arms relaxed at sides, looking forward, 16-bit retro style, clean pixels, transparent background" \
  jay_idle_01 --size 32x48

# Frame 2: 숨쉬기 (가슴 올라감)
python scripts/generate_asset.py sprite \
  "2D pixel art, same boy character, idle breathing pose, chest slightly raised, subtle pose shift, 16-bit style, transparent background" \
  jay_idle_02 --size 32x48

# Frame 3: 눈 깜빡임
python scripts/generate_asset.py sprite \
  "2D pixel art, same boy character, eyes closed blinking, neutral pose, 16-bit style, transparent background" \
  jay_idle_03 --size 32x48

# Frame 4: 원래 포즈로
python scripts/generate_asset.py sprite \
  "2D pixel art, same boy character, returning to neutral idle pose, 16-bit style, transparent background" \
  jay_idle_04 --size 32x48
```

**Run (달리기) - 8프레임**
```bash
# Frame 1
python scripts/generate_asset.py sprite \
  "2D pixel art running animation, Asian boy with glasses and green vest, frame 1 of 8, right leg forward stride, left arm swinging forward, body leaning forward, dynamic running pose, 16-bit style, transparent background" \
  jay_run_01 --size 32x48

# Frame 2
python scripts/generate_asset.py sprite \
  "2D pixel art running animation, same character, frame 2, right foot planted pushing off ground, left leg rising behind, momentum forward, 16-bit style, transparent background" \
  jay_run_02 --size 32x48

# Frame 3
python scripts/generate_asset.py sprite \
  "2D pixel art running animation, same character, frame 3, mid-air moment, both legs tucked under body, peak of running cycle, 16-bit style, transparent background" \
  jay_run_03 --size 32x48

# Frame 4
python scripts/generate_asset.py sprite \
  "2D pixel art running animation, same character, frame 4, left leg reaching forward, right arm swinging forward, preparing to land, 16-bit style, transparent background" \
  jay_run_04 --size 32x48

# Frame 5-8: 반대쪽 반복 (mirror of 1-4)
# ... 동일 패턴으로 좌우 반전
```

**Jump (점프) - 2프레임**
```bash
# 상승
python scripts/generate_asset.py sprite \
  "2D pixel art jump pose, Asian boy with glasses jumping upward, arms raised above head reaching up, legs bent beneath, looking upward with determined expression, upward momentum, 16-bit style, transparent background" \
  jay_jump_01 --size 32x48

# 하강
python scripts/generate_asset.py sprite \
  "2D pixel art falling pose, same character descending through air, arms spread outward for balance, legs dangling, looking slightly downward, falling momentum, 16-bit style, transparent background" \
  jay_fall_01 --size 32x48
```

**Attack (공격) - 4프레임**
```bash
# Frame 1: 준비
python scripts/generate_asset.py sprite \
  "2D pixel art attack windup, Asian boy with glasses, holding glowing golden chess pawn weapon behind shoulder, preparing to swing, determined expression, 16-bit style, transparent background" \
  jay_attack_01 --size 40x48

# Frame 2: 스윙 중
python scripts/generate_asset.py sprite \
  "2D pixel art attack mid-swing, same character, golden pawn weapon at head level moving forward, motion blur effect, intense expression, 16-bit style, transparent background" \
  jay_attack_02 --size 40x48

# Frame 3: 풀 스윙
python scripts/generate_asset.py sprite \
  "2D pixel art attack full extension, same character, golden pawn weapon extended forward, golden arc trail effect, attack climax, 16-bit style, transparent background" \
  jay_attack_03 --size 40x48

# Frame 4: 복귀
python scripts/generate_asset.py sprite \
  "2D pixel art attack follow-through, same character, weapon lowering, golden particles dispersing, returning to stance, 16-bit style, transparent background" \
  jay_attack_04 --size 40x48
```

**Hurt (피격) - 2프레임**
```bash
python scripts/generate_asset.py sprite \
  "2D pixel art hurt reaction, Asian boy with glasses recoiling from hit, eyes shut tight, body tilted backward, pained expression, impact effect, 16-bit style, transparent background" \
  jay_hurt_01 --size 32x48
```

---

### 2.2 적: Stone Pawn

#### 기본 정보
| 속성 | 값 |
|------|-----|
| 스프라이트 크기 | 24x32 픽셀 |
| 색상 | 회색/빨강 (균열) |
| 특징 | 얼굴 없음, 룬 문자 |

#### 프롬프트

**Idle & Walk**
```bash
# Idle
python scripts/generate_asset.py sprite \
  "2D pixel art enemy sprite, living stone chess Pawn piece, dark gray cracked stone texture, glowing red runes carved on body, no face only two glowing red cracks for eyes, menacing but cartoonish, floating stone debris, 16-bit style, transparent background" \
  pawn_idle_01 --size 24x32

# Walk frames
python scripts/generate_asset.py sprite \
  "2D pixel art walking animation, stone chess pawn enemy, slight body tilt forward, one side raised as if stepping, glowing red cracks, 16-bit style, transparent background" \
  pawn_walk_01 --size 24x32
```

---

### 2.3 적: Jumping Knight

```bash
# Idle
python scripts/generate_asset.py sprite \
  "2D pixel art enemy sprite, dark chess Knight piece come to life, horse-head shape with black metallic armor, glowing orange eyes in horse head, pointed ears like horns, rust spots on segmented body, standing pose, intimidating, 16-bit style, transparent background" \
  knight_idle_01 --size 32x40

# Charge (점프 준비)
python scripts/generate_asset.py sprite \
  "2D pixel art, same dark knight enemy, crouching pose, legs bent deeply, about to jump, energy gathering, orange glow intensifying, 16-bit style, transparent background" \
  knight_charge_01 --size 32x40

# Jump (공중)
python scripts/generate_asset.py sprite \
  "2D pixel art, same knight enemy mid-jump, L-shape trajectory pose, legs tucked, moving through air, dynamic action pose, 16-bit style, transparent background" \
  knight_jump_01 --size 32x40

# Stun (기절)
python scripts/generate_asset.py sprite \
  "2D pixel art, same knight enemy stunned after landing, dazed pose, stars circling head, wobbly stance, vulnerable, 16-bit style, transparent background" \
  knight_stun_01 --size 32x40
```

---

### 2.4 적: Sniper Bishop

```bash
# Idle (부유)
python scripts/generate_asset.py sprite \
  "2D pixel art enemy sprite, sinister chess Bishop piece floating, tall pointed hat, tattered purple and black robes, no face under hood only glowing purple slit, holding golden staff with crystal orb, mystical aura, 16-bit style, transparent background" \
  bishop_idle_01 --size 28x44

# Aim (조준)
python scripts/generate_asset.py sprite \
  "2D pixel art, same bishop enemy, aiming pose, staff pointed forward, glowing purple energy gathering at crystal orb, targeting laser line, intense magical glow, 16-bit style, transparent background" \
  bishop_aim_01 --size 28x44

# Shoot (발사)
python scripts/generate_asset.py sprite \
  "2D pixel art, same bishop enemy, shooting pose, purple magical projectile launching from staff, recoil motion, energy burst, 16-bit style, transparent background" \
  bishop_shoot_01 --size 28x44
```

---

### 2.5 적: Charging Rook

```bash
# Idle
python scripts/generate_asset.py sprite \
  "2D pixel art enemy sprite, massive chess Rook piece, castle tower shape, polished black marble with gold decorative trim, crenellated top battlements, large glowing red window as eye, heavy solid appearance, 16-bit style, transparent background" \
  rook_idle_01 --size 36x36

# Warning ("CHECK!")
python scripts/generate_asset.py sprite \
  "2D pixel art, same rook enemy, warning pose, red glow intensifying, exclamation mark above, about to charge, menacing, 16-bit style, transparent background" \
  rook_warning_01 --size 36x36

# Charge (돌진)
python scripts/generate_asset.py sprite \
  "2D pixel art, same rook enemy charging forward at high speed, motion blur, fire/energy trail behind, unstoppable momentum, 16-bit style, transparent background" \
  rook_charge_01 --size 36x36

# Stun (기절)
python scripts/generate_asset.py sprite \
  "2D pixel art, same rook enemy after wall collision, cracked surface, dizzy stars, tilted, vulnerable, 16-bit style, transparent background" \
  rook_stun_01 --size 36x36
```

---

### 2.6 보스: Caiso

```bash
# Main sprite
python scripts/generate_asset.py sprite \
  "2D pixel art boss character, Caiso the shadow monster, enormous gaping mouth filled with swirling broken chess pieces and torn book pages, two mechanical chess clock faces as eyes with ticking hands and glowing yellow numbers, body made of writhing dark purple and black shadows with tentacle extensions, terrifying but stylized for kids game, detailed 16-bit pixel art, transparent background" \
  caiso_main --size 192x160

# Attack pose
python scripts/generate_asset.py sprite \
  "2D pixel art, Caiso boss attacking, shadow tentacles reaching forward aggressively, mouth open wider, chess pieces spewing out, intense red glow from within, 16-bit style, transparent background" \
  caiso_attack_01 --size 192x160

# Hurt
python scripts/generate_asset.py sprite \
  "2D pixel art, Caiso boss taking damage, recoiling, cracks of light appearing on shadow body, clock eyes spinning, 16-bit style, transparent background" \
  caiso_hurt_01 --size 192x160
```

---

## 3. 타일셋

### 3.1 지형 타일

```bash
# 나무 바닥 (책장)
python scripts/generate_asset.py sprite \
  "2D pixel art game tile, wooden bookshelf surface viewed from side as ground, dark mahogany wood texture with visible grain, decorative carving on front edge, seamless tileable, 16-bit style" \
  tile_ground_wood --size 32x32

# 책 플랫폼
python scripts/generate_asset.py sprite \
  "2D pixel art game tile, large closed hardcover book lying flat as platform, deep red leather cover with gold embossed decorations, yellowed page edges visible, seamless tileable, 16-bit style" \
  tile_platform_book --size 32x16

# 흰 체스 타일
python scripts/generate_asset.py sprite \
  "2D pixel art game tile, white marble chess board square, polished surface with subtle veining, slight 3D depth with darker edges, 16-bit style" \
  tile_chess_white --size 32x32

# 검은 체스 타일
python scripts/generate_asset.py sprite \
  "2D pixel art game tile, black marble chess board square, polished obsidian surface, subtle reflection, 3D depth with lighter edge highlights, 16-bit style" \
  tile_chess_black --size 32x32
```

---

## 4. 배경

### 4.1 패럴랙스 레이어

```bash
# Far (가장 먼 배경)
python scripts/generate_asset.py background \
  "2D pixel art game background, infinite library far background, silhouettes of massive bookshelves fading into darkness, warm golden light rays from high windows, dusty atmospheric perspective, very low detail mood focused, deep browns warm golds soft shadows, 16-bit style" \
  bg_scriptorium_far --size 960x540

# Mid (중간 배경)
python scripts/generate_asset.py background \
  "2D pixel art game background, library middle ground, medium-detail wooden bookshelves with visible books, floating dust particles, ladders and walkways, some protruding books, rich browns burgundy books gold accents, 16-bit style" \
  bg_scriptorium_mid --size 1280x540

# Near (가까운 배경)
python scripts/generate_asset.py background \
  "2D pixel art game background, library foreground decorative, detailed bookshelf edges, candle sconces with flames, hanging chains, decorative scrollwork, dark wood warm flames metallic gold, 16-bit style" \
  bg_scriptorium_near --size 1920x540
```

---

## 5. UI 요소

```bash
# 하트 (풀)
python scripts/generate_asset.py sprite \
  "2D pixel art UI icon, red heart health indicator full, glossy cartoon style with highlight, clear silhouette, 16-bit style, transparent background" \
  ui_heart_full --size 20x20

# 하트 (빈)
python scripts/generate_asset.py sprite \
  "2D pixel art UI icon, empty heart outline, gray dark outline only hollow inside, matches full heart shape, 16-bit style, transparent background" \
  ui_heart_empty --size 20x20

# 코인
python scripts/generate_asset.py sprite \
  "2D pixel art UI icon, golden coin collectible, circular with embossed star, shiny with highlight, 16-bit style, transparent background" \
  ui_coin --size 16x16
```

---

## 6. 이펙트

```bash
# 타격 스파크
python scripts/generate_asset.py sprite \
  "2D pixel art effect sprite, impact spark for weapon hits, star-burst shape white center fading to yellow then orange, 4-point star with particles, 16-bit style, transparent background" \
  fx_hit_spark --size 32x32

# 먼지 구름
python scripts/generate_asset.py sprite \
  "2D pixel art effect sprite, small dust puff cloud for landing, soft beige brown circular cloud, semi-transparent edges, 16-bit style, transparent background" \
  fx_dust_cloud --size 24x16

# 마법 발사체
python scripts/generate_asset.py sprite \
  "2D pixel art effect sprite, purple magic orb projectile, glowing purple sphere darker core lighter edges, trailing particles, magical crackling energy, 16-bit style, transparent background" \
  fx_magic_projectile --size 16x16
```

---

## 7. 배치 생성 스크립트

### 7.1 전체 에셋 생성 스크립트

```python
#!/usr/bin/env python3
"""
Caiso Mario 전체 에셋 생성 스크립트
"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from image_generator import ImageGeneratorService

# 에셋 정의
ASSETS = {
    "sprites/player": [
        ("jay_idle_01", "2D pixel art, 11yo Asian boy, green vest, glasses, idle pose, 16-bit, transparent bg"),
        ("jay_run_01", "2D pixel art, same boy running, leg forward, 16-bit, transparent bg"),
        ("jay_jump_01", "2D pixel art, same boy jumping upward, arms up, 16-bit, transparent bg"),
        ("jay_attack_01", "2D pixel art, same boy swinging golden pawn weapon, 16-bit, transparent bg"),
    ],
    "sprites/enemies": [
        ("pawn_idle_01", "2D pixel art, stone chess pawn enemy, gray, red glowing cracks, 16-bit, transparent bg"),
        ("knight_idle_01", "2D pixel art, dark chess knight enemy, horse head, armor, 16-bit, transparent bg"),
        ("bishop_idle_01", "2D pixel art, chess bishop enemy, purple robes, glowing staff, 16-bit, transparent bg"),
        ("rook_idle_01", "2D pixel art, chess rook enemy, black marble tower, red eye, 16-bit, transparent bg"),
    ],
    "tiles": [
        ("ground_wood", "2D pixel art tile, wooden bookshelf ground, mahogany, 16-bit"),
        ("chess_white", "2D pixel art tile, white marble chess square, 16-bit"),
        ("chess_black", "2D pixel art tile, black marble chess square, 16-bit"),
    ],
}

async def generate_all():
    service = ImageGeneratorService()
    print(f"Using generator: {service.generator_type}")

    base_path = "games/caiso-mario/assets"

    for folder, assets in ASSETS.items():
        folder_path = f"{base_path}/{folder}"
        os.makedirs(folder_path, exist_ok=True)

        for name, prompt in assets:
            try:
                print(f"Generating: {name}...")
                image = await service.generate(prompt, width=512, height=512, style='pixel_art')
                image.save(f"{folder_path}/{name}.png")
                print(f"  ✓ Saved: {folder_path}/{name}.png")

                # Rate limit 방지
                await asyncio.sleep(2)

            except Exception as e:
                print(f"  ✗ Failed: {name} - {e}")
                continue

if __name__ == "__main__":
    asyncio.run(generate_all())
```

---

## 8. 문제 해결

### 8.1 일반적인 오류

| 오류 | 원인 | 해결 |
|------|------|------|
| `GeneratorError: GEMINI_API_KEY is required` | API 키 없음 | `export VERCEL_APP_URL=...` 설정 |
| `APIError: 403` | 네트워크 차단 | Vercel 프록시 확인 |
| `RateLimitError` | 요청 과다 | 2-5초 대기 후 재시도 |
| `GeneratorError: No image generated` | 프롬프트 필터링 | 표현 수정, 단순화 |

### 8.2 Mock 모드 사용
```bash
# 실제 생성이 안 될 때
export USE_MOCK_GENERATOR=true
python scripts/generate_asset.py sprite "test" test_sprite

# 플레이스홀더 이미지가 생성됨
# 나중에 실제 이미지로 교체
```

### 8.3 수동 대안
- Piskel (온라인 픽셀 아트 에디터): https://www.piskelapp.com/
- Aseprite (데스크톱 앱)
- GIMP + 픽셀 아트 브러시

---

*가이드 버전: 1.0*
*최종 수정: 2026-02-04*
