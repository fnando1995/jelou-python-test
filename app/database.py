import os
import sqlite3
import pandas as pd

# Database file location
DB_DIR = "dbs"
os.makedirs(DB_DIR, exist_ok=True)

DB_FILE = os.path.join(DB_DIR,"database.db")

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def save_data(data: pd.DataFrame):
    """Load data from CSV into SQLite database."""
    conn = get_db_connection()
    data.to_sql("tweets", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    return len(data)

def load_all():
    conn = get_db_connection()
    sql = "select * from tweets"
    data = pd.read_sql(sql,conn)
    conn.close()
    return data

def save_user(data: dict):
    conn = get_db_connection()
    data = pd.DataFrame.from_dict(data)
    data.to_sql("users", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()

def load_user(data: dict):
    conn = get_db_connection()
    sql = "select * from users where username = :username"
    data = pd.read_sql(sql,conn,params=data)
    conn.close()
    data = data.to_dict('records')
    print(data)
    return None if len(data)==0 else data[0]

    