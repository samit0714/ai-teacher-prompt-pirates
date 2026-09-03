import json
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()



# Asli key ki jagah yeh likh de
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_adaptive_lesson(student_level: str, time_available: str, user_query: str, student_input: str, rag_data: str):
    
    system_prompt = f"""
You are an expert AI Python Tutor. Output MUST be strictly raw JSON.

CRITICAL RAG RULE (ZERO HALLUCINATION):
- PDF Context: {rag_data}
- When the user asks for examples, definitions, or facts, you MUST ONLY list the EXACT items mentioned in the PDF Context. 
- DO NOT add extra examples from your own knowledge. If the PDF says 'os' and 'abc', you only say 'os' and 'abc'. NEVER add 'sys', 'math', or 'datetime'.
- IGNORE the "Pro" student level if it makes you want to add external facts. The PDF is the ultimate truth.
- Ignore random watermarks like "URBAN" or "EDGE".

UI FORMATTING RULE:
- Put your ENTIRE response inside the "feedback_message" field.
- Use explicit '\\n\\n' for paragraph breaks.

CONTEXT:
- User's Question: {user_query}
- Student Level: {student_level}

OUTPUT JSON FORMAT ONLY:
{{
  "phase": "LESSON",
  "feedback_message": "...",
  "lesson_body": "",
  "analogy": "",
  "misconception_detected": false,
  "mcqs": []
}}
"""
    
    try:
        response = client.models.generate_content(
           model="gemini-flash-lite-latest",
            contents=system_prompt,
        )
        
        # Pro-Tip Hack: Gemini kabhi-kabhi markdown text bhej deta hai, usko clean karna zaroori hai
        clean_json_str = response.text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_json_str) # Yeh string ko perfect Python Dictionary bana dega
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        # Error aane par bhi API crash na ho, isliye fallback JSON bhej rahe hain
        return {
            "phase": "ERROR",
            "feedback_message": "Sorry, I am taking a quick break. Let's try again in a minute!",
            "lesson_body": "",
            "analogy": "",
            "misconception_detected": False,
            "mcqs": []
        }