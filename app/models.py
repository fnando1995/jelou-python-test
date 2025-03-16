from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Define the data model for Tweet
class Tweet(BaseModel):
    tweet_id: str
    author_id: str
    inbound: bool
    created_at: datetime
    text: str
    response_tweet_id: Optional[str] = None
    in_response_to_tweet_id: Optional[str] = None

# Define the data model for the Normal Insights endpoint
class InsightsResponse(BaseModel):
    total_inbound: int
    total_outbound: int
    response_rate: float
    conversation_ratio: float
    average_response_time: Optional[float] = None

# Define the data model for the AI Insights of each Tweet
class AIInsight(BaseModel):
    issue: str
    percentage: float
    sentiment:str = None

# Define the data model for the AI Insights endpoint (list of AIInsight)
class AIInsightsResponse(BaseModel):
    insights: List[AIInsight]

# Define the data model for the User when registering
class CreateUserRequest(BaseModel):
    username: str
    password: str
    
# Define the data model for the OAuth2PasswordRequestForm
class Token(BaseModel):
    access_token: str
    token_type: str 

# Define the data model for the User when logging in
class User(BaseModel):
    username: str
    hashed_password: str