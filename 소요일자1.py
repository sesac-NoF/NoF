import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 미리저장한 결과 CSV 파일 불러오기
df_year = pd.read_csv('inheritance_years.csv')

# 데이터 확인
st.write("데이터 샘플:")
st.write(df_year.head())  # 데이터의 첫 몇 행을 출력하여 확인

# 레이아웃을 위해 두 개의 컬럼 생성
col_a, col_bc = st.columns([1, 1])  # 왼쪽 컬럼과 오른쪽 컬럼의 비율을 동일하게 설정

# 왼쪽에 A 영역을 길게 배치
with col_a:
    st.write("A 영역")  # 원하는 내용을 추가하세요

# 오른쪽에 B와 C 영역을 세로로 배치
with col_bc:
    st.write("B 영역")  # B 영역
    
    # 접수년도와 선고일자 데이터 준비
    df_year['선고일자'] = pd.to_datetime(df_year['선고일자'], errors='coerce')
    df_year['접수년도'] = pd.to_datetime(df_year['접수년도'], format='%Y', errors='coerce')

    # 소요일수 계산
    df_year['소요일수'] = (df_year['선고일자'] - df_year['접수년도']).dt.days

    # NaN 값을 제거한 후 10개 샘플 추출
    sample_df = df_year['소요일수'].dropna().sample(n=10, random_state=42)

    # 그래프 그리기
    plt.figure(figsize=(10, 6))
    plt.hist(sample_df, bins=30, alpha=0.7, color='skyblue')  # 샘플 데이터로 히스토그램 그리기
    plt.title('접수년도에서 선고일자까지 걸린 일수 (샘플 데이터)')
    plt.xlabel('소요일수 (일)')
    plt.ylabel('빈도수')

    # B 영역에 그래프 추가
    st.pyplot(plt)
    st.write("C 영역")  # C 영역
