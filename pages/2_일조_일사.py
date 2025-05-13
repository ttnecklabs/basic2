import streamlit as st
import plotly.express as px
from modules.load_data import load_data

st.title("☀️ 지점별 월별 일조시간 / 일사량")

_, df_sunshine = load_data()

selected_sites = st.multiselect('지점을 선택하세요', df_sunshine['지점명'].unique(), default=df_sunshine['지점명'].unique())

df_sunshine['연월'] = df_sunshine['일시'].dt.to_period('M').astype(str)
df_selected = df_sunshine[df_sunshine['지점명'].isin(selected_sites)]

df_monthly = df_selected.groupby(['연월', '지점명']).agg({
    '일조시간': 'mean',
    '일사량': 'mean'
}).reset_index()

fig1 = px.line(df_monthly, x='연월', y='일조시간', color='지점명', markers=True, title='월별 평균 일조시간')
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(df_monthly, x='연월', y='일사량', color='지점명', markers=True, title='월별 평균 일사량')
st.plotly_chart(fig2, use_container_width=True)
