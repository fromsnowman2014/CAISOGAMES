# Image Agent

AI-powered game asset generation with quality review and iterative improvement.

## Features

- **Prompt Generation**: Smart prompts based on asset type and style
- **Quality Review**: Automated transparency, style, and color checking  
- **Iterative Improvement**: Refines until 90% quality or max 5 iterations
- **Multiple Styles**: Kawaii, pixel art, cartoon, realistic, etc.

## Usage

### CLI

```bash
# Generate a sprite
python -m agents.image_agent generate "cute red apple" --type sprite --style kawaii

# Review existing asset
python -m agents.image_agent review path/to/image.png --type sprite

# Show help
python -m agents.image_agent --help
```

### Python API

```python
from agents.image_agent import ImageAgent, AssetRequest
from agents.image_agent.core.data_classes import AssetType, StyleType

# Create request
request = AssetRequest(
    description="cute monster eating pizza",
    asset_type=AssetType.SPRITE,
    style=StyleType.KAWAII,
    size=(64, 64),
    transparency=True
)

# Generate
agent = ImageAgent()
result = await agent.generate(request)

# Access result
if result.success:
    print(f"Score: {result.final_score}")
    result.final_image_path  # Saved image path
```

## Configuration

Edit `config.yaml` or use environment variables:

| Setting | Default | Description |
|---------|---------|-------------|
| `max_iterations` | 5 | Max improvement attempts |
| `quality_threshold` | 0.9 | Target quality score |
| `log_level` | INFO | Logging verbosity |

## Architecture

```
image_agent/
├── core/           # Data classes, main agent
├── prompts/        # Prompt generation & improvement
├── reviewers/      # Quality checking (transparency, style, color)
├── image_generator/ # Actual image generation service
└── utils/          # Config, logging
```

## Integration with Orchestrator

The Image Agent provides `비주얼 리뷰` (20 points) in the game scoring system:

```python
# Called by orchestrator
from agents.image_agent import ImageAgent
agent = ImageAgent()
result = await agent.review_existing(image_path, request)
score = result.overall_score  # 0.0 - 1.0
```
