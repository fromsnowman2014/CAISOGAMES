"""
Transparency Checker - Analyzes PNG transparency quality

This module checks if generated images meet transparency requirements:
- Alpha channel presence
- Background transparency
- Edge quality (no halos or artifacts)
- Clean cutouts
"""

from io import BytesIO
from typing import List, Optional, Tuple

from PIL import Image

from agents.image_agent.core.data_classes import TransparencyReport


class TransparencyChecker:
    """
    Checks and analyzes image transparency quality

    Used to verify that sprites and other game assets have
    proper transparent backgrounds as requested.
    """

    # Thresholds
    EDGE_SAMPLE_COUNT = 100  # Number of edge pixels to sample
    TRANSPARENCY_THRESHOLD = 10  # Alpha value below this = transparent
    BACKGROUND_SAMPLE_MARGIN = 5  # Pixels from edge to sample

    def __init__(self):
        """Initialize the transparency checker"""
        pass

    def check(
        self,
        image: Image.Image,
        expected_transparent: bool = True
    ) -> TransparencyReport:
        """
        Perform comprehensive transparency analysis

        Args:
            image: PIL Image to check
            expected_transparent: Whether transparency was requested

        Returns:
            TransparencyReport with detailed analysis
        """
        report = TransparencyReport()

        # Check alpha channel presence
        report.has_alpha_channel = image.mode in ('RGBA', 'LA', 'PA')

        if not report.has_alpha_channel:
            if expected_transparent:
                # Check if it has a white background (which is acceptable for Phase 6 pipeline)
                if image.mode == 'RGB':
                    is_white_bg = self._check_background(
                        image, list(image.getdata()), image.width, image.height, check_white_bg=True
                    )
                    if is_white_bg:
                        report.background_transparent = True
                        report.recommendation = "Background is white (convert to transparent)"
                        # Give it a passing score but not perfect
                        report.transparent_percentage = 0.0
                        report.opaque_percentage = 100.0
                        report.transparency_cleanliness = 0.9
                        return report

                report.artifacts.append("No alpha channel present")
                report.recommendation = "Convert to RGBA format"
                return report

        # Convert to RGBA if needed
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # Analyze transparency
        pixels = list(image.getdata())
        width, height = image.size

        # Calculate transparency percentages
        total = len(pixels)
        transparent_count = sum(1 for p in pixels if p[3] < self.TRANSPARENCY_THRESHOLD)
        opaque_count = sum(1 for p in pixels if p[3] > 250)
        semi_count = total - transparent_count - opaque_count

        report.transparent_percentage = transparent_count / total * 100
        report.opaque_percentage = opaque_count / total * 100
        report.semi_transparent_percentage = semi_count / total * 100

        # Check background transparency (sample corners and edges)
        report.background_transparent = self._check_background(image, pixels, width, height, check_white_bg=True)

        # Check edge quality
        edge_quality, edge_issues = self._check_edge_quality(image, pixels, width, height)
        report.edge_quality = edge_quality
        report.edge_issues = edge_issues

        # Calculate overall cleanliness
        report.transparency_cleanliness = self._calculate_cleanliness(
            report.background_transparent,
            edge_quality,
            len(report.artifacts),
            len(edge_issues)
        )

        # Generate recommendation
        report.recommendation = self._generate_recommendation(report, expected_transparent)

        return report

    def _check_background(
        self,
        image: Image.Image,
        pixels: List[Tuple],
        width: int,
        height: int,
        check_white_bg: bool = False
    ) -> bool:
        """Check if background (corners and edges) is transparent or solid white"""
        margin = self.BACKGROUND_SAMPLE_MARGIN

        # Sample corner regions
        corners = [
            (0, 0, margin, margin),  # Top-left
            (width - margin, 0, width, margin),  # Top-right
            (0, height - margin, margin, height),  # Bottom-left
            (width - margin, height - margin, width, height),  # Bottom-right
        ]

        transparent_corners = 0
        white_corners = 0

        for x1, y1, x2, y2 in corners:
            corner_transparent = True
            corner_white = True
            
            for y in range(y1, min(y2, height)):
                for x in range(x1, min(x2, width)):
                    idx = y * width + x
                    if idx >= len(pixels):
                        continue
                        
                    pixel = pixels[idx]
                    
                    # Check transparency
                    if len(pixel) > 3 and pixel[3] > self.TRANSPARENCY_THRESHOLD:
                        corner_transparent = False
                    
                    # Check white (RGB > 240)
                    if pixel[0] < 240 or pixel[1] < 240 or pixel[2] < 240:
                        corner_white = False
            
            if corner_transparent:
                transparent_corners += 1
            if corner_white:
                white_corners += 1

        # Accept if corners are transparent OR white (if allowed)
        if transparent_corners >= 3:
            return True
        
        if check_white_bg and white_corners >= 3:
            return True
            
        return False

    def _check_edge_quality(
        self,
        image: Image.Image,
        pixels: List[Tuple],
        width: int,
        height: int
    ) -> Tuple[float, List[str]]:
        """
        Check edge quality for halos and artifacts

        Returns:
            Tuple of (quality score 0-1, list of issues)
        """
        issues = []
        quality_score = 1.0

        # Find object boundaries
        boundaries = self._find_boundaries(pixels, width, height)

        if not boundaries:
            issues.append("No clear object boundary found")
            return 0.5, issues

        # Check for halos (semi-transparent pixels around edges)
        halo_count = 0
        harsh_edge_count = 0

        for x, y in boundaries[:self.EDGE_SAMPLE_COUNT]:
            idx = y * width + x
            if idx >= len(pixels):
                continue

            alpha = pixels[idx][3]

            # Check surrounding pixels
            surroundings = self._get_surrounding_pixels(pixels, x, y, width, height)

            # Look for halo effect (bright semi-transparent pixels)
            for sx, sy, pixel in surroundings:
                if 20 < pixel[3] < 200:  # Semi-transparent
                    # Check if it's a halo (lighter than object)
                    if sum(pixel[:3]) > 500:  # Bright pixel
                        halo_count += 1

            # Check for harsh edges (sudden alpha jumps)
            alpha_values = [p[3] for _, _, p in surroundings]
            if alpha_values:
                max_jump = max(abs(alpha - a) for a in alpha_values)
                if max_jump > 200:
                    harsh_edge_count += 1

        # Calculate quality score
        if boundaries:
            halo_ratio = halo_count / len(boundaries[:self.EDGE_SAMPLE_COUNT])
            harsh_ratio = harsh_edge_count / len(boundaries[:self.EDGE_SAMPLE_COUNT])

            if halo_ratio > 0.3:
                issues.append("Significant halo effect detected around edges")
                quality_score -= 0.3

            if harsh_ratio > 0.5:
                issues.append("Harsh/jagged edges detected")
                quality_score -= 0.2

        return max(0, quality_score), issues

    def _find_boundaries(
        self,
        pixels: List[Tuple],
        width: int,
        height: int
    ) -> List[Tuple[int, int]]:
        """Find pixels at object boundaries"""
        boundaries = []

        for y in range(height):
            for x in range(width):
                idx = y * width + x
                if idx >= len(pixels):
                    continue

                alpha = pixels[idx][3]
                if alpha < 128:  # Mostly transparent
                    continue

                # Check if adjacent to transparent pixel
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        nidx = ny * width + nx
                        if nidx < len(pixels) and pixels[nidx][3] < 128:
                            boundaries.append((x, y))
                            break

        return boundaries

    def _get_surrounding_pixels(
        self,
        pixels: List[Tuple],
        x: int,
        y: int,
        width: int,
        height: int
    ) -> List[Tuple[int, int, Tuple]]:
        """Get surrounding pixel data"""
        surrounding = []
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    idx = ny * width + nx
                    if idx < len(pixels):
                        surrounding.append((nx, ny, pixels[idx]))
        return surrounding

    def _calculate_cleanliness(
        self,
        bg_transparent: bool,
        edge_quality: float,
        artifact_count: int,
        issue_count: int
    ) -> float:
        """Calculate overall transparency cleanliness score"""
        score = 1.0

        if not bg_transparent:
            score -= 0.4

        score -= (1 - edge_quality) * 0.3
        score -= artifact_count * 0.1
        score -= issue_count * 0.05

        return max(0, min(1, score))

    def _generate_recommendation(
        self,
        report: TransparencyReport,
        expected_transparent: bool
    ) -> str:
        """Generate actionable recommendation"""
        if not expected_transparent:
            return "No transparency requirements"

        if not report.has_alpha_channel:
            return "Add alpha channel and remove background"

        if not report.background_transparent:
            return "Remove background completely - ensure corners are transparent"

        if report.edge_quality < 0.7:
            return "Clean up edges - remove halos and smooth transitions"

        if report.transparency_cleanliness > 0.9:
            return "Transparency quality is excellent"

        return "Minor transparency cleanup recommended"

    def check_from_bytes(
        self,
        image_data: bytes,
        expected_transparent: bool = True
    ) -> TransparencyReport:
        """
        Check transparency from image bytes

        Convenience method for checking images without loading them first
        """
        image = Image.open(BytesIO(image_data))
        return self.check(image, expected_transparent)
