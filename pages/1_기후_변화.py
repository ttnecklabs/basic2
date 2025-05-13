import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# DB 로딩
conn = sqlite3.connect('data/asos_weather.db')
df_weather = pd.read_sql("SELECT * FROM asos_weather", conn)
df_sunshine = pd.read_sql("SELECT * FROM sunshine_data", conn)
conn.close()

df_weather['일시'] = pd.to_datetime(df_weather['일시'])
df_sunshine['일시'] = pd.to_datetime(df_sunshine['일시'])

# JOIN
df_merge = pd.merge(df_weather, df_sunshine, on=['지점명', '일시'], how='left')

# 월별 집계
df_merge['연월'] = df_merge['일시'].dt.to_period('M').astype(str)

# 지점 선택
selected_sites = st.multiselect('지점을 선택하세요', df_merge['지점명'].unique(), default=df_merge['지점명'].unique())
df_selected = df_merge[df_merge['지점명'].isin(selected_sites)]

# 실제 존재하는 컬럼명 기준
agg_columns = ['평균기온(°C)', '일강수량(mm)', '평균상대습도(%)']
available_cols = [col for col in agg_columns if col in df_selected.columns]

if not available_cols:
    st.error("필요한 기후 데이터 컬럼이 없습니다. DB를 확인하세요.")
else:
    df_monthly = df_selected.groupby(['연월', '지점명'])[available_cols].mean().reset_index()

    # 기온 그래프
    fig = px.line(df_monthly, x='연월', y='평균기온(°C)', color='지점명', title='월별 평균기온', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # 강수량 그래프
    fig2 = px.line(df_monthly, x='연월', y='일강수량(mm)', color='지점명', title='월별 평균강수량', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    # 상대습도 그래프
    fig3 = px.line(df_monthly, x='연월', y='평균상대습도(%)', color='지점명', title='월별 평균상대습도', markers=True)
    st.plotly_chart(fig3, use_container_width=True)
