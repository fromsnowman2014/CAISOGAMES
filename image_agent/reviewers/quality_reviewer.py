"""
Quality Reviewer - Main quality assessment coordinator

This module coordinates all quality checks and produces
a comprehensive quality report for generated images.
"""

from io import BytesIO
from typing import Dict, List, Optional

from PIL import Image

from image_agent.core.data_classes import (
    AssetRequest,
    QualityReport,
    TransparencyReport,
)
from image_agent.reviewers.transparency_checker import TransparencyChecker
from image_agent.reviewers.style_checker import StyleChecker, StyleReport
from image_agent.reviewers.color_checker import ColorChecker, ColorReport


class QualityReviewer:
    """
    Main quality reviewer that coordinates all quality checks

    Acts as a professional game designer/developer evaluating:
    - Transparency quality
    - Style compliance
    - Color quality
    - Size accuracy
    - Overall game fitness
    """

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None
    ):
        """
        Initialize the quality reviewer

        Args:
            weights: Custom weights for scoring (optional)
        """
        self.transparency_checker = TransparencyChecker()
        self.style_checker = StyleChecker()
        self.color_checker = ColorChecker()

        self.weights = weights or {
            'transparency': 0.20,
            'size': 0.10,
            'style': 0.25,
            'color': 0.15,
            'quality': 0.20,
            'game_fit': 0.10,
        }

    def review(
        self,
        image: Image.Image,
        request: AssetRequest,
        iteration: int = 1
    ) -> QualityReport:
        """
        Perform comprehensive quality review

        Args:
            image: PIL Image to review
            request: Original asset request with specifications
            iteration: Current iteration number

        Returns:
            QualityReport with all scores and feedback
        """
        report = QualityReport(
            iteration=iteration,
            weights=self.weights,
        )

        # 1. Transparency check
        if request.transparency:
            trans_report = self.transparency_checker.check(image, expected_transparent=True)
            report.transparency_report = trans_report
            report.transparency_score = trans_report.score

            if not trans_report.background_transparent:
                report.issues.append("Background is not fully transparent")
            if trans_report.artifacts:
                report.warnings.extend(trans_report.artifacts)
            if trans_report.edge_issues:
                report.warnings.extend(trans_report.edge_issues)
        else:
            report.transparency_score = 1.0  # Not required

        # 2. Size check
        report.size_score = self._check_size(image, request, report)

        # 3. Style check
        style_report = self.style_checker.check(image, request.style)
        report.style_score = style_report.score

        if style_report.style_violations:
            report.issues.extend(style_report.style_violations)
        if style_report.missing_features:
            report.suggestions.extend([f"Add: {f}" for f in style_report.missing_features])
        if style_report.matching_features:
            report.strengths.extend(style_report.matching_features)

        # 4. Color check
        color_report = self.color_checker.check(
            image,
            expected_palette=request.color_palette,
            max_colors=self._get_max_colors_for_style(request.style)
        )
        report.color_score = color_report.score

        if color_report.issues:
            report.warnings.extend(color_report.issues)

        # 5. Quality check (general image quality)
        report.quality_score = self._check_quality(image, request, report)

        # 6. Game fit check
        report.game_fit_score = self._check_game_fit(image, request, report)

        # Calculate overall score
        report.calculate_overall_score()

        # Add reviewer notes
        report.reviewer_notes = self._generate_reviewer_notes(report, request)

        return report

    def _check_size(
        self,
        image: Image.Image,
        request: AssetRequest,
        report: QualityReport
    ) -> float:
        """Check if image size matches request"""
        expected_w, expected_h = request.size
        actual_w, actual_h = image.size

        # Calculate size deviation
        w_ratio = actual_w / expected_w if expected_w else 1
        h_ratio = actual_h / expected_h if expected_h else 1

        # Allow 5% tolerance
        w_ok = 0.95 <= w_ratio <= 1.05
        h_ok = 0.95 <= h_ratio <= 1.05

        if w_ok and h_ok:
            return 1.0

        # Calculate score based on deviation
        w_score = 1 - abs(1 - w_ratio) if w_ratio else 0
        h_score = 1 - abs(1 - h_ratio) if h_ratio else 0
        score = (w_score + h_score) / 2

        if score < 0.9:
            report.issues.append(
                f"Size mismatch: expected {expected_w}x{expected_h}, "
                f"got {actual_w}x{actual_h}"
            )

        return max(0, score)

    def _check_quality(
        self,
        image: Image.Image,
        request: AssetRequest,
        report: QualityReport
    ) -> float:
        """Check general image quality"""
        score = 1.0
        issues = []

        # Check for very small images (likely placeholder)
        if image.width < 16 or image.height < 16:
            issues.append("Image too small - may be placeholder")
            score -= 0.5

        # Check for blank/empty images
        if image.mode in ('RGBA', 'LA'):
            pixels = list(image.getdata())
            non_transparent = sum(1 for p in pixels if p[-1] > 10)
            if non_transparent < len(pixels) * 0.05:
                issues.append("Image appears mostly empty/transparent")
                score -= 0.4

        # Check for solid color images (likely failed generation)
        rgb_image = image.convert('RGB')
        colors = set(rgb_image.getdata())
        if len(colors) < 5:
            issues.append("Image has very few colors - may be failed generation")
            score -= 0.3

        report.issues.extend(issues)
        return max(0, score)

    def _check_game_fit(
        self,
        image: Image.Image,
        request: AssetRequest,
        report: QualityReport
    ) -> float:
        """Check if image is suitable for game use"""
        score = 1.0

        # Check content based on asset type
        asset_type = request.asset_type.value

        if asset_type == 'sprite':
            # Sprites should have clear subject
            if request.transparency:
                # Check that there's a clear object (not too spread out)
                if image.mode == 'RGBA':
                    alpha = [p[3] for p in image.getdata()]
                    opaque_count = sum(1 for a in alpha if a > 200)
                    opaque_ratio = opaque_count / len(alpha)

                    if opaque_ratio > 0.8:
                        report.warnings.append("Sprite may not have transparent background")
                        score -= 0.2
                    elif opaque_ratio < 0.05:
                        report.issues.append("Sprite has very little content")
                        score -= 0.4

        elif asset_type == 'background':
            # Backgrounds should fill the frame
            if image.mode == 'RGBA':
                alpha = [p[3] for p in image.getdata()]
                opaque_ratio = sum(1 for a in alpha if a > 200) / len(alpha)
                if opaque_ratio < 0.9:
                    report.warnings.append("Background has unexpected transparency")
                    score -= 0.1

        elif asset_type == 'icon':
            # Icons should be simple and recognizable
            rgb_image = image.convert('RGB')
            colors = set(rgb_image.getdata())
            if len(colors) > 256:
                report.warnings.append("Icon may be too detailed")
                score -= 0.1

        # Game context check
        if request.game_context:
            report.strengths.append(f"Designed for {request.game_context}")

        return max(0, score)

    def _get_max_colors_for_style(self, style) -> Optional[int]:
        """Get recommended max colors for style"""
        from image_agent.core.data_classes import StyleType

        color_limits = {
            StyleType.PIXEL_ART: 32,
            StyleType.RETRO_8BIT: 8,
            StyleType.RETRO_16BIT: 32,
            StyleType.FLAT: 16,
        }
        return color_limits.get(style)

    def _generate_reviewer_notes(
        self,
        report: QualityReport,
        request: AssetRequest
    ) -> str:
        """Generate professional reviewer notes"""
        notes = []

        # Overall assessment
        if report.passed:
            notes.append("Image meets quality requirements.")
        else:
            notes.append(f"Image needs improvement (score: {report.overall_score*100:.0f}%).")

        # Top issues
        if report.issues:
            notes.append(f"Primary issues: {report.issues[0]}")

        # Strengths
        if report.strengths:
            notes.append(f"Strengths: {', '.join(report.strengths[:2])}")

        # Next steps
        if not report.passed:
            lowest = min([
                ('transparency', report.transparency_score),
                ('style', report.style_score),
                ('color', report.color_score),
                ('quality', report.quality_score),
            ], key=lambda x: x[1])
            notes.append(f"Focus improvement on: {lowest[0]}")

        return " ".join(notes)

    def review_from_bytes(
        self,
        image_data: bytes,
        request: AssetRequest,
        iteration: int = 1
    ) -> QualityReport:
        """
        Review image from bytes data

        Convenience method for reviewing without loading image first
        """
        image = Image.open(BytesIO(image_data))
        return self.review(image, request, iteration)

    def quick_check(
        self,
        image: Image.Image,
        check_transparency: bool = True
    ) -> Dict[str, float]:
        """
        Quick quality check without full analysis

        Returns dict of basic scores for fast assessment
        """
        scores = {}

        # Quick transparency check
        if check_transparency and image.mode in ('RGBA', 'LA'):
            trans_report = self.transparency_checker.check(image)
            scores['transparency'] = trans_report.score

        # Quick color count
        rgb = image.convert('RGB')
        colors = len(set(rgb.getdata()))
        scores['color_complexity'] = min(1, colors / 256)

        # Quick size check
        w, h = image.size
        scores['size'] = 1.0 if 16 <= w <= 2048 and 16 <= h <= 2048 else 0.5

        return scores
