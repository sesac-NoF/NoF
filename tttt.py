import streamlit as st
import plotly.express as px
import pandas as pd

# 데이터 예시 (가상의 데이터 생성)
df = pd.DataFrame({
    'Year': [2020, 2021, 2022, 2023],
    'Cluster 1': [100, 120, 130, 150],
    'Cluster 2': [80, 90, 110, 120],
    'Cluster 3': [50, 60, 70, 80]
})

# 데이터프레임을 long format으로 변환
df_long = pd.melt(df, id_vars=['Year'], var_name='Cluster', value_name='Count')

# Plotly Bar chart
fig = px.bar(df_long, x='Year', y='Count', color='Cluster', barmode='group', 
             labels={'Year': 'Year', 'Count': 'Count', 'Cluster': 'Cluster'})

# Streamlit에서 Plotly 차트 표시
st.plotly_chart(fig, use_container_width=True)

