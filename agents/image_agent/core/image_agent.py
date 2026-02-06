"""
Image Agent - Main orchestrator for AI-powered game asset generation

This is the main entry point for the Image Agent system.
It coordinates prompt generation, image creation, quality review,
and iterative improvement.
"""

import asyncio
import sys
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Optional

from PIL import Image

# Add parent directory for image_generator import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.image_agent.core.data_classes import (
    AgentResult,
    AssetRequest,
    DetailedPrompt,
    IterationRecord,
    QualityReport,
)
from agents.image_agent.prompts.prompt_generator import PromptGenerator
from agents.image_agent.prompts.prompt_improver import PromptImprover
from agents.image_agent.reviewers.quality_reviewer import QualityReviewer
from agents.image_agent.utils.config import AgentConfig
from agents.image_agent.utils.logging import get_logger, setup_logging


class ImageAgent:
    """
    Main orchestrator for AI-powered game asset generation

    Workflow:
    1. Parse asset request
    2. Generate detailed prompt
    3. Generate image using image_generator
    4. Review quality
    5. If < 90% quality, improve prompt and retry (max 5 times)
    6. Return best result
    """

    def __init__(
        self,
        config: Optional[AgentConfig] = None,
        log_level: str = "INFO"
    ):
        """
        Initialize the Image Agent

        Args:
            config: Configuration settings (uses defaults if None)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.config = config or AgentConfig()
        self.logger = setup_logging(level=log_level)

        # Initialize components
        self.prompt_generator = PromptGenerator()
        self.prompt_improver = PromptImprover()
        self.quality_reviewer = QualityReviewer(weights=self.config.quality_weights)

        # Image generator service (lazy loaded)
        self._generator_service = None

    @property
    def generator_service(self):
        """Lazy load the image generator service"""
        if self._generator_service is None:
            try:
                from agents.image_agent.image_generator import ImageGeneratorService
                self._generator_service = ImageGeneratorService()
                self.logger.info(f"Using generator: {self._generator_service.generator_type}")
            except ImportError:
                self.logger.error("image_generator not found - using mock mode")
                self._generator_service = MockGeneratorService()
        return self._generator_service

    async def generate(self, request: AssetRequest) -> AgentResult:
        """
        Generate a game asset with quality iteration

        This is the main entry point. It will:
        1. Generate initial prompt
        2. Create image
        3. Review quality
        4. Iterate until 90% quality or 5 attempts

        Args:
            request: Asset request with specifications

        Returns:
            AgentResult with final image and history
        """
        start_time = time.time()
        self.logger.set_request(request.request_id)
        self.logger.info(f"Starting generation: {request.description[:50]}...")

        result = AgentResult(
            original_request=request,
            history=[],
        )

        # Generate initial prompt
        prompt = self.prompt_generator.generate(request)
        self.logger.debug(f"Initial prompt: {prompt.full_prompt[:100]}...")

        best_iteration = 0
        best_score = 0.0

        for iteration in range(1, self.config.max_iterations + 1):
            self.logger.iteration_start(iteration, prompt.version)

            try:
                # Generate image
                record = await self._run_iteration(
                    prompt=prompt,
                    request=request,
                    iteration=iteration
                )

                result.history.append(record)

                # Check if passed
                if record.review and record.review.passed:
                    self.logger.iteration_end(record.score, passed=True)
                    result.success = True
                    result.best_iteration = iteration - 1
                    result.final_score = record.score
                    result.final_image_data = record.image_data
                    break

                # Track best so far
                if record.score > best_score:
                    best_score = record.score
                    best_iteration = iteration - 1

                self.logger.iteration_end(record.score, passed=False)

                # Improve prompt for next iteration
                if iteration < self.config.max_iterations and record.review:
                    prompt = self.prompt_improver.improve(
                        original_prompt=prompt,
                        quality_report=record.review,
                        request=request
                    )
                    self.logger.improvement_applied(
                        record.review.get_feedback_for_improvement()[:3]
                    )

            except Exception as e:
                self.logger.error(f"Iteration {iteration} failed: {str(e)}")
                record = IterationRecord(
                    iteration=iteration,
                    prompt=prompt,
                )
                result.history.append(record)

        # Finalize result
        result.iterations = len(result.history)
        result.total_time = time.time() - start_time

        if not result.success:
            # Use best iteration if didn't pass
            result.best_iteration = best_iteration
            result.final_score = best_score
            result.max_iterations_reached = True

            if result.history and best_iteration < len(result.history):
                result.final_image_data = result.history[best_iteration].image_data

        # Save if output path specified
        if result.final_image_data and request.output_path:
            result.final_image_path = self._save_image(
                result.final_image_data,
                request.output_path
            )

        self.logger.final_result(
            result.success,
            result.final_score,
            result.iterations,
            result.total_time
        )

        return result

    async def _run_iteration(
        self,
        prompt: DetailedPrompt,
        request: AssetRequest,
        iteration: int
    ) -> IterationRecord:
        """Run a single generation-review iteration"""
        record = IterationRecord(
            iteration=iteration,
            prompt=prompt,
        )

        # Generate image
        gen_start = time.time()
        self.logger.generation_start()

        try:
            generated = await self.generator_service.generate(
                prompt=prompt.full_prompt,
                width=request.size[0],
                height=request.size[1],
                style=request.style.value if hasattr(request.style, 'value') else str(request.style),
            )
            record.image_data = generated.image_data
            record.prompt_generation_time = time.time() - gen_start
            self.logger.generation_complete(record.prompt_generation_time)

        except Exception as e:
            self.logger.error(f"Generation failed: {str(e)}")
            raise

        # Review quality
        review_start = time.time()
        self.logger.review_start()

        try:
            image = Image.open(BytesIO(record.image_data))
            record.review = self.quality_reviewer.review(
                image=image,
                request=request,
                iteration=iteration
            )
            record.review_time = time.time() - review_start

            self.logger.review_complete({
                'transparency': record.review.transparency_score,
                'style': record.review.style_score,
                'color': record.review.color_score,
                'quality': record.review.quality_score,
            })

        except Exception as e:
            self.logger.error(f"Review failed: {str(e)}")
            # Create minimal review if review fails
            record.review = QualityReport(
                overall_score=0.5,
                passed=False,
                issues=[f"Review error: {str(e)}"]
            )

        return record

    def _save_image(self, image_data: bytes, output_path: Path) -> Path:
        """Save image data to file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        image = Image.open(BytesIO(image_data))
        image.save(output_path)

        self.logger.info(f"Saved to: {output_path}")
        return output_path

    def generate_sync(self, request: AssetRequest) -> AgentResult:
        """
        Synchronous wrapper for generate()

        For use in non-async contexts
        """
        return asyncio.run(self.generate(request))

    async def review_existing(
        self,
        image_path: Path,
        request: AssetRequest
    ) -> QualityReport:
        """
        Review an existing image against requirements

        Useful for checking if existing assets meet quality standards
        """
        image = Image.open(image_path)
        return self.quality_reviewer.review(image, request)


