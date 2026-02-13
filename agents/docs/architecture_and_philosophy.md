# Caiso Games Agents & API Architecture

## 1. Overview (개요)
Caiso Games의 Agent 시스템은 게임 개발의 전 과정(기획, 디자인, 사운드, 개발, 테스트)을 AI Agent들이 협업하여 수행하는 것을 목표로 합니다. 각 Agent는 독립적인 역할(Role)과 책임(Responsibility)을 가지며, 공통된 프로토콜을 통해 소통합니다.

## 2. Core Philosophy (핵심 철학)

### 2.1 Separation of Concerns (관심사의 분리)
- **Role-Based:** 각 Agent는 명확히 정의된 역할만 수행합니다. (예: `ImageAgent`는 그림만 그리고, 기획에 관여하지 않음)
- **Modular Design:** 모든 Agent는 독립적인 모듈로 구성되어 있어, 하나를 교체하거나 업그레이드해도 전체 시스템에 영향을 주지 않습니다.

### 2.2 Iterative Improvement (반복적 개선)
- **Self-Correction:** 결과물을 단순히 생성하는 데 그치지 않고, 스스로 품질을 검토(Review)하고 기준에 미달하면 다시 생성(Retry)하여 품질을 높입니다.
- **Feedback Loop:** `PromptGenerator` -> `Generator` -> `Reviewer` -> `PromptImprover` -> `Generator` 순환 구조를 가집니다.

### 2.3 Deterministic & Reproducible (결정론적 및 재현 가능성)
- **Structured Inputs:** 모든 요청은 `AssetRequest`와 같은 명확한 데이터 클래스(Data Class)로 정의됩니다.
- **Controlled Randomness:** AI의 창의성을 허용하되, 스타일 가이드라인(Style Guideline)과 부정 프롬프트(Negative Prompt)를 통해 일관된 톤앤매너를 유지합니다.

---

## 3. Agent Architecture (에이전트 아키텍처)

### 3.1 Common Layers
모든 Agent는 다음과 같은 공통 계층 구조를 가집니다:
1.  **Interface Layer (CLI/API):** 외부(사용자 또는 다른 Agent)와의 소통 창구.
2.  **Core Core Layer:** Agent의 메인 로직 및 오케스트레이션(Orchestration) 담당.
3.  **Generator Layer:** 실제 작업물(코드, 이미지, 사운드)을 생성하는 LLM/Model 연동부.
4.  **Review Layer:** 생성된 작업물의 품질을 검증하는 로직.

### 3.2 Specific Agents

#### 🎨 ImageAgent
- **Goal:** 게임에 필요한 시각적 자산(Sprite, UI, Background) 생성.
- **Key Features:**
    - **White Background Enforcement:** 투명 배경이 필요한 경우, `isolated on solid white background`를 강제하여 후처리를 용이하게 함.
    - **No-Text Policy:** 이미지 생성 시 텍스트, 로고 등이 포함되지 않도록 강력한 Negative Prompt 적용.
    - **Quality Review:** 투명도, 크기, 스타일, 색상 등을 0.0~1.0 점수로 평가. (흰색 배경도 투명 배경의 일종으로 인정하여 Pass 처리 후 후가공)

#### 🎵 SoundAgent
- **Goal:** 효과음(SFX) 및 배경음악(BGM) 생성.
- **Key Features:**
    - **Procedural Generation:** Web Audio API 코드를 생성하여 실시간으로 합성되는 사운드 구현 (Phase 5+).
    - **Fallback Mechanism:** API 생성 실패 시 로컬 로직으로 대체.

#### 🧠 DesignAgent
- **Goal:** 게임 기획, 레벨 디자인, 밸런싱 담당.
- **Key Features:**
    - **Concept Definition:** 추상적인 아이디어를 구채적인 게임 명세서(GDD)로 변환.
    - **Style Guidance:** 프로젝트(Phase)별 디자인 철학(Modern, Ethereal 등)을 정의하고 다른 Agent에게 전파.

#### 💻 CodeAgent
- **Goal:** 실제 게임 코드 구현 및 리팩토링.
- **Key Features:**
    - **Context Awareness:** 현재 프로젝트의 파일 구조와 코딩 컨벤션을 이해하고 코드 작성.
    - **Test-Driven:** 테스트 케이스를 먼저 고려하거나 작성된 코드의 무결성 검증.

---

## 4. API Structure

### 4.1 Communication
- **Standard:** RESTful API 및 CLI(Command Line Interface) 지원.
- **Data Format:** JSON을 표준으로 사용.

### 4.2 Endpoints (Vercel/Server)
- `/api/generate-image`: 이미지 생성 요청 처리.
- `/api/generate-sound`: 사운드 생성 요청 처리.
- `/api/analyze-code`: 코드 분석 및 리뷰 요청.

---

## 5. Workflow Example (Image Generation)

1.  **Request:** "얼음 수정 모양의 적 캐릭터(Enemy)" 요청 접수.
2.  **Prompting:** `PromptGenerator`가 "crystallized ice enemy, floating, geometric shapes, glowing blue core, isolated on white background" 등으로 변환.
3.  **Generation:** `GeminiGenerator`가 이미지 생성.
4.  **Review:** `QualityReviewer`가 검사.
        - *Check 1:* 흰색 배경인가? (OK -> `TransparencyReport` Pass)
        - *Check 2:* 텍스트가 없는가? (OK)
5.  **Post-Processing:** (필요시) `ImageProcessor`가 흰색 배경을 투명하게 변환.
6.  **Final Output:** 게임 내 `assets` 폴더에 저장.

---
*This document serves as the "constitution" for Caiso Games' agent system.*
