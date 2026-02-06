"""
Color Checker - Analyzes color palette and harmony

This module evaluates the color quality of generated images:
- Palette compliance (if specified)
- Color harmony
- Contrast and readability
- Color count for style compliance
"""

from collections import Counter
from io import BytesIO
from typing import Dict, List, Optional, Tuple

from PIL import Image


class ColorReport:
    """Report on color analysis"""

    def __init__(self):
        self.score: float = 0.0
        self.unique_colors: int = 0
        self.dominant_colors: List[Tuple[int, int, int]] = []
        self.palette_compliance: float = 0.0
        self.color_harmony: float = 0.0
        self.contrast_score: float = 0.0
        self.issues: List[str] = []
        self.recommendation: str = ""


class ColorChecker:
    """
    Checks color quality and palette compliance

    Analyzes:
    - Color count and distribution
    - Palette matching (if specified)
    - Color harmony
    - Contrast for readability
    """

    def __init__(self):
        """Initialize the color checker"""
        pass

    def check(
        self,
        image: Image.Image,
        expected_palette: Optional[List[str]] = None,
        max_colors: Optional[int] = None
    ) -> ColorReport:
        """
        Analyze color quality of an image

        Args:
            image: PIL Image to analyze
            expected_palette: Optional list of hex colors to match
            max_colors: Maximum allowed unique colors

        Returns:
            ColorReport with analysis results
        """
        report = ColorReport()

        # Convert to RGB
        if image.mode != 'RGB':
            if image.mode == 'RGBA':
                # Only analyze non-transparent pixels
                pixels = [p[:3] for p in image.getdata() if p[3] > 128]
            else:
                rgb_image = image.convert('RGB')
                pixels = list(rgb_image.getdata())
        else:
            pixels = list(image.getdata())

        if not pixels:
            report.issues.append("No visible pixels to analyze")
            report.score = 0.0
            return report

        # Count colors
        color_counts = Counter(pixels)
        report.unique_colors = len(color_counts)

        # Get dominant colors
        report.dominant_colors = [color for color, _ in color_counts.most_common(5)]

        # Check palette compliance
        if expected_palette:
            report.palette_compliance = self._check_palette_compliance(
                pixels, expected_palette, report
            )
        else:
            report.palette_compliance = 1.0

        # Check color count
        color_count_score = 1.0
        if max_colors:
            if report.unique_colors > max_colors:
                overage = (report.unique_colors - max_colors) / max_colors
                color_count_score = max(0, 1 - overage * 0.5)
                report.issues.append(f"Too many colors: {report.unique_colors} (max: {max_colors})")

        # Check color harmony
        report.color_harmony = self._check_harmony(report.dominant_colors, report)

        # Check contrast
        report.contrast_score = self._check_contrast(report.dominant_colors, report)

        # Calculate overall score
        report.score = (
            report.palette_compliance * 0.3 +
            color_count_score * 0.2 +
            report.color_harmony * 0.25 +
            report.contrast_score * 0.25
        )

        # Generate recommendation
        report.recommendation = self._generate_recommendation(report)

        return report

    def _check_palette_compliance(
        self,
        pixels: List[Tuple[int, int, int]],
        expected_palette: List[str],
        report: ColorReport
    ) -> float:
        """Check how well colors match expected palette"""
        # Convert hex colors to RGB
        expected_rgb = []
        for hex_color in expected_palette:
            hex_color = hex_color.lstrip('#')
            try:
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                expected_rgb.append(rgb)
            except ValueError:
                continue

        if not expected_rgb:
            return 1.0

        # Check each pixel's distance to nearest palette color
        total_distance = 0
        for pixel in pixels:
            min_distance = min(
                self._color_distance(pixel, expected)
                for expected in expected_rgb
            )
            total_distance += min_distance

        # Normalize distance (max possible is ~441 for opposite corners of RGB cube)
        avg_distance = total_distance / len(pixels)
        compliance = max(0, 1 - avg_distance / 100)  # Tolerance of ~100

        if compliance < 0.7:
            report.issues.append("Colors don't match expected palette well")

        return compliance

    def _color_distance(
        self,
        c1: Tuple[int, int, int],
        c2: Tuple[int, int, int]
    ) -> float:
        """Calculate Euclidean distance between two colors"""
        return ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2) ** 0.5

    def _check_harmony(
        self,
        dominant_colors: List[Tuple[int, int, int]],
        report: ColorReport
    ) -> float:
        """Check color harmony using basic color theory"""
        if len(dominant_colors) < 2:
            return 1.0

        # Convert to HSL for harmony analysis
        hsl_colors = [self._rgb_to_hsl(c) for c in dominant_colors]

        # Check for complementary, analogous, or triadic harmony
        hues = [h for h, s, l in hsl_colors if s > 0.1]  # Only consider saturated colors

        if not hues:
            return 0.8  # Monochromatic or grayscale

        # Calculate hue variance
        hue_range = max(hues) - min(hues)

        # Good harmony: either tight (analogous) or spread (complementary/triadic)
        if hue_range < 30:  # Analogous
            return 1.0
        elif 150 < hue_range < 210:  # Complementary
            return 0.9
        elif 90 < hue_range < 150:  # Split-complementary or triadic
            return 0.85
        elif hue_range > 270:  # Wide spread, potentially chaotic
            report.issues.append("Colors may lack harmony")
            return 0.6

        return 0.75

    def _rgb_to_hsl(self, rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Convert RGB to HSL"""
        r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255

        max_c = max(r, g, b)
        min_c = min(r, g, b)
        l = (max_c + min_c) / 2

        if max_c == min_c:
            h = s = 0
        else:
            d = max_c - min_c
            s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)

            if max_c == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4

            h *= 60

        return (h, s, l)

    def _check_contrast(
        self,
        dominant_colors: List[Tuple[int, int, int]],
        report: ColorReport
    ) -> float:
        """Check contrast between dominant colors"""
        if len(dominant_colors) < 2:
            return 1.0

        # Calculate luminance for each color
        luminances = [self._get_luminance(c) for c in dominant_colors]

        # Check contrast ratios between colors
        max_contrast = 0
        for i, l1 in enumerate(luminances):
            for l2 in luminances[i+1:]:
                lighter = max(l1, l2)
                darker = min(l1, l2)
                contrast = (lighter + 0.05) / (darker + 0.05)
                max_contrast = max(max_contrast, contrast)

        # Good contrast is > 4.5:1 for readability
        if max_contrast >= 4.5:
            return 1.0
        elif max_contrast >= 3:
            return 0.8
        else:
            report.issues.append("Low contrast between colors")
            return 0.6

    def _get_luminance(self, rgb: Tuple[int, int, int]) -> float:
        """Calculate relative luminance"""
        def adjust(c):
            c = c / 255
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        r, g, b = adjust(rgb[0]), adjust(rgb[1]), adjust(rgb[2])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _generate_recommendation(self, report: ColorReport) -> str:
        """Generate actionable recommendation"""
        if report.score >= 0.9:
            return "Color quality is excellent"

        if report.issues:
            return f"Address: {report.issues[0]}"

        if report.color_harmony < 0.7:
            return "Improve color harmony - use complementary or analogous colors"

        if report.contrast_score < 0.7:
            return "Increase contrast between colors for better readability"

        return "Minor color adjustments recommended"

    def check_from_bytes(
        self,
        image_data: bytes,
        expected_palette: Optional[List[str]] = None,
        max_colors: Optional[int] = None
    ) -> ColorReport:
        """Check colors from image bytes"""
        image = Image.open(BytesIO(image_data))
        return self.check(image, expected_palette, max_colors)

    def get_palette_hex(
        self,
        image: Image.Image,
        num_colors: int = 5
    ) -> List[str]:
        """Extract dominant colors as hex strings"""
        if image.mode != 'RGB':
            if image.mode == 'RGBA':
                pixels = [p[:3] for p in image.getdata() if p[3] > 128]
            else:
                pixels = list(image.convert('RGB').getdata())
        else:
            pixels = list(image.getdata())

        color_counts = Counter(pixels)
        dominant = [color for color, _ in color_counts.most_common(num_colors)]

        return ['#{:02x}{:02x}{:02x}'.format(*c) for c in dominant]
