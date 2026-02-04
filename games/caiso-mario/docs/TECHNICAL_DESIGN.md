# Caiso Mario - Technical Design Document

## 1. 아키텍처 개요

### 1.1 기술 스택
- **렌더링**: HTML5 Canvas 2D API
- **언어**: Vanilla JavaScript (ES6+)
- **번들링**: 단일 HTML 파일 (인라인)
- **에셋**: PNG 스프라이트, AI 생성 이미지

### 1.2 게임 아키텍처
```
┌─────────────────────────────────────────────────────┐
│                    Game Loop                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  Input   │→ │  Update  │→ │     Render       │  │
│  │ Handler  │  │  Logic   │  │     Engine       │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────┘
         ↓              ↓              ↓
   ┌─────────┐   ┌───────────┐  ┌────────────┐
   │ Keyboard│   │  Physics  │  │  Sprite    │
   │ Manager │   │  Engine   │  │  Manager   │
   └─────────┘   └───────────┘  └────────────┘
         ↓              ↓              ↓
   ┌─────────┐   ┌───────────┐  ┌────────────┐
   │  Touch  │   │ Collision │  │  Camera    │
   │ Manager │   │  System   │  │  System    │
   └─────────┘   └───────────┘  └────────────┘
```

---

## 2. 물리 엔진 설계

### 2.1 마리오 스타일 물리 상수
```javascript
const PHYSICS = {
    // 중력 (Super Mario World 분석 기반)
    GRAVITY_HOLDING: 0.4,      // 점프 버튼 유지 시 (3.5g 근사)
    GRAVITY_FALLING: 0.9,      // 낙하 시 (6.9g 근사)

    // 속도 제한
    MAX_FALL_SPEED: 12,        // 종단 속도
    MAX_RUN_SPEED: 6,          // 최대 이동 속도
    MAX_SPRINT_SPEED: 8,       // 대시 시 최대 속도

    // 점프
    JUMP_FORCE: -14,           // 초기 점프 힘
    JUMP_CUT_MULTIPLIER: 0.5,  // 점프 취소 시 속도 감소

    // 수평 이동
    ACCELERATION: 0.5,         // 가속도
    DECELERATION: 0.3,         // 감속도
    AIR_CONTROL: 0.7,          // 공중 제어력 (지상의 70%)
    FRICTION: 0.85,            // 마찰 계수

    // 특수
    COYOTE_TIME: 6,            // 코요테 타임 (프레임)
    JUMP_BUFFER: 8,            // 점프 버퍼 (프레임)
    CORNER_CORRECTION: 4       // 모서리 보정 픽셀
};
```

### 2.2 가변 점프 시스템
```javascript
class VariableJump {
    update(player, input) {
        // 상승 중 점프 버튼 유지
        if (player.velocityY < 0 && input.jumpHeld) {
            player.velocityY += PHYSICS.GRAVITY_HOLDING;
        }
        // 하강 중 또는 점프 버튼 해제
        else {
            player.velocityY += PHYSICS.GRAVITY_FALLING;
        }

        // 점프 취소 (버튼 일찍 떼면)
        if (!input.jumpHeld && player.velocityY < 0) {
            player.velocityY *= PHYSICS.JUMP_CUT_MULTIPLIER;
        }

        // 종단 속도 제한
        player.velocityY = Math.min(player.velocityY, PHYSICS.MAX_FALL_SPEED);
    }
}
```

### 2.3 관성 기반 이동
```javascript
class InertiaMovement {
    update(player, input) {
        const acceleration = player.grounded
            ? PHYSICS.ACCELERATION
            : PHYSICS.ACCELERATION * PHYSICS.AIR_CONTROL;

        // 입력에 따른 가속
        if (input.right) {
            player.velocityX += acceleration;
        } else if (input.left) {
            player.velocityX -= acceleration;
        } else {
            // 마찰 적용 (감속)
            player.velocityX *= PHYSICS.FRICTION;
            if (Math.abs(player.velocityX) < 0.1) {
                player.velocityX = 0;
            }
        }

        // 최대 속도 제한
        const maxSpeed = input.sprint
            ? PHYSICS.MAX_SPRINT_SPEED
            : PHYSICS.MAX_RUN_SPEED;
        player.velocityX = Math.max(-maxSpeed,
                           Math.min(maxSpeed, player.velocityX));
    }
}
```

---

## 3. 충돌 시스템

