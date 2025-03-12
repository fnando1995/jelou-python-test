from fastapi import APIRouter, HTTPException, Depends
from app.models import InsightsResponse
from app.services.metrics import compute_insights
from app.dependencies import verify_token

router = APIRouter()

@router.get("/{company_id}/insights", response_model=InsightsResponse)
async def get_insights(company_id: str, token: dict = Depends(verify_token)):
    try:
        insights = compute_insights(company_id)
        return insights
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
