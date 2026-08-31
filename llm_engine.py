from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_ai_lesson(student_query: str, level: str, time: str):
    prompt = f"""
    You are an expert, human-like AI Teacher. 
    The student wants to learn about: '{student_query}'.
    The student's level is: {level}.
    You have {time} to teach this.
    
    Provide a structured, engaging lesson plan. 
    Include:
    1. A short introduction.
    2. Core concept explanation suitable for a {level}.
    3. One practical example.
    4. One conceptual question at the end to test their understanding.
    
    Keep the tone encouraging and conversational.
    """
    
    try:
        # Yahan par model ka naam update kar diya gaya hai
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I am facing a technical issue right now. Let's try again later."