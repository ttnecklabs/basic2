import streamlit as st
from modules.load_data import load_weather_data

st.set_page_config(page_title="제주/남도 기후 대시보드", layout="wide")
st.title("📊 제주/남도 기후 대시보드")

st.sidebar.success("왼쪽 메뉴에서 페이지를 선택하세요")

# 데이터 로딩
df = load_weather_data()

st.write("👈 왼쪽 메뉴에서 상세 항목을 선택해보세요.")
