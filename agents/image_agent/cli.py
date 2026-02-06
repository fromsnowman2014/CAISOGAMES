#!/usr/bin/env python3
"""
Image Agent CLI - Command-line interface for game asset generation

Usage:
    python -m image_agent generate --desc "cute red apple" --style kawaii --size 64x64
    python -m image_agent review --image sprite.png --type sprite --style kawaii
    python -m image_agent batch --config batch.yaml
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional


def parse_size(size_str: str) -> tuple:
    """Parse size string like '64x64' into tuple"""
    try:
        parts = size_str.lower().split('x')
        return (int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        raise argparse.ArgumentTypeError(f"Invalid size format: {size_str}. Use WIDTHxHEIGHT (e.g., 64x64)")


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog='image_agent',
        description='AI-powered game asset generation with quality review',
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate a new game asset')
    gen_parser.add_argument('--desc', '-d', required=True, help='Description of the asset')
    gen_parser.add_argument('--type', '-t', default='sprite',
                           choices=['sprite', 'background', 'ui', 'animation', 'icon', 'tile'],
                           help='Type of asset')
    gen_parser.add_argument('--style', '-s', default='kawaii',
                           choices=['pixel_art', 'kawaii', 'chibi', 'cartoon', 'flat',
                                   'realistic', 'retro_8bit', 'retro_16bit', 'watercolor', 'minimalist'],
                           help='Art style')
    gen_parser.add_argument('--size', default='64x64', type=parse_size,
                           help='Size in WIDTHxHEIGHT format (default: 64x64)')
    gen_parser.add_argument('--output', '-o', help='Output file path')
    gen_parser.add_argument('--no-transparency', action='store_true',
                           help='Disable transparent background')
    gen_parser.add_argument('--game', '-g', help='Game context (e.g., "Feeding Caiso")')
    gen_parser.add_argument('--palette', '-p', nargs='+', help='Color palette (hex codes)')
    gen_parser.add_argument('--must-have', nargs='+', help='Required elements')
    gen_parser.add_argument('--max-iterations', type=int, default=5,
                           help='Maximum improvement iterations')
    gen_parser.add_argument('--quality-threshold', type=float, default=0.9,
                           help='Quality threshold (0.0-1.0)')
    gen_parser.add_argument('--verbose', '-v', action='store_true',
                           help='Verbose output')

    # Review command
    review_parser = subparsers.add_parser('review', help='Review existing image quality')
    review_parser.add_argument('--image', '-i', required=True, help='Image file to review')
    review_parser.add_argument('--type', '-t', default='sprite',
                              choices=['sprite', 'background', 'ui', 'animation', 'icon', 'tile'],
                              help='Expected asset type')
    review_parser.add_argument('--style', '-s', default='kawaii',
                              choices=['pixel_art', 'kawaii', 'chibi', 'cartoon', 'flat',
                                      'realistic', 'retro_8bit', 'retro_16bit'],
                              help='Expected style')
    review_parser.add_argument('--check-transparency', action='store_true',
                              help='Check transparency quality')
    review_parser.add_argument('--json', action='store_true',
                              help='Output as JSON')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Generate multiple assets from config')
    batch_parser.add_argument('--config', '-c', required=True, help='YAML config file')
    batch_parser.add_argument('--output-dir', '-o', default='./generated',
                             help='Output directory')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show configuration info')

    return parser


async def cmd_generate(args) -> int:
    """Handle generate command"""
    from agents.image_agent import ImageAgent, AssetRequest
    from agents.image_agent.core.data_classes import AssetType, StyleType

    # Build request
    request = AssetRequest(
        description=args.desc,
        asset_type=AssetType(args.type),
        style=StyleType(args.style),
        size=args.size,
        transparency=not args.no_transparency,
        game_context=args.game or '',
        color_palette=args.palette,
        must_have=args.must_have or [],
        output_path=Path(args.output) if args.output else None,
    )

    # Configure agent
    from agents.image_agent.utils.config import AgentConfig
    config = AgentConfig(
        max_iterations=args.max_iterations,
        quality_threshold=args.quality_threshold,
    )

    # Run generation
    log_level = "DEBUG" if args.verbose else "INFO"
    agent = ImageAgent(config=config, log_level=log_level)

    print(f"\n{'='*60}")
    print(f"Generating: {args.desc}")
    print(f"Type: {args.type}, Style: {args.style}, Size: {args.size[0]}x{args.size[1]}")
    print(f"{'='*60}\n")

    result = await agent.generate(request)

    # Print results
    print(f"\n{'='*60}")
    print(f"RESULT: {'SUCCESS' if result.success else 'BEST EFFORT'}")
    print(f"{'='*60}")
    print(f"Final Score: {result.final_score * 100:.1f}%")
    print(f"Iterations: {result.iterations}")
    print(f"Time: {result.total_time:.2f}s")

    if result.final_image_path:
        print(f"Saved to: {result.final_image_path}")

    # Print iteration history
    print(f"\nIteration History:")
    for record in result.history:
        status = "PASS" if record.review and record.review.passed else "FAIL"
        print(f"  {record.iteration}: {record.score * 100:.1f}% [{status}]")
        if record.review and record.review.issues:
            for issue in record.review.issues[:2]:
                print(f"      - {issue}")

    print()

    return 0 if result.success else 1


async def cmd_review(args) -> int:
    """Handle review command"""
    from PIL import Image
    from agents.image_agent import AssetRequest
    from agents.image_agent.core.data_classes import AssetType, StyleType
    from agents.image_agent.reviewers.quality_reviewer import QualityReviewer

    # Load image
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"Error: Image not found: {image_path}")
        return 1

    image = Image.open(image_path)

    # Create request for context
    request = AssetRequest(
        description="Review existing image",
        asset_type=AssetType(args.type),
        style=StyleType(args.style),
        size=image.size,
        transparency=args.check_transparency,
    )

    # Run review
    reviewer = QualityReviewer()
    report = reviewer.review(image, request)

    if args.json:
        # JSON output
        output = {
            'file': str(image_path),
            'overall_score': report.overall_score,
            'passed': report.passed,
            'scores': {
                'transparency': report.transparency_score,
                'size': report.size_score,
                'style': report.style_score,
                'color': report.color_score,
                'quality': report.quality_score,
                'game_fit': report.game_fit_score,
            },
            'issues': report.issues,
            'suggestions': report.suggestions,
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print(f"\n{'='*60}")
        print(f"Quality Review: {image_path.name}")
        print(f"{'='*60}")
        print(f"Overall Score: {report.overall_score * 100:.1f}% [{'PASS' if report.passed else 'FAIL'}]")
        print()
        print("Detailed Scores:")
        print(f"  Transparency: {report.transparency_score * 100:.0f}%")
        print(f"  Size:         {report.size_score * 100:.0f}%")
        print(f"  Style:        {report.style_score * 100:.0f}%")
        print(f"  Color:        {report.color_score * 100:.0f}%")
        print(f"  Quality:      {report.quality_score * 100:.0f}%")
        print(f"  Game Fit:     {report.game_fit_score * 100:.0f}%")

        if report.issues:
            print("\nIssues:")
            for issue in report.issues:
                print(f"  - {issue}")

        if report.suggestions:
            print("\nSuggestions:")
            for suggestion in report.suggestions:
                print(f"  - {suggestion}")

        if report.strengths:
            print("\nStrengths:")
            for strength in report.strengths:
                print(f"  + {strength}")

        print()

    return 0 if report.passed else 1


async def cmd_batch(args) -> int:
    """Handle batch command"""
    import yaml
    from agents.image_agent import ImageAgent, AssetRequest
    from agents.image_agent.core.data_classes import AssetType, StyleType

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        return 1

    with open(config_path) as f:
        config = yaml.safe_load(f)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    agent = ImageAgent()
    results = []

    for item in config.get('assets', []):
        request = AssetRequest(
            description=item['description'],
            asset_type=AssetType(item.get('type', 'sprite')),
            style=StyleType(item.get('style', 'kawaii')),
            size=tuple(item.get('size', [64, 64])),
            transparency=item.get('transparency', True),
            output_path=output_dir / item.get('filename', f"{item['description'][:20]}.png"),
        )

        print(f"Generating: {item['description'][:40]}...")
        result = await agent.generate(request)
        results.append({
            'description': item['description'],
            'success': result.success,
            'score': result.final_score,
            'output': str(result.final_image_path) if result.final_image_path else None,
        })

    # Print summary
    print(f"\n{'='*60}")
    print("Batch Generation Complete")
    print(f"{'='*60}")
    success_count = sum(1 for r in results if r['success'])
    print(f"Success: {success_count}/{len(results)}")

    for r in results:
        status = "OK" if r['success'] else "FAIL"
        print(f"  [{status}] {r['description'][:30]}... ({r['score']*100:.0f}%)")

    return 0 if success_count == len(results) else 1


def cmd_info(args) -> int:
    """Handle info command"""
    from agents.image_agent.utils.config import AgentConfig

    config = AgentConfig()

    print(f"\n{'='*60}")
    print("Image Agent Configuration")
    print(f"{'='*60}")
    print(f"Quality Threshold: {config.quality_threshold * 100:.0f}%")
    print(f"Max Iterations: {config.max_iterations}")
    print(f"Model Tier: {config.model_tier}")
    print(f"Premium Model: {config.use_premium_model}")
    print()
    print("Quality Weights:")
    for key, value in config.quality_weights.items():
        print(f"  {key}: {value * 100:.0f}%")
    print()
    print("Environment:")
    print(f"  VERCEL_APP_URL: {config.vercel_app_url or 'Not set'}")
    print(f"  GEMINI_API_KEY: {'Set' if config.gemini_api_key else 'Not set'}")
    print()

    return 0


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'generate':
        return asyncio.run(cmd_generate(args))
    elif args.command == 'review':
        return asyncio.run(cmd_review(args))
    elif args.command == 'batch':
        return asyncio.run(cmd_batch(args))
    elif args.command == 'info':
        return cmd_info(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
