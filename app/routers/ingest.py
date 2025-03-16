from fastapi import APIRouter, HTTPException, UploadFile, File,Depends
from logger import get_logger
from database import save_data
import pandas as pd
import io

router = APIRouter()

@router.post("/")
async def ingest_data(file: UploadFile = File(...),logger = Depends(get_logger)):
    """Ingest data from a CSV file. Repeat info will be replaced."""
    try:
        contents = await file.read()
        # Read CSV from the uploaded file
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")), parse_dates=["created_at"])
        # save data using load data form database
        save_data(df)
        return {"message": "Data ingested successfully", "rows": len(df)}
    except Exception as e:
        logger.error(f"Exception at ingest_data: {e}")
        raise HTTPException(status_code=400, detail=f"Exception at ingest_data: {e}")
