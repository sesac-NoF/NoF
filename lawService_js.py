import pandas as pd
import requests
import xml.etree.ElementTree as ET


df = pd.read_csv('data/df_data.csv')

OC = 'younwjdtjr'
target = 'prec'
url = 'http://www.law.go.kr/DRF/lawService.do?'
data = []

# for i in range(1,df['판례일련번호'].value_counts().sum()+1):
#     params = {
#         'OC' : OC,
#         'target' : target,
#         'type' : 'XML',
#         'ID' : df['판례일련번호'].iloc[i-1]
#     }


params = {
    'OC' : OC,
    'target' : target,
    'type' : 'XML',
    'ID' : df['판례일련번호'].iloc[1]
}
response = requests.get(url, params=params)

if response.status_code == 200:
    root = ET.fromstring(response.content)
    CASE_NUM = root.find('.//사건번호')
    JUD = root.find('.//선고')
    JUD_TYPE = root.find('.//판결유형')
    ISSUE = root.find('.//판시사항')
    SUMMARY_JUD = root.find('.//판결요지')
    REF_STAT = root.find('.//참조조문')
    REF_CASE = root.find('.//참조판례')
    CASE_CONTENT = root.find('.//판례내용')
    print(CASE_CONTENT.text)
    for 판례내용 in root.findall('.//판례내용'):
        content = 판례내용.text
        # '【주 문】' 이후의 텍스트 추출
        start_index = content.find('【피 고 인】')
    if start_index != -1:
        # '【이 유】' 전까지 추출
        end_index = content.find('【상 고 인】', start_index)
        if end_index != -1:
            order_text = content[start_index:end_index].strip()
            print(order_text)
        else:
            order_text = content[start_index:].strip()  # '【이 유】'이 없는 경우
            print(order_text)
    for 판례내용 in root.findall('.//판례내용'):
        content = 판례내용.text
        # '【주 문】' 이후의 텍스트 추출
        start_index = content.find('【상 고 인】')
    if start_index != -1:
        # '【이 유】' 전까지 추출
        end_index = content.find('【변 호 인】', start_index)
        if end_index != -1:
            order_text = content[start_index:end_index].strip()
            print(order_text)
        else:
            order_text = content[start_index:].strip()  # '【이 유】'이 없는 경우
            print(order_text)
    for 판례내용 in root.findall('.//판례내용'):
        content = 판례내용.text
        # '【주 문】' 이후의 텍스트 추출
        start_index = content.find('【변 호 인】')
    if start_index != -1:
        # '【이 유】' 전까지 추출
        end_index = content.find('【원심판결】', start_index)
        if end_index != -1:
            order_text = content[start_index:end_index].strip()
            print(order_text)
        else:
            order_text = content[start_index:].strip()  # '【이 유】'이 없는 경우
            print(order_text)
    for 판례내용 in root.findall('.//판례내용'):
        content = 판례내용.text
        # '【주 문】' 이후의 텍스트 추출
        start_index = content.find('【원심판결】')
    if start_index != -1:
        # '【이 유】' 전까지 추출
        end_index = content.find('【주    문】', start_index)
        if end_index != -1:
            order_text = content[start_index:end_index].strip()
            print(order_text)
        else:
            order_text = content[start_index:].strip()  # '【이 유】'이 없는 경우
            print(order_text)
    for 판례내용 in root.findall('.//판례내용'):
        content = 판례내용.text
        # '【주 문】' 이후의 텍스트 추출
        start_index = content.find('【주    문】')
    if start_index != -1:
        # '【이 유】' 전까지 추출
        end_index = content.find('【이    유】', start_index)
        if end_index != -1:
            order_text = content[start_index:end_index].strip()
            print(order_text)
        else:
            order_text = content[start_index:].strip()  # '【이 유】'이 없는 경우
            print(order_text)