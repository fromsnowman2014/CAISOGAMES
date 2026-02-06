"""
Style Checker - Analyzes if image matches requested art style

This module evaluates whether a generated image matches the
requested art style (pixel art, kawaii, etc.)
"""

from io import BytesIO
from typing import Dict, List, Optional, Tuple

from PIL import Image

from agents.image_agent.core.data_classes import StyleType


class StyleReport:
    """Report on style analysis"""

    def __init__(self):
        self.score: float = 0.0
        self.detected_style: Optional[StyleType] = None
        self.style_confidence: float = 0.0
        self.matching_features: List[str] = []
        self.missing_features: List[str] = []
        self.style_violations: List[str] = []
        self.recommendation: str = ""


class StyleChecker:
    """
    Checks if generated images match requested art style

    Analyzes visual characteristics to determine style match:
    - Color palette complexity
    - Edge sharpness (pixel art vs smooth)
    - Proportions (chibi vs realistic)
    - Detail level
    """

    # Style characteristics for detection
    STYLE_CHARACTERISTICS: Dict[StyleType, Dict] = {
        StyleType.PIXEL_ART: {
            'max_colors': 32,
            'sharp_edges': True,
            'low_gradient': True,
            'features': ['limited palette', 'sharp pixels', 'no anti-aliasing'],
        },
        StyleType.KAWAII: {
            'min_brightness': 0.5,
            'soft_colors': True,
            'rounded_shapes': True,
            'features': ['soft colors', 'rounded shapes', 'cute proportions'],
        },
        StyleType.CHIBI: {
            'head_ratio': 0.4,  # Head should be ~40% of height
            'features': ['big head', 'small body', 'simplified features'],
        },
        StyleType.CARTOON: {
            'has_outlines': True,
            'vibrant_colors': True,
            'features': ['bold outlines', 'vibrant colors', 'exaggerated features'],
        },
        StyleType.FLAT: {
            'max_colors': 16,
            'no_gradients': True,
            'features': ['solid colors', 'no shadows', 'geometric shapes'],
        },
        StyleType.RETRO_8BIT: {
            'max_colors': 8,
            'chunky_pixels': True,
            'features': ['very limited palette', 'chunky pixels', 'simple shapes'],
        },
        StyleType.RETRO_16BIT: {
            'max_colors': 32,
            'features': ['medium palette', 'detailed pixels', 'classic gaming'],
        },
    }

    def __init__(self):
        """Initialize the style checker"""
        pass

    def check(
        self,
        image: Image.Image,
        expected_style: StyleType
    ) -> StyleReport:
        """
        Check if image matches expected style

        Args:
            image: PIL Image to analyze
            expected_style: The style that was requested

        Returns:
            StyleReport with analysis results
        """
        report = StyleReport()

        # Get characteristics for expected style
        characteristics = self.STYLE_CHARACTERISTICS.get(expected_style, {})

        # Analyze image
        analysis = self._analyze_image(image)

        # Check each characteristic
        score_components = []

        # Color analysis
        color_score = self._check_colors(analysis, expected_style, characteristics, report)
        score_components.append(color_score)

        # Edge analysis (for pixel art)
        if expected_style in [StyleType.PIXEL_ART, StyleType.RETRO_8BIT, StyleType.RETRO_16BIT]:
            edge_score = self._check_pixel_edges(analysis, report)
            score_components.append(edge_score)

        # Brightness/softness (for kawaii)
        if expected_style in [StyleType.KAWAII, StyleType.CHIBI]:
            soft_score = self._check_softness(analysis, characteristics, report)
            score_components.append(soft_score)

        # Outline detection (for cartoon)
        if expected_style == StyleType.CARTOON:
            outline_score = self._check_outlines(image, report)
            score_components.append(outline_score)

        # Calculate overall score
        report.score = sum(score_components) / len(score_components) if score_components else 0.5
        report.detected_style = self._detect_style(analysis)

        # Generate recommendation
        report.recommendation = self._generate_recommendation(report, expected_style)

        return report

    def _analyze_image(self, image: Image.Image) -> Dict:
        """Extract analysis data from image"""
        # Convert to RGB for analysis
        if image.mode != 'RGB':
            rgb_image = image.convert('RGB')
        else:
            rgb_image = image

        pixels = list(rgb_image.getdata())

        # Count unique colors
        unique_colors = len(set(pixels))

        # Calculate average brightness
        avg_brightness = sum(sum(p) / 3 for p in pixels) / len(pixels) / 255

        # Calculate color variance
        avg_r = sum(p[0] for p in pixels) / len(pixels)
        avg_g = sum(p[1] for p in pixels) / len(pixels)
        avg_b = sum(p[2] for p in pixels) / len(pixels)

        color_variance = sum(
            ((p[0] - avg_r)**2 + (p[1] - avg_g)**2 + (p[2] - avg_b)**2)
            for p in pixels
        ) / len(pixels)

        # Check for gradients (smooth color transitions)
        has_gradients = self._detect_gradients(rgb_image)

        # Check for sharp edges
        has_sharp_edges = self._detect_sharp_edges(rgb_image)

        return {
            'unique_colors': unique_colors,
            'brightness': avg_brightness,
            'color_variance': color_variance,
            'has_gradients': has_gradients,
            'has_sharp_edges': has_sharp_edges,
            'width': image.width,
            'height': image.height,
        }

    def _check_colors(
        self,
        analysis: Dict,
        style: StyleType,
        characteristics: Dict,
        report: StyleReport
    ) -> float:
        """Check color palette compliance"""
        score = 1.0

        max_colors = characteristics.get('max_colors')
        if max_colors:
            if analysis['unique_colors'] <= max_colors:
                report.matching_features.append(f"Color count OK ({analysis['unique_colors']} colors)")
            elif analysis['unique_colors'] <= max_colors * 2:
                report.missing_features.append(f"Slightly too many colors ({analysis['unique_colors']} vs {max_colors})")
                score -= 0.2
            else:
                report.style_violations.append(f"Too many colors ({analysis['unique_colors']} vs {max_colors})")
                score -= 0.4

        return max(0, score)

    def _check_pixel_edges(self, analysis: Dict, report: StyleReport) -> float:
        """Check for pixel art sharp edges"""
        score = 1.0

        if analysis['has_sharp_edges']:
            report.matching_features.append("Sharp pixel edges detected")
        else:
            report.missing_features.append("Missing sharp pixel edges")
            score -= 0.3

        if not analysis['has_gradients']:
            report.matching_features.append("No smooth gradients (good for pixel art)")
        else:
            report.style_violations.append("Unwanted gradients detected")
            score -= 0.2

        return max(0, score)

    def _check_softness(
        self,
        analysis: Dict,
        characteristics: Dict,
        report: StyleReport
    ) -> float:
        """Check for kawaii/soft style characteristics"""
        score = 1.0

        min_brightness = characteristics.get('min_brightness', 0.5)

        if analysis['brightness'] >= min_brightness:
            report.matching_features.append("Bright, cheerful colors")
        else:
            report.missing_features.append("Colors could be brighter/softer")
            score -= 0.2

        return max(0, score)

    def _check_outlines(self, image: Image.Image, report: StyleReport) -> float:
        """Check for cartoon-style outlines"""
        # Simple edge detection to find outlines
        gray = image.convert('L')
        pixels = list(gray.getdata())
        width = image.width

        # Count dark pixels that could be outlines
        dark_pixel_count = sum(1 for p in pixels if p < 50)
        dark_ratio = dark_pixel_count / len(pixels)

        if 0.05 < dark_ratio < 0.3:
            report.matching_features.append("Bold outlines detected")
            return 1.0
        elif dark_ratio < 0.05:
            report.missing_features.append("May need stronger outlines")
            return 0.7
        else:
            report.style_violations.append("Too much dark area (not typical cartoon style)")
            return 0.5

    def _detect_gradients(self, image: Image.Image) -> bool:
        """Detect if image has smooth gradients"""
        # Sample a few rows and check for smooth transitions
        width, height = image.size
        pixels = list(image.getdata())

        gradient_count = 0
        samples = min(10, height)

        for row in range(0, height, height // samples):
            for x in range(1, width - 1):
                idx = row * width + x
                if idx + 1 >= len(pixels):
                    continue

                # Check horizontal color transition
                p1, p2, p3 = pixels[idx-1], pixels[idx], pixels[idx+1]
                diff1 = sum(abs(a - b) for a, b in zip(p1, p2))
                diff2 = sum(abs(a - b) for a, b in zip(p2, p3))

                # Smooth gradient = small, consistent differences
                if 5 < diff1 < 30 and 5 < diff2 < 30:
                    gradient_count += 1

        return gradient_count > (samples * width * 0.1)

    def _detect_sharp_edges(self, image: Image.Image) -> bool:
        """Detect if image has sharp pixel edges"""
        width, height = image.size
        pixels = list(image.getdata())

        sharp_count = 0
        total_checks = 0

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                idx = y * width + x
                if idx >= len(pixels):
                    continue

                # Check for sudden color changes (sharp edges)
                current = pixels[idx]
                right = pixels[idx + 1]
                down = pixels[idx + width]

                diff_right = sum(abs(a - b) for a, b in zip(current, right))
                diff_down = sum(abs(a - b) for a, b in zip(current, down))

                total_checks += 1

                # Sharp edge = big color difference with no in-between
                if diff_right > 100 or diff_down > 100:
                    sharp_count += 1

        if total_checks == 0:
            return False

        return (sharp_count / total_checks) > 0.05

    def _detect_style(self, analysis: Dict) -> Optional[StyleType]:
        """Attempt to detect the actual style of the image"""
        colors = analysis['unique_colors']
        sharp = analysis['has_sharp_edges']
        gradients = analysis['has_gradients']
        brightness = analysis['brightness']

        # Simple heuristic-based detection
        if colors <= 8 and sharp and not gradients:
            return StyleType.RETRO_8BIT
        elif colors <= 32 and sharp and not gradients:
            return StyleType.PIXEL_ART
        elif colors <= 16 and not gradients:
            return StyleType.FLAT
        elif brightness > 0.6 and gradients:
            return StyleType.KAWAII
        elif not gradients and brightness < 0.5:
            return StyleType.CARTOON

        return None

    def _generate_recommendation(
        self,
        report: StyleReport,
        expected_style: StyleType
    ) -> str:
        """Generate actionable recommendation"""
        if report.score >= 0.9:
            return f"Image matches {expected_style.value} style well"

        if report.style_violations:
            return f"Fix style violations: {', '.join(report.style_violations[:2])}"

        if report.missing_features:
            return f"Add missing features: {', '.join(report.missing_features[:2])}"

        return f"Strengthen {expected_style.value} style characteristics"

    def check_from_bytes(
        self,
        image_data: bytes,
        expected_style: StyleType
    ) -> StyleReport:
        """Check style from image bytes"""
        image = Image.open(BytesIO(image_data))
        return self.check(image, expected_style)
