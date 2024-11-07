import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import requests
from streamlit_elements import dashboard, mui, elements

# 쿼리 파라미터 받기
query_params = st.query_params
case_serial = st.query_params.get("case_serial", "")
case_number = st.query_params.get("case_number", "")
case_name = st.query_params.get("case_name", "사건명 없음")

# 데이터 로딩
cluster_1 = pd.read_csv('data/cluster1.csv')

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

# elements()로 대시보드 구성
with elements("dashboard"):  # 'dashboard'라는 프레임으로 요소를 구성
    # 대시보드 기본 레이아웃 정의
    layout = [
        # 사건명과 SAVE 버튼을 위한 첫 번째 항목
        dashboard.Item("first_item", 0, 0, 3, 2),
        # 연도별 사건 수를 표시하는 bar_chart 항목
        dashboard.Item("second_item", 0, 3, 3, 2),
    ]

    # 대시보드 그리드 레이아웃 구성
    with dashboard.Grid(layout):  # 'elements' 내에서 dashboard.Grid 사용
        mui.Paper("first_item", key='first_item')
        
        mui.Paper("second_item", key='second_item')
        
        # # 첫 번째 아이템: 사건명과 SAVE 버튼
        # with mui.Paper("first_item", key="first_item"):
        #     col= st.columns((3, 1), gap="medium")
        #     col[0].write(f"사건명: {case_name}")  # 사건명 텍스트
        #     on = col[1].checkbox("SAVE")  # SAVE 체크박스
            
        #     # SAVE 버튼 상태에 따라 session_state 값 설정
        #     if on:
        #         if 'rating_value' not in st.session_state:
        #             st.session_state.rating_value = 700  # 초기값 설정
        #         st.session_state.rating_value += 1  # 값 증가
        #     else:
        #         st.session_state.rating_value = 701  # 취소 시 값 리셋

        # # 두 번째 아이템: bar_chart
        # with mui.Paper("second_item", key="second_item"):
        #     # 연도별 사건 수 계산
        #     yearly_counts = cluster_1.groupby(cluster_1['선고일자'].dt.year).size()
        #     st.write("연도별 관련사건 선고수")
        #     st.bar_chart(data=yearly_counts, width=400, height=200)

# ** 별도의 섹션으로 Metric과 Heatmap을 배치 **

# 두 개의 다른 항목으로 분리
with elements("metrics_and_heatmap"):  # 별도의 프레임으로 구성
    layout_2 = [
        dashboard.Item("metric_item", 0, 0, 3, 2),  # Metric 항목
        dashboard.Item("heatmap_item", 3, 0, 3, 2),  # Heatmap 항목
    ]

    # 대시보드 그리드 레이아웃 구성
    col = st.columns((1,1), gap="medium")
    with dashboard.Grid(layout_2):  # 'elements' 내에서 dashboard.Grid 사용
        with col[0]:
            with mui.Paper("metric_item", key="metric_item"):
                st.metric(label="✅ 판례 저장수", value=st.session_state.rating_value)
        # 첫 번째 항목: Metric
        # with mui.Paper("metric_item", key="metric_item"):
        #     col1, col2 = st.columns([2.5, 1.5])
        #     st.metric(label="✅ 판례 저장수", value=st.session_state.rating_value)

        # 두 번째 항목: Heatmap
        with col[1]:
            with mui.Paper("heatmap_item", key="heatmap_item"):
                # 히트맵 그리기
                plt.figure(figsize=(8, 2))  # 가로로 긴 히트맵 크기 설정
                sns.heatmap(heatmap_data, annot=True, cmap="Blues", cbar=False, xticklabels=weekday_order)
                st.write("요일별 선고수")
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

