from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_ai_lesson(student_query: str, level: str, time: str):
    
    # Prompt ko smartly update kiya gaya hai conditions ke sath
    prompt = f"""
    You are an expert, friendly AI Teacher. 
    
    The student's input is: '{student_query}'
    
    STRICT INSTRUCTIONS:
    1. If the student's input is just a simple greeting (like "hi", "hello", "good morning", "hey") or general small talk, DO NOT generate a lesson plan. 
       Instead, reply directly with: "Hello! I am your AI Teacher. What topic would you like to study today?"
       
    2. If the student's input is an actual study topic, generate a structured, engaging lesson plan for a {level} student. The lesson should take about {time} to read.
       
       Include:
       - A short introduction.
       - Core concept explanation suitable for a {level}.
       - One practical example.
       - One conceptual question at the end to test their understanding.
    
    Always keep the tone encouraging and conversational. Do not use complex markdown styling if it's just a greeting.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I am facing a technical issue right now. Let's try again later."