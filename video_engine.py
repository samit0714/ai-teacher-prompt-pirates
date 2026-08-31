import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
DID_API_KEY = os.getenv("DID_API_KEY")

def generate_avatar_video(text_script: str):
    """
    Yeh function D-ID API ko text bhejega aur wahan se MP4 video link wapas layega.
    """
    url = "https://api.d-id.com/talks"
    
    # Step 3 Handled: Yahan humne Avatar URL aur Voice ID set kar di hai
    # Purani line ko is nayi line se replace karein:
    # Yeh Wikipedia ka direct image link hai, jo kabhi block nahi hoga
    avatar_image_url = "https://randomuser.me/api/portraits/women/68.jpg" # Dummy professional face URL
    voice_id = "en-US-JennyNeural" # Standard female AI voice
    # voice id ="en-US-GuyNeural" for male ai voice
    
    payload = {
        "script": {
            "type": "text",
            "input": text_script,
            "provider": {
                "type": "microsoft",
                "voice_id": voice_id
            }
        },
        "source_url": avatar_image_url,
        "config": {
            "fluent": False,
            "pad_audio": "0.0"
        }
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {DID_API_KEY}"
    }

    try:
        # 1. Video generate karne ki request bhejna
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        
        if "id" not in response_data:
            print("D-ID Error:", response_data)
            return None
            
        video_id = response_data["id"]
        print(f"Video processing started. ID: {video_id}")
        
        # 2. Video ready hone ka wait karna (Polling)
        get_url = f"{url}/{video_id}"
        
        while True:
            time.sleep(5) # Har 5 second mein check karega ki video ban gayi kya
            status_response = requests.get(get_url, headers=headers)
            status_data = status_response.json()
            
            status = status_data.get("status")
            if status == "done":
                print("Video successfully generated!")
                return status_data.get("result_url")
            elif status == "error":
                print("Error in generating video.")
                return None
            else:
                print("Processing video... please wait.")
                
    except Exception as e:
        print(f"Video Generation Exception: {e}")
        return None

# Aap isko direct yahan test kar sakte hain:
#if __name__ == "__main__":
 #   link = generate_avatar_video("Hello Samit, I am your AI Teacher. How can I help you today?")
  #  print("Final Video URL:", link)