import pytesseract
from pdf2image import convert_from_bytes
import cv2
import numpy as np

def extract_text(file_contents, file_type):
    # For PDF files
    if file_type == 'pdf':
        images = convert_from_bytes(file_contents)
        extracted_text = ""
        for image in images:
            # Convert the PIL image to OpenCV format
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            extracted_text += pytesseract.image_to_string(image_cv)
        return extracted_text

    # For image files
    nparr = np.frombuffer(file_contents, np.uint8)
    image_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return pytesseract.image_to_string(image_cv)



