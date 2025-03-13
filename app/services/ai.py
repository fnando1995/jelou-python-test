from database import load_all
from models import AIInsightsResponse, AIInsight
import pandas as pd
from collections import Counter
import random

def get_ai_insights(company_id: str) -> AIInsightsResponse:
    tweet_df = load_all()
    if tweet_df.empty:
        raise Exception("Dataset not loaded")
    
    # For simplicity, filter all customer tweets (inbound == True)
    customer_tweets = tweet_df[tweet_df["inbound"] == True]
    texts = customer_tweets["text"].tolist()
    
    # Simulate an AI model extracting keywords by counting word frequencies
    all_words = " ".join(texts).split()
    word_counts = Counter(all_words)
    # Exclude a small set of common stopwords
    stopwords = {"the", "and", "is", "to", "of", "a", "in", "for", "it", "on"}
    filtered = {word.lower(): count for word, count in word_counts.items() if word.lower() not in stopwords}
    top_words = sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:5]

    total_count = sum(filtered.values())
    insights = []
    for word, count in top_words:
        percentage = (count / total_count) * 100 if total_count > 0 else 0
        # Simulate sentiment analysis (here, randomly assigned)
        sentiment = random.choice(["positive", "negative", "neutral"])
        insights.append(AIInsight(issue=word, percentage=percentage, sentiment=sentiment))
    
    return AIInsightsResponse(insights=insights)
