import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
import ast

# CSV 파일 불러오기
df_inheritance = pd.read_csv('df_inheritance_kobertmodel.csv')

# 다시 리스트를 NumPy 배열로 변환
df_inheritance['판례내용이유임베딩'] = df_inheritance['판례내용이유임베딩'].apply(lambda x: np.array(ast.literal_eval(x)) if pd.notnull(x) else None)
df_inheritance['키워드임베딩'] = df_inheritance['키워드임베딩'].apply(lambda x: np.array(ast.literal_eval(x)) if pd.notnull(x) else None)

df_inheritance['키워드'] = df_inheritance['키워드'].apply(lambda x: x.split(', '))

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


if 'page' not in st.session_state:
    st.session_state['page'] = 'home'  # 초기 페이지를 home으로 설정

# 버튼 클릭 시 세션 상태 변경 함수
def go_to_page(page_name):
    st.session_state['page'] = page_name

# 사용자가 선택한 키워드에 대한 임베딩을 찾는 함수
def get_keyword_embedding(user_keyword, df):
    matching_rows = df[df['키워드'].apply(lambda x: user_keyword in x if isinstance(x, list) else False)]
    if not matching_rows.empty:
        return matching_rows['키워드임베딩'].iloc[0]
    return None


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
    subject = st.selectbox("주제를 선택하세요:", keywordsdata['주제'])

    # 선택된 주제에 따른 키워드 버튼 표시
    selected_index = keywordsdata['주제'].index(subject)
    keywords = keywordsdata['키워드'][selected_index]
    
    # 라디오 버튼으로 키워드 선택
    selected_keyword = st.radio("키워드를 선택하세요:", keywords)

    # 확인 버튼 클릭 시 진행 표시와 유사도 계산
    if st.button("확인") and selected_keyword:
        # Progress bar와 placeholder 설정
        placeholder = st.empty()
        with placeholder:
            for percent in range(0, 101, 20):
                st.write("처리 중입니다...")
                st.progress(percent)
                time.sleep(0.5)

        # 선택된 키워드로 임베딩 찾기
        user_keyword_embedding = get_keyword_embedding(selected_keyword, df_inheritance)

        if user_keyword_embedding is not None:
            content_similarity_scores = []
            for idx, row in df_inheritance.iterrows():
                if row['판례내용이유임베딩'] is not None and not np.isnan(row['판례내용이유임베딩']).any():
                    content_similarity = cosine_similarity(
                        user_keyword_embedding.reshape(1, -1),
                        row['판례내용이유임베딩'].reshape(1, -1)
                    ).flatten()[0]
                    content_similarity_scores.append((row['사건번호'], content_similarity))

            sorted_scores = sorted(content_similarity_scores, key=lambda x: x[1], reverse=True)
            top_n = sorted_scores[:10]

            # 결과 탭 표시
            tab1, tab2 = st.tabs(["판례검색결과", "참조조문"])
            
            with tab1:
                st.header("사용자 키워드와 관련된 사건명")
                for 사건번호, score in top_n:
                    사건명 = df_inheritance.loc[df_inheritance['사건번호'] == 사건번호, '사건명'].values
                    사건명 = 사건명[0] if 사건명.size > 0 else "사건명 없음"
                    st.write(f"사건번호: {사건번호}, 사건명: {사건명}")
            
            with tab2:
                st.header("참조조문")
                # 여기에 참조조문 내용 추가
                st.write("참조조문 관련 내용이 여기에 표시됩니다.")
        else:
            st.warning("선택한 키워드에 대한 임베딩을 찾을 수 없습니다.")
    else:
        st.write("키워드를 선택하고 확인 버튼을 눌러주세요.")

    if st.button("홈으로 돌아가기"):
        go_to_page('home')

elif st.session_state['page'] == 'injury_page':
    st.title("상해 페이지")
    st.write("여기는 상해 페이지입니다.")
    if st.button("홈으로 돌아가기"):
        go_to_page('home')
