import pandas as pd

# Global variable to hold tweet data
tweet_df = pd.DataFrame()

def load_data(csv_path: str):
    global tweet_df
    tweet_df = pd.read_csv(csv_path, parse_dates=["created_at"])
    return tweet_df
