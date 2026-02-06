# Image Agent System - Design Plan

## Overview

Image Agent는 게임 에셋 요청을 받아 고품질 이미지를 자동으로 생성하고, 품질을 검토하며,
기대 수준에 도달할 때까지 반복 개선하는 AI 에이전트 시스템입니다.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        IMAGE AGENT SYSTEM                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │
│  │   Request   │───▶│   Prompt    │───▶│   Image     │             │
│  │   Parser    │    │  Generator  │    │  Generator  │             │
│  └─────────────┘    └─────────────┘    └──────┬──────┘             │
│                                               │                     │
│                                               ▼                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │
│  │   Result    │◀───│   Quality   │◀───│   Image     │             │
│  │   Handler   │    │  Reviewer   │    │  Processor  │             │
│  └─────────────┘    └─────────────┘    └─────────────┘             │
│         │                 │                                         │
│         │                 │ < 90%                                   │
│         │                 └──────────────────┐                      │
│         │                                    ▼                      │
│         │           ┌─────────────────────────────────┐            │
│         │           │     Prompt Improvement Loop     │            │
│         │           │     (max 5 iterations)          │            │
│         │           └─────────────────────────────────┘            │
│         ▼                                                           │
│  ┌─────────────────────────────────────────────────────┐           │
│  │                  Final Output                        │           │
│  │  - Generated Image (PNG/GIF)                        │           │
│  │  - Quality Report                                   │           │
│  │  - Generation History                               │           │
│  └─────────────────────────────────────────────────────┘           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Request Parser (`core/request_parser.py`)

게임 에셋 요청을 파싱하고 구조화된 요구사항으로 변환합니다.

```python
@dataclass
class AssetRequest:
    asset_type: str          # 'sprite', 'background', 'ui', 'animation'
    description: str         # 원하는 이미지 설명
    style: str              # 'pixel_art', 'kawaii', 'realistic', etc.
    size: Tuple[int, int]   # (width, height)
    transparency: bool      # 투명 배경 필요 여부
    color_palette: Optional[List[str]]  # 색상 팔레트 제한
    animation_frames: int   # 애니메이션 프레임 수 (1 = 정지 이미지)
    game_context: str       # 어떤 게임용인지
    reference_images: List[Path]  # 참조 이미지들
    constraints: Dict[str, Any]   # 추가 제약 조건
```

### 2. Prompt Generator (`prompts/prompt_generator.py`)

요청을 기반으로 최적의 이미지 생성 프롬프트를 작성합니다.

```python
class PromptGenerator:
    """전문 게임 아티스트 관점에서 프롬프트 생성"""

    def generate_prompt(self, request: AssetRequest) -> DetailedPrompt:
        """
        1. 기본 설명 분석
        2. 스타일 키워드 추가
        3. 기술적 요구사항 명시 (크기, 투명도 등)
        4. 게임 컨텍스트 반영
        5. 부정 프롬프트 생성 (피해야 할 것들)
        """
        pass

    def improve_prompt(self,
                       original: DetailedPrompt,
                       review_feedback: QualityReport) -> DetailedPrompt:
        """리뷰 피드백을 반영하여 프롬프트 개선"""
        pass

@dataclass
class DetailedPrompt:
    main_prompt: str        # 주 프롬프트
    style_modifiers: List[str]  # 스타일 수정자
    technical_specs: str    # 기술 명세
    negative_prompt: str    # 피해야 할 것들
    full_prompt: str        # 조합된 최종 프롬프트
    version: int            # 프롬프트 버전 (반복시 증가)
```

### 3. Quality Reviewer (`reviewers/quality_reviewer.py`)

생성된 이미지를 전문가 관점에서 검토합니다.

```python
class QualityReviewer:
    """게임 디자이너/개발자 관점에서 품질 검토"""

    def review(self,
               image: GeneratedImage,
               request: AssetRequest) -> QualityReport:
        """
        검토 항목:
        1. 투명도 검사 (요청시)
        2. 크기/해상도 검사
        3. 스타일 일치도 검사
        4. 색상 팔레트 준수 검사
        5. 개체 품질 검사 (선명도, 디테일)
        6. 게임 적합성 검사
        """
        pass

@dataclass
class QualityReport:
    overall_score: float    # 0.0 ~ 1.0 (90% = 0.9)
    passed: bool            # overall_score >= 0.9

    # 상세 점수
    transparency_score: float
    size_score: float
    style_score: float
    color_score: float
    quality_score: float
    game_fit_score: float

    # 피드백
    issues: List[str]       # 발견된 문제점
    suggestions: List[str]  # 개선 제안

    # 메타데이터
    iteration: int          # 몇 번째 반복인지
    review_time: datetime
```

### 4. Image Agent (`core/image_agent.py`)

전체 워크플로우를 조율하는 메인 에이전트입니다.