class MockGeneratorService:
    """
    Mock generator for testing when image_generator is not available
    """

    generator_type = "mock"

    async def generate(self, prompt: str, width: int, height: int, **kwargs):
        """Generate a mock placeholder image"""
        from dataclasses import dataclass

        @dataclass
        class MockResult:
            image_data: bytes

        # Create a simple colored rectangle as placeholder
        image = Image.new('RGBA', (width, height), (200, 200, 200, 255))

        # Add some variation based on prompt
        if 'red' in prompt.lower():
            image = Image.new('RGBA', (width, height), (255, 100, 100, 255))
        elif 'blue' in prompt.lower():
            image = Image.new('RGBA', (width, height), (100, 100, 255, 255))
        elif 'green' in prompt.lower():
            image = Image.new('RGBA', (width, height), (100, 255, 100, 255))

        # Save to bytes
        buffer = BytesIO()
        image.save(buffer, format='PNG')

        return MockResult(image_data=buffer.getvalue())


# Convenience function for quick generation
async def generate_asset(
    description: str,
    asset_type: str = 'sprite',
    style: str = 'kawaii',
    size: tuple = (64, 64),
    transparency: bool = True,
    output_path: Optional[str] = None,
    **kwargs
) -> AgentResult:
    """
    Convenience function for quick asset generation

    Args:
        description: What to generate
        asset_type: Type of asset (sprite, background, ui, etc.)
        style: Art style (kawaii, pixel_art, etc.)
        size: (width, height) tuple
        transparency: Whether to use transparent background
        output_path: Optional path to save result
        **kwargs: Additional request parameters

    Returns:
        AgentResult with generated image
    """
    from agents.image_agent.core.data_classes import AssetType, StyleType

    request = AssetRequest(
        description=description,
        asset_type=AssetType(asset_type),
        style=StyleType(style),
        size=size,
        transparency=transparency,
        output_path=Path(output_path) if output_path else None,
        **kwargs
    )

    agent = ImageAgent()
    return await agent.generate(request)
