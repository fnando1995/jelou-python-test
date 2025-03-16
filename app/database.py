import os
import sqlite3
import pandas as pd

# Database file location
DB_DIR = os.path.join(os.path.dirname(__file__),"dbs")
os.makedirs(DB_DIR, exist_ok=True)

DB_FILE = os.path.join(DB_DIR,"database.db")

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def save_data(data: pd.DataFrame)-> int:
    """Load data from CSV into SQLite database."""
    try:
        conn = get_db_connection()
        data.to_sql("tweets", conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
        return len(data)
    except Exception as e:
        # TODO Logging
        pass
    

def load_all()-> pd.DataFrame:
    """Load all tweets from SQLite database."""
    try:
        conn = get_db_connection()
        sql = "select * from tweets"
        data = pd.read_sql(sql,conn)
        conn.close()
    except Exception as e:
        data = pd.DataFrame()
    return data

def save_user(data: dict):
    """save user data to SQLite database, user and hashed password."""
    try:
        conn = get_db_connection()
        data = pd.DataFrame.from_dict(data)
        data.to_sql("users", conn, if_exists="append", index=False)
        conn.commit()
        conn.close()
    except Exception as e:
        # TODO Logging
        pass

def load_user(data: dict)-> dict:
    """Load user data from SQLite database, user and hashed password."""
    try:
        conn = get_db_connection()
        sql = "select * from users where username = :username"
        data = pd.read_sql(sql,conn,params=data)
        conn.close()
        data = data.to_dict('records')
        return None if len(data)==0 else data[0]
    except Exception as e:
        return None

    