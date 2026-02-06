import os
import sys
import json
import time
import random
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add parent directory to path to allow import of utils
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from agents.play_agent.utils.llm import LLMService
except ImportError:
    # Fallback for direct execution
    from utils.llm import LLMService

class PlayAgent:
    """
    Play Agent: Automated Game Testing & QA.
    Supports Playwright for real testing and Simulation Mode for fallback.
    """
    
    def __init__(self, output_dir: str = "docs"):
        self.output_dir = Path(output_dir)
        self.llm = LLMService()
        self.prompts_dir = Path(__file__).parent / "prompts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_prompt(self, name: str) -> str:
        path = self.prompts_dir / f"{name}.txt"
        if not path.exists():
            return "Analyze the following logs:\n{{ logs }}"
        return path.read_text(encoding="utf-8")

    def run(self, game_path: str, use_simulation: bool = False) -> str:
        """
        Run QA test on the specified game.
        """
        game_name = Path(game_path).parent.name
        print(f"🤖 Starting QA Test for: {game_name}")
        
        logs = []
        mode = "Automated Test (Playwright)"
        
        if use_simulation:
            print("⚠️ Playwright not detected or simulation requested. Running in Simulation Mode.")
            logs = self._run_simulation(game_name)
            mode = "Simulation Mode"
        else:
            try:
                # Try import inside method to avoid dependency errors at load time
                from playwright.sync_api import sync_playwright
                logs = self._run_playwright(game_path)
            except ImportError:
                print("⚠️ Playwright library not found. Falling back to Simulation Mode.")
                logs = self._run_simulation(game_name)
                mode = "Simulation Mode (Fallback)"
            except Exception as e:
                print(f"❌ Playwright execution failed: {e}")
                print("Falling back to Simulation Mode.")
                logs = self._run_simulation(game_name)
                mode = "Simulation Mode (Error Recovery)"
                
        # Analyze Logs
        print(f"📊 Analyzing logs with AI ({mode})...")
        report = self.analyze_logs(logs, mode)
        
        # Save Report
        report_path = self.output_dir / f"{game_name}_qa_report.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"✅ QA Report Saved: {report_path}")
        
        return str(report_path)

    def _run_playwright(self, game_path: str) -> List[Dict[str, Any]]:
        """Run real browser test using Playwright."""
        from playwright.sync_api import sync_playwright
        
        logs = []
        abs_path = "file://" + os.path.abspath(game_path)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Listen for console logs
            page.on("console", lambda msg: logs.append({
                "timestamp": time.time(),
                "type": msg.type,
                "text": msg.text
            }))
            
            # Listen for uncaught exceptions
            page.on("pageerror", lambda err: logs.append({
                "timestamp": time.time(),
                "type": "error",
                "text": str(err)
            }))
            
            print(f"🌍 Opening game: {abs_path}")
            page.goto(abs_path)
            page.wait_for_load_state("networkidle")
            
            # Simulate Gameplay (Random Actions)
            print("🎮 Simulating player actions...")
            for i in range(20): # 20 steps
                # Random click (Throw food)
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                page.mouse.click(x, y)
                
                # Measure FPS (approximate via JS)
                # fps = page.evaluate("() => window.performance.now()") 
                logs.append({"timestamp": time.time(), "type": "metric", "fps": 60}) # Mock metric
                
                time.sleep(0.5)
                
            browser.close()
            
        return logs

    def _run_simulation(self, game_name: str) -> List[Dict[str, Any]]:
        """Generate simulated logs for testing without Playwright."""
        print("🎭 Generating simulated gameplay logs...")
        logs = []
        start_time = time.time()
        
        # 1. Init
        logs.append({"timestamp": start_time, "type": "info", "text": f"Game Init: {game_name}"})
        logs.append({"timestamp": start_time + 0.1, "type": "info", "text": "Assets Loaded: 14/14"})
        
        # 2. Gameplay Loop (Simulated)
        for i in range(10):
            current_time = start_time + i
            
            # FPS stable mostly
            fps = random.randint(55, 60)
            logs.append({"timestamp": current_time, "type": "metric", "fps": fps})
            
            # Random Events
            if i == 3:
                logs.append({"timestamp": current_time, "type": "log", "text": "Player Action: Throw Food"})
            if i == 4:
                logs.append({"timestamp": current_time, "type": "log", "text": "Event: Caiso Hit (Happy)"})
                logs.append({"timestamp": current_time, "type": "log", "text": "Score: 10"})
            
            # Occasional warning
            if i == 7:
                 logs.append({"timestamp": current_time, "type": "warning", "text": "AudioContext was not allowed to start. It must be resumed (or created) after a user gesture."})

        return logs

    def analyze_logs(self, logs: List[Dict[str, Any]], mode: str) -> str:
        """Call LLM to analyze the logs."""
        log_str = json.dumps(logs, indent=2)
        prompt_tmpl = self.load_prompt("analyze_gameplay")
        prompt = prompt_tmpl.replace("{{ logs }}", log_str)
        
        analysis = self.llm.generate(prompt)
        
        return f"""# {os.environ.get('GAME_NAME', 'Game')} - QA Report

> **Generated by Play Agent**
> Date:Today
> Mode: {mode}

---

## 📊 Test Log Summary
- **Total Logs**: {len(logs)}

---

## 🤖 AI Analysis Report
{analysis}

---

## 📝 Raw Logs (Snippet)
```json
{json.dumps(logs[:5], indent=2)}
...
```
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent.py <game_path> [--sim]")
        sys.exit(1)
        
    game_path = sys.argv[1]
    use_sim = "--sim" in sys.argv
    
    agent = PlayAgent()
    agent.run(game_path, use_simulation=use_sim)