### 3.1 AABB 충돌 감지
```javascript
class CollisionSystem {
    // 기본 AABB 충돌 체크
    checkAABB(a, b) {
        return a.x < b.x + b.width &&
               a.x + a.width > b.x &&
               a.y < b.y + b.height &&
               a.y + a.height > b.y;
    }

    // 침투 깊이 계산
    getPenetration(a, b) {
        const overlapX = Math.min(a.x + a.width, b.x + b.width)
                       - Math.max(a.x, b.x);
        const overlapY = Math.min(a.y + a.height, b.y + b.height)
                       - Math.max(a.y, b.y);
        return { x: overlapX, y: overlapY };
    }

    // 충돌 해결 (밀어내기)
    resolveCollision(entity, platform, penetration) {
        if (penetration.x < penetration.y) {
            // 수평 충돌 해결
            if (entity.x < platform.x) {
                entity.x -= penetration.x;
            } else {
                entity.x += penetration.x;
            }
            entity.velocityX = 0;
        } else {
            // 수직 충돌 해결
            if (entity.y < platform.y) {
                entity.y -= penetration.y;
                entity.velocityY = 0;
                entity.grounded = true;
            } else {
                entity.y += penetration.y;
                entity.velocityY = 0;
            }
        }
    }
}
```

### 3.2 모서리 보정 (Corner Correction)
```javascript
// 점프 시 모서리에 살짝 걸리면 자동 보정
cornerCorrection(player, platform) {
    const correction = PHYSICS.CORNER_CORRECTION;

    // 위로 점프할 때 좌우 가장자리에 걸리면
    if (player.velocityY < 0) {
        const leftEdge = platform.x - player.x - player.width;
        const rightEdge = player.x - platform.x - platform.width;

        if (leftEdge > 0 && leftEdge <= correction) {
            player.x -= correction;
        } else if (rightEdge > 0 && rightEdge <= correction) {
            player.x += correction;
        }
    }
}
```

### 3.3 히트박스/허트박스 시스템
```javascript
class HitboxSystem {
    constructor() {
        this.hitboxes = [];  // 공격 판정
        this.hurtboxes = []; // 피격 판정
    }

    // 무기 히트박스 생성
    createAttackHitbox(entity, offset, size, duration, damage) {
        const hitbox = {
            owner: entity,
            x: entity.x + (entity.facing === 1 ? offset.x : -offset.x - size.width),
            y: entity.y + offset.y,
            width: size.width,
            height: size.height,
            framesRemaining: duration,
            damage: damage,
            hits: new Set() // 이미 맞춘 대상
        };
        this.hitboxes.push(hitbox);
        return hitbox;
    }

    // 매 프레임 충돌 체크
    update() {
        for (const hitbox of this.hitboxes) {
            for (const hurtbox of this.hurtboxes) {
                if (hitbox.owner === hurtbox.owner) continue;
                if (hitbox.hits.has(hurtbox.owner)) continue;

                if (this.checkAABB(hitbox, hurtbox)) {
                    hurtbox.owner.takeDamage(hitbox.damage, hitbox.owner);
                    hitbox.hits.add(hurtbox.owner);
                }
            }

            hitbox.framesRemaining--;
        }

        // 만료된 히트박스 제거
        this.hitboxes = this.hitboxes.filter(h => h.framesRemaining > 0);
    }
}
```

---

## 4. 적 AI 시스템

### 4.1 체스 기반 AI 인터페이스
```javascript
class ChessEnemyAI {
    constructor(enemy) {
        this.enemy = enemy;
        this.state = 'patrol';
        this.targetPlayer = null;
        this.cooldown = 0;
    }

    // 체스 기물별 움직임 패턴 (추상 메서드)
    getMovementPattern() { throw new Error('Implement in subclass'); }

    // 시야 체크
    canSeePlayer(player) {
        const distance = Math.hypot(
            player.x - this.enemy.x,
            player.y - this.enemy.y
        );
        return distance < this.enemy.sightRange;
    }

    update(player, deltaTime) {
        this.cooldown = Math.max(0, this.cooldown - deltaTime);

        if (this.canSeePlayer(player)) {
            this.targetPlayer = player;
            this.state = 'attack';
        }

        switch(this.state) {
            case 'patrol': this.patrol(); break;
            case 'attack': this.attack(); break;
            case 'cooldown': this.waitCooldown(); break;
        }
    }
}
```

### 4.2 개별 적 AI 구현

