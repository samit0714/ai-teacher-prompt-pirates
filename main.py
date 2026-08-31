from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os

# Gemini AI engine ko import karna
from llm_engine import generate_ai_lesson

app = FastAPI(title="AI Teacher Backend")

# CORS Setup - Siddhartha ke React frontend se connect karne ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development phase mein sab allow rakhein
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Endpoint (Server check karne ke liye)
@app.get("/")
def read_root():
    return {"status": "success", "message": "Prompt Pirates AI Backend is Live!"}

# Endpoint 1: Material Upload karna (Saumya ke RAG data ke liye)
@app.post("/upload_material")
async def upload_material(file: UploadFile = File(...)):
    
    # 1. Folder ka path set karein
    upload_dir = "temp_uploads"
    
    # 2. Agar folder nahi hai, toh automatic create kar le (Error 183 fix)
    os.makedirs(upload_dir, exist_ok=True)
    
    # 3. File ko safely save karein
    file_location = f"{upload_dir}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    # NOTE: Yahan baad mein Saumya ka code connect hoga
    # Example: process_pdf_for_rag(file_location)
    
    return {
        "status": "success", 
        "filename": file.filename, 
        "message": "File successfully uploaded and saved!"
    }

# Endpoint 2: Student ka query lena aur Gemini AI se padhana
@app.post("/ask_teacher")
async def ask_teacher(student_query: str = Form(...), level: str = Form("Beginner"), time: str = Form("5 mins")):
    
    # 1. Gemini Pro 1.5 API call (llm_engine.py se aayega)
    ai_generated_text = generate_ai_lesson(student_query, level, time)
    
    # 2. Dummy Video URL (Jab tak video API nahi lagti)
    dummy_video_url = "https://www.w3schools.com/html/mov_bbb.mp4" 
    
    return {
        "status": "success", 
        "text_response": ai_generated_text, 
        "video_url": dummy_video_url
    }