"""Sprite-specific processing for game assets."""

from pathlib import Path
from typing import List, Tuple, Optional, Union
from PIL import Image
import json

from .image_processor import ImageProcessor
from .format_converter import FormatConverter


class SpriteProcessor:
    """Specialized processing for game sprites and animations."""

    def __init__(self, output_dir: Union[str, Path] = './assets/sprites'):
        """
        Initialize sprite processor.

        Args:
            output_dir: Directory for processed sprites
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_sprite(
        self,
        image: Image.Image,
        name: str,
        size: Optional[Tuple[int, int]] = None,
        remove_bg: bool = True,
        pixelate: bool = False,
        pixel_size: int = 4,
        reduce_colors: bool = False,
        num_colors: int = 16,
        add_outline: bool = False,
        outline_color: Tuple[int, int, int, int] = (0, 0, 0, 255),
        outline_thickness: int = 1
    ) -> Path:
        """
        Process a sprite image with various effects.

        Args:
            image: Source PIL Image
            name: Sprite name (without extension)
            size: Target size (width, height)
            remove_bg: Whether to remove background
            pixelate: Whether to apply pixel art effect
            pixel_size: Pixel size for pixelation
            reduce_colors: Whether to reduce color palette
            num_colors: Number of colors if reducing
            add_outline: Whether to add outline
            outline_color: RGBA outline color
            outline_thickness: Outline thickness

        Returns:
            Path to saved sprite
        """
        # Ensure RGBA mode
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # Apply processing steps
        if remove_bg:
            image = ImageProcessor.remove_background(image)

        if pixelate:
            image = ImageProcessor.pixelate(image, pixel_size)

        if reduce_colors:
            image = ImageProcessor.reduce_colors(image, num_colors)

        if add_outline:
            image = ImageProcessor.add_outline(image, outline_color, outline_thickness)

        # Crop to content
        image = ImageProcessor.crop_to_content(image, padding=2)

        # Resize if specified
        if size:
            image = ImageProcessor.resize(image, size, maintain_aspect=True)

        # Save
        output_path = self.output_dir / f"{name}.png"
        image.save(output_path, 'PNG', optimize=True)

        return output_path

    def create_sprite_sheet(
        self,
        frames: List[Image.Image],
        name: str,
        frame_size: Tuple[int, int],
        columns: Optional[int] = None,
        padding: int = 0
    ) -> Tuple[Path, dict]:
        """
        Create a sprite sheet from animation frames.

        Args:
            frames: List of frame images
            name: Sprite sheet name
            frame_size: Size of each frame
            columns: Number of columns (auto if None)
            padding: Padding between frames

        Returns:
            Tuple of (path to sprite sheet, metadata dict)
        """
        if not frames:
            raise ValueError("No frames provided")

        num_frames = len(frames)

        # Calculate grid dimensions
        if columns is None:
            columns = min(num_frames, 8)  # Max 8 columns by default
        rows = (num_frames + columns - 1) // columns

        # Calculate sheet size
        sheet_width = columns * frame_size[0] + (columns - 1) * padding
        sheet_height = rows * frame_size[1] + (rows - 1) * padding

        # Create sprite sheet
        sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))

        # Place frames
        for i, frame in enumerate(frames):
            col = i % columns
            row = i // columns

            x = col * (frame_size[0] + padding)
            y = row * (frame_size[1] + padding)

            # Resize frame if needed
            if frame.size != frame_size:
                frame = ImageProcessor.resize(frame, frame_size, maintain_aspect=True)

            sheet.paste(frame, (x, y), frame if frame.mode == 'RGBA' else None)

        # Save sprite sheet
        output_path = self.output_dir / f"{name}_sheet.png"
        sheet.save(output_path, 'PNG', optimize=True)

        # Create metadata
        metadata = {
            'name': name,
            'frame_width': frame_size[0],
            'frame_height': frame_size[1],
            'columns': columns,
            'rows': rows,
            'frame_count': num_frames,
            'padding': padding,
            'sheet_width': sheet_width,
            'sheet_height': sheet_height,
        }

        # Save metadata
        meta_path = self.output_dir / f"{name}_sheet.json"
        meta_path.write_text(json.dumps(metadata, indent=2))

        return output_path, metadata

    def create_animation(
        self,
        frames: List[Image.Image],
        name: str,
        frame_duration: int = 100,
        loop: bool = True
    ) -> Path:
        """
        Create an animated GIF from frames.

        Args:
            frames: List of frame images
            name: Animation name
            frame_duration: Duration per frame in ms
            loop: Whether to loop infinitely

        Returns:
            Path to GIF file
        """
        gif_data = FormatConverter.create_gif_from_frames(
            frames,
            duration=frame_duration,
            loop=0 if loop else 1
        )

        output_path = self.output_dir / f"{name}.gif"
        output_path.write_bytes(gif_data)

        return output_path

    def split_sprite_sheet(
        self,
        sheet_path: Union[str, Path],
        frame_size: Tuple[int, int],
        num_frames: Optional[int] = None,
        columns: Optional[int] = None
    ) -> List[Image.Image]:
        """
        Split a sprite sheet into individual frames.

        Args:
            sheet_path: Path to sprite sheet
            frame_size: Size of each frame
            num_frames: Number of frames (auto-detect if None)
            columns: Number of columns (auto-detect if None)

        Returns:
            List of frame images
        """
        sheet = Image.open(sheet_path)

        if columns is None:
            columns = sheet.width // frame_size[0]

        if num_frames is None:
            rows = sheet.height // frame_size[1]
            num_frames = columns * rows

        frames = []
        for i in range(num_frames):
            col = i % columns
            row = i // columns

            x = col * frame_size[0]
            y = row * frame_size[1]

            frame = sheet.crop((x, y, x + frame_size[0], y + frame_size[1]))
            frames.append(frame)

        return frames

    def batch_process(
        self,
        images: List[Tuple[Image.Image, str]],
        **process_kwargs
    ) -> List[Path]:
        """
        Process multiple sprites with the same settings.

        Args:
            images: List of (image, name) tuples
            **process_kwargs: Arguments passed to process_sprite

        Returns:
            List of output paths
        """
        paths = []
        for image, name in images:
            path = self.process_sprite(image, name, **process_kwargs)
            paths.append(path)
        return paths

    def generate_asset_manifest(
        self,
        output_path: Optional[Union[str, Path]] = None
    ) -> dict:
        """
        Generate a manifest of all sprites in the output directory.

        Args:
            output_path: Path to save manifest (optional)

        Returns:
            Manifest dictionary
        """
        manifest = {
            'sprites': [],
            'animations': [],
            'sprite_sheets': []
        }

        for file_path in self.output_dir.iterdir():
            if file_path.suffix == '.png':
                if '_sheet' in file_path.stem:
                    # Load metadata if exists
                    meta_path = file_path.with_suffix('.json')
                    metadata = json.loads(meta_path.read_text()) if meta_path.exists() else {}
                    manifest['sprite_sheets'].append({
                        'name': file_path.stem.replace('_sheet', ''),
                        'path': str(file_path.relative_to(self.output_dir)),
                        **metadata
                    })
                else:
                    info = FormatConverter.get_format_info(file_path)
                    manifest['sprites'].append({
                        'name': file_path.stem,
                        'path': str(file_path.relative_to(self.output_dir)),
                        'width': info['width'],
                        'height': info['height']
                    })
            elif file_path.suffix == '.gif':
                info = FormatConverter.get_format_info(file_path)
                manifest['animations'].append({
                    'name': file_path.stem,
                    'path': str(file_path.relative_to(self.output_dir)),
                    'width': info['width'],
                    'height': info['height'],
                    'frame_count': info.get('frame_count', 1)
                })

        if output_path:
            output_path = Path(output_path)
            output_path.write_text(json.dumps(manifest, indent=2))

        return manifest
