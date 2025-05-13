# pages/2_일조_일사.py
import streamlit as st
import plotly.express as px
from modules.load_data import load_weather_data

st.subheader("☀️ 월별 일조시간 & 일사량 분석")

# 데이터 로딩
df = load_weather_data()

# 지점 선택 필터
selected_sites = st.multiselect('지점을 선택하세요', df['지점명'].unique(), default=df['지점명'].unique())

df_filtered = df[df['지점명'].isin(selected_sites)]

# 월별 집계
df_monthly = df_filtered.groupby(['연월', '지점명']).agg({
    '일조시간': 'mean',
    '일사량': 'mean'
}).reset_index()

# 시각화 1: 일조시간
fig_sunshine = px.line(df_monthly, x='연월', y='일조시간', color='지점명', markers=True, title='월별 평균 일조시간')
st.plotly_chart(fig_sunshine, use_container_width=True)

# 시각화 2: 일사량
fig_solar = px.line(df_monthly, x='연월', y='일사량', color='지점명', markers=True, title='월별 평균 일사량')
st.plotly_chart(fig_solar, use_container_width=True)
