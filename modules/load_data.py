import pandas as pd
import sqlite3

@st.cache_data
def load_data():
    conn = sqlite3.connect('data/asos_weather.db')
    df_weather = pd.read_sql("SELECT * FROM asos_weather", conn)
    try:
        df_sunshine = pd.read_sql("SELECT * FROM sunshine_data", conn)
    except Exception:
        df_sunshine = pd.DataFrame()
    conn.close()

    df_weather['일시'] = pd.to_datetime(df_weather['일시'])
    if not df_sunshine.empty:
        df_sunshine['일시'] = pd.to_datetime(df_sunshine['일시'])

    return df_weather, df_sunshine
