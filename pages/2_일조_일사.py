import streamlit as st
import pandas as pd
import plotly.express as px
from modules.db_loader import load_asos_data
from modules.preprocessing import preprocess_data

df_weather, df_sunshine = load_asos_data('data/asos_weather.db')
df_merge = preprocess_data(df_weather, df_sunshine)

st.subheader("☀️ 지점별 월별 일조시간 / 일사량")
selected_sites = st.multiselect('지점을 선택하세요', df_merge['지점명'].unique(), default=df_merge['지점명'].unique())

df_merge['연월'] = df_merge['일시'].dt.to_period('M').astype(str)
df_selected = df_merge[df_merge['지점명'].isin(selected_sites)]

df_monthly = df_selected.groupby(['연월', '지점명']).agg({
    '일조시간': 'mean',
    '일사량': 'mean'
}).reset_index()

fig1 = px.line(df_monthly, x='연월', y='일조시간', color='지점명', markers=True, title='월별 평균 일조시간')
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(df_monthly, x='연월', y='일사량', color='지점명', markers=True, title='월별 평균 일사량')
st.plotly_chart(fig2, use_container_width=True)
