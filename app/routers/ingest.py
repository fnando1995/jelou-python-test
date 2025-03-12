from fastapi import APIRouter, HTTPException, UploadFile, File
from app.database import load_data
import pandas as pd
import io

router = APIRouter()

@router.post("/")
async def ingest_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        # Read CSV from the uploaded file
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")), parse_dates=["created_at"])
        # For simplicity, assign the DataFrame to the global variable in the database module.
        from app.database import tweet_df
        tweet_df.drop(tweet_df.index, inplace=True)
        tweet_df = df.copy()
        return {"message": "Data ingested successfully", "rows": len(df)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