#### Pawn AI (좌우 순찰)
```javascript
class PawnAI extends ChessEnemyAI {
    patrol() {
        // 좌우로 순찰
        this.enemy.velocityX = this.enemy.facing * 2;

        // 절벽/벽 감지 시 방향 전환
        if (this.detectEdge() || this.detectWall()) {
            this.enemy.facing *= -1;
        }
    }

    attack() {
        // 플레이어 발견 시 속도 증가
        this.enemy.velocityX = this.enemy.facing * 3;
    }
}
```

#### Knight AI (L자 점프)
```javascript
class KnightAI extends ChessEnemyAI {
    constructor(enemy) {
        super(enemy);
        this.jumpCooldown = 180; // 3초
        this.isCharging = false;
        this.chargeTime = 0;
    }

    attack() {
        if (this.cooldown > 0) {
            this.state = 'cooldown';
            return;
        }

        if (!this.isCharging) {
            // 점프 준비 (0.5초)
            this.isCharging = true;
            this.chargeTime = 30;
            this.enemy.playAnimation('charge');
        } else if (this.chargeTime > 0) {
            this.chargeTime--;
        } else {
            // L자 점프 실행
            this.executeLJump();
            this.isCharging = false;
            this.cooldown = this.jumpCooldown;
            this.state = 'cooldown';
        }
    }

    executeLJump() {
        const dx = this.targetPlayer.x - this.enemy.x;
        const dy = this.targetPlayer.y - this.enemy.y;

        // L자 이동: 수직 2 + 수평 1 비율
        const horizontalDist = Math.sign(dx) * 64;  // 1 타일
        const verticalDist = -128; // 2 타일 높이 점프

        this.enemy.velocityX = horizontalDist / 30;
        this.enemy.velocityY = verticalDist / 30;
    }
}
```

#### Bishop AI (대각선 사격)
```javascript
class BishopAI extends ChessEnemyAI {
    constructor(enemy) {
        super(enemy);
        this.shootCooldown = 120; // 2초
        this.aimTime = 0;
    }

    canSeePlayer(player) {
        // 대각선 시야만 체크
        const dx = player.x - this.enemy.x;
        const dy = player.y - this.enemy.y;
        return Math.abs(Math.abs(dx) - Math.abs(dy)) < 32; // 대각선 허용 오차
    }

    attack() {
        if (this.cooldown > 0) return;

        // 조준선 표시 (1초)
        if (this.aimTime < 60) {
            this.aimTime++;
            this.enemy.showAimLine = true;
        } else {
            // 발사
            this.shootProjectile();
            this.aimTime = 0;
            this.cooldown = this.shootCooldown;
            this.enemy.showAimLine = false;
        }
    }

    shootProjectile() {
        const dx = Math.sign(this.targetPlayer.x - this.enemy.x);
        const dy = Math.sign(this.targetPlayer.y - this.enemy.y);

        game.spawnProjectile({
            x: this.enemy.x,
            y: this.enemy.y,
            velocityX: dx * 8,
            velocityY: dy * 8,
            damage: 1
        });
    }
}
```

#### Rook AI (직선 돌진)
```javascript
class RookAI extends ChessEnemyAI {
    constructor(enemy) {
        super(enemy);
        this.chargeSpeed = 12;
        this.isCharging = false;
        this.stunTime = 0;
    }

    canSeePlayer(player) {
        // 같은 X축 또는 Y축에 있는지 체크
        const sameX = Math.abs(player.x - this.enemy.x) < 32;
        const sameY = Math.abs(player.y - this.enemy.y) < 32;
        return sameX || sameY;
    }

    attack() {
        if (this.stunTime > 0) {
            this.stunTime--;
            return;
        }

        if (!this.isCharging) {
            // "Check!" 경고 후 돌진
            this.enemy.showWarning = true;
            setTimeout(() => {
                this.isCharging = true;
                this.enemy.showWarning = false;
            }, 500);
        } else {
            // 돌진 중
            const dx = Math.sign(this.targetPlayer.x - this.enemy.x);
            this.enemy.velocityX = dx * this.chargeSpeed;

            // 벽 충돌 시 기절
            if (this.enemy.hitWall) {
                this.isCharging = false;
                this.stunTime = 60; // 1초 기절
                this.enemy.playAnimation('stunned');
            }
        }
    }
}
```

---

## 5. 레벨 시스템

