# 🎮 CAISOGAMES 에이전트 아키텍처 계획서

## 현재 상태

| 항목 | 상태 |
|------|------|
| **프로젝트** | CAISOGAMES (HTML/Python, Vercel 배포) |
| **기존 에이전트** | `image_agent` ✅ 동작 확인 |
| **문제점** | 바이브 코딩으로 인한 mockup 수준의 완성도 |

---

## 에이전트 전체 구조 (Agent Ecosystem)

```
                    ┌─────────────────────┐
                    │   orchestrator      │
                    │   (총괄 에이전트)     │
                    └──────────┬──────────┘
                               │
        ┌──────────┬───────────┼───────────┬──────────┐
        │          │           │           │          │
   ┌────▼───┐ ┌───▼────┐ ┌───▼────┐ ┌───▼────┐ ┌───▼────┐
   │ design │ │  play  │ │ image  │ │ sound  │ │  code  │
   │ _agent │ │ _agent │ │ _agent │ │ _agent │ │ _agent │
   │ 기획   │ │ 플레이 │ │ 이미지 │ │ 사운드 │ │ 코드   │
   └────┬───┘ └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
        │         │          │          │          │
        └─────────┴──────────┼──────────┴──────────┘
                             │
                    ┌────────▼────────┐
                    │  review_agent   │
                    │  (종합 리뷰)     │
                    └─────────────────┘
```

---

## Phase 1: 핵심 에이전트 (우선 구현)

### 1. `design_agent` — 게임 기획 전문가

**역할**: 게임 디자이너/기획자 시점에서 게임을 분석하고 개선안 제시

**주요 기능**:
- 게임 HTML 파일을 파싱하여 현재 게임 메카닉 분석
- 시나리오/스토리 완성도 평가 및 개선안 생성
- 난이도 곡선(Difficulty Curve) 분석 및 밸런싱 제안
- 레벨 디자인 구조 제안
- 리텐션 요소 (보상, 진행감, 도전) 분석
- 타겟 연령대별 적합성 평가

**입력**: 게임 HTML/JS 소스코드, 기존 기획 문서
**출력**: `{game_name}_design_review.md` (개선 사항 + 구체적 수정 제안)

**구현 방식**:
```python
# design_agent/agent.py
class DesignAgent:
    def analyze_game(self, game_path: str) -> DesignReview:
        """게임 소스를 읽고 기획 관점에서 분석"""
        
    def evaluate_difficulty(self, game_path: str) -> DifficultyReport:
        """난이도 곡선 분석 - 적 스폰, 점수 체계, 파워업 등"""
        
    def suggest_improvements(self, review: DesignReview) -> list[Improvement]:
        """구체적인 코드 수정 제안 생성"""
        
    def generate_scenario(self, game_path: str) -> Scenario:
        """스토리/시나리오 보강안 생성"""
```

**평가 기준 (체크리스트)**:
- [ ] 튜토리얼/온보딩이 있는가?
- [ ] 난이도가 점진적으로 상승하는가?
- [ ] 명확한 목표와 피드백이 있는가?
- [ ] 보상 체계가 있는가?
- [ ] 재플레이 가치가 있는가?

---

### 2. `play_agent` — 자동 플레이 테스터

**역할**: 실제로 게임을 플레이하여 버그, UX 문제, 밸런스 이슈 탐지

**주요 기능**:
- Puppeteer/Playwright로 게임을 자동 실행
- 다양한 플레이 패턴 시뮬레이션 (초보자, 숙련자, 랜덤)
- 게임 상태 스냅샷 캡처 및 분석
- 조작 반응성 측정 (입력 → 화면 반영 딜레이)
- 게임오버/클리어 조건 검증
- 엣지 케이스 탐색 (화면 밖 이동, 연타, 무입력 등)

**입력**: 게임 URL 또는 로컬 HTML 파일
**출력**: `{game_name}_playtest_report.md` + 스크린샷들

**구현 방식**:
```python
# play_agent/agent.py
class PlayAgent:
    def setup_browser(self):
        """Playwright 브라우저 세팅"""
        
    def play_random(self, game_url: str, duration: int = 60):
        """랜덤 입력으로 플레이 - 크래시/버그 탐지"""
        
    def play_systematic(self, game_url: str):
        """체계적 입력으로 모든 경로 탐색"""
        
    def capture_metrics(self) -> PlayMetrics:
        """FPS, 반응 시간, 메모리 사용량 등 측정"""
        
    def detect_issues(self, screenshots: list) -> list[Issue]:
        """스크린샷을 AI로 분석하여 시각적 버그 탐지"""
```

**테스트 시나리오**:
- 🎯 정상 플레이: 의도된 경로로 플레이
- 🐒 몽키 테스트: 무작위 입력
- 🧊 방치 테스트: 아무 입력 없이 방치
- ⚡ 스트레스 테스트: 빠른 연속 입력
- 📱 반응형 테스트: 다양한 화면 크기

---

### 3. `sound_agent` — 사운드/음악 에이전트

