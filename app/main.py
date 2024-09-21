from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.ocr import extract_text
from app.table_extraction import extract_table_data

app = FastAPI()

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    if not file.filename.endswith(('.png', '.jpg', '.jpeg', '.pdf')):
        raise HTTPException(status_code=400, detail="Invalid file type.")
    
    contents = await file.read()

    # Check if the uploaded file is an image or a PDF
    if file.filename.endswith('.pdf'):
        file_type = 'pdf'
    else:
        file_type = 'image'

    # Extract text and table data
    try:
        text = extract_text(contents, file_type)
        tables = extract_table_data(contents, file_type)
        return JSONResponse(content={"extracted_text": text, "tables": tables})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during OCR: {str(e)}")

