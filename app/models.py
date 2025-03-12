from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Tweet(BaseModel):
    tweet_id: str
    author_id: str
    inbound: bool
    created_at: datetime
    text: str
    response_tweet_id: Optional[str] = None
    in_response_to_tweet_id: Optional[str] = None

class InsightsResponse(BaseModel):
    total_inbound: int
    total_outbound: int
    response_rate: float
    conversation_ratio: float
    average_response_time: Optional[float] = None

class AIInsight(BaseModel):
    issue: str
    percentage: float
    sentiment: Optional[str] = None

class AIInsightsResponse(BaseModel):
    insights: List[AIInsight]

class CreateUserRequest(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str