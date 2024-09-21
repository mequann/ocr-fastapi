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
    text = extract_text(contents)
    tables = extract_table_data(contents)

    return JSONResponse(content={"extracted_text": text, "tables": tables})