**역할**: 게임에 적합한 사운드 효과와 배경 음악 생성/적용

**주요 기능**:
- 현재 게임의 사운드 상태 분석 (없는 경우 식별)
- 게임 장르/분위기에 맞는 사운드 요구사항 정의
- Web Audio API 기반 프로시저럴 사운드 효과 생성
- 무료 사운드 라이브러리에서 적합한 효과음 매칭
- BGM 루프 생성 (Tone.js 활용)
- 사운드 통합 코드 자동 생성

**입력**: 게임 소스코드 + 장르 정보
**출력**: 사운드 파일들 + 통합 코드 스니펫

**구현 방식**:
```python
# sound_agent/agent.py
class SoundAgent:
    def audit_sounds(self, game_path: str) -> SoundAudit:
        """현재 게임의 사운드 현황 분석"""
        
    def define_sound_requirements(self, game_path: str) -> list[SoundReq]:
        """필요한 사운드 목록 생성 (효과음, BGM, UI 사운드)"""
        
    def generate_procedural_sfx(self, req: SoundReq) -> str:
        """Web Audio API 코드로 효과음 생성"""
        
    def generate_bgm_code(self, mood: str, tempo: int) -> str:
        """Tone.js 기반 배경음악 코드 생성"""
        
    def integrate_sounds(self, game_path: str, sounds: dict):
        """게임 코드에 사운드 자동 통합"""
```

**사운드 카테고리**:
- 🔊 UI: 버튼 클릭, 메뉴 전환, 선택
- 💥 게임플레이: 충돌, 점프, 아이템 획득, 공격
- 🎵 BGM: 메인 메뉴, 인게임, 게임오버
- 📣 피드백: 성공, 실패, 콤보, 레벨업

---

## Phase 2: 심화 에이전트

### 4. `code_agent` — 코드 품질/최적화 전문가

**역할**: 게임 코드의 품질, 성능, 구조 개선

**주요 기능**:
- 코드 구조 분석 및 리팩토링 제안
- 성능 최적화 (렌더링, 메모리, 이벤트 처리)
- 크로스 브라우저 호환성 검사
- 모바일 대응 (터치 이벤트, 반응형)
- 코드 중복 제거 및 모듈화
- 게임 루프 패턴 표준화

**입력**: 게임 소스코드
**출력**: 최적화된 코드 + 변경 사항 리포트

```python
# code_agent/agent.py  
class CodeAgent:
    def analyze_structure(self, game_path: str) -> CodeAnalysis:
        """코드 구조, 패턴, 안티패턴 분석"""
        
    def optimize_performance(self, game_path: str) -> list[Optimization]:
        """렌더링 루프, RAF, 메모리 관리 최적화"""
        
    def add_mobile_support(self, game_path: str) -> str:
        """터치 이벤트, 가상 조이스틱, 반응형 캔버스"""
        
    def standardize_game_loop(self, game_path: str) -> str:
        """requestAnimationFrame 기반 표준 게임 루프 적용"""
        
    def apply_fixes(self, game_path: str, fixes: list[Fix]) -> str:
        """자동 코드 수정 적용"""
```

---

### 5. `review_agent` — 종합 리뷰 에이전트

**역할**: 모든 에이전트의 결과를 종합하여 우선순위 기반 개선 로드맵 생성

**주요 기능**:
- 각 에이전트 리포트 수집 및 종합
- 개선 사항 우선순위 매기기 (Impact × Effort 매트릭스)
- 게임별 종합 점수 산정 (100점 만점)
- 자동 개선 작업 생성 (GitHub Issue 형태)
- 이전 리뷰 대비 개선도 추적

**입력**: 모든 에이전트의 리포트들
**출력**: `{game_name}_comprehensive_review.md` + 개선 태스크 목록

```python
# review_agent/agent.py
class ReviewAgent:
    def collect_reports(self, game_name: str) -> dict:
        """모든 에이전트의 리뷰 결과 수집"""
        
    def score_game(self, reports: dict) -> GameScore:
        """종합 점수 산정"""
        
    def prioritize_improvements(self, reports: dict) -> list[Task]:
        """Impact/Effort 기반 우선순위 결정"""
        
    def generate_roadmap(self, tasks: list[Task]) -> Roadmap:
        """단계별 개선 로드맵 생성"""
        
    def compare_versions(self, old: GameScore, new: GameScore):
        """버전간 개선도 비교"""
```

**종합 점수 체계**:
| 카테고리 | 배점 | 평가 에이전트 |
|---------|------|-------------|
| 게임성/재미 | 25점 | design_agent |
| 조작감/UX | 20점 | play_agent |
| 비주얼 | 20점 | image_agent |
| 사운드 | 15점 | sound_agent |
| 코드 품질 | 10점 | code_agent |
| 안정성 | 10점 | play_agent |

---

### 6. `orchestrator` — 총괄 에이전트

**역할**: 전체 파이프라인을 자동화하고 반복 개선 사이클 관리

