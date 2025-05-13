import streamlit as st
import plotly.express as px
from modules.load_data import load_data

st.title("📊 지점별 월별 기후 변화")

df_weather, _ = load_data()

df_weather['연월'] = df_weather['일시'].dt.to_period('M').astype(str)
selected_sites = st.multiselect('지점을 선택하세요', df_weather['지점명'].unique(), default=df_weather['지점명'].unique())

df_selected = df_weather[df_weather['지점명'].isin(selected_sites)]
df_monthly = df_selected.groupby(['연월', '지점명'])[['평균기온(°C)', '평균상대습도(%)', '일강수량(mm)']].mean().reset_index()

for col, title in [('평균기온(°C)', '월별 평균기온'), ('평균상대습도(%)', '월별 평균습도'), ('일강수량(mm)', '월별 강수량')]:
    fig = px.line(df_monthly, x='연월', y=col, color='지점명', markers=True, title=title)
    st.plotly_chart(fig, use_container_width=True)
