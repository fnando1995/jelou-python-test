from fastapi import APIRouter, HTTPException, Depends
from models import InsightsResponse, User
from services.metrics import compute_insights
from routers.auth import get_current_user
from logger import get_logger
router = APIRouter()

@router.get("/{company_id}/insights", response_model=InsightsResponse)
async def get_insights(company_id: str, current_user: User = Depends(get_current_user),logger = Depends(get_logger)):
    """compute the insights for a company."""
    try:
        logger.info(f"Getting insights for company {company_id}")
        insights = compute_insights(company_id)
        return insights
    except Exception as e:
        logger.error(f"Exception at get insights: {e}")
        raise HTTPException(status_code=400, detail=f"Exception at get insights: {e}")