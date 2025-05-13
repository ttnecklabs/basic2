import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# DB 연결 및 데이터 로딩
conn = sqlite3.connect('asos_weather.db')
df_weather = pd.read_sql("SELECT * FROM asos_weather", conn)
conn.close()

# 일시 변환 & 연월 추가
df_weather['일시'] = pd.to_datetime(df_weather['일시'], errors='coerce')
df_weather['연월'] = df_weather['일시'].dt.to_period('M').astype(str)

# 지점 선택 필터
st.subheader("📊 지점별 월별 기후 변화")
selected_sites = st.multiselect(
    '지점을 선택하세요', 
    df_weather['지점명'].unique(), 
    default=df_weather['지점명'].unique()
)

df_selected = df_weather[df_weather['지점명'].isin(selected_sites)]

# 집계 컬럼
agg_cols = {
    '평균기온(°C)': '평균기온(°C)',
    '일강수량(mm)': '일강수량(mm)',
    '평균상대습도(%)': '평균상대습도(%)'
}

# 실제 존재하는 컬럼만
available_cols = {k: v for k, v in agg_cols.items() if k in df_selected.columns}

if not available_cols:
    st.error("필요한 컬럼이 없습니다. DB 컬럼명을 확인하세요.")
else:
    df_monthly = df_selected.groupby(['연월', '지점명'])[list(available_cols.keys())].mean().reset_index()

    # 평균기온
    if '평균기온(°C)' in df_monthly.columns:
        fig_temp = px.line(df_monthly, x='연월', y='평균기온(°C)', color='지점명', markers=True, title='월별 평균기온')
        st.plotly_chart(fig_temp, use_container_width=True)

    # 강수량
    if '일강수량(mm)' in df_monthly.columns:
        fig_rain = px.line(df_monthly, x='연월', y='일강수량(mm)', color='지점명', markers=True, title='월별 평균강수량')
        st.plotly_chart(fig_rain, use_container_width=True)

    # 상대습도
    if '평균상대습도(%)' in df_monthly.columns:
        fig_humid = px.line(df_monthly, x='연월', y='평균상대습도(%)', color='지점명', markers=True, title='월별 평균상대습도')
        st.plotly_chart(fig_humid, use_container_width=True)
