import streamlit as st
import plotly.express as px
from modules.load_data import load_data

st.title("📊 지점별 월별 기후 변화")

# 데이터 로딩
df_weather, _ = load_data()

# 지점 선택
selected_sites = st.multiselect('지점을 선택하세요', df_weather['지점명'].unique(), default=df_weather['지점명'].unique())

# 연월 컬럼 생성
df_weather['연월'] = df_weather['일시'].dt.to_period('M').astype(str)

# 선택된 지점 필터링
df_selected = df_weather[df_weather['지점명'].isin(selected_sites)]

# 월별 평균 집계 (있는 컬럼 기준)
df_monthly = df_selected.groupby(['연월', '지점명']).agg({
    '평균기온(°C)': 'mean',
    '평균최고기온(°C)': 'mean',
    '평균최저기온(°C)': 'mean',
    '평균상대습도(%)': 'mean'
}).reset_index()

# 시각화 컬럼 리스트 (있는 것만)
for col, title in [
    ('평균기온(°C)', '월별 평균기온'),
    ('평균최고기온(°C)', '월별 평균최고기온'),
    ('평균최저기온(°C)', '월별 평균최저기온'),
    ('평균상대습도(%)', '월별 평균습도')
]:
    fig = px.line(df_monthly, x='연월', y=col, color='지점명', markers=True, title=title)
    st.plotly_chart(fig, use_container_width=True)
