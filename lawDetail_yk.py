import pandas as pd
import numpy as np
import re 
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


df_case = pd.read_csv('df_data2.csv')

# 데이터 목록 초기화
data_list = []

# 판례 데이터를 담은 CSV 파일 로드 (인코딩 문제 해결 위해 encoding 옵션 추가)
try:
    df_case = pd.read_csv('df_data2.csv', encoding='utf-8')
except FileNotFoundError:
    print("파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")
except pd.errors.ParserError:
    print("CSV 파일을 파싱하는 중 오류가 발생했습니다.")
else:
   
    
        # 판례 데이터 가져오기
    for i in range(len(df_case)):  # 'df_case' DataFrame의 길이만큼 반복
        
        content = df_case['판례내용'].iloc[i]

        # 모든 "【 】" 형식의 텍스트 찾기
        matches = re.findall(r'【(.*?)】\s*(.*?)<br/>', content, re.DOTALL)
        
        # "【주    문】" 부분 별도 추출 (띄어쓰기 무시)
        jumun = re.search(r'【주\s*문】\s*<br/>\s*(.*?)(?=<br/>)', content, re.DOTALL)
        
        # 딕셔너리 생성 및 데이터 추가
        data = {col.strip(): val.strip() for col, val in matches}
        if jumun:
            data['주 문'] = jumun.group(1).strip()
        
        # 데이터를 리스트에 추가
        data_list.append(data)

    # DataFrame으로 변환

    if data_list:
        final_df = pd.DataFrame(data_list)
        print(final_df.head())
    else:
        print("추출된 데이터가 없습니다.")

final_df.to_csv('df_data_fin.csv')

