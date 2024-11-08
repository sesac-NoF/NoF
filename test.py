import streamlit as st
import pandas as pd
from db_info import user, password, host, port, database  # 데이터베이스 접속 정보 불러오기
import mysql.connector  # MySQL 데이터베이스 연결 라이브러리
from urllib.parse import quote  # URL 인코딩을 위한 모듈 (필요시 사용 가능)

# Streamlit 앱에 초기 메시지 표시
st.write("참조조문 관련 내용이 여기에 표시됩니다.")

# 데이터베이스 연결 설정
db_connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)

# SQL 쿼리 실행을 위한 커서 객체 생성
cursor = db_connection.cursor()

# SQL 쿼리: 두 테이블(inheritance_keyword와 inheritance_case_clause_preprocessed)에서 
# 판례일련번호가 일치하는 레코드를 가져옴. 클러스터가 '1'인 경우로 필터링
cursor.execute(
    """
    SELECT a.판례일련번호, a.클러스터, a.키워드, b.참조조문_전처리 AS 참조조문 
    FROM inheritance_keyword AS a 
    JOIN inheritance_case_clause_preprocessed AS b 
    ON a.판례일련번호 = b.판례정보일련번호 
    WHERE a.클러스터 = '1'
    """
)

# 쿼리 결과의 모든 행을 가져옴
result = cursor.fetchall()

# 쿼리 결과를 DataFrame으로 변환
# 컬럼 이름은 원본 테이블 스키마와 일치하도록 커서 설명에서 가져옴
inheritance_참조조문 = pd.DataFrame(result, columns=[i[0] for i in cursor.description])

# 데이터 조회가 끝난 후 커서와 데이터베이스 연결을 닫아 자원을 해제
cursor.close()
db_connection.close()

# 데이터가 없을 경우 메시지를 표시하고, 데이터가 있을 경우 DataFrame을 표시
if inheritance_참조조문.empty:
    # 쿼리 결과가 없을 경우 메시지를 표시
    st.write("검색 결과가 없습니다.")
else:
    # DataFrame에 데이터가 있으면 Streamlit에 테이블 형식으로 출력
    st.dataframe(inheritance_참조조문)
    