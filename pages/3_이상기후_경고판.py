import streamlit as st
import pandas as pd
from modules.load_data import load_data

st.title("🌪️ 이상기후 경고판")

df_weather, _ = load_data()

df_weather['연속무강수'] = df_weather['평균상대습도(%)'].rolling(5).apply(lambda x: (x == 0).sum())
df_weather['고온경고'] = df_weather['평균기온(°C)'] >= 30
df_weather['강풍경고'] = df_weather['평균 풍속(m/s)'] >= 14

alerts_df = df_weather[(df_weather['연속무강수'] >= 5) | (df_weather['고온경고']) | (df_weather['강풍경고'])]
st.dataframe(alerts_df[['일시', '지점명', '평균기온(°C)', '평균 풍속(m/s)', '연속무강수', '고온경고', '강풍경고']])
