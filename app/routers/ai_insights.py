from fastapi import APIRouter, HTTPException, Depends
from models import AIInsightsResponse
from services.ai import get_ai_insights
from routers.auth import oauth2_scheme
router = APIRouter()

@router.get("/{company_id}/ai-insights", response_model=AIInsightsResponse)
# async def get_ai_insights_endpoint(company_id: str, payload: dict = Depends(oauth2_scheme)):
async def get_ai_insights_endpoint(company_id: str):
    try:
        insights = get_ai_insights(company_id)
        return insights
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))
