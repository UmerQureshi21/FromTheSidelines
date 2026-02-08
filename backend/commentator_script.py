# from dotenv import load_dotenv
# from google import genai
# from google.genai import types
# import os
# import requests

# load_dotenv()  # loads variables from .env into environment

# apiKey = os.getenv("GEMINI_API_KEY")
# apiKey = os.getenv("FEATHERLESS")

# # moonshotai/Kimi-K2-Thinking

# # The client gets the API key from the environment variable `GEMINI_API_KEY`.

# example_trickshot = """
# [00:00] The video opens with a wide-angle shot of a blue basketball court, featuring two individuals positioned on separate platforms, each holding a basketball.  
# [00:01] The person on the left initiates the trickshot by tossing their basketball straight upward while simultaneously performing a backflip.  
# [00:02] Midway through the backflip, they catch the basketball in mid-air, demonstrating precise timing and control.  
# [00:03] Simultaneously, the individual on the right mirrors the action—throwing their ball upward and executing a backflip, then catching it at the peak of their motion.  
# [00:04] Both performers are now airborne, having completed their flips and secured the balls, showcasing synchronized coordination.  
# [00:05] The left performer throws their basketball toward the hoop, while the right performer prepares to release theirs.  
# [00:06] Both individuals release their basketballs at the same moment, sending them on a trajectory toward the hoop.  
# [00:07] The balls are seen in mid-flight, arcing gracefully through the air, with clear visibility of their paths.  
# [00:08] Both basketballs successfully pass through the hoop in perfect unison, completing the trickshot with precision and flair.  
# [00:09] The video concludes with a close-up shot of the balls swishing through the net, emphasizing the flawless execution of the sequence.  

# The entire trickshot is performed with seamless timing, synchronized movements, and exceptional skill, all captured from a consistent camera angle that maintains full visibility of the court and performers throughout.
# """

# prompt = f"""
            
#             You are an extremely excited and hyped commentator for sports. Any trickshot that happens, 
#             give me what you would say. make sure that if it was spoken, then the duration of the speech would be about 6 seconds, and match what you're saying to 
#             each timestamp. Be short, concise and straight forward with what you say, but also be excited, nothing too long. Don't tell me the timestamps or put any astericks though, just what you would say in a short paragraph.


#             """



# def getScript(trickshot):
#     client = genai.Client()

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         config=types.GenerateContentConfig(
#             system_instruction=f"""
            
#             You are an extremely excited and hyped commentator for sports. Any trickshot that happens, 
#             give me what you would say. make sure that if it was spoken, then the duration of the speech would be about 6 seconds, and match what you're saying to 
#             each timestamp. Be short, concise and straight forward with what you say, but also be excited, nothing too long. Don't tell me the timestamps or put any astericks though, just what you would say in a short paragraph.
#             """),
#         contents=trickshot
#     )
#     text = response.text
#     print(f"THIS IS THE COMMENTARY SCRIPT:\n{text}")
#     return text

# # #chris voice id = Anr9GtYh2VRXxiPplzxM

# # from dotenv import load_dotenv
# # import os
# # import requests

# # load_dotenv()  # loads variables from .env into environment

# # FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
# # FEATHERLESS_URL = "https://api.featherless.ai/v1/chat/completions"

# # example_trickshot = """
# # [00:00] The video opens with a wide-angle shot of a blue basketball court, featuring two individuals positioned on separate platforms, each holding a basketball.  
# # [00:01] The person on the left initiates the trickshot by tossing their basketball straight upward while simultaneously performing a backflip.  
# # [00:02] Midway through the backflip, they catch the basketball in mid-air, demonstrating precise timing and control.  
# # [00:03] Simultaneously, the individual on the right mirrors the action—throwing their ball upward and executing a backflip, then catching it at the peak of their motion.  
# # [00:04] Both performers are now airborne, having completed their flips and secured the balls, showcasing synchronized coordination.  
# # [00:05] The left performer throws their basketball toward the hoop, while the right performer prepares to release theirs.  
# # [00:06] Both individuals release their basketballs at the same moment, sending them on a trajectory toward the hoop.  
# # [00:07] The balls are seen in mid-flight, arcing gracefully through the air, with clear visibility of their paths.  
# # [00:08] Both basketballs successfully pass through the hoop in perfect unison, completing the trickshot with precision and flair.  
# # [00:09] The video concludes with a close-up shot of the balls swishing through the net, emphasizing the flawless execution of the sequence.  

# # The entire trickshot is performed with seamless timing, synchronized movements, and exceptional skill, all captured from a consistent camera angle that maintains full visibility of the court and performers throughout.
# # """

# # def getScript(trickshot: str) -> str:
# #     """
# #     Generate sports commentary using Featherless.ai
    
# #     Args:
# #         trickshot: Video description from 12Labs
    
# #     Returns:
# #         Commentary script
# #     """
    
# #     headers = {
# #         "Authorization": f"Bearer {FEATHERLESS_API_KEY}",
# #         "Content-Type": "application/json"
# #     }
    
# #     payload = {
# #         "model": "moonshotai/Kimi-K2-Thinking",
# #         "messages": [
# #             {
# #                 "role": "system",
# #                 "content": """You are an extremely excited and hyped commentator for sports. 
# #                 When given a trickshot description, respond with authentic ESPN-style commentary 
# #                 that would take about 6 seconds to speak (roughly 60-80 words). 
# #                 Be short, concise, and straightforward but also extremely excited and energetic. 
# #                 Don't tell me the timestamps or put any asterisks. Just give me what you would say 
# #                 as a short paragraph of pure hype."""
# #             },
# #             {
# #                 "role": "user",
# #                 "content": trickshot
# #             }
# #         ],
# #         "temperature": 0.9,
# #         "max_tokens": 250
# #     }
    
# #     try:
# #         response = requests.post(FEATHERLESS_URL, headers=headers, json=payload)
# #         response.raise_for_status()
        
# #         text = response.json()['choices'][0]['message']['content']
# #         print(f"THIS IS THE COMMENTARY SCRIPT:\n{text}")
# #         return text
        
# #     except requests.exceptions.RequestException as e:
# #         print(f"Error calling Featherless API: {e}")
# #         raise




from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()  # loads variables from .env into environment

apiKey = os.getenv("GEMINI_API_KEY")

# The client gets the API key from the environment variable `GEMINI_API_KEY`.

example_trickshot = """
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
"""

def getScript(trickshot):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=f"""
            
            You are an extremely excited and hyped commentator for sports. Any trickshot that happens, 
            give me what you would say. make sure that if it was spoken, then the duration of the speech would be about 6 seconds, and match what you're saying to 
            each timestamp. Don't tell me the timestamps or put any astericks though, just what you would say in a short paragraph.
            """),
        contents=trickshot
    )
    text = response.text
    print(f"THIS IS THE COMMENTARY SCRIPT:\n{text}")
    return text

#chris voice id = Anr9GtYh2VRXxiPplzxM