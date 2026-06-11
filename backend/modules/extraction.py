import os


def process_pdf_pipeline(file_path):
    # TODO: Process page by page and run OCR for scanned PDFs, or extract text for text PDFs
    print(f"Routing to PDF Pipeline: {file_path}")
    return "raw_text_from_pdf"

def process_image_pipeline(file_path):
    # TODO: Preprocess the image first before running OCR
    print(f"Routing to Image Pipeline: {file_path}")
    return "raw_text_from_image"

def clean_extracted_text(raw_text):
    # TODO: Clean OCR noise like extra spaces, weird characters, and broken line breaks
    print("Cleaning raw text...")
    return "cleaned_text"

# --- The Smart Router ---

def route_and_extract(file_path):
    """
    Automatically detects the file type and routes it.
    Maintains paper-wise separation by catching errors.
    """
    _, extension = os.path.splitext(file_path.lower())
    raw_text = ""
    
    try:
        if extension == '.pdf':
            raw_text = process_pdf_pipeline(file_path)
        elif extension in ['.jpg', '.jpeg', '.png']:
            raw_text = process_image_pipeline(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
            
        # Both pipelines produce raw extracted text, which is then cleaned
        final_text = clean_extracted_text(raw_text)
        
        return {"status": "success", "text": final_text}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}