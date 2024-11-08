import streamlit as st
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

query_params = st.query_params
case_serial = st.query_params.case_serial
case_number = st.query_params.case_number
case_name = st.query_params.case_name

# params = 사건번호

OC = 'younwjdtjr'
target = 'prec'
type = 'HTML'
url = 'http://www.law.go.kr/DRF/lawService.do?'
parameters = {
    'OC': OC,
    'target': target,
    'type' : type,
    'ID': case_serial
}
response = requests.get(url=url, params=parameters)
if response.status_code == 200 :
    html_content = response.text
    st.components.v1.html(html_content, width= 800, height=1000)
else:
    st.error(response.status_code)

