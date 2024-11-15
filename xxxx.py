import streamlit as st
import pandas as pd

# 데이터프레임 생성
data = {
    "Name": ["Google", "Streamlit", "GitHub"],
    "Link": [
        '<a href="https://www.google.com" target="_blank">Visit Google</a>',
        '<a href="https://www.streamlit.io" target="_blank">Visit Streamlit</a>',
        '<a href="https://www.github.com" target="_blank">Visit GitHub</a>'
    ]
}

df = pd.DataFrame(data)

# HTML 렌더링을 위한 함수
# def make_clickable(val):
#     return f'<a href="{val}" target="_blank">{val}</a>'

# Streamlit에서 데이터프레임 표시
st.markdown(
    df.to_html(escape=False, index=False), 
    unsafe_allow_html=True
)
