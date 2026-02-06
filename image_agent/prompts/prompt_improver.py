"""
Prompt Improver - Enhances prompts based on quality review feedback

This module takes a prompt and quality feedback, then generates
an improved prompt that addresses the identified issues.
"""

from typing import Dict, List, Optional

from image_agent.core.data_classes import (
    AssetRequest,
    DetailedPrompt,
    QualityReport,
)


class PromptImprover:
    """
    Improves prompts based on quality review feedback

    Analyzes what went wrong and adjusts the prompt to fix issues
    while preserving what worked well.
    """

    # Improvement strategies for different issue types
    IMPROVEMENT_STRATEGIES: Dict[str, Dict[str, any]] = {
        'transparency': {
            'add_modifiers': [
                'completely transparent background',
                'PNG alpha channel',
                'isolated object only',
                'no background elements',
                'cutout style',
            ],
            'add_negative': [
                'background',
                'solid background',
                'any background',
                'scene',
                'environment',
            ],
            'emphasis': 'IMPORTANT: transparent background only, no background at all',
        },
        'style': {
            'add_modifiers': [
                'consistent style throughout',
                'unified art style',
                'cohesive design',
            ],
            'emphasis': 'strictly follow the specified art style',
        },
        'color': {
            'add_modifiers': [
                'vibrant colors',
                'proper color harmony',
                'balanced palette',
            ],
            'emphasis': 'use the exact specified color palette',
        },
        'quality': {
            'add_modifiers': [
                'high quality',
                'detailed',
                'professional',
                'crisp edges',
                'clean lines',
            ],
            'add_negative': [
                'blurry',
                'low quality',
                'pixelated unintentionally',
                'artifacts',
                'noise',
            ],
            'emphasis': 'highest quality output',
        },
        'size': {
            'add_modifiers': [
                'proper proportions',
                'well-composed',
                'centered',
            ],
            'emphasis': 'correct dimensions and composition',
        },
        'game_fit': {
            'add_modifiers': [
                'game-ready asset',
                'suitable for games',
                'professional game art',
            ],
            'emphasis': 'optimized for game use',
        },
    }

    def __init__(self):
        """Initialize the prompt improver"""
        pass

    def improve(
        self,
        original_prompt: DetailedPrompt,
        quality_report: QualityReport,
        request: AssetRequest
    ) -> DetailedPrompt:
        """
        Improve a prompt based on quality review feedback

        Args:
            original_prompt: The prompt that was used
            quality_report: The quality review results
            request: Original asset request for context

        Returns:
            Improved DetailedPrompt addressing the issues
        """
        # Get improvement feedback
        feedback = quality_report.get_feedback_for_improvement()

        # Identify areas that need improvement
        areas_to_improve = self._identify_improvement_areas(quality_report)

        # Create improved prompt
        improved = DetailedPrompt(
            main_prompt=self._improve_main_prompt(
                original_prompt.main_prompt,
                areas_to_improve,
                request
            ),
            style_modifiers=self._improve_modifiers(
                original_prompt.style_modifiers,
                areas_to_improve
            ),
            technical_specs=original_prompt.technical_specs,
            negative_prompt=self._improve_negative(
                original_prompt.negative_prompt,
                areas_to_improve
            ),
            version=original_prompt.version + 1,
            source_request_id=original_prompt.source_request_id,
            previous_feedback=feedback,
            improvement_notes=self._generate_improvement_notes(areas_to_improve),
        )

        return improved

    def _identify_improvement_areas(
        self,
        quality_report: QualityReport
    ) -> List[str]:
        """Identify which areas need improvement based on scores"""
        areas = []

        score_map = {
            'transparency': quality_report.transparency_score,
            'style': quality_report.style_score,
            'color': quality_report.color_score,
            'quality': quality_report.quality_score,
            'size': quality_report.size_score,
            'game_fit': quality_report.game_fit_score,
        }

        # Sort by score (lowest first) and get areas below threshold
        for area, score in sorted(score_map.items(), key=lambda x: x[1]):
            if score < 0.9:
                areas.append(area)

        return areas

    def _improve_main_prompt(
        self,
        original: str,
        areas: List[str],
        request: AssetRequest
    ) -> str:
        """Improve the main prompt with emphasis on problem areas"""
        parts = [original]

        # Add emphasis for each problem area
        for area in areas[:3]:  # Focus on top 3 issues
            strategy = self.IMPROVEMENT_STRATEGIES.get(area, {})
            emphasis = strategy.get('emphasis', '')
            if emphasis:
                parts.append(emphasis)

        # Re-emphasize the description
        parts.append(f"specifically: {request.description}")

        return ', '.join(parts)

    def _improve_modifiers(
        self,
        original: List[str],
        areas: List[str]
    ) -> List[str]:
        """Add modifiers to address problem areas"""
        modifiers = original.copy()

        for area in areas:
            strategy = self.IMPROVEMENT_STRATEGIES.get(area, {})
            new_modifiers = strategy.get('add_modifiers', [])
            for mod in new_modifiers:
                if mod not in modifiers:
                    modifiers.append(mod)

        return modifiers

    def _improve_negative(
        self,
        original: str,
        areas: List[str]
    ) -> str:
        """Strengthen negative prompt for problem areas"""
        negatives = original.split(', ') if original else []

        for area in areas:
            strategy = self.IMPROVEMENT_STRATEGIES.get(area, {})
            new_negatives = strategy.get('add_negative', [])
            for neg in new_negatives:
                if neg not in negatives:
                    negatives.append(neg)

        return ', '.join(negatives)

    def _generate_improvement_notes(self, areas: List[str]) -> str:
        """Generate human-readable notes about improvements made"""
        if not areas:
            return "Minor refinements applied"

        notes = [f"Focused improvements on: {', '.join(areas)}"]

        for area in areas[:3]:
            strategy = self.IMPROVEMENT_STRATEGIES.get(area, {})
            if 'emphasis' in strategy:
                notes.append(f"- {area}: {strategy['emphasis']}")

        return '\n'.join(notes)

    def apply_specific_feedback(
        self,
        prompt: DetailedPrompt,
        feedback_items: List[str]
    ) -> DetailedPrompt:
        """
        Apply specific feedback items to a prompt

        Used when the QualityReviewer provides specific
        actionable feedback that should be incorporated.
        """
        improved = DetailedPrompt(
            main_prompt=prompt.main_prompt,
            style_modifiers=prompt.style_modifiers.copy(),
            technical_specs=prompt.technical_specs,
            negative_prompt=prompt.negative_prompt,
            version=prompt.version + 1,
            source_request_id=prompt.source_request_id,
            previous_feedback=feedback_items,
        )

        # Parse feedback and apply
        for feedback in feedback_items:
            feedback_lower = feedback.lower()

            # Handle transparency feedback
            if 'transparent' in feedback_lower or 'background' in feedback_lower:
                if 'transparent background' not in improved.style_modifiers:
                    improved.style_modifiers.insert(0, 'completely transparent background')
                if 'isolated object' not in improved.style_modifiers:
                    improved.style_modifiers.append('isolated object only')

            # Handle quality feedback
            if 'quality' in feedback_lower or 'blurry' in feedback_lower:
                if 'high quality' not in improved.style_modifiers:
                    improved.style_modifiers.append('high quality')
                    improved.style_modifiers.append('sharp details')

            # Handle style feedback
            if 'style' in feedback_lower or 'consistent' in feedback_lower:
                improved.style_modifiers.append('strictly consistent style')

            # Handle color feedback
            if 'color' in feedback_lower:
                improved.style_modifiers.append('proper color balance')

        return improved
