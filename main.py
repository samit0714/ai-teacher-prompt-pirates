from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os

from llm_engine import generate_adaptive_lesson
from video_engine import generate_avatar_video # Naya import

app = FastAPI(title="AI Teacher Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "success", "message": "Prompt Pirates AI Backend is Live!"}

@app.post("/upload_material")
async def upload_material(file: UploadFile = File(...)):
    upload_dir = "temp_uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_location = f"{upload_dir}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"status": "success", "filename": file.filename, "message": "File successfully uploaded!"}

@app.post("/ask_teacher")
async def ask_teacher(student_query: str = Form(...), level: str = Form("Beginner"), time: str = Form("5 mins")):
    
    # 1. Text Generation (Gemini)
    ai_generated_text = generate_adaptive_lesson(student_query, level, time)
    
    # 2. Video Generation (D-ID) ke liye short script (Taaki fast chale)
    short_video_script = f"Hello! Welcome to your class on {student_query}. Let's dive in!"
    
    real_video_url = generate_avatar_video(short_video_script)
    
    # Fallback agar D-ID API limit khatam ho jaye
    if not real_video_url:
        real_video_url = "https://www.w3schools.com/html/mov_bbb.mp4"
    
    return {
        "status": "success", 
        "text_response": ai_generated_text, 
        "video_url": real_video_url
    }