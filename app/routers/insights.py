from fastapi import APIRouter, HTTPException, Depends
from models import InsightsResponse
from services.metrics import compute_insights
from routers.auth import oauth2_scheme

router = APIRouter()

@router.get("/{company_id}/insights", response_model=InsightsResponse)
async def get_insights(company_id: str, payload: dict = Depends(oauth2_scheme)):
# async def get_insights(company_id: str):
    try:
        insights = compute_insights(company_id)
        return insights
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
