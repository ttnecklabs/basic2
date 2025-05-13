# pages/3_이상기후_경고판.py
import streamlit as st
import plotly.express as px
from modules.load_data import load_weather_data

st.subheader("⚠️ 이상기후 경고판 (무강수, 고온, 강풍)")

# 데이터 로딩
df = load_weather_data()

# 지점 선택 필터
selected_sites = st.multiselect('지점을 선택하세요', df['지점명'].unique(), default=df['지점명'].unique())

df_filtered = df[df['지점명'].isin(selected_sites)]

# 이상기후 기준 컬럼 생성
df_filtered['무강수'] = (df_filtered['일강수량(mm)'] == 0).astype(int)
df_filtered['고온경고'] = (df_filtered['평균기온(°C)'] >= 30).astype(int)
df_filtered['강풍경고'] = (df_filtered['평균 풍속(m/s)'] >= 14).astype(int)

# 연속 무강수 일수 계산
df_filtered['연속무강수'] = df_filtered.groupby('지점명')['무강수'].apply(
    lambda x: x * (x.groupby((x != x.shift()).cumsum()).cumcount() + 1)
)

# 경고 요약 데이터
df_alerts = df_filtered.groupby(['연월', '지점명']).agg({
    '연속무강수': 'max',
    '고온경고': 'sum',
    '강풍경고': 'sum'
}).reset_index()

# 무강수 5일 이상 경고
df_alerts['무강수경고'] = (df_alerts['연속무강수'] >= 5).astype(int)

# 시각화 1: 무강수 경고 (막대그래프)
fig_dry = px.bar(df_alerts, x='연월', y='무강수경고', color='지점명', title='월별 무강수 경고 (5일 이상)')
st.plotly_chart(fig_dry, use_container_width=True)

# 시각화 2: 고온 경고일 수
fig_hot = px.line(df_alerts, x='연월', y='고온경고', color='지점명', markers=True, title='월별 고온경고 발생일 수')
st.plotly_chart(fig_hot, use_container_width=True)

# 시각화 3: 강풍 경고일 수
fig_wind = px.line(df_alerts, x='연월', y='강풍경고', color='지점명', markers=True, title='월별 강풍경고 발생일 수')
st.plotly_chart(fig_wind, use_container_width=True)
