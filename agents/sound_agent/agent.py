"""
Sound Agent - AI-powered game sound analysis and generation

This module provides:
1. Sound audit for games
2. Sound requirements definition
3. Procedural SFX generation (Web Audio API)
4. BGM generation (Tone.js)
5. Integration code generation

Uses SoundMakerService (Vercel API) when available, falls back to local LLM.
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Path setup
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Try to import sound_maker service (Vercel API client)
try:
    from agents.sound_agent.generators.sound_maker import SoundMakerService
    SOUND_MAKER_AVAILABLE = True
except ImportError:
    SOUND_MAKER_AVAILABLE = False

# LLM service (sound_agent's own, extends shared base)
try:
    from agents.sound_agent.utils.llm import LLMService
except ImportError:
    from .utils.llm import LLMService


@dataclass
class SoundRequirement:
    """Represents a single sound requirement."""
    name: str
    category: str  # ui, gameplay, bgm, feedback
    description: str
    duration_ms: int = 200
    priority: str = "medium"  # high, medium, low


@dataclass
class SoundAudit:
    """Result of auditing a game's sound implementation."""
    existing_sounds: List[str]
    missing_sounds: List[str]
    priority_sounds: List[str]
    analysis_text: str


class SoundAgent:
    """
    Main orchestrator for AI-powered game sound analysis and generation.
    
    Workflow:
    1. Audit existing sounds in game
    2. Define sound requirements
    3. Generate procedural SFX code
    4. Generate BGM code
    5. Create integration snippets
    
    Uses SoundMakerService (Vercel API) when available, falls back to local LLM.
    """
    
    def __init__(self, api_key: Optional[str] = None, use_api: bool = True):
        """
        Initialize the Sound Agent.
        
        Args:
            api_key: Gemini API key (uses env var if not provided)
            use_api: Whether to use Vercel API (True) or local LLM (False)
        """
        self.prompts_dir = Path(__file__).parent / "prompts"
        self.use_sound_maker = False
        
        # Try to use SoundMakerService if available and requested
        if use_api and SOUND_MAKER_AVAILABLE:
            try:
                self.sound_maker = SoundMakerService()
                health = self.sound_maker.check_health()
                if health.get('status') == 'ok' and health.get('api_configured'):
                    self.use_sound_maker = True
                    print("✅ Using SoundMaker API (Vercel)")
                else:
                    print("⚠️ SoundMaker API not configured, using local LLM")
            except Exception as e:
                print(f"⚠️ SoundMaker API unavailable: {e}")
        
        # Fallback to local LLM
        if not self.use_sound_maker:
            self.llm = LLMService(api_key=api_key)
        
    def load_prompt(self, name: str) -> str:
        """Load a prompt template by name."""
        prompt_path = self.prompts_dir / f"{name}.txt"
        if prompt_path.exists():
            return prompt_path.read_text()
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    
    def audit_sounds(self, game_path: str) -> SoundAudit:
        """
        Analyze a game's current sound implementation.
        
        Args:
            game_path: Path to game HTML file
            
        Returns:
            SoundAudit with analysis results
        """
        print("🔍 Phase 1: Auditing Sounds...")
        
        # Read game source
        game_file = Path(game_path)
        if not game_file.exists():
            raise FileNotFoundError(f"Game file not found: {game_path}")
        
        source_code = game_file.read_text()
        
        # Quick scan for existing audio
        existing_sounds = self._scan_existing_audio(source_code)
        
        # LLM analysis
        prompt_template = self.load_prompt("audit_sounds")
        prompt = prompt_template.replace("{source_code}", source_code[:15000])  # Limit size
        
        analysis = self.llm.generate(prompt)
        
        # Parse priority sounds from analysis
        priority_sounds = self._extract_priority_sounds(analysis)
        
        return SoundAudit(
            existing_sounds=existing_sounds,
            missing_sounds=priority_sounds,
            priority_sounds=priority_sounds[:5],
            analysis_text=analysis
        )
    
    def _scan_existing_audio(self, source: str) -> List[str]:
        """Quick scan for existing audio references."""
        patterns = [
            r'<audio[^>]*>',
            r'new Audio\([^)]*\)',
            r'AudioContext',
            r'\.mp3|\.wav|\.ogg',
            r'Tone\.',
        ]
        found = []
        for pattern in patterns:
            matches = re.findall(pattern, source, re.IGNORECASE)
            found.extend(matches)
        return list(set(found))
    
    def _extract_priority_sounds(self, analysis: str) -> List[str]:
        """Extract priority sound names from analysis."""
        # Simple extraction - look for numbered lists
        lines = analysis.split('\n')
        sounds = []
        for line in lines:
            if re.match(r'^\d+\.', line.strip()):
                # Extract sound name from numbered item
                match = re.search(r'[`"\']([\w_]+)[`"\']', line)
                if match:
                    sounds.append(match.group(1))
                else:
                    # Use first few words as name
                    words = line.split(':')[0].strip().split()
                    if len(words) > 1:
                        sounds.append('_'.join(words[1:3]).lower())
        return sounds[:10]
    
    def define_requirements(self, game_path: str, audit: SoundAudit, genre: str = "casual") -> List[SoundRequirement]:
        """
        Generate detailed sound requirements based on audit.
        
        Args:
            game_path: Path to game file
            audit: Previous audit result
            genre: Game genre
            
        Returns:
            List of SoundRequirement objects
        """
        print("📋 Phase 2: Defining Requirements...")
        
        prompt_template = self.load_prompt("define_requirements")
        prompt = prompt_template.replace("{game_analysis}", audit.analysis_text[:5000])
        prompt = prompt.replace("{genre}", genre)
        
        requirements_text = self.llm.generate(prompt)
        
        # Parse requirements (simplified - in production would parse tables)
        requirements = []
        for sound in audit.priority_sounds[:5]:
            requirements.append(SoundRequirement(
                name=sound,
                category="gameplay",
                description=f"SFX for {sound.replace('_', ' ')}",
                duration_ms=200,
                priority="high"
            ))
        
        return requirements
    
    def generate_sfx_code(self, requirement: SoundRequirement) -> str:
        """
        Generate Web Audio API code for a sound effect.
        
        Args:
            requirement: Sound requirement specification
            
        Returns:
            JavaScript code string
        """
        print(f"🔊 Generating SFX: {requirement.name}...")
        
        # Use SoundMaker API if available
        if self.use_sound_maker:
            try:
                return self.sound_maker.generate_sfx(
                    name=requirement.name,
                    description=requirement.description,
                    duration=requirement.duration_ms,
                    category=requirement.category
                )
            except Exception as e:
                print(f"⚠️ API error, falling back to local: {e}")
        
        # Fallback to local LLM
        prompt_template = self.load_prompt("generate_sfx")
        prompt = prompt_template.replace("{sound_name}", requirement.name)
        prompt = prompt.replace("{description}", requirement.description)
        prompt = prompt.replace("{duration}", str(requirement.duration_ms))
        prompt = prompt.replace("{category}", requirement.category)
        prompt = prompt.replace("{SoundName}", requirement.name.title().replace("_", ""))
        
        return self.llm.generate(prompt)
    
    def generate_bgm_code(self, track_name: str, scene: str, mood: str, tempo: int = 120) -> str:
        """
        Generate Tone.js code for background music.
        
        Args:
            track_name: Name for the BGM track
            scene: Scene type (menu, gameplay, gameover)
            mood: Mood description
            tempo: BPM
            
        Returns:
            JavaScript code string
        """
        print(f"🎵 Generating BGM: {track_name}...")
        
        # Use SoundMaker API if available
        if self.use_sound_maker:
            try:
                return self.sound_maker.generate_bgm(
                    track_name=track_name,
                    scene=scene,
                    mood=mood,
                    tempo=tempo
                )
            except Exception as e:
                print(f"⚠️ API error, falling back to local: {e}")
        
        # Fallback to local LLM
        prompt_template = self.load_prompt("generate_bgm")
        prompt = prompt_template.replace("{track_name}", track_name)
        prompt = prompt.replace("{scene}", scene)
        prompt = prompt.replace("{mood}", mood)
        prompt = prompt.replace("{tempo}", str(tempo))
        prompt = prompt.replace("{looping}", "Yes")
        prompt = prompt.replace("{TrackName}", track_name.title().replace("_", ""))
        
        return self.llm.generate(prompt)
    
    def analyze(self, game_path: str) -> str:
        """
        Run full sound analysis and generate report.
        
        Args:
            game_path: Path to game HTML file
            
        Returns:
            Path to generated report
        """
        game_file = Path(game_path)
        game_name = game_file.stem
        
        print(f"🎧 Analyzing sounds for: {game_name}")
        print("-" * 40)
        
        # 1. Audit existing sounds
        audit = self.audit_sounds(game_path)
        
        # 2. Define requirements
        requirements = self.define_requirements(game_path, audit)
        
        # 3. Generate SFX code for top 3 priority sounds
        sfx_codes = {}
        for req in requirements[:3]:
            sfx_codes[req.name] = self.generate_sfx_code(req)
        
        # 4. Generate report
        print("📝 Phase 4: Compiling Report...")
        report = self._compile_report(game_name, audit, requirements, sfx_codes)
        
        # 5. Save report
        report_path = Path("docs") / f"{game_name}_sound_audit.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report)
        
        print(f"✅ Sound Audit Saved: {report_path}")
        return str(report_path)
    
    def _compile_report(
        self, 
        game_name: str, 
        audit: SoundAudit,
        requirements: List[SoundRequirement],
        sfx_codes: Dict[str, str]
    ) -> str:
        """Compile the final sound audit report."""
        report = f"""# {game_name.replace('-', ' ').title()} - Sound Audit Report

> **Generated by Sound Agent**
> Date: {self._get_date()}

---

## 🔍 Current Sound Status

### Existing Audio Elements
"""
        if audit.existing_sounds:
            for sound in audit.existing_sounds:
                report += f"- `{sound}`\n"
        else:
            report += "- ⚠️ No existing audio implementation found\n"
        
        report += f"""
---

## 📋 Sound Requirements

| Priority | Sound | Category | Description |
|----------|-------|----------|-------------|
"""
        for req in requirements:
            report += f"| {req.priority.upper()} | `{req.name}` | {req.category} | {req.description} |\n"
        
        report += """
---

## 🔊 Generated SFX Code

"""
        for name, code in sfx_codes.items():
            report += f"### {name}\n\n```javascript\n{code}\n```\n\n"
        
        report += f"""---

## 🎵 BGM Recommendations

| Scene | Mood | Tempo | Priority |
|-------|------|-------|----------|
| Menu | Upbeat, Catchy | 100 BPM | Medium |
| Gameplay | Energetic | 120 BPM | High |
| Game Over | Melancholic | 80 BPM | Low |

---

## 🚀 Next Steps

1. Add the generated SFX functions to your game
2. Initialize AudioContext on first user interaction
3. Call sound functions at appropriate game events
4. Consider adding volume controls
5. Test on mobile devices (touch-to-unlock audio)

---

## 📊 Analysis Details

{audit.analysis_text}
"""
        return report
    
    
    def _get_date(self) -> str:
        """Get current date string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Sound Agent: Analyze game and generate audio assets.')
    parser.add_argument('game_path', help='Path to the game index.html file')
    parser.add_argument('--key', help='Gemini API Key (optional)', default=None)
    
    args = parser.parse_args()
    
    print("🎵 Starting Sound Agent...")
    agent = SoundAgent(api_key=args.key)
    
    try:
        if not os.path.exists(args.game_path):
            print(f"❌ Error: Game file not found at {args.game_path}")
            sys.exit(1)
            
        report_path = agent.analyze(args.game_path)
        print(f"\n✨ Sound Agent finished successfully!")
        print(f"📄 Report: {report_path}")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
