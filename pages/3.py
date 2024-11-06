import streamlit as st
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

query_params = st.query_params
case_serial = st.query_params.case_serial
case_number = st.query_params.case_number
case_name = st.query_params.case_name

st.markdown("""
    <style>
    * {
        font-family: 'Nanum Gothic', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 데이터 로딩
cluster_1 = pd.read_csv('cluster1.csv')

# '선고일자' 칼럼을 datetime 형식으로 변환
cluster_1['선고일자'] = pd.to_datetime(cluster_1['선고일자'])

# 요일 순서 정의
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# 요일 리스트 생성 (0: 월요일, 1: 화요일, ..., 6: 일요일)
weekdays = cluster_1['선고일자'].dt.day_name()

# 요일 빈도수 계산
weekday_counts = Counter(weekdays)

# 요일별 빈도수를 0으로 초기화 (빈도수가 없으면 0으로 처리)
counts = [weekday_counts[day] for day in weekday_order]

# 히트맵 데이터 생성 (1행 5열로 변환)
heatmap_data = np.array(counts).reshape(1, 5)

# 첫 번째 줄: 사건번호와 SAVE 버튼 배치
container = st.container(border=True)

# 첫 번째 줄에 두 개의 열 배치 (사건번호, SAVE 버튼)
col1, col2 = container.columns([3, 1])  # 첫 번째 열은 3배 크기, 두 번째 열은 1배 크기
col1.write(f"사건명: {case_name}")  # 사건명 텍스트
on = col2.toggle("SAVE")  # SAVE 토글 버튼

container = st.container(border=True)
with container:
    col1, col2 = st.columns([2.5, 1.5])  # bar_chart는 왼쪽 3배 크기, metric과 heatmap은 오른쪽 1배 크기

    # 첫 번째 열에 bar_chart 배치 (길게)
    with col1:
        # 연도별 사건 수 계산
        yearly_counts = cluster_1.groupby(cluster_1['선고일자'].dt.year).size()
        col1.write("연도별 관련사건 선고수")
        st.bar_chart(data=yearly_counts, width=400, height=200)
        # # 막대 그래프 생성
        # fig_bar, ax_bar = plt.subplots(figsize=(8, 4))
        # ax_bar.bar(yearly_counts.index, yearly_counts.values, color='blue')
        # ax_bar.set_xlabel("Year")
        # ax_bar.set_ylabel("Count")
        # st.pyplot(fig_bar)

    # 두 번째 열에 metric과 heatmap 배치
    with col2:
        # Metric (위)
        if on:
            if 'rating_value' not in st.session_state:
                st.session_state.rating_value = 700  # 초기값 설정
            st.session_state.rating_value += 1  # 값 증가
        else:
            st.session_state.rating_value = 701  # 취소 시 값 리셋
        st.metric(label="✅ 판례 저장수", value=st.session_state.rating_value)

        # Heatmap (아래)
        # 히트맵 그리기
        plt.figure(figsize=(8, 2))  # 가로로 긴 히트맵 크기 설정
        sns.heatmap(heatmap_data, annot=True, cmap="Blues", cbar=False, xticklabels=weekday_order)
        st.write("요일별 선고수")

        # 그래프 표시
        st.pyplot(plt)

st.write("---------------------------------")

# params = 사건번호

OC = 'younwjdtjr'
target = 'prec'
type = 'HTML'
url = 'http://www.law.go.kr/DRF/lawService.do?'
parameters = {
    'OC': OC,
    'target': target,
    'type' : type,
    'ID': case_serial
}
response = requests.get(url=url, params=parameters)
if response.status_code == 200 :
    html_content = response.text
    st.components.v1.html(html_content, width= 800, height=1000)
else:
    st.error(response.status_code)

