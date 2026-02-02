#!/usr/bin/env python3
"""
Combine audio and video files using FFmpeg.

This script combines AI-generated audio with manually created video
to create a complete music video.
"""

import subprocess
import sys
from pathlib import Path


def combine_audio_video(
    video_path: str,
    audio_path: str,
    output_path: str,
    overwrite: bool = True,
) -> bool:
    """
    Combine video and audio using FFmpeg.
    
    Args:
        video_path: Path to input video file
        audio_path: Path to input audio file
        output_path: Path to output combined video
        overwrite: Whether to overwrite existing output file
    
    Returns:
        True if successful, False otherwise
    """
    video_file = Path(video_path)
    audio_file = Path(audio_path)
    output_file = Path(output_path)
    
    # Validate inputs
    if not video_file.exists():
        print(f"❌ Error: Video file not found: {video_path}")
        return False
    
    if not audio_file.exists():
        print(f"❌ Error: Audio file not found: {audio_path}")
        return False
    
    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if output exists
    if output_file.exists() and not overwrite:
        print(f"⚠️  Output file exists: {output_path}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return False
    
    print(f"🎬 Combining video and audio...")
    print(f"   Video: {video_path}")
    print(f"   Audio: {audio_path}")
    print(f"   Output: {output_path}")
    
    # Build FFmpeg command
    cmd = [
        "ffmpeg",
        "-i", str(video_file),
        "-i", str(audio_file),
        "-c:v", "copy",  # Copy video codec (no re-encoding)
        "-c:a", "aac",   # Use AAC audio codec (YouTube compatible)
        "-shortest",     # Match shortest input duration
    ]
    
    if overwrite:
        cmd.append("-y")  # Overwrite output file
    
    cmd.append(str(output_file))
    
    try:
        # Run FFmpeg
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        
        print(f"✅ Success! Combined video saved to: {output_path}")
        print(f"   File size: {output_file.stat().st_size / (1024*1024):.2f} MB")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error:")
        print(f"   {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ Error: FFmpeg not found!")
        print("   Please install FFmpeg: https://ffmpeg.org/download.html")
        print("   Or on Windows: winget install ffmpeg")
        return False


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 4:
        print("Usage: python combine_audio_video.py <video> <audio> <output>")
        print("\nExample:")
        print("  python combine_audio_video.py canva_video.mp4 exports/jazz.wav output/music_video.mp4")
        sys.exit(1)
    
    video_path = sys.argv[1]
    audio_path = sys.argv[2]
    output_path = sys.argv[3]
    
    success = combine_audio_video(video_path, audio_path, output_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

