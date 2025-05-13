import streamlit as st
import pandas as pd
from modules.load_data import load_data

st.title("🌪️ 이상기후 경고판")

# 데이터 로딩
df_weather, _ = load_data()

# 컬럼명 맞게 수정 (띄어쓰기 없는 버전 주의!)
humid_col = '평균상대습도(%)'
wind_col = '평균풍속(m/s)'

# 연속무강수 계산 (습도가 0인 날 기준)
df_weather['연속무강수'] = (df_weather[humid_col] == 0).astype(int).rolling(5).sum()

# 고온경고 (30도 이상)
df_weather['고온경고'] = df_weather['평균기온(°C)'] >= 30

# 강풍경고 (5m/s 이상)
df_weather['강풍경고'] = df_weather[wind_col] >= 5

# 경고 데이터 필터링
alerts_df = df_weather[(df_weather['연속무강수'] >= 5) | (df_weather['고온경고']) | (df_weather['강풍경고'])]

# 결과 표시
st.dataframe(alerts_df[['일시', '지점명', '평균기온(°C)', wind_col, '연속무강수', '고온경고', '강풍경고']])
