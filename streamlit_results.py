import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
import ast
from urllib.parse import quote


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
keywordsdata = pd.DataFrame({
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
})

# 미리저장한 결과 CSV 파일 불러오기
inheritance_results = pd.read_csv('inheritance_results.csv')


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
    st.title("상속페이지")
    subject = st.selectbox("👆주제를 선택하세요:", keywordsdata['주제'])

    # 선택된 주제에 따른 키워드 버튼 표시
    selected_index =  keywordsdata[keywordsdata['주제'] == subject].index[0]
    keywords = keywordsdata['키워드'][selected_index]
    
    # 키워드는 주제선택 참고용자료로 보여주기
    st.write(f"**{subject}**와 관련된 키워드:")

    st.write(", ".join(keywords[:10]))

    # 확인 버튼 클릭 시 진행 표시와 유사도 계산
    if st.button("주제선택 완료") :
        # Progress bar와 placeholder 설정
        placeholder = st.empty()
        with placeholder:
            for percent in range(0, 101, 20):
                st.write("처리 중입니다...")
                st.progress(percent)
                time.sleep(0.5)

         # 이미 계산된 inheritance_results에서 주제,키워드로 필터링
        df_results = inheritance_results[inheritance_results['주제'] == subject].sort_values(by='유사도', ascending=False).head(10)

        # 결과가 있으면 탭에 표시
        if not df_results.empty:
            tab1, tab2 = st.tabs(["판례검색결과", "참조조문"])
            
            with tab1:
                st.header(f"{subject}와 관련된 사건명")
                for _, row in df_results.iterrows():
                    사건번호_encoded = quote(row['사건번호'])  # 사건번호 인코딩
                    판례일련번호_encoded = quote(str(row['판례일련번호'])) # 판례일련번호 인코딩
                    if pd.isna(row['사건명']):
                        사건명_encoded = "없음"
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
        else:
            st.warning("선택한 주제와 키워드에 대한 결과가 없습니다.")
    
    if st.button("홈으로 돌아가기"):
        go_to_page('home')

elif st.session_state['page'] == 'injury_page':
    st.title("상해 페이지")
    st.write("여기는 상해 페이지입니다.")
    if st.button("홈으로 돌아가기"):
        go_to_page('home')
