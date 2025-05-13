# 일조데이터 merge (지점명+일시 기준)
df_sunshine['연월'] = df_sunshine['일시'].dt.to_period('M').astype(str)
df_merged = pd.merge(df_weather, df_sunshine, on=['지점명', '연월'], how='left')

df_selected = df_merged[df_merged['연월'] == selected_month]

fmap = folium.Map(location=[34.0, 126.5], zoom_start=8)

for station, (lat, lon) in stations.items():
    data = df_selected[df_selected['지점명'] == station]
    if data.empty: continue

    row = data.iloc[0]
    temp = row['평균기온(°C)']
    humid = row['평균상대습도(%)']
    sunshine = row.get('일조시간', None)
    radiation = row.get('일사량', None)

    # 적합도 평가 (예시: 기온/습도/일조 각각 33%)
    score = 0
    score += 33 if 12 <= temp <= 18 else 0
    score += 33 if 60 <= humid <= 85 else 0
    score += 33 if sunshine and sunshine >= 150 else 0  # 일조시간 기준 예시

    # 색상 스케일링
    if score >= 66:
        color = 'green'
    elif score >= 33:
        color = 'orange'
    else:
        color = 'gray'

    tooltip = f"""
    <b>{station} ({selected_month})</b><br>
    🌡 평균기온: {temp:.1f}°C<br>
    💧 평균습도: {humid:.1f}%<br>
    ☀️ 일조시간: {sunshine:.1f}h<br>
    🔆 일사량: {radiation:.1f} MJ/m²<br>
    <b>적합도 점수: {score}%</b>
    """

    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        color=color,
        fill=True,
        fill_opacity=0.9,
        popup=folium.Popup(tooltip, max_width=300)
    ).add_to(fmap)

html(fmap._repr_html_(), height=550, width=750)
