import pandas as pd
import requests
import xml.etree.ElementTree as ET
import re

#판례목록 가져오기
OC = 'wanja1996'
target = 'prec'
url = 'http://www.law.go.kr/DRF/lawSearch.do?'
data = []
for i in range(1,226): #판례목록과 판례본문 수가 많아 인원수별로 22500개 나눠서 받아오기로 하였다.
    params = {
        'OC' : OC,
        'target' : target,
        'type' : 'XML',
        'display' : 100,
        'search' : 1,
        'page' : i
        }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        items = root.findall('.//prec')
        # xml구조확인
        print(ET.tostring(root, encoding='utf-8').decode('utf-8'))
        if len(items) != 0:
            for item in items:
                ORDER_NUM = item.find('.//판례일련번호')
                CASE_NAME = item.find('.//사건명')
                CASE_NUM = item.find('.//사건번호')
                CASE_DATE = item.find('.//선고일자')
                SCOURT = item.find('.//법원명')
                CASE = item.find('.//사건종류명')
                LINK = item.find('.//판례상세링크')
                data.append([ORDER_NUM.text, CASE_NAME.text, CASE_NUM.text, CASE_DATE.text, SCOURT.text, CASE.text, LINK.text])
        else:
            print('error')
df = pd.DataFrame(data=data, columns=['판례일련번호','사건명','사건번호','선고일자','법원명','사건종류명','판례상세링크'])
df.to_csv('data/lawSearch_dh.csv',index=False) #csv파일로 저장

##판례 본문 API 읽어오기##
url = 'http://www.law.go.kr/DRF/lawService.do?'
data2 = []
for i in range(1,df['판례일련번호'].value_counts().sum()+1):
    params = {
        'OC' : OC,
        'target' : target,
        'type' : 'XML',
        'ID' : df['판례일련번호'].iloc[i-1]
        }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        # xml구조확인
        print(f"판례 {i}개째 진행 중")
        CASE_NUM = root.find('.//사건번호')
        JUD = root.find('.//선고')
        JUD_TYPE = root.find('.//판결유형')
        ISSUE = root.find('.//판시사항')
        SUMMARY_JUD = root.find('.//판결요지')
        REF_STAT = root.find('.//참조조문')
        REF_CASE = root.find('.//참조판례')
        CASE_CONTENT = root.find('.//판례내용')
        
        for 판례내용 in root.findall('.//판례내용'):
            content = 판례내용.text
            # '【피 고 인】' 이후의 텍스트 추출
            start_index = content.find('【피 고 인】')
        if start_index != -1:
            # '【상 고 인】' 전까지 추출
            end_index = content.find('【상 고 인】', start_index)
            if end_index != -1:
                order_text = content[start_index:end_index].strip()
            else:
                order_text = content[start_index:].strip()  # '【상 고 인】' 이후의 모든 텍스트 추출
        for 판례내용 in root.findall('.//판례내용'):
            content = 판례내용.text
            # '【변 호 인】' 이후의 텍스트 추출
            start_index = content.find('【변 호 인】')
        if start_index != -1:
            # '【원심판결】' 전까지 추출
            end_index = content.find('【원심판결】', start_index)
            if end_index != -1:
                order_text = content[start_index:end_index].strip()
            else:
                order_text = content[start_index:].strip()  # '【원심판결】' 이후의 모든 텍스트 추출
        for 판례내용 in root.findall('.//판례내용'):
            content = 판례내용.text
            #  '【원심판결】' 이후의 텍스트를 추출
            start_index = content.find('【원심판결】')
        if start_index != -1:
            # '【주    문】' 전까지 추출
            end_index = content.find('【주    문】', start_index)
            if end_index != -1:
                order_text = content[start_index:end_index].strip()
            else:
                order_text = content[start_index:].strip()  # '【주 문】' 이후의 모든 텍스트 추출
        for 판례내용 in root.findall('.//판례내용'):
            content = 판례내용.text
            # '【주 문】' 이후의 텍스트 추출
            start_index = content.find('【주    문】')
        if start_index != -1:
            # '【이 유】' 전까지 추출
            end_index = content.find('【이    유】', start_index)
            if end_index != -1:
                order_text = content[start_index:end_index].strip()
            else:
                order_text = content[start_index:].strip()  # '【이 유】'이 없는 경우
        data2.append([
        df['판례일련번호'].iloc[i-1],  # 판례일련번호
        CASE_NUM.text if CASE_NUM is not None else None, #사건번호
        JUD.text if JUD is not None else None, #선고
        JUD_TYPE.text if JUD_TYPE is not None else None, #판결유형
        ISSUE.text if ISSUE is not None else None,  # 판시사항
        SUMMARY_JUD.text if SUMMARY_JUD is not None else None, #판결요지
        REF_STAT.text if REF_STAT is not None else None, #참조조문
        REF_CASE.text if REF_CASE is not None else None, #참조판례
        CASE_CONTENT.text if CASE_CONTENT is not None else None #판례내용
        ])

df2 = pd.DataFrame(data=data2, columns=['판례정보일련번호','사건번호','선고','판결유형','판시사항','판결요지','참조조문','참조판례','판례내용'])
df2.to_csv('data/lawService_dh2.csv',index=False) #csv파일로 저장