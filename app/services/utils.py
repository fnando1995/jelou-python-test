from typing import List, Optional
from datetime import datetime
import pandas as pd

def filter_tweets_by_company(tweet_df, company_id)-> Optional[List[pd.DataFrame]]:
    """Compute insights for a company based on the dataset."""
        
    # get the tweets of the company and filter to be outbound (company)
    company_tweet_df = tweet_df[(tweet_df["author_id"] == company_id) & (tweet_df["inbound"] == False)]
    
    # check for no tweets and return empty insights
    if company_tweet_df.empty:
        return None

    # Customers tweets: Will be obtained from response_tweet_id and in_response_to_tweet_id, filtering inbound tweets (customer tweets)
    response_tweet_ids = list(company_tweet_df[~company_tweet_df["response_tweet_id"].isna()]["response_tweet_id"])
    response_tweet_ids = list(set([int(float(id_)) for item in response_tweet_ids for id_ in str(item).split(",")])) # extend and remove duplicates
    in_response_to_tweet_ids = list(company_tweet_df[~company_tweet_df["in_response_to_tweet_id"].isna()]["in_response_to_tweet_id"])
    in_response_to_tweet_ids = list(set([int(float(id_)) for item in in_response_to_tweet_ids for id_ in str(item).split(",")])) # extend and remove duplicates (not seen in dataset but still)
    customer_tweets_response_tweet_ids = tweet_df[(tweet_df["inbound"] == True) & (tweet_df["tweet_id"].isin(response_tweet_ids))]
    customer_tweets_in_response_to_tweet_ids = tweet_df[(tweet_df["inbound"] == True) & (tweet_df["tweet_id"].isin(in_response_to_tweet_ids))]
    
    return [company_tweet_df, [customer_tweets_in_response_to_tweet_ids,customer_tweets_response_tweet_ids]]