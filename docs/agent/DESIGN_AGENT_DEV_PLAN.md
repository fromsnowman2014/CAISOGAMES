# Design Agent Development Plan

> **Role**: Game Planning & Design Expert
> **Goal**: Analyze game source code and propose improvements for mechanics, difficulty, story, and retention.

---

## 1. 개요 (Overview)

`design_agent`는 게임의 소스 코드(HTML/JS)를 분석하여 기획자 관점에서 **재미 요소, 난이도 밸런스, 사용자 경험(UX), 스토리텔링**을 평가하고 구체적인 개선안을 제시하는 AI 에이전트입니다.

### 주요 책임
- **Game Analysis**: 현재 게임의 장르, 코어 루프, 규칙 분석
- **Difficulty Audit**: 난이도 곡선이 적절한지 평가
- **Creativity**: 스토리, 세계관, 캐릭터 설정 보강
- **Retention Strategy**: 플레이어가 계속 게임을 하게 만드는 요소(보상, 도전과제) 제안

---

## 2. 모듈 구조 (Module Structure)

`design_agent/` 디렉토리 내에 다음과 같이 구성합니다.

```
design_agent/
├── __init__.py
├── agent.py              # Main DesignAgent class
├── config.yaml           # Agent configuration (LLM model, max tokens)
├── prompts/              # Prompt templates
│   ├── analyze_mechanics.txt
│   ├── evaluate_balance.txt
│   └── suggest_narrative.txt
└── templates/
    └── design_review.md  # Output report template
```

---

## 3. 핵심 로직 (Core Logic)

`DesignAgent` 클래스는 `BaseAgent`를 상속받아 구현합니다.

### 3.1 `analyze_game(game_path)`
- **기능**: 게임의 핵심 메카닉과 규칙을 추출합니다.
- **입력**: 전체 소스 코드 (Token limit 고려하여 중요 로직 위주 추출)
- **출력**: `GameMechanics` 객체 (장르, 조작법, 승리/패배 조건)

### 3.2 `evaluate_difficulty(mechanics)`
- **기능**: 게임의 난이도 설계를 평가합니다.
- **분석 포인트**:
    - 적/장애물 스폰 주기 및 속도
    - 플레이어 스탯 (체력, 공격력) 변화
    - 보상 지급 빈도
- **출력**: `DifficultyReport` (현재 상태, 문제점, 개선 제안)

### 3.3 `generate_scenario(mechanics)`
- **기능**: 게임에 어울리는 스토리와 세계관을 생성합니다.
- **분석 포인트**:
    - 캐릭터 이름 및 배경 설정
    - 게임의 목표(Goal)에 대한 서사적 당위성 부여
    - 스테이지별 테마 제안

### 3.4 `suggest_improvements(analysis_report)`
- **기능**: 분석 결과를 종합하여 구체적인 개선 아이디어를 도출합니다.
- **출력**: `ImprovementTask` 리스트 (우선순위, 예상 난이도 포함)

---

## 4. 프롬프트 엔지니어링 전략 (Prompt Strategy)

### 4.1 페르소나 설정
> "You are a lead game designer with 15 years of experience in casual and arcade games. Your goal is to maximize player retention and fun factor."

### 4.2 Context Injection (맥락 주입)
코드 전체를 넣는 대신 핵심 게임 루프와 변수 선언부 위주로 추출하여 프롬프트에 주입합니다.

**Prompt Example (Analysis):**
```text
Analyze the following game code:
[CODE_SNIPPET]

Identify:
1. Core Loop (Action -> Feedback -> Reward)
2. Win/Loss Conditions
3. Progression System (Leveling, Scoring)
```

---

## 5. 입출력 정의 (I/O)

### 입력 (Input)
- `game_path`: 게임 소스 코드 경로 (예: `games/feeding-caiso/index.html`)
- `constraints`: (Optional) 타겟 연령층, 플랫폼 제약 사항

### 출력 (Output Details)
- **파일명**: `docs/{game_name}_design_review.md`
- **포맷**: Markdown
- **내용 구성**:
    1. **요약 (Executive Summary)**: 게임의 장단점 3줄 요약
    2. **메카닉 분석**: 현재 게임 시스템 정의
    3. **밸런스 평가**: 난이도 및 보상 체계 리뷰
    4. **스토리 제안**: 캐릭터 및 세계관 설정
    5. **개선 로드맵**: 즉시 적용 가능한 개선 사항 (P1, P2 우선순위)

---

## 6. 구현 단계 (Implementation Steps)

1. **Setup**: `BaseAgent` 클래스 정의 (공통 모듈)
2. **Prompts**: `prompts/` 디렉토리에 시스템 프롬프트 작성
3. **Core Logic**: `agent.py`에 분석 및 제안 로직 구현
4. **Integration**: `orchestrator` 또는 단독 실행 스크립트(`main.py`)로 실행 테스트
5. **Validation**: `feeding-caiso` 게임을 대상으로 리포트 생성 및 퀄리티 검증

---

## 7. 검증 계획 (Validation Plan)

- [ ] `feeding-caiso` 실행 후 분석 리포트 생성
- [ ] 리포트가 게임의 실제 로직(변수명, 함수 등)을 정확히 인용하는지 확인
- [ ] 제안된 개선안이 기술적으로 구현 가능한지 확인
