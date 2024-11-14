import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
import ast
from urllib.parse import quote
from pyvis.network import Network
import streamlit.components.v1 as components
from db_info import user, password, host, database, port
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go


# 전체 배경색 설정
page_bg = """
<style> 
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, rgba(147, 182, 217, 1), rgba(178, 208, 211, 0.8));
}
[data-testid="stHeader"] {
    background: #9EB8D7;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)


if 'page' not in st.session_state:
    st.session_state['page'] = 'home'  # 초기 페이지를 home으로 설정

# 버튼 클릭 시 세션 상태 변경 함수
def go_to_page(page_name):
    st.session_state['page'] = page_name


# 홈 페이지
if st.session_state['page'] == 'home':
    st.title("Welcome to NoF")
    st.write("안녕하세요 판례검색서비스입니다. 원하는 카테고리를 선택하세요.")

    # 버튼에 각각 다른 페이지로 이동하도록 설정
    button_labor = st.button("근로 페이지로 이동", on_click=lambda: go_to_page('labor_page'))
    button_fraud = st.button("사기 페이지로 이동", on_click=lambda: go_to_page('fraud_page'))
    button_inheritance = st.button("상속 페이지로 이동", on_click=lambda: go_to_page('inheritance_page'))
    button_injury = st.button("상해 페이지로 이동", on_click=lambda: go_to_page('injury_page'))

# 다른 페이지들
elif st.session_state['page'] == 'labor_page':
    with st.status("loading report data..."):
        time.sleep(2)
        st.title("근로 페이지")
        st.write("여기는 근로 페이지입니다.")
        if st.button("홈으로 돌아가기"):
            go_to_page('home')

elif st.session_state['page'] == 'fraud_page':
    st.title("사기 페이지")
    st.write("여기는 사기 페이지입니다.")
    

elif st.session_state['page'] == 'inheritance_page':
    with st.status("loading report data...") as status:
        time.sleep(2)
    status.update(
        label="load complete!", state="complete", expanded=False
    )
    st.title("상속 페이지")
    # MySQL 데이터베이스 연결
    db_connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )

    cursor = db_connection.cursor()

    # 데이터 가져오기
    cursor.execute("SELECT 판례일련번호,사건번호,클러스터,키워드,선고일자 FROM inheritance_keyword")
    result = cursor.fetchall()

    # DataFrame 생성 및 컬럼 이름 설정
    df_inheritance = pd.DataFrame(result, columns=[i[0] for i in cursor.description])


    # '선고일자' 칼럼을 datetime 형식으로 변환
    df_inheritance['선고일자'] = pd.to_datetime(df_inheritance['선고일자'])
    # '키워드' 형식변환
    df_inheritance['키워드'] = df_inheritance['키워드'].apply(lambda x: x.split(', '))

    col = st.columns((3,8), gap='small')

    with col[0]:
        #판례아이콘
        gavel_icon_url = "https://static.thenounproject.com/png/2569293-512.png"
        law_icon_url = "https://static.thenounproject.com/png/6847970-512.png"
        people_icon_url = "https://static.thenounproject.com/png/5007058-512.png"
        # 카테고리별 사건수 선언
        data = {
            '카테고리': ['근로', '사기', '상속', '상해'],
            '사건수': [5012, 4178, 4127, 4189]
        }

        # 데이터프레임 생성
        df_data = pd.DataFrame(data)

        # 전체 사건수 계산
        total = df_data['사건수'].sum()

        # 근로 카테고리의 사건수만 추출
        상속_사건수 = df_data[df_data['카테고리'] == '상속']['사건수'].values[0]

        # 근로와 기타 카테고리로 분리하여 파이 차트 데이터 준비
        data_pie = {
            '카테고리': ['상속', '기타'],
            '사건수': [상속_사건수, total - 상속_사건수]
        }

        df_pie = pd.DataFrame(data_pie)

        # 파이 차트 생성
        fig = px.pie(df_pie, names='카테고리', values='사건수',
                    title= '상속데이터비율', hole=0.5)  # 도넛 차트 효과

        fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)", 
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(t=50, b=120, l=0, r=0),  # 공백을 줄임
        legend=dict(
            y=-0.07,                  # 범례를 차트 아래로 배치
            x=1,                   
            xanchor="right",
            yanchor="top"
        ))

        st.markdown(f'''
        <div style="font-size: 16px;">
            <strong>카테고리 전체 데이터 수<strong>
            <span style="font-size: 20px; color: #DA5663;"></br>
            　<img src="{gavel_icon_url}" width="40" style="vertical-align:middle;">　　{total}</span>
        </div>
        ''', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)


    with col[1]:
        cluster_labels = {
        1: '상속 및 재산 평가',
        2: '부동산 소유권 및 취득',
        3: '부동산 상속 및 사망 관련',
        4: '부동산 등기 및 소유권 이전',
        5: '손해배상 및 사망 보상',
        6: '농지 및 경작',
        7: '상속세 및 납부',
        8: '부동산 등기 및 거래',
        9: '상속 분할 및 유류분',
        10: '보험 및 보상'
        }
        
        # 연도별로 클러스터별 사건 수 계산
        df_inheritance['선고년도'] = df_inheritance['선고일자'].dt.year
        cluster_counts = df_inheritance.groupby(['선고년도', '클러스터']).size().reset_index(name='사건수')

        fig = go.Figure()

        for cluster_num, cluster_name in cluster_labels.items():
            cluster_data = cluster_counts[cluster_counts['클러스터'] == cluster_num]
            fig.add_trace(go.Bar(
                x=cluster_data['선고년도'],
                y=cluster_data['사건수'],
                name=cluster_name
            ))

        # 막대 두께 조정
        fig.update_traces(marker=dict(line=dict(width=0)), width=0.8)

        # 레이아웃 설정
        fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)", 
        plot_bgcolor="rgba(0, 0, 0, 0)",
        legend=dict(
            orientation="h",      # 수평 정렬
            y=-0.2,               # y 위치
            x=0.5,                # x 위치
            xanchor="center",     # x 기준을 중앙으로 맞춤
            yanchor="top",     # y 기준을 아래쪽으로 맞춤
            itemwidth=30,        # 각 범례 항목의 최대 너비를 제한하여 여러 줄로 나뉨
            traceorder="normal"   # 항목의 표시 순서를 유지
        ),
        xaxis_title="Year",
        yaxis_title="Count",
        barmode='group',  # 그룹으로 묶어서 나란히 보이게 설정
        margin=dict(t=30),
        title=dict(
        text="연도별 관련사건 선고수")
        )


        # Streamlit에서 Plotly 차트 표시
        st.markdown(f'''
        <div style="display: flex; justify-content: space-between; font-size: 16px;">
            <div style="flex: 1; padding: 10px;align-items: center;">
                <strong>　　최다 빈도수 법원명</strong>
                <span style="font-size: 15px; color: #DA5663; display: inline-flex; align-items: center;">
                    <img src="{law_icon_url}" width="40" style="vertical-align: middle; margin-right: 10px;">
                    <div style="line-height: 1.2;">
                        <span style="display: block;">대법원</span>
                        <span style="display: block;">2,253회</span>
                    </div>
                </span>
            </div>
            <div style="flex: 1; padding: 10px;">
                <strong>최다 언급수 재판장</strong>
                <span style="font-size: 18px; color: #29283d;">
                    <br>　
                    <img src="{people_icon_url}" width="40" style="vertical-align:middle;">　박만호
                </span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        

    with st.container():
        cluster_keywords = {}
        for _, row in df_inheritance.iterrows():
            cluster_keywords[f'Cluster {row["클러스터"]}'] = row['키워드']

        # pyvis 네트워크 생성
        net = Network(height='600px', width='100%', bgcolor='#ffffff', font_color='black', notebook=True)

        # 네트워크에 노드와 엣지 추가
        for cluster, keywords in cluster_keywords.items():
            # 상위 레벨 노드 추가
            net.add_node(keywords[0], title=keywords[0], size=50, color='red', font={'size': 50})
            
            # 2레벨 노드 연결 (상위 3개 키워드)
            for keyword in keywords[1:4]:
                net.add_node(keyword, title=keyword, size=35, color='orange', font={'size': 50})
                net.add_edge(keywords[0], keyword)
            
            # 3레벨 노드 연결 (하위 7개 키워드)
            for keyword in keywords[4:]:
                net.add_node(keyword, title=keyword, size=15, color='yellow', font={'size': 50})
                net.add_edge(keywords[1], keyword)  # 2레벨 키워드에 연결

        # 네트워크 시각화 설정
        net.set_options("""
            var options = {
            "nodes": {
                "borderWidth": 2,
                "borderWidthSelected": 4
            },
            "edges": {
                "color": {
                "highlight": "rgba(0, 255, 0, 0.8)"
                },
                "smooth": {
                "type": "continuous"
                }
            },
            "physics": {
                "enabled": true,
                "barnesHut": {
                "gravitationalConstant": -10000,
                "springLength": 100
                }
            }
            }
        """)

        # 네트워크 그래프 출력
        st.markdown('키워드 네트워크')
        net.show('keyword_network.html')

        # Streamlit에서 HTML 파일 표시
        components.html(open('keyword_network.html', 'r').read(), height=600)

    # 데이터베이스 연결 닫기
    cursor.close()
    db_connection.close()
    st.button("자세한 판례검색 페이지로 이동")

    

elif st.session_state['page'] == 'injury_page':
    st.title("상해 페이지")
    st.write("여기는 상해 페이지입니다.")
    
