import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URL 파라미터에서 사건번호 가져오기
query_params = st.experimental_get_query_params()
사건번호 = query_params.get("사건번호", [None])[0]

if 사건번호:
    st.title(f"{사건번호}의 그래프")
    
    # 예시: 사건번호에 해당하는 데이터 불러오기
    df_year = pd.read_csv('inheritance_years.csv')
    
    # 사건번호에 따라 필터링 (여기에 필터링 로직 추가 필요)
    # 아래는 임시로 데이터 프레임에서 사건번호가 일치하는 경우 필터링하는 코드입니다.
    filtered_data = df_year[df_year['사건번호'] == 사건번호]  # 실제 사건번호와 비교

    if not filtered_data.empty:
        # 접수년도와 선고일자 데이터 준비
        filtered_data['선고일자'] = pd.to_datetime(filtered_data['선고일자'])
        filtered_data['접수년도'] = pd.to_datetime(filtered_data['접수년도'], format='%Y', errors='coerce')

        # 소요일수 계산
        filtered_data['소요일수'] = (filtered_data['선고일자'] - filtered_data['접수년도']).dt.days

        # 그래프 그리기
        plt.figure(figsize=(10, 6))
        plt.hist(filtered_data['소요일수'].dropna(), bins=30, alpha=0.7)
        plt.title('접수년도에서 선고일자까지 걸린 일수')
        plt.xlabel('소요일수 (일)')
        plt.ylabel('빈도수')
        st.pyplot(plt)
    else:
        st.warning("해당 사건번호에 대한 데이터가 없습니다.")
else:
    st.write("사건번호가 제공되지 않았습니다.")
