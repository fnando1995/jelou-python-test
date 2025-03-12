from fastapi import APIRouter, HTTPException, UploadFile, File
from database import load_data
import pandas as pd
import io

router = APIRouter()

@router.post("/")
async def ingest_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        # Read CSV from the uploaded file
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")), parse_dates=["created_at"])
        # save data using load data form database
        load_data(df)
        return {"message": "Data ingested successfully", "rows": len(df)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
