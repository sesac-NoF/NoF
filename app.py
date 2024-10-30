import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
from db_info import user,password,host,database,port

st.tabs(['근로','사기','상속','상해'])

option = st.selectbox(
    '주제를 선택하세요',
    ('부동산과 관련된 법적 절차', '회사와 자금, 주식과 관련된 금융 이슈','세금 신고와 소득 관련 이슈','보험 계약 및 보험금 청구', '문서 위조와 관련된 사건','형법 및 형사소송법과 관련된 법적 절차', '계약 및 사기죄와 관련된 법적 이슈', '수표와 어음 발행')
)

st.write("선택된 주제:", option)

col_list = ['판례일련번호','사건번호','클러스터','키워드']
sample = pd.read_csv('data/df_fraud_keyword.csv', index_col=False, usecols=col_list)
st.dataframe(sample)