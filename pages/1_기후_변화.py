import streamlit as st
import plotly.express as px
from modules.load_data import load_weather_data

st.subheader("📊 월별 기후 변화 (온도 / 강수량 / 습도)")

# 데이터 로딩
df = load_weather_data()

# 지점 선택 필터
selected_sites = st.multiselect('지점을 선택하세요', df['지점명'].unique(), default=df['지점명'].unique())
df_filtered = df[df['지점명'].isin(selected_sites)]

# 월별 집계
df_monthly = df_filtered.groupby(['연월', '지점명']).agg({
    '평균기온(°C)': 'mean',
    '일강수량(mm)': 'mean',
    '평균 상대습도(%)': 'mean'
}).reset_index()

# 시각화 1: 평균기온
fig_temp = px.line(df_monthly, x='연월', y='평균기온(°C)', color='지점명', markers=True, title='월별 평균기온')
st.plotly_chart(fig_temp, use_container_width=True)

# 시각화 2: 강수량
fig_rain = px.line(df_monthly, x='연월', y='일강수량(mm)', color='지점명', markers=True, title='월별 평균 강수량')
st.plotly_chart(fig_rain, use_container_width=True)

# 시각화 3: 상대습도
fig_humid = px.line(df_monthly, x='연월', y='평균 상대습도(%)', color='지점명', markers=True, title='월별 평균 상대습도')
st.plotly_chart(fig_humid, use_container_width=True)