**주요 기능**:
- 게임 목록 자동 감지 및 파이프라인 실행
- 에이전트 실행 순서 관리
- 개선 → 리뷰 → 재개선 반복 루프
- 결과 대시보드 생성
- Git 커밋/PR 자동 생성

```python
# orchestrator/agent.py
class Orchestrator:
    def discover_games(self) -> list[Game]:
        """games/ 폴더에서 게임 목록 자동 감지"""
        
    def run_full_review(self, game: Game):
        """모든 에이전트 순차 실행"""
        # 1. design_agent → 기획 리뷰
        # 2. play_agent → 플레이 테스트
        # 3. image_agent → 비주얼 리뷰 (기존)
        # 4. sound_agent → 사운드 리뷰
        # 5. code_agent → 코드 리뷰
        # 6. review_agent → 종합 리포트
        
    def run_improvement_cycle(self, game: Game, max_iterations: int = 3):
        """리뷰 → 개선 → 재리뷰 반복"""
        
    def generate_dashboard(self) -> str:
        """전체 게임 상태 대시보드 HTML 생성"""
```

---

## 에이전트 공통 구조

각 에이전트 폴더의 표준 구조:

```
{agent_name}/
├── agent.py          # 메인 에이전트 로직
├── prompts/          # LLM 프롬프트 템플릿
│   ├── analyze.txt
│   └── improve.txt
├── config.yaml       # 에이전트 설정
├── templates/        # 리포트 템플릿
│   └── report.md
├── tests/            # 에이전트 자체 테스트
│   └── test_agent.py
└── README.md         # 에이전트 사용법
```

**공통 베이스 클래스**:
```python
# agents/base.py
class BaseAgent:
    def __init__(self, game_path: str, config: dict):
        self.game_path = game_path
        self.config = config
        
    def read_game_source(self) -> str:
        """게임 HTML/JS 소스 읽기"""
        
    def call_llm(self, prompt: str) -> str:
        """Claude API 호출"""
        
    def save_report(self, report: dict, output_path: str):
        """리포트 저장"""
        
    def run(self) -> dict:
        """에이전트 실행 (각 서브클래스에서 구현)"""
        raise NotImplementedError
```

---

## 구현 우선순위 로드맵

```
Week 1-2: Foundation
├── 공통 베이스 클래스 (agents/base.py)
├── design_agent 구현
└── 단일 게임으로 파이프라인 검증

Week 3-4: Core Testing
├── play_agent 구현 (Playwright 기반)
├── code_agent 구현
└── design_agent + play_agent 연동 테스트

Week 5-6: Polish
├── sound_agent 구현
├── review_agent 구현
└── 종합 점수 체계 검증

Week 7-8: Automation
├── orchestrator 구현
├── 반복 개선 사이클 자동화
├── GitHub Actions 연동
└── 전체 게임 대상 파이프라인 실행
```

---

## 반복 개선 사이클 (핵심 워크플로우)

```
┌─────────────┐
│ 1. 게임 감지 │
└──────┬──────┘
       ▼
┌─────────────┐     ┌──────────────┐
│ 2. 전체 리뷰 │────▶│ 종합 점수:   │
│   (6개 에이전트)│    │ 45/100      │
└──────┬──────┘     └──────────────┘
       ▼
┌─────────────┐
│ 3. 우선순위  │  → 1순위: 튜토리얼 추가
│   개선 선정  │  → 2순위: 사운드 추가
└──────┬──────┘  → 3순위: 난이도 조정
       ▼
┌─────────────┐
│ 4. 자동 개선 │  → code_agent가 코드 수정
│   적용      │  → sound_agent가 사운드 추가
└──────┬──────┘
       ▼
┌─────────────┐     ┌──────────────┐
│ 5. 재리뷰   │────▶│ 종합 점수:   │
│             │     │ 68/100 (+23) │
└──────┬──────┘     └──────────────┘
       ▼
  목표 점수 달성? ──No──▶ 3번으로 돌아감
       │
      Yes
       ▼
┌─────────────┐
│ 6. Git 커밋  │
│   & 배포    │
└─────────────┘
```

---

## 기술 스택 요약

| 구성 요소 | 기술 |
|-----------|------|
| LLM | Claude API (Sonnet 4 for speed, Opus for deep analysis) |
| 자동 플레이 | Playwright (브라우저 자동화) |
| 사운드 생성 | Web Audio API, Tone.js (코드 생성) |
| 이미지 생성 | 기존 image_agent 활용 |
| 코드 분석 | AST 파싱 + LLM 분석 |
| 리포트 | Markdown → HTML 대시보드 |
| CI/CD | GitHub Actions |
| 배포 | Vercel (기존) |

---

## 첫 번째 액션 아이템

1. **`agents/base.py`** 공통 베이스 클래스 생성
2. **`design_agent`** 구현 — 가장 높은 ROI (코드 수정 없이 분석만으로 가치 제공)
3. **Feeding Caiso** 게임을 첫 번째 타겟으로 선정하여 파이프라인 검증
4. **종합 점수 기준** 확정 후 다른 게임으로 확대
