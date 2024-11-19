import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
# import ast
from urllib.parse import quote
from pyvis.network import Network
import streamlit.components.v1 as components
from db_info import user, password, host, database, port
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter


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

# 데이터 설정
keywordsdata = {
    '주제': [
        '상속 및 재산 평가', '부동산 소유권 및 취득', '부동산 상속 및 사망 관련',
        '부동산 등기 및 소유권 이전', '손해배상 및 사망 보상', '농지 및 경작',
        '상속세 및 납부', '부동산 등기 및 거래', '상속 분할 및 유류분', '보험 및 보상'
    ],
    '키워드': [
        ['가액', '시가', '평가', '상속', '세법', '주식', '재산', '과세', '증여', '상속세'],
        ['점유', '토지', '취득시효', '등기', '소유권', '완성', '자주', '부동산', '취득', '의사'],
        ['신청', '상속', '부동산', '주택', '사망', '건물', '계약', '회사', '재산', '호주'],
        ['등기', '임야', '소유권', '부동산', '이전', '명의', '원인', '상속', '명의신탁', '토지'],
        ['망인', '손해', '차량', '위자료', '지급', '손해배상', '사망', '유족', '운전', '운행'],
        ['농지', '분배', '농지개혁법', '토지', '상환', '등기', '본건', '소유권', '경작', '완료'],
        ['상속세', '세액', '부과', '납부', '과세', '상속', '재산', '가액', '신고', '납세'],
        ['토지', '등기', '소유권', '이전', '명의', '분할', '지번', '주소', '환지', '매매'],
        ['상속', '재산', '분할', '유류분', '상속인', '부동산', '민법', '한정승인', '피상', '포기'],
        ['보험', '보험금', '계약', '지급', '망인', '보험료', '자동차', '연금', '수익', '상해']
    ]
}


# 미리저장한 결과 CSV 파일 불러오기
inheritance_results = pd.read_csv('data/inheritance_results_241118.csv')


if 'page' not in st.session_state:
    st.session_state['page'] = 'home'  # 초기 페이지를 home으로 설정

# 버튼 클릭 시 세션 상태 변경 함수
def go_to_page(page_name):
    st.session_state['page'] = page_name

def load_csv():
    return pd.read_csv('용어정리_최종선정.csv')

# CSV 파일 불러오기
dfword = load_csv()

# 스트리밍으로 개념을 출력하는 함수
def stream_concept(concept):
    words = concept.split(" ")
    for word in words:
        yield word + " "
        time.sleep(0.02)

# 주제와 클러스터 매핑 정의
topic_cluster_map = {
    '상속 및 재산 평가': 1,
    '부동산 소유권 및 취득': 2,
    '부동산 상속 및 사망 관련': 3,
    '부동산 등기 및 소유권 이전': 4,
    '손해배상 및 사망 보상': 5,
    '농지 및 경작': 6,
    '상속세 및 납부': 7,
    '부동산 등기 및 거래': 8,
    '상속 분할 및 유류분': 9,
    '보험 및 보상': 10
}


# 홈 페이지
if st.session_state['page'] == 'home':
    st.title("Welcome to NoF")
    st.write("안녕하세요 판례검색서비스입니다. 원하는 카테고리를 선택하세요.")

    # 버튼에 각각 다른 페이지로 이동하도록 설정
    button_labor = st.button("근로 페이지로 이동", on_click=lambda: go_to_page('labor_page'))
    button_fraud = st.button("사기 페이지로 이동", on_click=lambda: go_to_page('fraud_page'))
    button_inheritance = st.button("상속 페이지로 이동", on_click=lambda: go_to_page('inheritance_page'))
    button_injury = st.button("상해 페이지로 이동", on_click=lambda: go_to_page('injury_page'))
    button_word = st.button("법률용어사전 이동", on_click=lambda: go_to_page('word_page'))

# 다른 페이지들

