import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_bytes

def detect_tables(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Use adaptive thresholding to get a binary image
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    table_data = []

    # Iterate through the contours to find and extract tables
    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter out small contours to avoid noise
        if w < 50 or h < 50:
            continue
        
        # Extract the table area from the original image
        table_image = image[y:y+h, x:x+w]
        
        # Use pytesseract to extract text from the table area
        data = pytesseract.image_to_string(table_image, config='--psm 6')
        table_data.append(data)

    return table_data

def extract_table_data(file_contents, file_type):
    if file_type == 'pdf':
        images = convert_from_bytes(file_contents)
        all_tables = []
        for image in images:
            # Convert the PIL image to OpenCV format
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            tables = detect_tables(image_cv)
            all_tables.extend(tables)
        return all_tables

    # For image files
    nparr = np.frombuffer(file_contents, np.uint8)
    image_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    tables = detect_tables(image_cv)
    
    return tables
