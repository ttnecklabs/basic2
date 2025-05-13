import streamlit as st
import pandas as pd
import folium
from streamlit.components.v1 import html
from modules.load_data import load_data

st.title("🍊 감귤 재배 적합도 지도")

df_weather, df_sunshine = load_data()

stations = {
    '제주시': (33.4996, 126.5312),
    '고산': (33.2931, 126.1628),
    '서귀포': (33.2540, 126.5618),
    '성산': (33.3875, 126.8808),
    '고흥': (34.6076, 127.2871),
    '완도': (34.3111, 126.7531)
}

df_weather['연월'] = df_weather['일시'].dt.to_period('M').astype(str)
month_options = sorted(df_weather['연월'].unique())

selected_month = st.selectbox("월을 선택하세요", month_options, index=len(month_options)-1)

df_selected = df_weather[df_weather['연월'] == selected_month]

fmap = folium.Map(location=[34.0, 126.5], zoom_start=8)

for station, (lat, lon) in stations.items():
    data = df_selected[df_selected['지점명'] == station]
    if data.empty: continue

    row = data.iloc[0]
    temp = row['평균기온(°C)']
    humid = row['평균상대습도(%)']

    suitable = (12 <= temp <= 18) and (60 <= humid <= 85)
    color = 'green' if suitable else 'gray'
    tooltip = f"{station} ({selected_month})<br>🌡 {temp}°C | 💧 {humid}%<br>{'적합' if suitable else '부적합'}"

    folium.CircleMarker(location=[lat, lon], radius=10, color=color, fill=True, fill_opacity=0.8, popup=tooltip).add_to(fmap)

html(fmap._repr_html_(), height=550, width=750)
