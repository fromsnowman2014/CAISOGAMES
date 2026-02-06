
import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.image_agent.core.image_agent import ImageAgent
from agents.image_agent.core.data_classes import AssetRequest, AssetType, StyleType
from agents.sound_agent.agent import SoundAgent, SoundRequirement

async def generate_assets():
    print("🚀 Starting Phase 4 Asset Generation...")
    
    base_path = Path("games/feeding-caiso/assets")
    src_path = Path("games/feeding-caiso/src/generated")
    
    # Initialize agents
    image_agent = ImageAgent()
    sound_agent = SoundAgent()
    
    # --- IMAGE ASSETS ---
    image_tasks = [
        # Caiso
        {
            "name": "caiso_idle",
            "desc": "Cute purple slime monster baby, kawaii face, neon glowing outline, vector style, transparent background",
            "path": base_path / "sprites/caiso/caiso_idle.png",
            "type": AssetType.SPRITE
        },
        {
            "name": "caiso_hungry",
            "desc": "Round purple monster with open mouth, hungry expression, neon highlights, vector illustration",
            "path": base_path / "sprites/caiso/caiso_hungry.png",
            "type": AssetType.SPRITE
        },
        {
            "name": "caiso_happy",
            "desc": "Happy purple monster chewing food, closed eyes, neon sparkles, vector style",
            "path": base_path / "sprites/caiso/caiso_happy.png",
            "type": AssetType.SPRITE
        },
        # Foods
        {
            "name": "food_apple",
            "desc": "Neon glowing red apple, stylized vector icon, transparent background",
            "path": base_path / "items/food_apple.png",
            "type": AssetType.ICON
        },
        {
            "name": "food_burger",
            "desc": "Stylized hamburger with neon glowing lettuce and bun, vector icon",
            "path": base_path / "items/food_burger.png",
            "type": AssetType.ICON
        },
        {
            "name": "food_pizza",
            "desc": "Slice of pepperoni pizza with dripping neon cheese, holographic effect, vector",
            "path": base_path / "items/food_pizza.png",
            "type": AssetType.ICON
        },
        {
            "name": "food_dorito",
            "desc": "Neon orange nacho chip, glowing triangle shape, vector style",
            "path": base_path / "items/food_dorito.png",
            "type": AssetType.ICON
        },
        {
             "name": "food_dynamite",
             "desc": "Red dynamite stick with sparking fuse, cartoon style, neon glow",
             "path": base_path / "items/food_dynamite.png",
             "type": AssetType.ICON
        },
        # Villagers
        {
            "name": "villager_normal",
            "desc": "Tiny cute blue blob character, simple face, neon outline, vector style",
            "path": base_path / "sprites/villagers/villager_normal.png",
            "type": AssetType.SPRITE
        },
        {
            "name": "villager_scared",
            "desc": "Tiny cute blue blob character, scared expression, sweating, neon outline",
            "path": base_path / "sprites/villagers/villager_scared.png",
            "type": AssetType.SPRITE
        },
        # Player
        {
            "name": "player_throwing",
            "desc": "White stick figure character in throwing pose, neon glow, minimal vector style",
            "path": base_path / "sprites/player/player_throwing.png",
            "type": AssetType.SPRITE
        },
        # Backgrounds
        {
            "name": "bg_sky",
            "desc": "Synthwave sunset sky gradient, purple to orange, retro grid capability",
            "path": base_path / "backgrounds/bg_sky.png",
            "type": AssetType.BACKGROUND,
            "size": (480, 854)
        },
        {
            "name": "bg_city",
            "desc": "Silhouette of futuristic cute city skyline, neon windows, seamless horizontal",
            "path": base_path / "backgrounds/bg_city.png",
            "type": AssetType.BACKGROUND,
            "size": (480, 300)
        }
    ]

    print(f"🎨 Generating {len(image_tasks)} image assets...")
    
    for task in image_tasks:
        if task["path"].exists():
            print(f"Skipping {task['name']} (exists)")
            continue
            
        print(f"Generating {task['name']}...")
        req = AssetRequest(
            description=task["desc"],
            asset_type=task["type"],
            style=StyleType.KAWAII,
            size=task.get("size", (128, 128)),
            output_path=task["path"]
        )
        
        result = await image_agent.generate(req)
        
        if result.success and result.final_image_data:
            with open(task["path"], "wb") as f:
                f.write(result.final_image_data)
            print(f"✅ Saved {task['path']}")
        else:
            print(f"❌ Failed to generate {task['name']}: {result.error}")

    # --- SOUND ASSETS ---
    sound_tasks = [
        {"name": "throw", "desc": "Retro jump/throw sound, light synth pluck", "duration": 200, "cat": "gameplay"},
        {"name": "eat", "desc": "Crunchy bite sound mixed with a happy chirp", "duration": 300, "cat": "gameplay"},
        {"name": "combo", "desc": "Rising pitch synth scale, energetic", "duration": 500, "cat": "feedback"},
        {"name": "fever", "desc": "Explosive neon transition, power-up sound, rapid arpeggio", "duration": 1500, "cat": "gameplay"},
        {"name": "gameover", "desc": "Slow down tape stop effect, sad trombone synth", "duration": 2000, "cat": "ui"}
    ]
    
    print(f"🔊 Generating {len(sound_tasks)} sound assets (Code)...")
    
    sound_library_code = "// Generated Sound Library (Web Audio API)\nexport const SoundLibrary = {\n"
    
    for task in sound_tasks:
        print(f"Generating SFX: {task['name']}...")
        req = SoundRequirement(
            name=task["name"],
            description=task["desc"],
            duration_ms=task["duration"],
            category=task["cat"]
        )
        
        code = sound_agent.generate_sfx_code(req)
        # Wrap in function
        func_name = f"play{task['name'].title()}"
        sound_library_code += f"    {task['name']}: (ctx, masterVol) => {{\n        {code}\n    }},\n"
        
    sound_library_code += "};\n"
    
    with open(src_path / "SoundLibrary.js", "w") as f:
        f.write(sound_library_code)
    print(f"✅ Saved SoundLibrary.js")

    print("🎉 Asset Generation Complete!")

if __name__ == "__main__":
    asyncio.run(generate_assets())
