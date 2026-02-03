"""Image format conversion utilities."""

from pathlib import Path
from typing import List, Optional, Union, Tuple
from PIL import Image
import io


class FormatConverter:
    """Handles image format conversions for game assets."""

    SUPPORTED_FORMATS = {
        'png': 'PNG',
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'gif': 'GIF',
        'webp': 'WEBP',
        'bmp': 'BMP',
    }

    @classmethod
    def convert(
        cls,
        image: Image.Image,
        target_format: str,
        quality: int = 95,
        optimize: bool = True
    ) -> bytes:
        """
        Convert image to specified format.

        Args:
            image: PIL Image to convert
            target_format: Target format (png, jpg, gif, webp)
            quality: Quality for lossy formats (1-100)
            optimize: Whether to optimize the output

        Returns:
            Converted image as bytes
        """
        format_upper = cls.SUPPORTED_FORMATS.get(target_format.lower())
        if not format_upper:
            raise ValueError(f"Unsupported format: {target_format}")

        buffer = io.BytesIO()

        # Handle format-specific requirements
        if format_upper == 'JPEG':
            # JPEG doesn't support transparency
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')

            image.save(buffer, format=format_upper, quality=quality, optimize=optimize)

        elif format_upper == 'PNG':
            if image.mode not in ('RGBA', 'RGB', 'L', 'LA', 'P'):
                image = image.convert('RGBA')
            image.save(buffer, format=format_upper, optimize=optimize)

        elif format_upper == 'GIF':
            # GIF requires palette mode for single images
            if image.mode == 'RGBA':
                # Preserve transparency
                alpha = image.split()[3]
                image = image.convert('RGB').convert('P', palette=Image.Palette.ADAPTIVE, colors=255)
                mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                image.paste(255, mask)
                image.save(buffer, format=format_upper, transparency=255, optimize=optimize)
            else:
                if image.mode != 'P':
                    image = image.convert('P', palette=Image.Palette.ADAPTIVE)
                image.save(buffer, format=format_upper, optimize=optimize)

        elif format_upper == 'WEBP':
            image.save(buffer, format=format_upper, quality=quality, optimize=optimize)

        else:
            image.save(buffer, format=format_upper)

        return buffer.getvalue()

    @classmethod
    def convert_file(
        cls,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        quality: int = 95,
        optimize: bool = True
    ) -> Path:
        """
        Convert an image file to a different format.

        Args:
            input_path: Path to input image
            output_path: Path for output image (format determined by extension)
            quality: Quality for lossy formats
            optimize: Whether to optimize

        Returns:
            Path to converted file
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        target_format = output_path.suffix.lstrip('.')

        image = Image.open(input_path)
        converted = cls.convert(image, target_format, quality, optimize)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(converted)

        return output_path

    @classmethod
    def create_gif_from_frames(
        cls,
        frames: List[Image.Image],
        duration: int = 100,
        loop: int = 0,
        optimize: bool = True
    ) -> bytes:
        """
        Create an animated GIF from a list of frames.

        Args:
            frames: List of PIL Images
            duration: Duration of each frame in milliseconds
            loop: Number of loops (0 = infinite)
            optimize: Whether to optimize

        Returns:
            Animated GIF as bytes
        """
        if not frames:
            raise ValueError("No frames provided")

        buffer = io.BytesIO()

        # Convert all frames to palette mode
        processed_frames = []
        for frame in frames:
            if frame.mode == 'RGBA':
                # Handle transparency
                alpha = frame.split()[3]
                p_frame = frame.convert('RGB').convert('P', palette=Image.Palette.ADAPTIVE, colors=255)
                mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                p_frame.paste(255, mask)
                processed_frames.append(p_frame)
            else:
                if frame.mode != 'P':
                    frame = frame.convert('P', palette=Image.Palette.ADAPTIVE)
                processed_frames.append(frame)

        # Save as animated GIF
        processed_frames[0].save(
            buffer,
            format='GIF',
            save_all=True,
            append_images=processed_frames[1:],
            duration=duration,
            loop=loop,
            optimize=optimize,
            transparency=255 if any(f.mode == 'RGBA' for f in frames) else None
        )

        return buffer.getvalue()

    @classmethod
    def create_gif_from_files(
        cls,
        file_paths: List[Union[str, Path]],
        output_path: Union[str, Path],
        duration: int = 100,
        loop: int = 0
    ) -> Path:
        """
        Create an animated GIF from image files.

        Args:
            file_paths: Paths to frame images
            output_path: Output path for GIF
            duration: Frame duration in ms
            loop: Number of loops

        Returns:
            Path to created GIF
        """
        frames = [Image.open(p) for p in file_paths]
        gif_data = cls.create_gif_from_frames(frames, duration, loop)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(gif_data)

        return output_path

    @classmethod
    def extract_gif_frames(
        cls,
        gif_path: Union[str, Path]
    ) -> List[Image.Image]:
        """
        Extract all frames from an animated GIF.

        Args:
            gif_path: Path to GIF file

        Returns:
            List of PIL Images
        """
        gif = Image.open(gif_path)
        frames = []

        try:
            while True:
                frames.append(gif.copy().convert('RGBA'))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        return frames

    @staticmethod
    def get_format_info(image_path: Union[str, Path]) -> dict:
        """
        Get information about an image file.

        Args:
            image_path: Path to image

        Returns:
            Dict with format info
        """
        image = Image.open(image_path)

        info = {
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
            'width': image.width,
            'height': image.height,
        }

        # Check if animated
        try:
            image.seek(1)
            info['animated'] = True
            # Count frames
            frame_count = 1
            while True:
                try:
                    image.seek(image.tell() + 1)
                    frame_count += 1
                except EOFError:
                    break
            info['frame_count'] = frame_count
        except EOFError:
            info['animated'] = False
            info['frame_count'] = 1

        return info
