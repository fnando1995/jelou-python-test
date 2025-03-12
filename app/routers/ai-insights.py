from fastapi import APIRouter, HTTPException, Depends
from app.models import AIInsightsResponse
from app.services.ai import get_ai_insights
from app.dependencies import verify_token

router = APIRouter()

@router.get("/{company_id}/ai-insights", response_model=AIInsightsResponse)
async def get_ai_insights_endpoint(company_id: str, token: dict = Depends(verify_token)):
    try:
        insights = get_ai_insights(company_id)
        return insights
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
