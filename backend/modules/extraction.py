import os
import fitz

from pdf2image import convert_from_path
import cv2
import pytesseract
import numpy as np

import re

def process_pdf_pipeline(file_path):
    # Subrouter: detects if a PDF is text-based or scanned and proceses accordingly
    print(f"Checking PDF type for: {file_path}")

    try:
        # Open PDF
        doc = fitz.open(file_path)
        first_page = doc.load_page(0)
        text_check = first_page.get_text().strip()
        doc.close()

        # If text is found, it is a Text PDF
        if len(text_check) > 0:
            print("Detected text based PDF...")
            print(f"Routing to PDF Pipeline: {file_path}")

            raw_text = ""
        
            doc = fitz.open(file_path)

            for page_num in range(len(doc)):
                page = doc.load(page_num)
                raw_text += page.get_text() + '\n'
            
            print(raw_text)
            doc.close()
            return raw_text
        
        # If no text is found, it is a scanned PDF. Route it to process_scanned_pdf_pipeline()
        else:
            print("Detected scanned PDF...")
            return process_scanned_pdf_pipeline(file_path)
    
    except Exception as e:
        print(f"Error checking PDF: {e}")
        return ""
    


def process_scanned_pdf_pipeline(file_path):
    #Converts scanned PDFs to images, preprocesses them and runs OCR
    print(f"Routing to Scanned PDF Pipeline: {file_path}")
    raw_text = ""

    try:
        # Convert PDF to list of images
        pages = convert_from_path(file_path, dpi = 300)

        for page in pages:
            # Convert image to OpenCV friendly format
            open_cv_image = np.array(page)

            # Preprocessing using OpenCV
            image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, preprocessed_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Pytesseract OCR
            extracted_text = pytesseract.image_to_string(preprocessed_image)
            raw_text += extracted_text + '\n'
        
        return raw_text
    except Exception as e:
        print(f"Error processing scanned PDF: {e}")
        return ""



def process_image_pipeline(file_path):
    # Preprocesses the image first and then runs OCR
    print(f"Routing to Image Pipeline: {file_path}")
    raw_text = ""
    
    try:
        # Load image from temporary path
        image = cv2.imread(file_path)

        image = cv2.resize(image, None, fx = 2, fy = 2, interpolation=cv2.INTER_CUBIC) # LARGER IMAGE

        # Preprocessing using OpenCV
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # GRAYSCALE
        blur = cv2.GaussianBlur(gray_image,(5, 5), 0) # BLUR TO SMOOTHEN THE NOISE
        preprocessed_image = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 13) 

        # Pytesseract OCR
        extracted_text = pytesseract.image_to_string(preprocessed_image)
        raw_text += extracted_text + '\n'
        
        return raw_text

    except Exception as e:
        print(f"Error processing image: {e}")
        return ""



# --- The Smart Router ---

def route_and_extract(file_path):
    """
    Automatically detects the file type and routes it.
    Maintains paper-wise separation by catching errors.
    """
    _, extension = os.path.splitext(file_path.lower())
    raw_text = ""
    
    try:
        # Identify file type using extension
        if extension == '.pdf':
            raw_text = process_pdf_pipeline(file_path)
        elif extension in ['.jpg', '.jpeg', '.png']:
            raw_text = process_image_pipeline(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
            
        # Both pipelines produce raw extracted text
        
        return {"status": "success", "text": raw_text}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}