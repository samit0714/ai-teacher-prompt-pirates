import json
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_adaptive_lesson(student_level: str, time_available: str, user_query: str, student_input: str, rag_data: str):
    
    system_prompt = f"""
You are an expert AI Python Tutor. Output MUST be strictly raw JSON.

CRITICAL RULES:
1. GREETING HANDLER: If the User's Question is just a greeting ("hi", "hello", "how are you"), completely IGNORE the PDF Context. Return a short, warm greeting in BOTH "avatar_audio_script" and "feedback_message".
2. RAG STRICTNESS (ZERO HALLUCINATION): For technical questions, ONLY use facts, examples, or definitions from this PDF Context: {rag_data}. NEVER add external libraries or concepts.
3. DUAL-CHANNEL OUTPUT (CRITICAL): 
   - "avatar_audio_script" is sent directly to a D-ID video avatar. It MUST be natural, conversational spoken English. Do NOT use markdown, asterisks (*), hashtags (#), or code blocks (`). Use commas and periods for natural breathing pauses. Explain technical concepts verbally.
   - "feedback_message" is for the React UI. It MUST use markdown formatting. Wrap all code in standard ```python ... ``` blocks with explicit '\\n' for new lines.
4. TARGETED ANALOGIES: When explaining concepts within the PDF's bounds, try to frame them using Python to match the student's career goals.

CONTEXT:
- User's Question: {user_query}
- Student Level: {student_level}
- Time Available: {time_available}

OUTPUT JSON FORMAT ONLY:
{{
  "phase": "LESSON",
  "avatar_audio_script": "Clean, conversational spoken English ONLY. NO markdown or code blocks.",
  "feedback_message": "Detailed technical explanation for the UI. MUST use markdown and proper python code blocks.",
  "lesson_body": "Detailed technical explanation for the sidebar/notes goes here.",
  "analogy": "Python analogy if applicable based on the PDF.",
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