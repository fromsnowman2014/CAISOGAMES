# 🎮 CAISOGAMES Play Agent

**Play Agent**는 게임의 QA(Quality Assurance)를 담당하는 AI 에이전트입니다.
브라우저 자동화 도구인 **Playwright**를 사용하여 실제 게임 플레이를 테스트하고, 로그를 분석하여 버그와 성능 문제를 찾아냅니다.

## 기능
1. **🤖 Automated Testing**: 실제 브라우저에서 게임을 실행하고 랜덤 입력을 수행합니다.
2. **🎭 Simulation Mode**: Playwright 설치가 어려운 환경을 위한 Mock 테스트 모드를 지원합니다.
3. **📊 Log Analysis**: FPS, Error, Gameplay Event 로그를 LLM으로 분석하여 리포트를 작성합니다.

## 설치 (Playwright)

`Play Agent`의 모든 기능을 사용하려면 Playwright 설치가 필요합니다.

```bash
pip install playwright
playwright install chromium
```

Playwright가 없어도 **Simulation Mode**로 기본 분석 기능을 테스트할 수 있습니다.

## 실행 방법

### 1. Automated Test (Requires Playwright)
```bash
python -m agents.play_agent.agent games/feeding-caiso/index.html
```

### 2. Simulation Mode (Fallback)
```bash
python -m agents.play_agent.agent games/feeding-caiso/index.html --sim
```

## 출력
`docs/{game_name}_qa_report.md` 경로에 Markdown 리학트가 생성됩니다.

### 리포트 예시
- **Stability**: Crash 여부, JS 에러 리스팅
- **Performance**: 평균 FPS, 프레임 드랍 분석
- **Mechanics**: 점수 증가, 충돌 판정 정상 여부
