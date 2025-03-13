from database import load_all
from models import InsightsResponse
import pandas as pd

def compute_insights(company_id: str) -> InsightsResponse:
    tweet_df = load_all()
    if tweet_df.empty:
        raise Exception("Dataset not loaded")
    tweet_df = tweet_df[tweet_df["author_id"] == company_id]
    
    if tweet_df.empty:
        return InsightsResponse(
                                total_inbound=0,
                                total_outbound=0,
                                response_rate=0,
                                conversation_ratio=0,
                                average_response_time=0
                            )

    # Identify customer tweets (inbound == True)
    customer_tweets = tweet_df[tweet_df["inbound"] == True]
    # Identify company responses (assuming company tweets have inbound == False and matching author_id)
    company_tweets = tweet_df[(tweet_df["inbound"] == False)]
    
    total_inbound = len(customer_tweets)
    total_outbound = len(company_tweets)
    
    # Calculate response rate: percentage of customer tweets that received at least one response
    responded = customer_tweets[customer_tweets["response_tweet_id"].notna()]
    response_rate = (len(responded) / total_inbound) * 100 if total_inbound > 0 else 0

    # Average response time (if applicable)
    response_times = []
    for _, tweet in customer_tweets.iterrows():
        if pd.notna(tweet["response_tweet_id"]):
            company_response = tweet_df[tweet_df["tweet_id"] == tweet["response_tweet_id"]]
            if not company_response.empty:
                diff = (company_response.iloc[0]["created_at"] - tweet["created_at"]).total_seconds()
                response_times.append(diff)

    # Conversation ratio: ratio of company responses to customer inquiries
    conversation_ratio = (len(response_times) / total_inbound) if total_inbound > 0 else 0
                
    average_response_time = sum(response_times) / len(response_times) if response_times else None

    insights = InsightsResponse(
        total_inbound=total_inbound,
        total_outbound=total_outbound,
        response_rate=response_rate,
        conversation_ratio=conversation_ratio,
        average_response_time=average_response_time
    )
    return insights
