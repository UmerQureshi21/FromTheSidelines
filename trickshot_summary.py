import time
from twelvelabs import TwelveLabs
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env into environment

apiKey = os.getenv("TWELVELABS_API_KEY")
indexId = os.getenv("INDEX_ID")
prompt = "Give me a detailed explanation of the trickshot. At each new step of the trickshot, annotate it with timestamps"


# # 1. Initialize the client
client = TwelveLabs(api_key=apiKey)

# # 2. Create an index (Already done)

def getSummary(videoPath):
    # 3. Upload a video
    asset = client.assets.create(
        method="direct",
        file=open(videoPath, "rb") # Use direct links to raw media files. Video hosting platforms and cloud storage sharing links are not supported
        # Or use method="direct" and file=open("<PATH_TO_VIDEO_FILE>", "rb") to upload a file from the local file system
    )

    print(f"Created asset: id={asset.id}")

    # 4. Index your video
    indexed_asset = client.indexes.indexed_assets.create(
        index_id=indexId,
        asset_id=asset.id
    )
    print(f"Created indexed asset: id={indexed_asset.id}")
    # 5. Monitor the indexing process
    print("Waiting for indexing to complete.")
    while True:
        indexed_asset = client.indexes.indexed_assets.retrieve(
            indexId,
            indexed_asset.id
        )
        print(f"  Status={indexed_asset.status}")
        if indexed_asset.status == "ready":
            print("Indexing complete!")
            break
        elif indexed_asset.status == "failed":
            raise RuntimeError("Indexing failed")
        time.sleep(5)

    # 6. Analyze your video
    text_stream = client.analyze_stream(video_id=indexed_asset.id, prompt=prompt)

    answer = ""

    # 7. Process the results
    for text in text_stream:
        if text.event_type == "text_generation":
            answer += text.text
    return answer

videoPath = "test-vids/trickshot.mp4"
answer = getSummary(videoPath)
print (f"ANSWER: {answer}")


'''
EXAMPLE ANSWER:

[00:00] The video opens with a wide-angle shot of a blue basketball court, featuring two individuals positioned on separate platforms, each holding a basketball.  
[00:01] The person on the left initiates the trickshot by tossing their basketball straight upward while simultaneously performing a backflip.  
[00:02] Midway through the backflip, they catch the basketball in mid-air, demonstrating precise timing and control.  
[00:03] Simultaneously, the individual on the right mirrors the action—throwing their ball upward and executing a backflip, then catching it at the peak of their motion.  
[00:04] Both performers are now airborne, having completed their flips and secured the balls, showcasing synchronized coordination.  
[00:05] The left performer throws their basketball toward the hoop, while the right performer prepares to release theirs.  
[00:06] Both individuals release their basketballs at the same moment, sending them on a trajectory toward the hoop.  
[00:07] The balls are seen in mid-flight, arcing gracefully through the air, with clear visibility of their paths.  
[00:08] Both basketballs successfully pass through the hoop in perfect unison, completing the trickshot with precision and flair.  
[00:09] The video concludes with a close-up shot of the balls swishing through the net, emphasizing the flawless execution of the sequence.  

The entire trickshot is performed with seamless timing, synchronized movements, and exceptional skill, all captured from a consistent camera angle that maintains full visibility of the court and performers throughout.
'''