elif st.session_state['page'] == 'word_page':
    st.title("법률용어사전")
    # 각 용어에 대해 버튼을 생성하고, 클릭 시 개념을 스트리밍
    for _, row in dfword.iterrows():
        term = row['용어']
        concept = row['개념']
        
        # 용어 버튼 표시
        if st.button(term, key=term):
            # 스트리밍 방식으로 개념을 출력
            st.write_stream(stream_concept(concept))
    if st.button("홈으로 돌아가기"):
        go_to_page('home')


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
        <div style="display: flex; align-items: flex-start; font-size: 16px; padding: 10px;">
            <img src="{gavel_icon_url}" width="40" style="margin-right: 10px;">
            <div>
                <strong>전체 데이터 수</strong><br>
                <span style="font-size: 20px; color: #DA5663;">
                    {total}
                </span>
            </div>
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
        text="연도별 관련사건수")
        )


        # Streamlit에서 Plotly 차트 표시
        st.markdown(f'''
        <div style="display: flex; justify-content: space-between; font-size: 16px;">
            <div style="flex: 1; padding: 10px; display: flex; align-items: flex-start;">
                <img src="{law_icon_url}" width="40" style="margin-right: 10px;">
                <div style="line-height: 1.2;">
                    <strong>최다 빈출 법원명</strong><br>
                    <span style="font-size: 15px; color: #DA5663;">
                        대법원 2,253회
                    </span>
                </div>
            </div>
            <div style="flex: 1; padding: 10px; display: flex; align-items: flex-start;">
                <img src="{people_icon_url}" width="40" style="margin-right: 10px;">
                <div>
                    <strong>최다 빈출 재판장</strong><br>
                    <span style="font-size: 18px; color: #29283d;">
                        박만호
                    </span>
                </div>
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
    # st.button("자세한 판례검색 페이지로 이동")
    button_inheritance_detail = st.button("자세한 판례검색 페이지로 이동", on_click=lambda: go_to_page('inheritance_detailpage'))

    

elif st.session_state['page'] == 'injury_page':
    st.title("상해 페이지")
    st.write("여기는 상해 페이지입니다.")
    


elif st.session_state['page'] == 'inheritance_detailpage':
    st.title("상속 페이지")
    st.write("여기는 상속 페이지입니다.")
    subject = st.selectbox("👆주제를 선택하세요:", keywordsdata['주제'])

    # 선택된 주제에 따른 키워드 버튼 표시
    selected_index = keywordsdata['주제'].index(subject)
    keywords = keywordsdata['키워드'][selected_index]
    
    st.write(f"**{subject}**와 관련된 키워드:")

    # 키워드를 한 줄로 출력 (쉼표로 구분)
    st.write(", ".join(keywords[:10]))

    # 확인 버튼 클릭 시 진행 표시와 유사도 계산
    if st.button("주제 선택 완료") :
        # Progress bar와 placeholder 설정
        placeholder = st.empty()
        with placeholder:
            for percent in range(0, 101, 20):
                st.write("처리 중입니다...")
                st.progress(percent)
                time.sleep(0.5)

         # 이미 계산된 inheritance_results에서 주제,키워드로 필터링
        df_results = inheritance_results[inheritance_results['주제'] == subject].sort_values(by='유사도', ascending=False).drop_duplicates(subset=['사건번호', '사건명','판례일련번호']).head(10)
        
        # 결과가 있으면 탭에 표시
        if not df_results.empty:
            tab1, tab2 = st.tabs(["판례검색결과", "참조조문"])
            
            with tab1:
                st.header(f"{subject}와 관련된 사건명")
                판례_url = 'https://www.law.go.kr/DRF/lawService.do?OC=younwjdtjr&target=prec&type=HTML&ID='
                df_results['상세링크'] = df_results['판례일련번호'].apply(lambda x: 판례_url + str(x))
                # st.dataframe(df_results)
                # # HTML 링크 추가
                df_results['사건번호'] = df_results.apply(
                    lambda df_results: f'<a href="{df_results["상세링크"]}" target="_blank">{df_results["사건번호"]}</a>', axis=1
                )

                
                st.markdown(
                    f"""
                    <div class="dataframe-container">
                        {df_results[['사건번호', '사건명']].to_html(escape=False, index=False)}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )



                for _, row in df_results.iterrows():
                    사건번호_encoded = quote(row['사건번호'])  # 사건번호 인코딩
                    판례일련번호_encoded = quote(str(row['판례일련번호'])) # 판례일련번호 인코딩
                #     if pd.isna(row['사건명']):
                #         사건명_encoded = '없음'
                #     else:
                #         사건명_encoded = quote(row['사건명'])
                #     # 사건번호를 클릭하면 2_page.py로 이동하도록 링크 생성
                #     if pd.isna(row['사건명']):
                #         # st.write(f"[go to page 3](3?param={value})")/
                #         st.write(f"[사건번호: {row['사건번호']}]")
                #         # st.button('1')
                #     else:
                #         st.write(f"[사건번호: {row['사건번호']}, 사건명: {row['사건명']}](/3?case_number={사건번호_encoded}&case_serial={판례일련번호_encoded}&case_name={사건명_encoded})")
            
            with tab2:
                st.header("참조조문")
                cluster_num = topic_cluster_map.get(subject) # 선택한 클러스터 번호 추출
                판례일련번호_encoded = quote(str(row['판례일련번호'])) # 판례일련번호 인코딩
                법령_url = 'https://www.law.go.kr/법령/'
                # 판례일련번호로 데이터베이스에서 불러오기
                db_connection = mysql.connector.connect(
                    host = host,
                    user = user,
                    password = password,
                    database = database,
                    port = port
                )
                cursor = db_connection.cursor()
                # 불러오는 컬럼 판례일련번호, 클러스터, 키워드, 참조조문_파라미터
                cursor.execute(
                    f"""
                    SELECT a.판례일련번호, a.클러스터, a.키워드, b.참조조문_파라미터 as 참조조문 
                    FROM inheritance_keyword as a 
                    JOIN inheritance_case_clause_preprocessed as b 
                        ON a.판례일련번호 = b.판례정보일련번호 
                    WHERE a.클러스터 ={cluster_num} 
                    """)
                result = cursor.fetchall()
                inheritance_참조조문 = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
                cursor.close()
                db_connection.close()
                
                # inheritance_참조조문의 각 행에 대해 참조조문을 쉼표로 분리하여 누적
                참조조문_counts = []
                for i in range(len(inheritance_참조조문)):
                    참조조문 = inheritance_참조조문['참조조문'].iloc[i].split(',')
                    상세링크 = 법령_url+inheritance_참조조문['참조조문']
                    참조조문_counts.extend([item.strip().replace('/', ' ') for item in 참조조문])  # 각 조문을 개별 항목으로 추가
                
                # Counter를 사용하여 요소별 빈도 계산
                참조조문_counts = Counter(참조조문_counts)
                
                # 참조조문 빈도수를 계산하고 데이터프레임으로 변환
                df_참조조문_counts = pd.DataFrame(list(참조조문_counts.items()), columns=['참조조문이름','참조횟수'])
                df_참조조문_counts = df_참조조문_counts[df_참조조문_counts['참조조문이름'] != '참조조문 없음']
                # 공백 제거된 이름과 원래 이름을 매핑할 딕셔너리 생성
                name_mapping = {name.replace(' ', ''): name for name in df_참조조문_counts['참조조문이름'].unique()}
                
                df_참조조문_counts['상세링크'] = df_참조조문_counts['참조조문이름'].apply(
                    lambda x: 법령_url + x.replace(' 제', '/제')
                )
                
                df_참조조문2 = df_참조조문_counts
                
                df_참조조문_counts['참조조문이름'] = df_참조조문_counts['참조조문이름'].apply(lambda x: x.replace(' ', ''))

                df_참조조문2 = (
                    df_참조조문_counts.groupby('참조조문이름', as_index=False)
                    .agg({'참조횟수': 'sum', '상세링크': 'first'})
                    .sort_values(by='참조횟수', ascending=False)
                )
                df_참조조문2['참조조문이름'] = df_참조조문2['참조조문이름'].map(name_mapping)
                # df_참조조문2['참조조문이름'] = df_참조조문2.apply(
                #     lambda row: f'<a href="{row["상세링크"]}" target="_blank">{row["참조조문이름"]}</a>', axis=1
                # )
                
                # '참조횟수' 기준 상위 20개 데이터 필터링
                top_20_df = df_참조조문2.nlargest(20, '참조횟수')

                # HTML 링크 추가
                top_20_df['참조조문이름'] = top_20_df.apply(
                    lambda row: f'<a href="{row["상세링크"]}" target="_blank">{row["참조조문이름"]}</a>', axis=1
                )


                # CSS 스타일 추가
                st.markdown(
                    """
                    <style>
                    .dataframe-container {
                        width: 80%; /* 너비를 80%로 설정 */
                        margin: auto; /* 가운데 정렬 */
                    }
                    .dataframe-container table {
                        width: 100%; /* 표 너비를 100%로 설정 */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                # 상위 20개의 필터링된 데이터프레임을 HTML로 표시
                st.markdown(
                    f"""
                    <div class="dataframe-container">
                        {top_20_df[['참조조문이름', '참조횟수']].to_html(escape=False, index=False)}
                    </div>
                    """,
                    unsafe_allow_html=True,

                )
                st.bar_chart(df_참조조문2.set_index('참조조문이름')['참조횟수'][:20], x_label='법령',y_label= '참조횟수', width=200, height=500)
        else:
            st.warning("선택한 주제와 키워드에 대한 결과가 없습니다.")