from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_uploads"

@app.get("/")
def read_root():
    return{"message": "Hello World! The backend is running."}

@app.post("/upload-papers/")
async def upload_papers(files: list[UploadFile] = File(...)):
    saved_files = []

    try:
        for file in files:
            file_location = f"{TEMP_DIR}/{file.filename}"
            with open(file_location,"wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            saved_files.append(file_location)
        
        # < processing the file here >
        print(f"Processing {len(saved_files)} files...")

        return{"message": "Files successfully uploaded and processed. ", "files": [f.filename for f in files]}
    
    finally:
        for file_path in saved_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted temporary file: {file_path}")