### 5.1 타일맵 구조
```javascript
const TILE_TYPES = {
    EMPTY: 0,
    GROUND: 1,
    PLATFORM: 2,
    SPIKE: 3,
    CHECKPOINT: 4,
    CHEST_WHITE: 5,
    CHEST_BLACK: 6,
    BOOKSHELF: 7,
    GOAL: 9
};

// 레벨 데이터 예시
const level1 = {
    width: 50,
    height: 15,
    tileSize: 32,
    tiles: [
        [0,0,0,0,0,0,0,0,0,0,...],
        [0,0,0,0,0,0,0,0,0,0,...],
        // ... 타일 데이터
    ],
    enemies: [
        { type: 'pawn', x: 320, y: 384 },
        { type: 'knight', x: 640, y: 384 }
    ],
    items: [
        { type: 'coin', x: 200, y: 300 },
        { type: 'upgrade', x: 800, y: 200 }
    ],
    playerStart: { x: 64, y: 384 }
};
```

### 5.2 카메라 시스템
```javascript
class Camera {
    constructor(width, height) {
        this.x = 0;
        this.y = 0;
        this.width = width;
        this.height = height;
        this.smoothing = 0.1; // Lerp 계수
    }

    follow(target, levelBounds) {
        // 목표 위치 (플레이어 중심)
        const targetX = target.x - this.width / 2;
        const targetY = target.y - this.height / 2;

        // 부드러운 추적 (Lerp)
        this.x += (targetX - this.x) * this.smoothing;
        this.y += (targetY - this.y) * this.smoothing;

        // 레벨 경계 제한
        this.x = Math.max(0, Math.min(this.x,
                 levelBounds.width - this.width));
        this.y = Math.max(0, Math.min(this.y,
                 levelBounds.height - this.height));
    }

    worldToScreen(worldX, worldY) {
        return {
            x: worldX - this.x,
            y: worldY - this.y
        };
    }
}
```

---

## 6. 게임 상태 관리

### 6.1 State Machine
```javascript
class GameStateManager {
    constructor() {
        this.states = {
            TITLE: new TitleState(),
            PLAYING: new PlayingState(),
            PAUSED: new PausedState(),
            GAME_OVER: new GameOverState(),
            STAGE_CLEAR: new StageClearState()
        };
        this.currentState = 'TITLE';
    }

    changeState(newState) {
        this.states[this.currentState].exit();
        this.currentState = newState;
        this.states[newState].enter();
    }

    update(deltaTime) {
        this.states[this.currentState].update(deltaTime);
    }

    render(ctx) {
        this.states[this.currentState].render(ctx);
    }
}
```

---

## 7. 에셋 관리

### 7.1 스프라이트 시트 구조
```javascript
const SPRITE_CONFIG = {
    player: {
        idle: { frames: 4, frameTime: 150 },
        run: { frames: 8, frameTime: 80 },
        jump: { frames: 2, frameTime: 100 },
        fall: { frames: 2, frameTime: 100 },
        attack: { frames: 4, frameTime: 50 }
    },
    enemies: {
        pawn: { idle: 2, walk: 4, hurt: 1 },
        knight: { idle: 2, charge: 3, jump: 4, stun: 1 },
        bishop: { idle: 2, aim: 3, shoot: 2 },
        rook: { idle: 2, charge: 6, stun: 1 }
    }
};
```

### 7.2 에셋 로더
```javascript
class AssetLoader {
    constructor() {
        this.images = {};
        this.loaded = 0;
        this.total = 0;
    }

    loadImage(name, src) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                this.images[name] = img;
                this.loaded++;
                resolve(img);
            };
            img.onerror = reject;
            img.src = src;
            this.total++;
        });
    }

    async loadAll(manifest) {
        const promises = Object.entries(manifest).map(
            ([name, src]) => this.loadImage(name, src)
        );
        await Promise.all(promises);
    }

    getProgress() {
        return this.loaded / this.total;
    }
}
```

---

## 8. 성능 최적화

### 8.1 렌더링 최적화
- **오프스크린 캔버스**: 정적 배경 미리 렌더링
- **더티 렉탱글**: 변경된 영역만 다시 그리기
- **오브젝트 풀링**: 투사체, 파티클 재사용

### 8.2 충돌 최적화
- **공간 분할**: 쿼드트리 또는 그리드 기반 탐색
- **브로드 페이즈**: AABB 간단 체크 후 정밀 체크

### 8.3 메모리 관리
- **에셋 캐싱**: 중복 로딩 방지
- **이벤트 정리**: 화면 전환 시 리스너 제거
