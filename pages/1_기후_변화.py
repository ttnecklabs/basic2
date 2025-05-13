
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import db_loader, preprocessing

df_weather, df_sunshine = db_loader.load_data()
df_merge = preprocessing.merge_data(df_weather, df_sunshine)

st.subheader("📊 지점별 월별 기후 변화")
selected_sites = st.multiselect('지점을 선택하세요', df_merge['지점명'].unique(), default=df_merge['지점명'].unique())

df_merge['연월'] = df_merge['일시'].dt.to_period('M').astype(str)
df_selected = df_merge[df_merge['지점명'].isin(selected_sites)]

df_monthly = df_selected.groupby(['연월', '지점명']).agg({
    '평균기온(°C)': 'mean',
    '일강수량(mm)': 'mean',
    '평균 상대습도(%)': 'mean'
}).reset_index()

fig = px.line(df_monthly, x='연월', y='평균기온(°C)', color='지점명', title='월별 평균기온')
st.plotly_chart(fig, use_container_width=True)
