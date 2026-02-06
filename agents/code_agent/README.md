# 💻 CAISOGAMES Code Agent

**Code Agent**는 게임 소스 코드를 분석하여 구조적, 성능적 개선안을 제시하는 AI 엔지니어입니다.

## 기능
1. **🏗️ 구조 분석**: 코드의 아키텍처, 패턴, 안티패턴을 분석합니다.
2. **⚡ 성능 최적화**: 렌더링 루프, 메모리 관리, 이벤트 핸들링의 병목을 찾아냅니다.
3. **📱 모바일 지원 평가**: 터치 이벤트 지원 및 반응형 디자인 여부를 점검합니다.

## 설치 및 실행

### 필수 요구사항
- Python 3.8+
- Gemini API Key (Optional for real analysis, Mock mode available)

### 실행 방법

```bash
# 환경 변수 설정 (권장)
export GEMINI_API_KEY="your_api_key_here"

# CLI로 실행
python -m agents.code_agent.agent <path_to_game_file>
```

예시:
```bash
python -m agents.code_agent.agent games/feeding-caiso/index.html
```

## 출력
`docs/{game_name}_code_review.md` 경로에 Markdown 형태의 리포트가 생성됩니다.

## 디렉토리 구조
- `agent.py`: 메인 에이전트 로직
- `utils/llm.py`: Gemini API 클라이언트 (Mock 모드 포함)
- `prompts/`: 분석 주제별 프롬프트 템플릿
