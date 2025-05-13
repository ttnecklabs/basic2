import streamlit as st
import plotly.express as px
from modules.load_data import load_weather_data

# 데이터 로딩
df_weather, df_sunshine, df_merge = load_weather_data()

# 탭 제목
st.subheader("📊 지점별 월별 기후 변화")

# 지점 선택 필터
selected_sites = st.multiselect(
    '지점을 선택하세요',
    df_merge['지점명'].unique(),
    default=df_merge['지점명'].unique()
)

# 필터링
df_selected = df_merge[df_merge['지점명'].isin(selected_sites)]

# 월별 평균 집계 (컬럼명 정확히 매칭)
agg_cols = ['평균기온(°C)', '일강수량', '평균상대습도']
available_cols = [col for col in agg_cols if col in df_selected.columns]

if not available_cols:
    st.error("필요한 기후 데이터 컬럼이 없습니다. DB를 확인하세요.")
else:
    df_monthly = df_selected.groupby(['연월', '지점명'])[available_cols].mean().reset_index()

    # 📈 평균기온 그래프
    if '평균기온(°C)' in df_monthly.columns:
        fig1 = px.line(df_monthly, x='연월', y='평균기온(°C)', color='지점명', markers=True, title='월별 평균기온')
        st.plotly_chart(fig1, use_container_width=True)

    # 📈 강수량 그래프
    if '일강수량' in df_monthly.columns:
        fig2 = px.line(df_monthly, x='연월', y='일강수량', color='지점명', markers=True, title='월별 평균강수량')
        st.plotly_chart(fig2, use_container_width=True)

    # 📈 상대습도 그래프
    if '평균상대습도' in df_monthly.columns:
        fig3 = px.line(df_monthly, x='연월', y='평균상대습도', color='지점명', markers=True, title='월별 평균상대습도')
        st.plotly_chart(fig3, use_container_width=True)
