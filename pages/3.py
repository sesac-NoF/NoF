import streamlit as st
import requests
import numpy as np

col1, col2 = st.columns([0.8, 0.2])



with col1: 
    query_params = st.query_params
    params = st.query_params.case_serial


    st.write(f"receive parameter: {params}")

    # params = 사건번호

    OC = 'younwjdtjr'
    target = 'prec'
    type = 'HTML'
    url = 'http://www.law.go.kr/DRF/lawService.do?'
    parameters = {
        'OC': OC,
        'target': target,
        'type' : type,
        'ID': params
    }
    response = requests.get(url=url, params=parameters)
    if response.status_code == 200 :
        html_content = response.text
        st.components.v1.html(html_content, width= 600, height=1000)
    else:
        st.error(response.status_code)

with col2: 
    data = np.random.randn(10, 1)
    col2.line_chart(data)