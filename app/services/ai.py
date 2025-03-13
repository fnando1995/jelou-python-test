from database import load_all
from models import AIInsightsResponse, AIInsight
import pandas as pd
from collections import Counter
import random
from transformers import pipeline
from collections import Counter
import re

# Initialize Hugging Face pipelines
topic_model = pipeline("zero-shot-classification")
sentiment_model = pipeline("sentiment-analysis")

# Define potential issues to classify (you can expand this list as needed)
possible_labels = [
    "customer service", "delivery", "price", "product quality", "user experience",
    "website issues", "payment issues", "returns", "support", "features"
]


# Define a function to clean the text (remove special characters, URLs, etc.)
def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)     # Remove mentions
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    return text


def analyze_tweets(tweets):
    if not tweets:
        return []

    # Clean the tweets
    cleaned_tweets = [clean_text(tweet) for tweet in tweets]

    issues = []
    for tweet in cleaned_tweets:
        # Use zero-shot classification to classify the topic of the tweet
        
        result = topic_model(tweet, candidate_labels=possible_labels)
        top_issue = result['labels'][0]  # Top label (issue)
        # top_issue = random.choice(possible_labels)
        issues.append(top_issue)

    # Count the frequency of each issue
    issue_counts = Counter(issues)

    # Calculate percentages
    total_tweets = len(tweets)
    issue_metrics = []
    for issue, count in issue_counts.items():
        percentage = (count / total_tweets) * 100
        issue_metrics.append({
            "issue": issue,
            "percentage": round(percentage, 2)
        })

    # Sort by percentage in descending order and limit to top 5 (or less)
    issue_metrics = sorted(issue_metrics, key=lambda x: x['percentage'], reverse=True)
    top_n = 5
    top_issues = issue_metrics[:top_n]

    # Add sentiment summary for each issue
    for issue_info in top_issues:
        # Filter tweets for this issue
        issue_tweets = [tweet for tweet, issue in zip(tweets, issues) if issue == issue_info['issue']]
        # sentiments = [ {'label':i} for i in random.choices(['POSITIVE', 'NEGATIVE'],k=len(issue_tweets))]
        sentiments = [sentiment_model(tweet)[0] for tweet in issue_tweets]
        positive = sum(1 for sentiment in sentiments if sentiment['label'] == 'POSITIVE')
        negative = sum(1 for sentiment in sentiments if sentiment['label'] == 'NEGATIVE')

        issue_info["sentiment"] = 'positive' if positive > negative else "negative"


    top_issues = [ AIInsight(issue=issue_info["issue"],
                                percentage=issue_info["percentage"],
                                sentiment=issue_info["sentiment"]
                                ) for issue_info in top_issues]
    return top_issues


def get_ai_insights(company_id: str) -> AIInsightsResponse:
    tweet_df = load_all()

    if tweet_df.empty:
        raise Exception("No company id found")
    
    tweet_df = tweet_df[tweet_df["author_id"] == company_id]
    
    if tweet_df.empty:
        return AIInsightsResponse(
                                total_inbound=0,
                                total_outbound=0,
                                response_rate=0,
                                conversation_ratio=0,
                                average_response_time=0
                            )

    
    # Filter customer Tweets
    customer_tweets = tweet_df[tweet_df["inbound"] == True]
    texts = customer_tweets["text"].tolist()
    
    insights = analyze_tweets(texts)
        
    return AIInsightsResponse(insights=insights)