```python
class ImageAgent:
    """메인 오케스트레이터"""

    MAX_ITERATIONS = 5
    QUALITY_THRESHOLD = 0.9  # 90%

    async def generate(self, request: AssetRequest) -> AgentResult:
        """
        메인 생성 루프:
        1. 요청 파싱 및 검증
        2. 초기 프롬프트 생성
        3. 이미지 생성
        4. 품질 검토
        5. 통과시 반환, 미달시 프롬프트 개선 후 재시도
        6. 최대 5회 반복 또는 90% 달성시 완료
        """
        pass

@dataclass
class AgentResult:
    success: bool
    final_image: GeneratedImage
    final_score: float
    iterations: int
    history: List[IterationRecord]  # 모든 반복 기록
    total_time: float

@dataclass
class IterationRecord:
    iteration: int
    prompt: DetailedPrompt
    image: GeneratedImage
    review: QualityReport
    time_taken: float
```

### 5. Transparency Checker (`reviewers/transparency_checker.py`)

PNG 투명도를 전문적으로 검사합니다.

```python
class TransparencyChecker:
    """투명도 전문 검사기"""

    def check(self, image: Image) -> TransparencyReport:
        """
        검사 항목:
        1. 알파 채널 존재 여부
        2. 배경 투명도 (가장자리 픽셀)
        3. 개체 경계 품질
        4. 반투명 영역 검사
        5. 홀/구멍 검사
        """
        pass

@dataclass
class TransparencyReport:
    has_alpha: bool
    background_transparent: bool
    edge_quality: float      # 0.0 ~ 1.0
    artifacts_found: List[str]
    transparent_percentage: float
    recommendation: str
```

## Folder Structure

```
image_agent/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── image_agent.py      # 메인 에이전트
│   ├── request_parser.py   # 요청 파서
│   └── result_handler.py   # 결과 처리
├── prompts/
│   ├── __init__.py
│   ├── prompt_generator.py # 프롬프트 생성기
│   ├── prompt_improver.py  # 프롬프트 개선기
│   └── templates/          # 프롬프트 템플릿
│       ├── sprite.py
│       ├── background.py
│       └── ui.py
├── reviewers/
│   ├── __init__.py
│   ├── quality_reviewer.py # 품질 검토기
│   ├── transparency_checker.py  # 투명도 검사기
│   ├── style_checker.py    # 스타일 검사기
│   └── color_checker.py    # 색상 검사기
├── utils/
│   ├── __init__.py
│   ├── image_analysis.py   # 이미지 분석 유틸
│   ├── logging.py          # 로깅
│   └── config.py           # 설정
├── tests/
│   ├── __init__.py
│   ├── test_agent.py
│   ├── test_prompt.py
│   └── test_reviewer.py
├── docs/
│   ├── DESIGN_PLAN.md      # 이 문서
│   ├── API_REFERENCE.md
│   └── USAGE_GUIDE.md
└── cli.py                  # CLI 인터페이스
```

## Workflow Diagram

```
[게임에서 에셋 요청]
        │
        ▼
┌───────────────────┐
│  Request Parser   │ ← "64x64 pixel art apple, transparent bg, kawaii style"
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ Prompt Generator  │ ← 전문가 수준의 상세 프롬프트 작성
└───────────────────┘
        │
        ├─────────────────────────────────────┐
        ▼                                     │
┌───────────────────┐                         │
│ Prompt Validator  │ ← 프롬프트 품질 검사    │
└───────────────────┘                         │
        │ (통과)                              │
        ▼                                     │
┌───────────────────┐                         │
│ Image Generator   │ ← image_generator API   │
│ (Gemini/Imagen)   │   (최상위 모델 사용)    │
└───────────────────┘                         │
        │                                     │
        ▼                                     │
┌───────────────────┐                         │
│ Quality Reviewer  │                         │
├───────────────────┤                         │
│ - Transparency    │                         │
│ - Style Match     │                         │
│ - Color Palette   │                         │
│ - Object Quality  │                         │
│ - Game Fit        │                         │
└───────────────────┘                         │
        │                                     │
        ▼                                     │
    Score >= 90%? ──────────────────────────┐ │
        │ No                                │ │
        ▼                                   │ │
    Iteration < 5? ─────────┐               │ │
        │ Yes               │ No            │ │
        ▼                   ▼               │ │
┌───────────────────┐  ┌────────────┐       │ │
│ Prompt Improver   │  │ Best Image │       │ │
│ (피드백 반영)      │  │ Selection  │       │ │
└───────────────────┘  └────────────┘       │ │
        │                   │               │ │
        └───────────────────┴───────────────┘ │
                            │                 │ Yes
                            ▼                 │
                    ┌───────────────┐         │
                    │ Final Result  │◀────────┘
                    │ + Report      │
                    └───────────────┘
```

## API Level Updates Required

### image_generator 업데이트 사항

