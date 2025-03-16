from database import load_all
from models import AIInsightsResponse, AIInsight
import pandas as pd
from collections import Counter
import random
from transformers import pipeline
from collections import Counter
import re
from services.utils import filter_tweets_by_company

# Initialize Hugging Face pipelines

# Model to easily classify the topic of a tweet in a zero-shot manner for a given set of issue's labels.
topic_model = pipeline("zero-shot-classification")

# Model to classify the sentiment of the tweet's text.
sentiment_model = pipeline("sentiment-analysis")

# Top 5 issues to classify tweets
top_n = 5

# Define potential issues to classify tweets
possible_labels = [
    "customer service", "delivery", "price", "product quality", "user experience",
    "website issues", "payment issues", "returns", "support", "features"
]


def return_empty()-> AIInsightsResponse:
    return AIInsightsResponse(insights=[])

def clean_text(text) -> str:
    """function to clean the text (remove special characters, URLs, etc.)"""
    text = re.sub(r'http\S+', '', text)         # Remove URLs
    text = re.sub(r'@\w+', '', text)            # Remove mentions
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    text = text.lower()                         # Convert to lowercase
    return text


def analyze_tweets(tweets) -> list[AIInsight]:
    """Analyze a list of tweets and return the top issues and the general sentiment"""
    if not tweets:
        return []

    # Clean the tweets
    cleaned_tweets = [clean_text(tweet) for tweet in tweets]

    # Classify tweets in a issue topic
    issues = []
    for tweet in cleaned_tweets:
        # zero-shot classification
        result = topic_model(tweet, candidate_labels=possible_labels)
        top_issue = result['labels'][0]  # Top label (issue)
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


def compute_ai_insights(company_id: str) -> AIInsightsResponse:
    """Compute AI insights for a company based on the dataset."""
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

    company_tweet_df, [in_response_df, responded_df],  = tweets_data

    # concatenate customer tweets and get text from tweets
    customer_tweets = pd.concat([in_response_df, responded_df])
    texts = customer_tweets["text"].tolist()
    
    # Analyze
    insights = analyze_tweets(texts)
        
    return AIInsightsResponse(insights=insights)
