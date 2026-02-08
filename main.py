import sys
from trickshot_summary import getSummary
from commentator_script import getScript
from eleven_sfx import generate_crowd_sfx_mp3
from tts_chris import generate_chris_mp3
from video_processor import VideoProcessor


def main():
    # Get video file from command line or use default
    video_file = sys.argv[1] if len(sys.argv) > 1 else "trickshot.mp4"
    
    print(f"\n🎬 Processing: {video_file}\n")
    
    # Step 1: Get video summary from 12Labs
    print("Step 1: Analyzing video...")
    summary = getSummary(video_file)
    print("✓ Video analysis complete\n")
    
    # Step 2: Generate commentary script from Gemini
    print("Step 2: Generating commentary script...")
    script = getScript(summary)
    print("✓ Script generated\n")
    
    # Step 3: Generate commentary audio with Chris voice
    print("Step 3: Generating commentary audio...")
    voice_file = generate_chris_mp3(script, out_path="trickshot-voice.mp3")
    print(f"✓ Commentary saved to {voice_file}\n")
    
    # Step 4: Generate crowd noise
    print("Step 4: Generating crowd noise...")
    crowd_prompt = (
        "Background audio of a crowded basketball arena as heard through a TV broadcast. "
        "Include cheering, clapping, chanting, and natural crowd reactions. "
        "No narration or music."
    )
    crowd_file = generate_crowd_sfx_mp3(crowd_prompt, "crowd-noises.mp3", duration_seconds=13, loop=False)
    print(f"✓ Crowd noise saved to {crowd_file}\n")
    
    # Step 5: Overlay audio on video
    print("Step 5: Processing video with audio...")
    processor = VideoProcessor(video_file, voice_file, crowd_file)
    processor.process(cleanup=True)
    
    print(f"\n✓ Done! Your video is ready: {processor.final_video}\n")


if __name__ == "__main__":
    main()