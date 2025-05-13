import pandas as pd
import sqlite3

@st.cache_data
def load_weather_data():
    conn = sqlite3.connect('data/asos_weather.db')
    df_weather = pd.read_sql("SELECT * FROM asos_weather", conn)
    df_sunshine = pd.read_sql("SELECT * FROM sunshine_data", conn)
    conn.close()

    df_weather['일시'] = pd.to_datetime(df_weather['일시'])
    df_sunshine['일시'] = pd.to_datetime(df_sunshine['일시'])

    df_merge = pd.merge(df_weather, df_sunshine, on=['지점명', '일시'], how='left')
    df_merge['연월'] = df_merge['일시'].dt.to_period('M').astype(str)
    return df_merge
