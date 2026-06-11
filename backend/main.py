import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from modules.extraction import route_and_extract

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return{"message": "Hello World! The backend is running."}

async def process_single_file(file: UploadFile):
    file_location = f"{TEMP_DIR}/{file.filename}"

    with open(file_location,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        print(f"\n--- Processing File: {file.filename} ---")
        extraction_result = await asyncio.to_thread(route_and_extract, file_location)

        return {"filename": file.filename,
                "result": extraction_result}

    finally:
        if os.path.exists(file_location):
            os.remove(file_location)
            print(f"Deleted temporary file: {file_location}")


@app.post("/upload-papers/")
async def upload_papers(files: list[UploadFile] = File(...)):

    print(f"Processing {len(files)} files...")
    tasks = [process_single_file(file) for file in files]
    result = await asyncio.gather(*tasks)

    errors = [item for item in result if item.get("result", {}).get("status") == "error"]
    if errors:
        error = errors[0]
        detail = error.get("result", {}).get("message", "Unsupported file type")
        raise HTTPException(status_code=400, detail=f"{error.get('filename')}: {detail}")

    return {"message": "Files successfully uploaded and processed.", "data": result}