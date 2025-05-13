import sqlite3
import pandas as pd

def load_asos_data(db_path):
    conn = sqlite3.connect(db_path)
    df_weather = pd.read_sql("SELECT * FROM asos_weather", conn)
    df_sunshine = pd.read_sql("SELECT * FROM sunshine_data", conn)
    conn.close()
    return df_weather, df_sunshine
