import os
import subprocess
import sys
from pathlib import Path


class VideoProcessor:
    """Process video files with FFmpeg to add audio overlays."""
    
    def __init__(self, video_file, voice_file="trickshot-voice.mp3", crowd_file="crowd-noises.mp3"):
        """
        Initialize the video processor.
        
        Args:
            video_file (str): Path to the input video file
            voice_file (str): Path to the voice-over audio file (default: trickshot-voice.mp3)
            crowd_file (str): Path to the crowd noise audio file (default: crowd-noises.mp3)
        """
        self.video_file = video_file
        self.voice_file = voice_file
        self.crowd_file = crowd_file
        self.temp_video = "flipshot.mp4"
        self.output_video = "trickshot_output.mp4"
        self.final_video = "full-trickshot.mp4"
        
        # Validate that all input files exist
        self._validate_files()
    
    def _validate_files(self):
        """Check that all input files exist in the current directory."""
        for file in [self.video_file, self.voice_file, self.crowd_file]:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")
    
    def remove_audio(self):
        """Remove audio from the original video file."""
        print(f"Step 1: Removing audio from {self.video_file}...")
        
        cmd = [
            "ffmpeg",
            "-i", self.video_file,
            "-c:v", "copy",
            "-an",
            self.temp_video
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=False)
            print(f"✓ Audio removed. Created: {self.temp_video}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error removing audio: {e}")
            raise
    
    def add_voice_over(self):
        """Add voice-over commentary to the video."""
        print(f"\nStep 2: Adding voice-over ({self.voice_file})...")
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", self.temp_video,
            "-i", self.voice_file,
            "-filter_complex", "[0:v]tpad=stop_mode=clone:stop_duration=999[v]",
            "-map", "[v]",
            "-map", "1:a:0",
            "-shortest",
            "-c:v", "libx264",
            "-c:a", "aac",
            self.output_video
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=False)
            print(f"✓ Voice-over added. Created: {self.output_video}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error adding voice-over: {e}")
            raise
    
    def add_crowd_noise(self):
        """Add crowd noise as background audio mixed with voice-over."""
        print(f"\nStep 3: Adding crowd noise ({self.crowd_file})...")
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", self.output_video,
            "-i", self.crowd_file,
            "-filter_complex",
            "[1:a]afade=t=in:st=0:d=1,volume=0.25[a1];[0:a][a1]amix=inputs=2:duration=longest[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            self.final_video
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=False)
            print(f"✓ Crowd noise added. Created: {self.final_video}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error adding crowd noise: {e}")
            raise
    
    def process(self, cleanup=True):
        """
        Execute the full video processing pipeline.
        
        Args:
            cleanup (bool): If True, remove temporary files after processing (default: True)
        """
        try:
            self.remove_audio()
            self.add_voice_over()
            self.add_crowd_noise()
            
            if cleanup:
                self._cleanup_temp_files()
            
            print(f"\n✓ Processing complete! Final video: {self.final_video}")
            
        except Exception as e:
            print(f"\n✗ Processing failed: {e}")
            sys.exit(1)
    
    def _cleanup_temp_files(self):
        """Remove temporary files created during processing."""
        print(f"\nCleaning up temporary files...")
        temp_files = [self.temp_video, self.output_video]
        
        for file in temp_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"✓ Deleted: {file}")


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python video_processor.py <video_file> [voice_file] [crowd_file]")
        print("\nExample: python video_processor.py trickshot.mp4")
        print("         python video_processor.py trickshot.mp4 my-voice.mp3 my-crowd.mp3")
        sys.exit(1)
    
    video_file = sys.argv[1]
    voice_file = sys.argv[2] if len(sys.argv) > 2 else "trickshot-voice.mp3"
    crowd_file = sys.argv[3] if len(sys.argv) > 3 else "crowd-noises.mp3"
    
    processor = VideoProcessor(video_file, voice_file, crowd_file)
    processor.process(cleanup=True)


if __name__ == "__main__":
    main()