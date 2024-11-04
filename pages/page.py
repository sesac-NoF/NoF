import streamlit as st
from urllib.parse import unquote

# URL 파라미터에서 사건번호 가져오기
query_params = st.experimental_get_query_params()
encoded_case_number = query_params.get("case_number", [None])[0]

# URL 디코딩
사건번호 = unquote(encoded_case_number) if encoded_case_number else None

# 디코딩된 사건번호 출력
if 사건번호:
    st.write(f"디코딩된 사건번호: {사건번호}")
else:
    st.write("사건번호가 제공되지 않았습니다.")
