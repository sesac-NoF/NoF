import streamlit as st

# 전체 배경색 설정
page_bg = """
<style> 
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, rgba(147, 182, 217, 1), rgba(178, 208, 211, 0.8));
}
[data-testid="stHeader"] {
    background: #9EB8D7;
}
[data-baseweb="tab-list"] {
    background-color: transparent; /* 탭 배경을 투명하게 설정 */
}
[data-testid="stTab"] {
    color: transparent; /* 탭 글씨색을 완전히 투명하게 설정 */
}
.stTabs [data-baseweb="tab-highlight"] {
    background-color:transparent; /* 탭 선택 하이라이트 삭제 */
}
[data-testid="stBaseButton-secondary"] {
    background-color: #B2D0D3; /* 버튼 배경색 */
    color: #F0F4F7; /* 글씨색 */
    width: 165px; /* 버튼 너비 설정 */
    font-weight: bold; /* 글씨를 볼드체로 설정 */
    text-align: center; /* 텍스트 중앙 정렬 */
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# 이미지 파일 경로
image_path1 = "근로.png"
image_path2 = "사기.png"
image_path3 = "상속.png"
image_path4 = "상해.png"

# 데이터 설정
inheritancedata = {
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

# 현재 활성화된 탭을 관리
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = '메인'

# 탭 생성
tabs = st.tabs(['메인', '근로', '사기', '상속', '상해',
                 '근로1', '근로2', '사기1', '사기2',
                 '상속1', '상속2', '상해1', '상해2'])

# 현재 선택된 탭에 따라 내용 표시
if st.session_state.active_tab == '메인':
    with tabs[0]:
        st.title("Welcome to NoF")
        st.write("안녕하세요 판례검색서비스입니다. 원하는 카테고리를 선택하세요.")
        
        # 이미지 버튼을 클릭하면 해당 탭으로 이동
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.image(image_path1, use_column_width=True)
            if st.button("근로 상세보기", key="근로_btn"):
                st.session_state.active_tab = '근로'

        with col2:
            st.image(image_path2, use_column_width=True)
            if st.button("사기 상세보기", key="사기_btn"):
                st.session_state.active_tab = '사기'

        with col3:
            st.image(image_path3, use_column_width=True)
            if st.button("상속 상세보기", key="상속_btn"):
                st.session_state.active_tab = '상속'

        with col4:
            st.image(image_path4, use_column_width=True)
            if st.button("상해 상세보기", key="상해_btn"):
                st.session_state.active_tab = '상해'

# 각 탭에 대한 내용 표시
if st.session_state.active_tab == '근로':
    with tabs[1]:
        st.write("근로에 대한 내용입니다.")
elif st.session_state.active_tab == '사기':
    with tabs[2]:
        st.write("사기에 대한 내용입니다.")
elif st.session_state.active_tab == '상속':
    with tabs[3]:
        st.title("상속 주제 선택")
        subject = st.selectbox("주제를 선택하세요:", inheritancedata['주제'])
        
        # 선택된 주제에 따른 키워드 버튼 표시
        selected_index = inheritancedata['주제'].index(subject)
        keywords = inheritancedata['키워드'][selected_index]
        
        st.write("관련 키워드:")
        for keyword in keywords:
            if st.button(keyword):
                st.write(f"{keyword} 버튼 클릭됨.")

elif st.session_state.active_tab == '상해':
    with tabs[4]:
        st.write("상해에 대한 내용입니다.")