import sqlite3
import pandas as pd
import os

# Database file location
DB_FILE = "dbs/database.db"

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# def initialize_database():
#     """Initialize the database with the necessary table."""
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS tweets (
#             tweet_id TEXT PRIMARY KEY,
#             author_id TEXT,
#             inbound BOOLEAN,
#             created_at TEXT,
#             text TEXT,
#             response_tweet_id TEXT,
#             in_response_to_tweet_id TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

def load_data(data: pd.DataFrame):
    """Load data from CSV into SQLite database."""
    conn = get_db_connection()
    data.to_sql("tweets", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    return len(data)

def load_user(data: dict):
    conn = get_db_connection()
    data = pd.DataFrame(data,columns = ["username","password"])
    data.to_sql("users", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()


def get_all():
    conn = get_db_connection()
    sql = "select * from tweets"
    data = pd.read_sql(sql,conn)
    conn.close()
    return data
    