import streamlit as st
import pandas as pd
# import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
import ast
from urllib.parse import quote
from db_info import user,password,port,database,host
import mysql.connector
import plotly.express as px
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

# 미리저장한 결과 CSV 파일 불러오기
inheritance_results = pd.read_csv('data/inheritance_results.csv')


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
    st.title("근로 페이지")
    st.write("여기는 근로 페이지입니다.")
    if st.button("홈으로 돌아가기"):
        go_to_page('home')

elif st.session_state['page'] == 'fraud_page':
    st.title("사기 페이지")
    st.write("여기는 사기 페이지입니다.")
    if st.button("홈으로 돌아가기"):
        go_to_page('home')

elif st.session_state['page'] == 'inheritance_page':
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
        df_results = inheritance_results[inheritance_results['주제'] == subject].sort_values(by='유사도', ascending=False).drop_duplicates(subset=['사건번호', '사건명']).head(10)
        
        # 결과가 있으면 탭에 표시
        if not df_results.empty:
            tab1, tab2 = st.tabs(["판례검색결과", "참조조문"])
            
            with tab1:
                st.header(f"{subject}와 관련된 사건명")
                for _, row in df_results.iterrows():
                    사건번호_encoded = quote(row['사건번호'])  # 사건번호 인코딩
                    판례일련번호_encoded = quote(str(row['판례일련번호'])) # 판례일련번호 인코딩
                    if pd.isna(row['사건명']):
                        사건명_encoded = '없음'
                    else:
                        사건명_encoded = quote(row['사건명'])
                    # 사건번호를 클릭하면 2_page.py로 이동하도록 링크 생성
                    if pd.isna(row['사건명']):
                        # st.write(f"[go to page 3](3?param={value})")/
                        st.write(f"[사건번호: {row['사건번호']}](/3?case_number={사건번호_encoded}&case_serial={판례일련번호_encoded}&case_name={사건명_encoded})")
                        # st.button('1')
                    else:
                        st.write(f"[사건번호: {row['사건번호']}, 사건명: {row['사건명']}](/3?case_number={사건번호_encoded}&case_serial={판례일련번호_encoded}&case_name={사건명_encoded})")
            
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
    
    if st.button("홈으로 돌아가기"):
        go_to_page('home')

elif st.session_state['page'] == 'injury_page':
    st.title("상해 페이지")
    st.write("여기는 상해 페이지입니다.")
    if st.button("홈으로 돌아가기"):
        go_to_page('home')
