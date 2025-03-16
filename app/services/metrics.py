from models import InsightsResponse
from services.utils import *
from database import load_all


def return_empty():
    return InsightsResponse(
                                total_inbound=0,
                                total_outbound=0,
                                response_rate=0,
                                conversation_ratio=0,
                                average_response_time=0
                            )

def compute_insights(company_id: str) -> InsightsResponse:
    """Compute insights for a company based on the dataset."""

    # Load all tweets
    tweet_df = load_all()

    # Check if dataset is loaded
    if tweet_df.empty:
        return return_empty()

    # get tweets data filtered as mentioned in the function
    tweets_data = filter_tweets_by_company(tweet_df,company_id)
    
    # if no tweets data, return empty insights
    if not tweets_data:
        return return_empty()
    
    company_tweet_df, [in_response_df, responded_df]  = tweets_data

    # print(company_tweet_df, [in_response_df, responded_df])

    customer_tweets = pd.concat([in_response_df, responded_df])

    # Calculate total inbound and outbound tweets
    total_inbound = len(customer_tweets)
    total_outbound = len(company_tweet_df)
    
    # Calculate response rate: The percentage of inbound tweets that received at least one response (not mentioned to be response from company, just responded or response_tweet_id not null).
    responded = customer_tweets[customer_tweets["response_tweet_id"].notna()]
    response_rate = (len(responded) / total_inbound) * 100 if total_inbound > 0 else 0

    # Calculate conversation ratio: ratio of company responses to customer inquiries (tweets from company in response to tweets from customers)
    conversation_ratio = (len(in_response_df) / total_outbound) if total_outbound > 0 else 0

    # Average response time (if applicable)
    response_times = []
    for row_tweet, data_tweet in company_tweet_df.iterrows():
        if pd.notna(data_tweet["in_response_to_tweet_id"]):
            customer_tw = tweet_df[tweet_df["tweet_id"]==data_tweet["in_response_to_tweet_id"]]
            if not customer_tw.empty:
                customer_dt = datetime.fromisoformat(customer_tw.iloc[0]["created_at"])
                company_dt = datetime.fromisoformat(data_tweet["created_at"])

                diff = (company_dt - customer_dt).total_seconds()
                response_times.append(diff)

    average_response_time = sum(response_times) / len(response_times) if response_times else None

    insights = InsightsResponse(
                                total_inbound=total_inbound,
                                total_outbound=total_outbound,
                                response_rate=response_rate,
                                conversation_ratio=conversation_ratio,
                                average_response_time=average_response_time
                            )
    return insights
