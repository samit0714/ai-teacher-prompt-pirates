import os
import shutil
import pdfplumber
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings 

load_dotenv()

DB_DIR = "./chroma_db"


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path: str) -> str:
    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                
                text = page.extract_text(x_tolerance=2, y_tolerance=2)
                if text:
                    extracted_text += f"\n--- [Page {page_num + 1}] ---\n" + text
    except Exception as e:
        print(f"PDF Extract Error: {e}")
        
    return extracted_text

def process_and_store_document(file_path: str, collection_name: str = "course_material") -> int:
    raw_text = extract_text_from_pdf(file_path)
    
    if not raw_text.strip():
        raise ValueError("Failed to extract text. The PDF might be an image-based scan.")

    
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)
    os.makedirs(DB_DIR, exist_ok=True)

   
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = text_splitter.split_text(raw_text)
    docs = [Document(page_content=chunk, metadata={"source": os.path.basename(file_path)}) for chunk in chunks]

    
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=DB_DIR
    )
    
    return len(docs)

def get_relevant_context(query: str, collection_name: str = "course_material", top_k: int = 4) -> str:
    
    if not os.path.exists(DB_DIR) or not os.listdir(DB_DIR):
        return ""

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    
    
    results = vector_store.similarity_search(query, k=top_k)
    
    if not results:
        return ""
        
    context = "\n\n---\n\n".join([doc.page_content for doc in results])
    return context