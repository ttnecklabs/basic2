import streamlit as st
import pandas as pd
from modules.load_data import load_data

st.title("🌪️ 이상기후 경고판")

# 데이터 로딩
df_weather, _ = load_data()

# 컬럼명 자동 매핑 (풍속)
wind_col_candidates = [col for col in df_weather.columns if '풍속' in col]
humid_col_candidates = [col for col in df_weather.columns if '습도' in col]

# 평균 풍속 컬럼명 찾기
if wind_col_candidates:
    wind_col = wind_col_candidates[0]
else:
    st.error("❗ 풍속 관련 컬럼이 없습니다.")
    wind_col = None

# 평균 상대습도 컬럼명 찾기
if humid_col_candidates:
    humid_col = humid_col_candidates[0]
else:
    st.error("❗ 습도 관련 컬럼이 없습니다.")
    humid_col = None

# 무강수 → 습도 0 기준 (없으면 skip)
if humid_col:
    df_weather['연속무강수'] = (df_weather[humid_col] == 0).astype(int).rolling(5).sum()
else:
    df_weather['연속무강수'] = 0

# 고온 경고
df_weather['고온경고'] = df_weather['평균기온(°C)'] >= 30

# 강풍 경고 (컬럼 없으면 False 처리)
if wind_col:
    df_weather['강풍경고'] = df_weather[wind_col] >= 14
else:
    df_weather['강풍경고'] = False

# 이상기후 경고 데이터 필터링
alerts_df = df_weather[
    (df_weather['연속무강수'] >= 5) |
    (df_weather['고온경고']) |
    (df_weather['강풍경고'])
]

# 결과 출력
st.dataframe(alerts_df[['일시', '지점명', '평균기온(°C)',
                        wind_col if wind_col else '지점명',  # wind_col 없으면 지점명 자리채움
                        '연속무강수', '고온경고', '강풍경고']])