1. **최상위 모델 지원** (`generators/gemini_rest_generator.py`)
```python
# 기존
IMAGEN_MODEL = "imagen-3.0-generate-001"

# 업데이트 (옵션 추가)
class GeminiRestGenerator:
    MODELS = {
        'standard': 'imagen-3.0-generate-001',
        'premium': 'imagen-3.0-generate-002',  # 또는 최신 버전
        'fast': 'imagen-3.0-fast-generate-001'
    }

    def __init__(self, model_tier: str = 'premium'):
        self.model = self.MODELS.get(model_tier, self.MODELS['premium'])
```

2. **메타데이터 확장**
```python
@dataclass
class GeneratedImage:
    # 기존 필드들...

    # 추가 필드
    model_used: str         # 사용된 모델
    generation_params: Dict # 생성 파라미터
    raw_response: Dict      # API 원본 응답
```

3. **품질 힌트 지원**
```python
async def generate(self,
                   prompt: str,
                   quality_hints: Dict = None) -> GeneratedImage:
    """
    quality_hints = {
        'transparency': True,
        'style': 'pixel_art',
        'detail_level': 'high',
        'color_depth': 16
    }
    """
    pass
```

## Implementation Plan

### Phase 1: 기본 구조 (Week 1)
- [ ] 폴더 구조 생성
- [ ] 데이터 클래스 정의
- [ ] Request Parser 구현
- [ ] 기본 Prompt Generator 구현

### Phase 2: 핵심 기능 (Week 2)
- [ ] Quality Reviewer 구현
- [ ] Transparency Checker 구현
- [ ] Prompt Improver 구현
- [ ] Image Agent 메인 루프 구현

### Phase 3: 통합 및 테스트 (Week 3)
- [ ] image_generator API 업데이트
- [ ] CLI 인터페이스 구현
- [ ] 단위 테스트 작성
- [ ] 통합 테스트

### Phase 4: 최적화 (Week 4)
- [ ] 프롬프트 템플릿 최적화
- [ ] 품질 검사 알고리즘 개선
- [ ] 캐싱 전략 구현
- [ ] 문서화

## Usage Example

```python
from image_agent import ImageAgent
from image_agent.core import AssetRequest

# 에이전트 생성
agent = ImageAgent()

# 요청 생성
request = AssetRequest(
    asset_type='sprite',
    description='귀여운 빨간 사과',
    style='kawaii',
    size=(64, 64),
    transparency=True,
    game_context='Feeding Caiso',
    constraints={
        'must_have': ['stem', 'leaf', 'shine'],
        'color_dominant': 'red'
    }
)

# 이미지 생성 (자동 반복 개선)
result = await agent.generate(request)

# 결과 확인
print(f"성공: {result.success}")
print(f"최종 점수: {result.final_score * 100:.1f}%")
print(f"반복 횟수: {result.iterations}")
print(f"소요 시간: {result.total_time:.2f}초")

# 이미지 저장
result.final_image.save('assets/sprites/food_apple_v3.png')

# 생성 히스토리 확인
for record in result.history:
    print(f"  Iter {record.iteration}: {record.review.overall_score * 100:.1f}%")
    if record.review.issues:
        print(f"    Issues: {record.review.issues}")
```

## CLI Usage

```bash
# 기본 생성
python -m image_agent generate \
    --type sprite \
    --desc "cute red apple" \
    --style kawaii \
    --size 64x64 \
    --transparent \
    --output assets/sprites/apple.png

# 게임 컨텍스트 포함
python -m image_agent generate \
    --type sprite \
    --desc "baby blob monster" \
    --style kawaii \
    --game "Feeding Caiso" \
    --size 128x128 \
    --transparent \
    --output assets/sprites/caiso_baby.png

# 품질 검사만 실행
python -m image_agent review \
    --image assets/sprites/apple.png \
    --check-transparency \
    --check-style kawaii

# 배치 생성
python -m image_agent batch \
    --config assets/batch_config.yaml \
    --output-dir assets/sprites/
```

## Quality Metrics

| 검사 항목 | 가중치 | 기준 |
|----------|--------|------|
| 투명도 | 20% | 배경이 완전 투명 (요청시) |
| 크기 정확도 | 10% | 요청 크기 ±5% 이내 |
| 스타일 일치 | 25% | 요청 스타일과 일치도 |
| 색상 팔레트 | 15% | 지정 팔레트 준수율 |
| 개체 품질 | 20% | 선명도, 디테일, 완성도 |
| 게임 적합성 | 10% | 게임에서 사용 가능 여부 |

**총점 90% 이상 = 통과**

## Dependencies

```
# 기존 image_generator 의존성 +
pillow>=10.0.0
numpy>=1.24.0
scikit-image>=0.21.0  # 이미지 분석용
colormath>=3.0.0      # 색상 분석용
```

## Notes

- 최대 5회 반복으로 API 비용 제한
- 각 반복마다 이전 피드백을 프롬프트에 반영
- 모든 반복 히스토리 보존 (디버깅/학습용)
- 캐싱으로 동일 요청 재처리 방지
