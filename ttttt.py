import streamlit as st
import pandas as pd
import time

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


# 각 용어에 대해 버튼을 생성하고, 클릭 시 개념을 스트리밍
for _, row in dfword.iterrows():
    term = row['용어']
    concept = row['개념']
    
    # 용어 버튼 표시
    if st.button(term, key=term):
        # 스트리밍 방식으로 개념을 출력
        st.write_stream(stream_concept(concept))
