import streamlit as st
import plotly.express as px
import pandas as pd
import time
from urllib.parse import quote
from db_info import user, password, host, port, database
import mysql.connector

# # 데이터 예시 (가상의 데이터 생성)
# df = pd.DataFrame({
#     'Year': [2020, 2021, 2022, 2023],
#     'Cluster 1': [100, 120, 130, 150],
#     'Cluster 2': [80, 90, 110, 120],
#     'Cluster 3': [50, 60, 70, 80]
# })

# # 데이터프레임을 long format으로 변환
# df_long = pd.melt(df, id_vars=['Year'], var_name='Cluster', value_name='Count')

# # Plotly Bar chart
# fig = px.bar(df_long, x='Year', y='Count', color='Cluster', barmode='group', 
#              labels={'Year': 'Year', 'Count': 'Count', 'Cluster': 'Cluster'})

# # Streamlit에서 Plotly 차트 표시
# st.plotly_chart(fig, use_container_width=True)


# 상속 데이터 생성
data = {
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

df_clusterdata = pd.DataFrame(data)

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

# 사용자 키워드에 대한 임베딩을 찾기 위한 함수
def get_keyword_embedding(user_keyword, df, cluster):
    # 주어진 클러스터로 필터링한 데이터에서 키워드 찾기
    matching_rows = df[(df['클러스터'] == cluster) & 
                       (df['키워드'].apply(lambda x: user_keyword in x if isinstance(x, list) else False))]
    
    if not matching_rows.empty:
        # 첫 번째 매칭된 키워드의 임베딩 반환
        return matching_rows['키워드임베딩'].iloc[0]
    else:
        return None  # 매칭되는 키워드가 없으면 None 반환

subject = st.selectbox("주제를 선택하세요:", data['주제'])

# 선택된 주제에 따른 키워드 버튼 표시
selected_index = data['주제'].index(subject)
keywords = data['키워드'][selected_index]
# 라디오 버튼으로 키워드 선택
selected_keyword = st.radio("키워드를 선택하세요:", keywords)

# 확인 버튼 클릭 시 진행 표시와 유사도 계산
if st.button("확인") and selected_keyword:
    # Progress bar와 placeholder 설정
    placeholder = st.empty()
    placeholder.write("처리 중입니다...")
    
    placeholder2 = st.empty()
    with placeholder2:
        for percent in range(0, 101, 20):
            st.progress(percent)
            time.sleep(0.5)
            
    placeholder.empty()
    
    # 주제,키워드,사건번호,사건명,유사도,판례일련번호 저장된 csv 불러오기
    # 불러온 데이터프레임에 클러스터 맵핑해서 추가
    inheritance_results = pd.read_csv('data/inheritance_results.csv')
    inheritance_results['클러스터'] = inheritance_results['주제'].map(topic_cluster_map) 
    
    # inheritance_results에서 주제,키워드로 필터링
    df_results = inheritance_results[(inheritance_results['주제'] == subject) 
                                        & (inheritance_results['키워드'] == selected_keyword)].sort_values(by='유사도', ascending=False).head(10)
    df_laws = inheritance_results[(inheritance_results['주제'] == subject)
                                  & (inheritance_results['키워드'] == selected_keyword)]
    # 결과가 있으면 탭에 표시
    if not df_results.empty:
        tab1, tab2 = st.tabs(["판례검색결과", "참조조문"])
        
        with tab1:
            df_results
            st.header("사용자 키워드와 관련된 사건명")
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
            st.write("참조조문 관련 내용이 여기에 표시됩니다.")
            all_results = []
            for _, row in df_laws.iterrows():
                판례일련번호_encoded = quote(str(row['판례일련번호'])) # 판례일련번호 인코딩
                db_connection = mysql.connector.connect(
                    host = host,
                    user = user,
                    password = password,
                    database = database,
                    port = port
                )
                cursor = db_connection.cursor()
                cursor.execute(f"SELECT 판례정보일련번호, 참조조문_전처리 as 참조조문 FROM inheritance_case_clause_preprocessed where 판례정보일련번호 = {판례일련번호_encoded}")
                result = cursor.fetchall()
                if result:
                    df_inheritance = pd.DataFrame(result, columns = [i[0] for i in cursor.description])
                    all_results.append(df_inheritance)
                cursor.close()
                db_connection.close()
            results_all = pd.concat(all_results, ignore_index=True)
            results_all
            참조조문_couts = results_all['참조조문'].value_counts().reset_index()
            참조조문_couts.columns = ['참조조문','빈도']
            
            with st.container():
                st.write('참조조문 빈도')
                st.dataframe(참조조문_couts)
                
                st.bar_chart(참조조문_couts.set_index('참조조문'))

    else:
        st.warning("선택한 주제와 키워드에 대한 결과가 없습니다.")