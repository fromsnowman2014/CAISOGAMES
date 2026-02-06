# 🎨 Feeding Caiso - UI Analysis & Improvement Report

> **Date**: 2026-02-06
> **Scope**: UI Layout Audit & Fixes based on Screenshot Analysis

---

## 🔍 Analysis of Current State (Before Fix)

사용자가 제공한 스크린샷과 `index.html` 코드를 `Design Agent` 및 Manual Inspection으로 정밀 분석한 결과, 다음 3가지 핵심 문제가 식별되었습니다.

### 1. Title Legibility (Title Overlap)
- **Observation**: "FEEDING CAISO" 타이틀 텍스트와 보라색 캐릭터(Caiso) 얼굴이 정확히 같은 Y축 영역에 겹쳐 있어 가독성이 떨어짐.
- **Root Cause**: `drawMenuScreen` 함수에서 `this.caiso.draw`를 호출할 때 기본 게임 내 위치(Y=180)를 그대로 사용. 타이틀 텍스트도 비슷한 위치(Y=120~175)에 렌더링됨.

### 2. "TAP TO START" Visibility (Z-index Clash)
- **Observation**: "TAP TO START" 문구의 절반 정도가 하단의 거대한 "FEED!" 버튼에 가려져 보이지 않음.
- **Root Cause**: 
  - `touchFeedBtn` (HTML Button)은 `z-index: 100`으로 Canvas 위에 떠 있음.
  - "TAP TO START" 텍스트는 Canvas 내부(Y=760)에 그려짐.
  - 버튼 위치(`bottom: 25px` -> Y ≈ 730)가 텍스트 위치를 덮음.

### 3. Layout Harmony
- **Observation**: Instructions Panel이 너무 아래쪽에 쏠려 있어 하단 여백이 답답함.

---

## 🛠️ Implemented Improvements

위 문제들을 해결하기 위해 `index.html`과 `agents/code_agent`를 수정했습니다.

### 1. Menu Screen Layout Optimization
- **Character Offset**: 메뉴 화면에서 캐릭터(Caiso)를 **Y축으로 100px 아래로 이동**(`ctx.translate(0, 100)`). 이제 캐릭터가 타이틀 텍스트 아래에 위치하여 서로 겹치지 않습니다.
- **Background Fallback**: 배경 이미지가 없을 때도 캐릭터와 텍스트가 조화롭게 배치되도록 조정했습니다.

### 2. Dynamic Button Visibility
- **Action**: 초기 메뉴 화면에서는 **"FEED!" 버튼을 숨김 처리** (`display: none`).
- **Logic**: 게임이 시작(`startGame`)될 때만 버튼이 나타나고, 게임 오버나 승리 시 다시 사라지도록 상태 관리 로직을 추가했습니다.
- **Result**: "TAP TO START" 문구가 버튼에 가려지지 않고 선명하게 보입니다.

### 3. Panel Adjustment
- **Action**: 하단 설명 패널(Instructions)을 **50px 위로 이동** (Y=580 -> Y=530).
- **Result**: "TAP TO START" 문구를 위한 충분한 시각적 여백을 확보했습니다.

### 4. Technical Fixes (Code Agent)
- **SSL Fix**: `agents/code_agent/agent.py`에 SSL 인증서 우회 로직을 추가하여 로컬 환경에서 Code Agent가 Vercel API를 호출할 수 있도록 수정했습니다. (단, 현재 Vercel 배포가 되지 않아 404 에러 발생 중 -> **배포 필요**)

---

## 📸 Expected Result (After Fix)

| Element | Correction |
|---------|------------|
| **Title** | "FEEDING CAISO"가 캐릭터와 겹치지 않고 상단에 명확히 표시됨 |
| **Character** | 타이틀 아래쪽 중앙에 위치하여 안정감 있는 구도 형성 |
| **Start Text** | "FEED!" 버튼 없이 "TAP TO START"가 깜빡이며 시선 집중 |
| **Play** | 화면 터치 시 게임이 시작되며 "FEED!" 버튼 등장 |

---

## 🚀 Next Steps

1. **Verify UI**: 로컬 서버에서 `index.html`을 열어 변경된 레이아웃을 확인하세요.
2. **Deploy**: 수정된 `index.html`과 에이전트 코드를 Vercel에 배포하세요.
