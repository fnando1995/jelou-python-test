from fastapi import APIRouter, HTTPException, Depends
from models import AIInsightsResponse, User
from services.ai import compute_ai_insights
from routers.auth import oauth2_scheme
from routers.auth import get_current_user
from logger import get_logger

router = APIRouter()

@router.get("/{company_id}/ai-insights", response_model=AIInsightsResponse)
async def get_ai_insights(company_id: str,current_user: User = Depends(get_current_user),logger = Depends(get_logger)):
    """Get AI insights for a company."""
    try:
        insights = compute_ai_insights(company_id)
        return insights
    except Exception as e:
        logger.error(f"Exception at get_ai_insights: {e}")
        raise HTTPException(status_code=400, detail=str(e))
