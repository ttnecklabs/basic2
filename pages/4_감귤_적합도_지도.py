import streamlit as st
import pandas as pd
import folium
from streamlit.components.v1 import html
from modules.load_data import load_weather_data

st.subheader("🍊 감귤 재배 적합도 지도")

# 데이터 로딩
df = load_weather_data()

# 지점 좌표 정보
stations = {
    '제주시': (33.4996, 126.5312),
    '서귀포': (33.2540, 126.5618),
    '한림': (33.4125, 126.2614),
    '성산': (33.3875, 126.8808),
    '고흥': (34.6076, 127.2871),
    '완도': (34.3111, 126.7531)
}

# 월 선택 위젯
month_options = sorted(df['연월'].unique())
selected_month = st.selectbox("월을 선택하세요", month_options, index=len(month_options)-1)

# 선택 월 기준 필터링
df_selected = df[df['연월'] == selected_month]

# 월별 평균값 계산
df_monthly = df_selected.groupby('지점명').agg({
    '평균기온(°C)': 'mean',
    '평균 상대습도(%)': 'mean',
    '일조시간': 'mean'
}).reset_index()

# 감귤 재배 적합 기준
def is_suitable(temp, humid, sun):
    return (12 <= temp <= 18) and (60 <= humid <= 85) and (sun >= 100)

# 지도 생성
m = folium.Map(location=[34.0, 126.5], zoom_start=8)

for _, row in df_monthly.iterrows():
    name = row['지점명']
    lat, lon = stations.get(name, (None, None))
    if lat is None: continue

    temp = row['평균기온(°C)']
    humid = row['평균 상대습도(%)']
    sun = row['일조시간']

    suitable = is_suitable(temp, humid, sun)

    # 마커 색상
    color = 'green' if suitable else 'gray'

    # 팝업 내용
    popup_content = f"""
    <b>{name}</b> ({selected_month})<br>
    🌡 {temp:.1f}℃ | 💧 {humid:.1f}% | ☀️ {sun:.1f}h<br>
    {'✅ 감귤 재배 적합' if suitable else '❌ 부적합'}
    """

    folium.CircleMarker(
        location=(lat, lon),
        radius=10,
        color=color,
        fill=True,
        fill_opacity=0.8,
        popup=folium.Popup(popup_content, max_width=300)
    ).add_to(m)

# Streamlit 지도 출력
html(m._repr_html_(), height=550, width=750)
